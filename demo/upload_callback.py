# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag

from demo.qiniu_utils import *
# access_key = '...'
# secret_key = '...'

q = Auth(access_key, secret_key)

# bucket_name = 'Bucket_Name'

key = f'tmp/123.png'

# 上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
policy = {
    'callbackUrl': 'https://eip-dev.ijiwei.com/api-free-nologin/eip/json',
    'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
}

token = q.upload_token(bucket_name, key, 3600, policy)

localfile = r'D:\tmp\123.png'

ret, info = put_file(token, key, localfile)
print(info)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)

# zz = {"func": "saveLog", "lineno": 68, "pathname": "/home/links/var_www_html/eip/app/Services/LogService.php", "time": "2024-09-06 13:07:35", "levelno": 200, "levelname": "INFO",
#       "process": 12723, "message": "{\"message\":\"{\\\"filename\\\":\\\"123.png\\\",\\\"filesize\\\":\\\"121839\\\"}\"}"}
