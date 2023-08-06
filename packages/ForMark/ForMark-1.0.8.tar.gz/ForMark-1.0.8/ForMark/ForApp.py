import datetime

import pymongo
import pymysql
from bson import ObjectId
from flask import Flask, g, request, session
from mongoengine import connect

from ForMark.ForLog import ForLog
from ForMark.ForPath import get_root_path
from ForMark.flask_session import Session
import os

from ForMark.model.foot import Foot
from ForMark.model.session import Session as SessionDB

pymysql.install_as_MySQLdb()


class ForApp():
    def __init__(self, import_name, MONGO_HOST_URL, secret_key, log_folder=None, root_path=None):
        self.import_name = import_name
        self.log_folder = log_folder

        if root_path is None:
            root_path = get_root_path(self.import_name)

        self.root_path = root_path
        # 初始化日志
        ForLog(os.path.join(self.root_path, log_folder))

        app = Flask(__name__)
        # json支持中文显示
        app.config['JSON_AS_ASCII'] = False
        app.secret_key = secret_key
        app.config['MONGO_HOST_URL'] = 'MONGO_HOST_URL'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

        # 设置默认session过期时间
        app.config['SESSION_TYPE'] = 'mongodb'
        app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
        app.config[' SESSION_MONGODB'] = pymongo.MongoClient(MONGO_HOST_URL)
        app.config['SESSION_PERMANENT'] = True
        app.config['SESSION_USE_SIGNER'] = False  # 是否对发送到浏览器上session的cookie值进行加密
        app.config['SESSION_KEY_PREFIX'] = 'eic_session:'  # 保存到session中的值的前缀
        app.config['SESSION_MONGODB_DB'] = SessionDB

        Session(app)

        @app.before_request
        def before_request():
            g.request_start_time = datetime.datetime.now()
            # request.json 只能够接受方法为POST、Body为raw，header 内容为 application/json类型的数据：
            # print(request.json if request.method == "POST" else request.args)
            # g.params = request.json if request.method in [
            #     "POST", "PUT"] else request.args
            # if g.params is None and request.method == 'POST' and request.files:
            #     g.params = request.form
            params = {}
            if request.args:
                params.update(request.args.to_dict(flat=True))
            if request.method != 'GET' and request.json:
                if type(request.json) == type([]):
                    for x in request.json:
                        params.update(x)
                else:
                    params.update(request.json)
            if request.form:
                params.update(request.form.to_dict(flat=True))
            g.params = params
            ip = request.remote_addr
            # print("请求头",request.headers)
            try:
                _ip = request.headers["X-Real-IP"]
                if _ip is not None:
                    ip = _ip
            except Exception as e:
                pass
            g.ip = ip
            g.error = False

        @app.after_request
        def after_request(response):
            foot = Foot()
            # 访问用户ID
            user_id = session.get('user_id', None)
            if user_id:
                foot.user_id = ObjectId(user_id)
            # 请求url
            foot.url = request.url
            # 请求原网址
            foot.referrer = request.referrer
            # IP
            foot.ip = g.ip

            # 请求开始时间：
            foot.request_start_time = g.request_start_time
            # 请求结束时间：
            foot.request_end_time = datetime.datetime.now()
            foot.cookies = request.cookies
            ForLog.show("请求的cookies",request.cookies)
            ForLog.show("请求的cookies type",type(request.cookies))
            headers_before = request.headers
            if headers_before:
                headers = {}
                for key, value in headers_before.to_wsgi_list():
                    headers[key] = value
                foot.headers = headers

            # 请求方式
            foot.method = request.method
            # 错误异常
            foot.error = str(g.error) if g.error else None
            foot.save()
            return response

        @app.teardown_request
        def teardown_request(error):
            g.error = error
        ForLog.show("连接mongodb数据库",MONGO_HOST_URL)
        connect(host=MONGO_HOST_URL)
        self.app = app
