# -*- coding:utf-8 -*-
# @Function  : 
# @Author    : wjh
# @Time      : 2024/9/6
# Version    : 1.0

import hashlib
import json
import mimetypes

import requests

from qiniu.http import ResponseInfo

qiniu_config = {
    'pic': {  # 图库
        'access_key': '99vFAJy1wVeXiJdSV2BB-VHqOhgKrdRZydXfUv58',
        'secret_key': '0_U300euhKNww5ziodpEZmQ2l8rMVRlKnNwqEywx',
        'image_url': 'https://s.laoyaoba.com/',
        'document_name': 'jwImg/',
        'bucket': 'jiwei-images',
    },
    'trade': {  # 贸易管制
        'access_key': '99vFAJy1wVeXiJdSV2BB-VHqOhgKrdRZydXfUv58',
        'secret_key': '0_U300euhKNww5ziodpEZmQ2l8rMVRlKnNwqEywx',
        'image_url': 'https://privte.laoyaoba.com/',
        'document_name': 'infoplat/trade/',
        'bucket': 'jiwei-private-video',
    }
}

access_key = qiniu_config['pic']['access_key']
secret_key = qiniu_config['pic']['secret_key']
bucket_name = qiniu_config['pic']['bucket']
bucket_domain = 'https://s.laoyaoba.com'


def fetch_and_get_image_info(bucket_domain: str, key: str):
    """
    从第三方 URL 抓取图片并返回图片的元数据信息。
    :param bucket_domain: 域名
    :param key: 在七牛云存储空间保存的文件名（key）
    :return: 图片的元数据信息 (width, height, format) 信息
    """
    image_info_url = f'{bucket_domain}/{key}?imageInfo'
    print(image_info_url)
    response = requests.get(image_info_url)

    if response.status_code == 200:
        return response.json()  # 返回图片的元数据信息
    else:
        return {"error": f"Failed to get image info: {response.status_code}"}


def get_image_info(info: ResponseInfo) -> dict:
    """
    转化图片信息格式
    :param info: 图片信息
    :return:
    """
    try:
        assert info.status_code == 200
        data = json.loads(info.text_body)
        data['req_id'] = info.req_id
        data['x_log'] = info.x_log
        print(data)
        return data
    except Exception as ex:
        print(f"ex: {str(ex)}")
        return None


def calculate_md5(input_string) -> str:
    """
    计算字符串 md5
    :param str input_string:
    :return:
    """
    # Create an md5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the string (it needs to be encoded to bytes)
    md5_hash.update(input_string.encode('utf-8'))

    # Return the hexadecimal digest of the hash
    return md5_hash.hexdigest()


def get_extension_from_url(url, default_extension='.jpg'):
    """
    根据图片 URL 请求头的 Content-Type 推断文件扩展名。
    :param url: 图片的 URL 地址
    :param default_extension: 无法推断时的默认扩展名，默认为 '.jpg'
    :return: 文件扩展名 (例如 '.jpg', '.png')，如果无法推断则返回默认扩展名
    """
    try:
        # 发起 HEAD 请求，获取图片的 Content-Type
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type')

        # 根据 Content-Type 推断扩展名
        extension = mimetypes.guess_extension(content_type)
        if extension is None:
            return default_extension
        return extension
    except Exception as e:
        # 请求失败时，返回默认扩展名
        print(f"Error fetching extension: {e}")
        return default_extension
