#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
'''Tests of database base class.
'''
import arrow
import pkg_resources
import nose.tools as tools
from ..database import DBSession, DBBase, DBSessionMaker
from ..constant import TEST_SERVICE_CONFIG
from mock import Mock, patch
from decimal import Decimal


def test_DBSession():
    '''Tests of ``database.DBSession``
    '''
    # Generate Mock object.
    mock_session = Mock()
    mock_maker = Mock()
    mock_session.commit.return_value = None
    mock_session.rollback.return_value = None
    mock_session.close.return_value = None
    mock_maker.return_value = mock_session

    # Test 1: Normal call.
    with DBSession(mock_maker) as session:
        tools.assert_equal(session, mock_session)
        mock_maker.assert_called_with()
    mock_session.commit.assert_called_with()
    mock_session.close.assert_called_with()

    # Test 2: Exception raised in the with clause.
    def _nested_func():
        with DBSession(mock_maker):
            raise Exception()
    tools.assert_raises(Exception, _nested_func)
    mock_session.rollback.assert_called_with()
    mock_session.close.assert_called_with()


@patch.object(DBBase, '_datetime')
@patch.object(DBBase, '_decimal')
def test_DBBase_eq(mock_decimal, mock_time):
    '''Test of ``database.DBBase.__eq__``
    '''
    # Test 1: Non-dict object is not considered equal
    tools.assert_not_equals(DBBase(), 'test')

    # Test 2: Dict object
    test_dict = {}

    # Test 2.1: Key not in object, return False
    test_dict['test'] = 'test'
    tools.assert_not_equals(DBBase(), test_dict)

    # Set up test class for following test cases.
    class TestBase(DBBase):
        test = 'test'
        test_date = '1995-01-08'
        test_decimal = Decimal(9.999)

    # Non-equal value, return False
    test_dict['test_date'] = '1995-01-01'
    tools.assert_not_equals(TestBase(), test_dict)

    # Equal value after formatting, return True
    test_dict['test_date'] = '1995-01-08'
    base = TestBase()
    base.test_date = arrow.get('1995-01-08').datetime
    mock_time.return_value = '1995-01-08'
    tools.assert_equals(base, test_dict)
    mock_time.assert_called_with(base.test_date)

    decimal_dict = dict()
    decimal_base = TestBase()
    decimal_dict['test_decimal'] = 9.999
    mock_decimal.return_value = 9.999
    tools.assert_equals(decimal_base, decimal_dict)
    mock_decimal.assert_called_with(decimal_base.test_decimal)


class TestService(object):
    '''Test class for set up environment.
    '''
    def setUp(self):
        '''Set up test database connection
        '''
        self.session_maker = DBSessionMaker(TEST_SERVICE_CONFIG).session_maker
