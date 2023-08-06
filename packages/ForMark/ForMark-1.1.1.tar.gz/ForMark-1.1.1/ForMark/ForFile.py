import os

from flask import current_app

from ForMark.ForOSSLocalRsaProvide import upload_from_localfile
from ForMark.ForTime import get_time_file


def get_url_from_file(file_name, local_url,remove_local=False):
    status, key = upload_from_localfile(get_time_file() + file_name, local_url)
    # 删除临时文件
    if os.path.exists(local_url):
        os.remove(local_url)
    return status, key


def get_local_image(name):
    dir = current_app.root_path
    images_dir = os.path.join(dir, 'images')
    image = os.path.join(images_dir, name)
    if os.path.exists(image):
        with open(image, 'rb') as img:
            return img.read()
    return None
