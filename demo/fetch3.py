# -*- coding: utf-8 -*-
# flake8: noqa
from hashlib import md5

from qiniu import Auth
from qiniu import BucketManager

from demo.qiniu_utils import *
from qiniu.http import ResponseInfo

# access_key = '...'
# secret_key = '...'

# bucket_name = 'Bucket_Name'

q = Auth(access_key, secret_key)

bucket = BucketManager(q)

url = 'https://mmbiz.qpic.cn/sz_mmbiz_jpg/hywqATMqTK1z66Ql95jWPO0FuenNF7FaD75EwrM6icOnh2nX0HeKX8NQLMe1noI6r8ZDmebXPnrpwuYD4Aab5ow/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1'

key = 'tmp/t1.jpg'

images = [
    'https://n.sinaimg.cn/spider20240906/521/w850h471/20240906/bb88-c6db3c308874b7bb0fab8f0208781c8a.png',
    'https://n.sinaimg.cn/spider20240906/514/w850h464/20240906/5324-72bd1f35ace5406b9e7b6da192bb53c2.png',
    'https://n.sinaimg.cn/spider20240906/562/w850h512/20240906/dd2b-08d321279244d3c6d2cf297b0f6ebe18.png',
    'https://n.sinaimg.cn/spider20240906/635/w850h585/20240906/187b-ee7593ba0a5b277336856e03571d7ab2.png',
    'https://n.sinaimg.cn/finance/d3f34f8d/20240626/fireicon.png',
    'https://n.sinaimg.cn/news/42f7389d/20190523/JiJin300x250.jpg'
]

result = []

for image in images:
    key = 'tmp/' + image.split('/')[-1]
    print(key)

    # {'fsize': 72654, 'hash': 'Fu0IphqenJupuBVEZSXPE-RSjCBM', 'key': 'tmp/t1.jpg', 'mimeType': 'image/webp'}
    # _ResponseInfo__response:<Response [200]>, exception:None, status_code:200, text_body:{"fsize":72654,"hash":"Fu0IphqenJupuBVEZSXPE-RSjCBM","key":"tmp/t1.jpg","mimeType":"image/webp"}, req_id:pgQAAACFD54B1fIX, x_log:X-Log
    ret, info = bucket.fetch(image, bucket_name, key)  # type: dict, ResponseInfo
    print(ret)
    print(info)
    assert info.status_code == 200, 'fetch is fail'

    info2: dict = get_image_info(info)
    print(info2)

    pic_info: dict = fetch_and_get_image_info(bucket_domain, key)
    print(pic_info)
    assert info2['fsize'] == pic_info['size']
    del pic_info['size']

    info2.update(pic_info)

    result.append({
        'key': calculate_md5(image),
        'url': image,
        'meta': info2
    })

    # {'size': 72654, 'format': 'webp', 'width': 1080, 'height': 720, 'colorModel': 'ycbcr'}
    #  stata
    # {"fsize":72654,"hash":"Fu0IphqenJupuBVEZSXPE-RSjCBM","md5":"fcf62954731c51980a305f9307e70592","mimeType":"image/webp","putTime":17256015305382705,"type":0}


print(result)