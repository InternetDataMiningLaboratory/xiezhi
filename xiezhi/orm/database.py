#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
'''Database Connection
'''
import arrow
import logging

from .config import Config
from .constant import DEPLOY_CONFIG

from decimal import Decimal
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base


LOGGER = logging.getLogger(__name__)
BASE = declarative_base()


class DBSessionMaker(object):
    '''An instance of sessionmaker.
    '''
    def __init__(self, config_file=DEPLOY_CONFIG):
        '''Initialize connection with given config filename.

        Read configuration from a ``Config`` instance with given config
        filename, and initialize the ``engine`` with user, password, host, port
        and database. If any exception raised by ``create_engine`` will be
        logged and no engine will be created. If the exception is created
        successfully, a ``metadata`` is created with ``engine`` to create a
        ``sessionmaker`` which can create ``session`` later
        '''
        settings = Config(config_file).mysql
        user, password, host, port, database = \
            (
                settings.user, settings.password, settings.host, settings.port,
                settings.database
            )
        try:
            self.engine = create_engine(
                'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
                    user, password, host, port, database,
                ),
                pool_recycle=3600,
                encoding='utf8',
            )
        except Exception, e:
            LOGGER.exception(e)
            return None
        else:
            LOGGER.info('Successfully Build Connection')
        self.metadata = MetaData(bind=self.engine)
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=self.engine)


class DBSession(object):
    '''Encapsulate the session to be used in with statement.
    '''
    def __init__(self, session_maker):
        '''Initialize class with given session maker.

        Args:
            session_maker: sessionmaker
        '''
        self.session_maker = session_maker

    def __enter__(self):
        '''Method called before get into the with clause.

        Return the session created by given session_maker.

        Args:
            config_file: a ``String`` representing the config filename.
        '''
        self._session = self.session_maker()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Method called when exit the with clause or exception raised.

        Commit the session if no exception raised, or rollback.

        Args:
            exc_type: a ``class`` representing the type of raised Exception.
            exc_val: raised exception.
            exc_tb: the traceback of raised exception.

        Raised:
            Any exceptions raised in the with clause.
        '''
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()
            self._session.close()
            raise exc_val
        self._session.close()


class DBBase(object):
    '''Persisted object class
    '''
    value_type_dict = {
        datetime: '_datetime',
        time: '_time',
        date: '_date',
        Decimal: '_decimal'
    }

    def get_items(self):
        ''' Get columns and values from ``_sa_instance_state.attr.items()``
        '''
        return self._sa_instance_state.attrs.items()

    def __eq__(self, other):
        '''Overlap the eq method to compare object to dict.

        If key not in self, then return False, or get the value in self. If the
        type of the value in ``value_type_dict``, namely that the value need a
        transform before compare, call corresponding method in
        ``value_type_dict``. Finally, return if the value is equal to self
        value.

        Args:
            other: a dict with all key-value pairs to be compared.
        '''
        if isinstance(other, dict):
            for key, value in other.iteritems():
                try:
                    self_value = getattr(self, key)
                except AttributeError:
                    return False
                for value_type, method in self.value_type_dict.iteritems():
                    if type(self_value) == value_type:
                        self_value = getattr(self, method)(self_value)
                        break
                if self_value != value:
                    return False
            return True
        return False

    def _time(self, time):
        '''Method to transform ``time``.
        '''
        return time.strftime('%H:%M:%S')

    def _date(self, date):
        '''Method to transform ``date``.
        '''
        return arrow.get(date).format('YYYY-MM-DD')

    def _datetime(self, date):
        '''Method to transform ``datetime``.
        '''
        return arrow.get(date).format('YYYY-MM-DD')

    def _decimal(self, decimal):
        '''Method to transform ``decimal.Decimal()`` to ``float``
        '''
        return float(decimal)
