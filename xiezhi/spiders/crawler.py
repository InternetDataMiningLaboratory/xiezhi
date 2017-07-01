#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
'''Spider class
'''
import scrapy
import logging


LOGGER = logging.getLogger(__name__)


class Xiezhi(scrapy.Spider):
    '''Class of the spider inherit ``scrapy.Spider``
    '''
    name = 'xiezhi'

    def __init__(self, start_ip, end_ip, *args, **kwargs):
        '''Initialize spider

        Args:
            start_ip: a str as the start ip address
            end_ip: a str as the end ip address
        '''
        super(Xiezhi, self).__init__(*args, **kwargs)
        self.start_ip = start_ip
        self.end_ip = end_ip
