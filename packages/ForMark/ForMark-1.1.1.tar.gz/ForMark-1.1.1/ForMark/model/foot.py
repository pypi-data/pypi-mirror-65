import datetime

from mongoengine import DynamicDocument, ObjectIdField, DateTimeField, StringField, DictField


class Foot(DynamicDocument):
    """足迹"""
    __tablename__ = 'foot'
    # 访问用户ID
    user_id = ObjectIdField()
    # 请求url
    url = StringField()
    # 请求原网址
    referrer = StringField()
    # IP
    ip = StringField()
    create_time = DateTimeField(required=True, default=datetime.datetime.now)

    # 请求开始时间：
    request_start_time = DateTimeField()
    # 请求结束时间：
    request_end_time = DateTimeField()

    cookies = DictField()
    # 请求头
    headers = DictField()
    # 请求方式
    method = StringField()
    # 错误异常
    error = StringField()
