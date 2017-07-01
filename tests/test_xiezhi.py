#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: tests/test_xiezhi.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 01.07.2017
from nose.tools import assert_equals

from tests.test_spider import TestSpider
from xiezhi.spiders.crawler import (
    Xiezhi
)


def test_xiezhi_init():
    '''Check if ``xiezhi.__init__`` works
    '''
    spider = Xiezhi('test1', 'test2')
    assert_equals(spider.start_ip, 'test1')
    assert_equals(spider.end_ip, 'test2')
