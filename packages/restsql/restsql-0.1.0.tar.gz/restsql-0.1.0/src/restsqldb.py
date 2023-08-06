# -*- coding:utf-8 -*-
from peewee import SqliteDatabase, PostgresqlDatabase, Database, Model
from elasticsearch import Elasticsearch
from model import ModelMeta
from table import Table, StringField, NumberField, BoolField


class EnumDataBase:
    PG = 'PostgreSQL'
    MYSQL = 'MySql'
    SQLITE = 'SQLite'
    ES = 'Elasticsearch'


class RestSqlDb(object):

    def __init__(self, db_setting):
        db_type = db_setting.get('type', None)
        db = None
        if db_type == EnumDataBase.PG:
            # todo：初始化pg链接实例
            self._check_db_setting(setting=db_setting, check_fields=['name', 'type', 'host', 'schema', 'user', 'password', 'db'])
            db = PostgresqlDatabase(
                db_setting['db'],
                user=db_setting['user'],
                password=db_setting['password'],
                host=db_setting['host'],
                port=db_setting['port']
            )
            # db = SqliteDatabase(db_setting['host'])
            pass
        elif db_type == EnumDataBase.MYSQL:
            # todo：初始化mysql链接实例
            # db = SqliteDatabase(db_setting['host'])
            pass
        elif db_type == EnumDataBase.SQLITE:
            # 初始化sqlite实例
            self._check_db_setting(setting=db_setting, check_fields=['name', 'host', 'tables'])
            db = SqliteDatabase(db_setting['host'])

        elif db_type == EnumDataBase.ES:
            # todo：初始化es实例
            self._check_db_setting(setting=db_setting, check_fields=['name', 'host', 'tables'])
            db = Elasticsearch(db_setting['host'])
        else:
            raise RuntimeError('db type is invalid')
        if db:
            self.type = db_type
            self.name = db_setting['name']
            self.tables = db_setting['tables']
            self.db = db
            self.schema = db_setting.get('schema', None)

    @staticmethod
    def _check_db_setting(setting, check_fields):
        for field in check_fields:
            if setting.get(field, None) is None:
                raise RuntimeError('db setting need field: {}'.format(field))






