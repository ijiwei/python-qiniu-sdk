# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth
from qiniu import BucketManager

from demo.qiniu_utils import *
# access_key = '...'
# secret_key = '...'

# bucket_name = 'Bucket_Name'

q = Auth(access_key, secret_key)

bucket = BucketManager(q)

url = 'https://mmbiz.qpic.cn/sz_mmbiz_jpg/hywqATMqTK1z66Ql95jWPO0FuenNF7FaD75EwrM6icOnh2nX0HeKX8NQLMe1noI6r8ZDmebXPnrpwuYD4Aab5ow/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1'

key = 'tmp/t1.jpg'

ret, info = bucket.fetch(url, bucket_name, key)
print(info)
assert ret['key'] == key
