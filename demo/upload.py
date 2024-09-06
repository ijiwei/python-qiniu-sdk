# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from qiniu.compat import is_py2, is_py3

# 需要填写你的 Access Key 和 Secret Key
from demo.qiniu_utils import *
# access_key = '...'
# secret_key = '...'

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 要上传的空间
# bucket_name = ''

# 上传到七牛后保存的文件名
key = f'tmp/123.png'

# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

# 要上传文件的本地路径
localfile = r'D:\tmp\123.png'

ret, info = put_file(token, key, localfile)
print(ret)
print(info)

if is_py2:
    assert ret['key'].encode('utf-8') == key
elif is_py3:
    assert ret['key'] == key

assert ret['hash'] == etag(localfile)

# {'hash': 'FlN0-C_wd5E0E7K4BOhT0xAWN6Ym', 'key': 'tmp/123.png'}
# _ResponseInfo__response:<Response [200]>, exception:None, status_code:200, text_body:{"hash":"FlN0-C_wd5E0E7K4BOhT0xAWN6Ym","key":"tmp/123.png"}, req_id:0LIAAADKXthujfIX, x_log:X-Log