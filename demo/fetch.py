# -*- coding: utf-8 -*-
# flake8: noqa
import json

from qiniu import Auth
from qiniu import BucketManager
import requests

from demo.qiniu_utils import *
from qiniu.http import ResponseInfo

# access_key = '...'
# secret_key = '...'

# bucket_name = 'Bucket_Name'

q = Auth(access_key, secret_key)

bucket = BucketManager(q)

url = 'https://mmbiz.qpic.cn/sz_mmbiz_jpg/hywqATMqTK1z66Ql95jWPO0FuenNF7FaD75EwrM6icOnh2nX0HeKX8NQLMe1noI6r8ZDmebXPnrpwuYD4Aab5ow/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1'

key = 'tmp/t1.jpg'

ret, info = bucket.fetch(url, bucket_name, key)  # type: dict, ResponseInfo
print(ret)
print(info)
assert ret['key'] == key

info2: dict = get_image_info(info)
print(info2)

pic_info: dict = fetch_and_get_image_info(bucket_domain, key)
print(pic_info)

assert info2['fsize'] == pic_info['size']
del pic_info['size']

info2.update(pic_info)

print(info2)
