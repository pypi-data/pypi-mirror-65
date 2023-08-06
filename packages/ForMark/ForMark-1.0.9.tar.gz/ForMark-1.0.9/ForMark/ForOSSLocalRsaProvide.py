# -*- coding: utf-8 -*-
import uuid

import oss2
import requests
from flask import current_app
from oss2.crypto import LocalRsaProvider

from ForMark.ForTime import get_time_file

"""
参考文档：https://help.aliyun.com/document_detail/74371.html?spm=a2c4g.11186623.6.903.33962324MWRmY8
数据加密密钥的保存方式有如下两种：
    1、用户自主管理（RSA）
    2、KMS托管
本代码采用第一种
"""

# 以下代码展示了客户端文件加密上传下载的用法，如下载文件、上传文件等，注意在客户端加密的条件下，oss暂不支持文件分片上传下载操作。


# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# 分别以HTTP、HTTPS协议访问。
access_key_id=""
access_key_secret =""
bucket_name =""
endpoint =""

# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param


# 上传网络图片到阿里云
def uploadFileByWebImg(img_url):
    response = requests.get(img_url)
    img = response.content
    return uploadFile(img)


def uploadFile(img):
    # 防止中文
    name = get_time_file() + str(uuid.uuid1()) + "." + img.filename.split('.')[-1]
    dir=current_app.root_path+'/.oss-local-rsa'

    bucket = oss2.CryptoBucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name,
                               crypto_provider=LocalRsaProvider(dir=dir))
    result = bucket.put_object(name, img)

    # 返回key
    return result.status, name


def upload_from_localfile(object_name, filename):
    dir = current_app.root_path + '/.oss-local-rsa'
    bucket = oss2.CryptoBucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name,
                               crypto_provider=LocalRsaProvider(dir=dir))
    result = bucket.put_object_from_file(object_name, filename)
    return result.status, object_name


def get_file_from_key(key):
    dir = current_app.root_path + '/.oss-local-rsa'
    # 创建Bucket对象，可以进行客户端数据加密(用户端RSA)，此模式下只提供对象整体上传下载操作
    bucket = oss2.CryptoBucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name,
                               crypto_provider=LocalRsaProvider(dir=dir))
    file = bucket.get_object(key)
    return file


# key = 'motto.txt'
# content = b'a' * 1024 * 1024
# filename = 'download.txt'
#
# # 创建Bucket对象，可以进行客户端数据加密(用户端RSA)，此模式下只提供对象整体上传下载操作
# bucket = oss2.CryptoBucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name,
#                            crypto_provider=LocalRsaProvider())
#
# key1 = 'motto-copy.txt'
#
# # 上传文件
# bucket.put_object(key, content, headers={'content-length': str(1024 * 1024)})
#
# """
# 文件下载
# """
#
# # 下载文件
# # 原文件
# result = bucket.get_object(key)
#
# # 验证一下
# content_got = b''
# for chunk in result:
#     content_got += chunk
# assert content_got == content
#
# # 下载原文件到本地文件
# result = bucket.get_object_to_file(key, filename)
#
# # 验证一下
# with open(filename, 'rb') as fileobj:
#     assert fileobj.read() == content
#
# os.remove(filename)

# # 创建Bucket对象，可以进行客户端数据加密(使用阿里云KMS)，此模式下只提供对象整体上传下载操作
# bucket = oss2.CryptoBucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name,
#                            crypto_provider=AliKMSProvider(access_key_id, access_key_secret, region, cmk, '1234'))
#
# key1 = 'motto-copy.txt'
#
# # 上传文件
# bucket.put_object(key, content, headers={'content-length': str(1024 * 1024)})
#
# """
# 文件下载
# """
#
# # 下载文件
# # 原文件
# result = bucket.get_object(key)

# # 验证一下
# content_got = b''
# for chunk in result:
#     content_got += chunk
# assert content_got == content
#
# # 下载原文件到本地文件
# result = bucket.get_object_to_file(key, filename)
#
# # 验证一下
# with open(filename, 'rb') as fileobj:
#     assert fileobj.read() == content
#
# os.remove(filename)

if __name__ == '__main__':
    crypto_provider = LocalRsaProvider()
    print(crypto_provider.dir)
    # print(uploadFileByWebImg('https://img.yaofun.vip/%E4%B8%8A%E4%BC%A0logo.png'))
