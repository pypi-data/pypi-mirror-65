import datetime
import pickle
import uuid

from flask import json
from flask.sessions import SessionMixin, SessionInterface
from itsdangerous import Signer, BadSignature, want_bytes


class MongodbSession(dict, SessionMixin):
    def __init__(self, initial=None, sid=None, permanent=None):
        self.sid = sid
        self.initial = initial
        if permanent:
            self.permanent = permanent
        super(MongodbSession, self).__init__(initial or ())

    def __setitem__(self, key, value):
        super(MongodbSession, self).__setitem__(key, value)

    def __getitem__(self, item):
        return super(MongodbSession, self).__getitem__(item)

    def __delitem__(self, key):
        super(MongodbSession, self).__delitem__(key)


class MongodbSessionInterface(SessionInterface):
    session_class = MongodbSession

    def __init__(self, key_prefix, my_session, serializer=pickle, use_signer=True):
        # use_signer：是否使用签名算法
        self.use_signer = use_signer
        # key_prefix：设置key的前缀
        self.key_prefix = key_prefix
        self.my_session = my_session
        self.serializer = serializer

    def _generate_sid(self):
        return str(uuid.uuid4())

    def _get_signer(self, app):
        if not app.secret_key:
            return None
        return Signer(app.secret_key, salt='flask-session',
                      key_derivation='hmac')

    def open_session(self, app, request):
        """程序刚启动时执行，需要返回一个session对象"""
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self._generate_sid()
            return self.session_class(sid=sid)
        if self.use_signer:
            signer = self._get_signer(app)
            if signer is None:
                return None
            try:
                sid_as_bytes = signer.unsign(sid)
                sid = sid_as_bytes.decode()
            except BadSignature:
                sid = self._generate_sid()
                return self.session_class(sid=sid, permanent=self.permanent)

        store_id = self.key_prefix + sid
        the_one = self.my_session.objects(store_id=store_id).first()
        if the_one and the_one.expiration <= datetime.datetime.utcnow():
            # Delete expired session
            the_one.delete()
            document = None
        if the_one is not None:
            try:
                val = the_one.val
                data = self.serializer.loads(want_bytes(val))
                return self.session_class(data, sid=sid)
            except:
                return self.session_class(sid=sid, permanent=self.permanent)
        return self.session_class(sid=sid, permanent=self.permanent)

    def save_session(self, app, session, response):
        """
        程序结束前执行，可以保存session中所有的值
        如：
        保存到 mongodb
        写入到用户cookie
        """
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        store_id = self.key_prefix + session.sid
        the_one = self.my_session.objects(store_id=store_id).first()
        if not session:
            if session.modified:
                if the_one:
                    the_one.delete()
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain, path=path)
            return

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))

        # session保存在mongodb中
        if not the_one:
            the_one = self.my_session()
        the_one.store_id = store_id
        the_one.expiration = expires
        the_one.val = val

        if self.use_signer:
            session_id = self._get_signer(app).sign(want_bytes(session.sid))
        else:
            session_id = session.sid
        response.set_cookie(app.session_cookie_name, session_id,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure)
