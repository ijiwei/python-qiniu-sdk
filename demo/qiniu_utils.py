# -*- coding:utf-8 -*-
# @Function  : 
# @Author    : wjh
# @Time      : 2024/9/6
# Version    : 1.0


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
