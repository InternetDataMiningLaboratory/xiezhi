#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 15.02.2017
import logging
import os
from scrapy import signals
from xiezhi.models.instance import Instance
from xiezhi.models.caduceus import Caduceus
logger = logging.getLogger(__name__)


class XiezhiExtension(object):
    '''Extension class to log status.
    '''
    def __init__(self, stats):
        '''Initialize class with stats

        Args:
            stats: an instance of the stats in crawler.
        '''
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        '''Initialize an instance using given spider

        Args:
            crawler: an instance of the scrapy crawler.
        '''
        extension = cls(crawler.stats)
        crawler.signals.connect(
            extension.spider_opened,
            signal=signals.spider_opened
        )
        crawler.signals.connect(
            extension.spider_closed,
            signal=signals.spider_closed
        )
        crawler.signals.connect(
            extension.item_dropped,
            signal=signals.item_dropped
        )
        return extension

    def item_dropped(self, item, response, exception, spider):
        '''Log status when item dropped

        Args:
            item: an item dropped.
            response: a ``scrapy.Response`` instance of the item.
            exception: the instance of the exception raised.
            spider: an instance of the scrapy spider.
        '''
        self.stats.inc_value('database_error_count')

    def spider_opened(self, spider):
        '''Log status when spider opened

        Args:
            spider: a instance of the scrapy spider
        '''
        logger.info('Start recording stats from crawler')
        self.stats.set_value('database_error_count', 0)

    def spider_closed(self, spider):
        values = {
            'instance_id': spider.instance_id,
            'start_time': self.stats.get_value('start_time'),
            'finish_time': self.stats.get_value('finish_time'),
            'finish_reason': self.stats.get_value('finish_reason'),
            'item_scraped_count': self.stats.get_value(
                'item_scraped_count'
            ),
            'database_error_count': self.stats.get_value(
                'database_error_count'
            )
        }

        Caduceus.insert(Caduceus(
            title='Crawler xiezhi finished',
            body='\n'.join(
                [
                    '{0}: {1}'.format(key, value)
                    for key, value in values.iteritems()
                ]
            ),
            body_type='text',
            status='pending',
            rule_name='crawler_xiezhi'
        ))


class InstanceExtension(object):
    '''Extension class for creating and tracking instance
    '''
    error_status = False

    @classmethod
    def from_crawler(cls, crawler):
        '''Create an instance from given crawler

        Args:
            crawler: an instance of the scrapy crawler.
        '''
        extension = cls()

        # Connect extensionension object to signals
        crawler.signals.connect(
            extension.spider_opened,
            signal=signals.spider_opened
        )
        crawler.signals.connect(
            extension.spider_closed,
            signal=signals.spider_closed
        )
        crawler.signals.connect(
            extension.spider_error,
            signal=signals.spider_error
        )
        return extension

    def spider_opened(self, spider):
        '''Create instance when spider opened

        Args:
            spider: an instance of the scrapy spider.
        '''
        spider.instance_id = Instance.insert(Instance(
            name=os.environ['SCRAPY_JOB'],
            address='',
            service='xiezhi',
            module='crawler',
            status='running',
        ))

    def spider_closed(self, spider, reason):
        '''Close instance when spider closed.

        Args:
            spider: an instance of the scrapy spider.
            reason: the reason why spider closed.
        '''
        if reason == 'finished' and not self.error_status:
            Instance.update(spider.instance_id, 'status', 'closed')
        else:
            Instance.update(spider.instance_id, 'status', 'error')

    def spider_error(self, failure, response, spider):
        '''Log error when spider raised exception

        Args:
            failure: the exception raised.
            response: the response raised the exception.
            spider: an instance of the scrapy spider.
        '''
        Instance.update(spider.instance_id, 'status', 'error')
        self.error_status = True
