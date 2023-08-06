from mongoengine import *


class Session(DynamicDocument):
    """session"""
    __tablename__ = 'session'
    #  store_id = self.key_prefix + sid
    store_id = StringField(required=True)
    expiration = DateTimeField()
    val = StringField()
