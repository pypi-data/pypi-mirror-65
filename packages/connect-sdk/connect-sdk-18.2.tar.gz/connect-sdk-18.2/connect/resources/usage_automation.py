# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import json
import logging
from abc import ABCMeta
from tempfile import NamedTemporaryFile

import openpyxl
import requests
from typing import List, Optional

from connect.exceptions import FileCreationError, FileRetrievalError
from connect.models.usage_listing import UsageListing
from connect.models.usage_file import UsageFile
from connect.models.usage_record import UsageRecord
from .automation_engine import AutomationEngine


class UsageAutomation(AutomationEngine):
    """ Automates reporting of Usage Files.

    For an example on how to use this class, see :ref:`usage_example`.
    """

    __metaclass__ = ABCMeta
    resource = 'listings'
    model_class = UsageFile
    logger = logging.getLogger('Usage.logger')

    def filters(self, status='listed', **kwargs):
        """
        :param str status: Status of the requests. Default: ``'listed'``.
        :param dict[str,Any] kwargs: Additional filters to add to the default ones.
        :return: The set of filters for this resource.
        :rtype: dict[str,Any]
        """
        filters = super(UsageAutomation, self).filters(status, **kwargs)
        if self.config.products:
            filters['product__id'] = ','.join(self.config.products)
        return filters

    def dispatch(self, request):
        # type: (UsageListing) -> str

        self._set_custom_logger(request.id, request.contract.marketplace.id)

        # TODO Shouldn't this raise an exception on ALL automation classes?
        if self.config.products \
                and request.product.id not in self.config.products:
            return 'Listing not handled by this processor'

        self.logger.info(
            'Processing Usage for Product {} ({}) '.format(request.product.id,
                                                           request.product.name) +
            'on Contract {} '.format(request.contract.id) +
            'and provider {}({})'.format(request.provider.id, request.provider.name))

        try:
            result = self.process_request(request)
        except FileCreationError:
            self.logger.info(
                'Error processing Usage for Product {} ({}) '.format(request.product.id,
                                                                     request.product.name) +
                'on Contract {} '.format(request.contract.id) +
                'and provider {}({})'.format(request.provider.id, request.provider.name))
            return 'failure'

        self.logger.info('Processing result for usage on listing {}: {}'
                         .format(request.product.id, result))
        return 'success'

    def get_usage_template(self, product):
        """ Returns the template file contents for a specified product.

        :param Product product: Specific product.
        :return: The template file contents.
        :rtype: bytes
        :raises FileRetrievalError: Raised if the file contents could not be retrieved.
        """
        location = self._get_usage_template_download_location(product.id)
        if not location:
            msg = 'Error obtaining template usage file location'
            self.logger.error(msg)
            raise FileRetrievalError(msg)

        contents = self._retrieve_usage_template(location) if location else None
        if not contents:
            msg = 'Error obtaining template usage file from `{}`'.format(location)
            self.logger.error(msg)
            raise FileRetrievalError(msg)
        return contents

    def submit_usage(self, usage_file, usage_records):
        """ Submit a usage file.

        :param UsageFile usage_file: Usage file.
        :param list[UsageRecord] usage_records: Records.
        :return: Usage file.
        :rtype: UsageFile
        :raises FileCreationError: Raised if creation or uploading of the file fails.
        """
        usage_file = self._create_usage_file(usage_file)
        self._upload_usage_records(usage_file, usage_records)
        return usage_file

    def _get_usage_template_download_location(self, product_id):
        # type: (str) -> str
        try:
            response, _ = self._api.get(url='{}usage/products/{}/template/'
                                        .format(self.config.api_url, product_id))
            response_dict = json.loads(response)
            return response_dict['template_link']
        except (requests.exceptions.RequestException, KeyError, TypeError, ValueError):
            return ''

    @staticmethod
    def _retrieve_usage_template(location):
        # type: (str) -> Optional[bytes]
        try:
            response = requests.get(location)
            return response.content
        except requests.exceptions.RequestException:
            return None

    def _create_usage_file(self, usage_file):
        # type: (UsageFile) -> UsageFile
        if not usage_file.name or not usage_file.product.id or not usage_file.contract.id:
            raise FileCreationError('Usage File Creation requires name, product id, contract id')
        if not usage_file.description:
            # Could be because description is empty or None, so make sure it is empty
            usage_file.description = ''
        response, _ = self._api.post(url='{}usage/files/'
                                     .format(self.config.api_url), json=usage_file.json)
        return self.model_class.deserialize(response)

    def _upload_usage_records(self, usage_file, usage_records):
        # type: (UsageFile, List[UsageRecord]) -> None
        # TODO: Using xslx mechanism till usage records json api is available
        book = self._create_spreadsheet(usage_records)
        self._upload_spreadsheet(usage_file, book)

    @staticmethod
    def _create_spreadsheet(usage_records):
        # type: (List[UsageRecord]) -> openpyxl.Workbook
        book = openpyxl.Workbook()
        sheet = book.active
        sheet.title = 'usage_records'
        sheet['A1'] = 'record_id'
        sheet['B1'] = 'item_search_criteria'
        sheet['C1'] = 'item_search_value'
        sheet['D1'] = 'quantity'
        sheet['E1'] = 'start_time_utc'
        sheet['F1'] = 'end_time_utc'
        sheet['G1'] = 'asset_search_criteria'
        sheet['H1'] = 'asset_search_value'
        for index, record in enumerate(usage_records):
            row = str(index + 2)
            sheet['A' + row] = record.usage_record_id
            sheet['B' + row] = record.item_search_criteria
            sheet['C' + row] = record.item_search_value
            sheet['D' + row] = record.quantity
            sheet['E' + row] = record.start_time_utc
            sheet['F' + row] = record.end_time_utc
            sheet['G' + row] = record.asset_search_criteria
            sheet['H' + row] = record.asset_search_value
        return book

    def _upload_spreadsheet(self, usage_file, spreadsheet):
        # type: (UsageFile, openpyxl.Workbook) -> None

        # Generate spreadsheet file
        with NamedTemporaryFile() as tmp:
            spreadsheet.save(tmp)
            tmp.seek(0)
            file_contents = tmp.read()

        # Setup request
        url = '{}usage/files/{}/upload/'.format(self.config.api_url, usage_file.id)
        headers = self._api.headers
        headers['Accept'] = 'application/json'
        del headers['Content-Type']  # This must NOT be set for multipart post requests
        multipart = {'usage_file': ('usage_file.xlsx', file_contents)}
        self.logger.info('HTTP Request: {} - {} - {}'.format(url, headers, multipart))

        # Post request
        try:
            content, status = self._api.post(
                url=url,
                headers=headers,
                files=multipart)
        except requests.RequestException as ex:
            raise FileCreationError('Error uploading file: {}'.format(ex))
        self.logger.info('HTTP Code: {}'.format(status))
        if status != 201:
            msg = 'Unexpected server response, returned code {}'.format(status)
            self.logger.error('{} -- Raw response: {}'.format(msg, content))
            raise FileCreationError(msg)
