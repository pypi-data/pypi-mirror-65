# -*- coding: utf-8 -*-

import datetime
import hashlib
import random
import string
import time
import requests
import json
import base64
from Crypto.Cipher import AES
from flask import current_app as app, g


class Wechat(object):


    @classmethod
    def code2token(cls, code,doctor=True):
        '''服务号code to access_token'''
        if doctor:
            APPID = app.config["WX_APP_ID_DOCTOR"]
            SECRET = app.config["WX_APP_SECRET_DOCTOR"]
        else:
            APPID = app.config["WX_APP_ID_PATIENT"]
            SECRET = app.config["WX_APP_SECRET_PATIENT"]
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(
            APPID, SECRET, code)
        try:
            response = requests.request("GET", url)
            return json.loads(response.text)
        except Exception as e:
            g.logger.error("code2token failed,{}".format(e))

    @classmethod
    def get_userinfo(cls, access_token, openid):
        url = "https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN".format(
            access_token, openid)
        try:
            response = requests.request("GET", url)
            return json.loads(response.text)
        except Exception as e:
            g.logger.error("code2token failed,{}".format(e))

    @classmethod
    def code2Session(cls, code,doctor=True):
        '''小程序code to session'''
        if doctor:
            APPID = app.config["WX_APP_ID_DOCTOR"]
            SECRET = app.config["WX_APP_SECRET_DOCTOR"]
        else:
            APPID = app.config["WX_APP_ID_PATIENT"]
            SECRET = app.config["WX_APP_SECRET_PATIENT"]
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(
            APPID, SECRET, code)
        try:
            response = requests.request("GET", url)
            return json.loads(response.text)
        except Exception as e:
            g.logger.error("code2token failed,{}".format(e))

    @classmethod
    def get_user_info(cls, session_key, encrypted_data, iv,doctor=True):
        """获取用户信息，解析用户手机号也可以"""
        if doctor:
            APPID = app.config["WX_APP_ID_DOCTOR"]
            SECRET = app.config["WX_APP_SECRET_DOCTOR"]
        else:
            APPID = app.config["WX_APP_ID_PATIENT"]
            SECRET = app.config["WX_APP_SECRET_PATIENT"]
        pc = WXBizDataCrypt(APPID, session_key)

        user_info = pc.decrypt(encrypted_data, iv)
        # 获取手机号
        # user_info.get('purePhoneNumber',None)
        return user_info

    
    

class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
