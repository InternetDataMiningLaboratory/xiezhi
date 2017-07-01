#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
'''Spider class
'''
import scrapy
import logging


logger = logging.getLogger(__name__)


class Xiezhi(scrapy.Spider):
    '''Class of the spider inherit ``scrapy.Spider``
    '''
    name = 'xiezhi'
