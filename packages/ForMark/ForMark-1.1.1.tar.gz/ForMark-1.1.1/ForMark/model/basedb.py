import datetime

from mongoengine import DynamicDocument, ObjectIdField, DateTimeField, StringField, DictField


class BaseDb(DynamicDocument):
    pass

