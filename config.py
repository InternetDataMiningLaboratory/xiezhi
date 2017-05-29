#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
'''Logics of configuration
'''
import yaml
import pkg_resources
from constant import PROJECT_NAME


class ObjectNotDictError(Exception):
    '''Exception class raised when the initialization arguments of
    ``ClassAsDict`` not an instance of ``dict``
    '''
    def __init__(self, dic):
        '''Initialize the class with the mistaken dict.

        Args:
            dic: an object of the wrongly input object.
        '''
        self.dic = dic

    def __str__(self):
        '''Serialize the Exception.
        '''
        return 'Try to inialize with a non-dict object: {0}'.format(
            self.dic
        )


class DictAsClass(object):
    '''Self-defined class to read keys from a dict as an attribute of an instance.
    '''
    def __init__(self, dic):
        '''Initialize the class with an dict

        If ``dic`` not an instance of ``dict``, raise ``ObjectNotDictError``
        with ``dic``

        Args:
            dic: a dict.
        '''
        if not isinstance(dic, dict):
            raise ObjectNotDictError(dic)

        self.__dict__ = dic

        for key, value in self.__dict__.iteritems():
            if isinstance(value, dict):
                self.__dict__[key] = DictAsClass(value)

    def __getattr__(self, key):
        '''Overload magic method to get attribute from the dict

        Args:
            key: a string reperesenting the key in dict.

        Returns:
            the value from ``self.__dict__``
        '''
        return self.__dict__.get(key)

    def as_dict(self):
        '''Return the dict of the instance

        Returns:
            a dict of the ``self.__dict__``
        '''
        return self.__dict__


class Config(DictAsClass):
    '''Class for config files
    '''
    def __init__(self, filename):
        '''Initialize the class with given filename.

        Read configureation from ``filename`` after generate the absolute path
        and initialize the class with the configuration dict.

        Args:
            filename: a string representing the configuration file.
        '''
        with open(
            pkg_resources.resource_filename(
                PROJECT_NAME+'.conf',
                '{0}'.format(filename)
            )
        ) as ymlfile:
            super(Config, self).__init__(yaml.load(ymlfile))
