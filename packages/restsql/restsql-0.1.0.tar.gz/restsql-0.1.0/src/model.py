# -*- coding:utf-8 -*-
from peewee import ModelBase, Model, TextField, DoubleField, BooleanField, Database, SqliteDatabase, IntegerField
from table import Table, StringField, NumberField, BoolField
from copy import deepcopy


class ModelMeta(ModelBase):

    def __new__(mcs, name, bases, attrs):
        base_attrs = deepcopy(attrs)
        meta = base_attrs.get('Meta', None)
        for field, field_type in meta.fields.items():
            if isinstance(field_type, StringField):
                base_attrs[field] = TextField()
            elif isinstance(field_type, NumberField):
                base_attrs[field] = DoubleField()
            elif isinstance(field_type, BoolField):
                base_attrs[field] = BooleanField()
        del meta.fields  # 删除该类属性，否则进入base.new中fields属性会产生冲突
        return super(ModelMeta, mcs).__new__(mcs, name, bases, base_attrs)


# def gen_model(db, schema):
#     if not isinstance(db, Database):
#         raise RuntimeError('db is not Database instance')
#     if schema.__bases__[0] != Schema:
#         raise RuntimeError('schema is not Schema class')
#
#     class NewModel(Model):
#         __metaclass__ = ModelMeta
#
#         class Meta:
#             database = db
#             table_name = schema.table_name
#             fields = schema.fields
#     return NewModel


class User(Table):
    table_name = 'user'
    fields = {
        'version': NumberField(),
        'login': StringField(),
        'email': StringField()
    }


if __name__ == '__main__':
    user = gen_model(db, User)
    result = user.get(user.login == 'venzozhang')
    print result.login, result.email, result.version






