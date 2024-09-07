# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth
from qiniu import BucketManager

import requests
from demo.qiniu_utils import *

# access_key = '...'
# secret_key = '...'

# bucket_name = 'Bucket_Name'


key = 'tmp/t1.jpg'

image_url = 'https://s.laoyaoba.com/tmp/t1.jpg?imageInfo'
bucket_domain = 'https://s.laoyaoba.com'


def fetch_and_get_image_info(bucket_domain, key):
    """
    从第三方 URL 抓取图片并返回图片的元数据信息。

    参数:
    - url: 第三方图片的 URL
    - key: 在七牛云存储空间保存的文件名（key）

    返回:
    - 图片的元数据信息 (width, height, format) 或错误信息
    """
    image_info_url = f'{bucket_domain}/{key}?imageInfo'
    response = requests.get(image_info_url)

    if response.status_code == 200:
        return response.json()  # 返回图片的元数据信息
    else:
        return {"error": f"Failed to get image info: {response.status_code}"}


dd = fetch_and_get_image_info(bucket_domain, key)
print(dd)
