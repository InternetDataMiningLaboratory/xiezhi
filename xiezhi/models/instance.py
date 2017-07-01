#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 15.02.2017
'''Persistent object for ``instance``
'''
from xiezhi.database import Base, DBBase
from sqlalchemy import Column, String, Integer
import logging


logger = logging.getLogger(__name__)


class Instance(Base, DBBase):
    '''Persistent class of table ``instance``
    '''
    __tablename__ = 'instance'

    id = Column('id', Integer, primary_key=True)
    address = Column('address', String(255))
    name = Column('name', String(255))
    status = Column('status', String(255))
    module = Column('module', String(255))
    service = Column('service', String(255))

    @classmethod
    def insert(cls, obj, session):
        '''Insert object using given session.

        Args:
            obj: the object to be inserted.
            session: the session to be used.
        Returns:
            a ``String`` representing the inserted primary key.
        '''
        session.add(obj)
        session.flush()
        id = obj.id
        return id

    @classmethod
    def update(cls, id, value_dict, session):
        '''Update object with value dict using given session.
        '''
        session.query(Instance).filter(
            Instance.id == id
        ).update(value_dict)
