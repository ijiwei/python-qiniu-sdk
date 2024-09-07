# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth
from qiniu import BucketManager

from demo.qiniu_utils import *
# access_key = '...'
# secret_key = '...'

# 初始化Auth状态
q = Auth(access_key, secret_key)

# 初始化BucketManager
bucket = BucketManager(q)

# 你要测试的空间， 并且这个key在你空间中存在
# bucket_name = 'Bucket_Name'
key = 'tmp/t1.jpg'

# 获取文件的状态信息
ret, info = bucket.stat(bucket_name, key)
print(ret)
print(info.text_body)
assert 'hash' in ret
