#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
'''Test class for crawler.
'''
from xiezhi.spiders.crawler import (
    Xiezhi
)
from scrapy.http import Request, Response
import pkg_resources


class TestSpider(object):
    '''Test base class for crawler.
    '''
    def fake_response_from_file(self, file_name, url=None, meta=None):
        '''Create a fake response from given file.

        Args:
            file_name: a string of the name of input file.
            url: a string of the url in response.
            meta: a dict of the meta in response.

        Returns:
            a ``scrapy.Response`` instance
        '''
        if url is None:
            url = 'http://www.example.com'

        request = Request(url=url, meta=meta)
        response = None
        with open(
            pkg_resources.resource_filename(
                'xiezhi.conf',
                '{0}'.format(file_name)
            )
        ) as file:
            response = Response(
                url=url,
                request=request,
                body=file.read()
            )
            response.encoding = 'utf-8'
        return response

    def setUp(self):
        '''Setup for tests.

        Create a crawler instance for tests.
        '''
        self.crawler = Xiezhi()
