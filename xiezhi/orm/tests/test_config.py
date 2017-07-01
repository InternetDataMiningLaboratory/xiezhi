#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
'''Test ``config``
'''
import yaml
import pkg_resources

from .. import config
from ..config import ObjectNotDictError, DictAsClass, Config
from nose.tools import assert_equals
from mock import patch


def test_objectnotdicterror():
    '''UnitTest of ``config.ObjectNotDictError``
    '''
    assert_equals(
        'Try to inialize with a non-dict object: test',
        str(ObjectNotDictError('test'))
    )


def test_dictasclass():
    '''UnitTest of ``config.DictAsClass``
    '''
    example = {
        'test': 'test',
        'test_dict': {
            'test': 'test'
        }
    }
    test_ins = DictAsClass(example)
    assert_equals(
        test_ins.test,
        'test'
    )
    assert_equals(
        test_ins.test_dict.test,
        'test'
    )


@patch.object(pkg_resources, 'resource_filename')
@patch.object(yaml, 'load')
@patch.object(config, 'PROJECT_NAME', 'test')
@patch.object(config, 'open')
@patch.object(DictAsClass, '__init__')
def test_Config(mock_dict_class, mock_open, mock_load, mock_resource):
    '''UnitTest of ``config.Config``

    Args:
        mock_dict_class: mock object of 'config.DictAsClass'
        mock_open: mock object of 'config.open'
        mock_load: mock object of 'yaml.load'
        mock_resource: mock object of 'pkg_resources.resource_filename'
    '''
    mock_resource.return_value = 'test'
    mock_open.return_value.__enter__.return_value = 'test'
    mock_load.return_value = 'test'

    test_arg = 'test'

    Config(test_arg)

    mock_resource.assert_called_with('test.conf', test_arg)
    mock_open.assert_called_with('test')
    mock_load.assert_called_with('test')
    mock_dict_class.assert_called_with('test')
