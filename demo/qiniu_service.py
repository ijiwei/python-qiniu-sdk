"""
功能描述
:author wjh
:date 2024-09-07
"""
import os.path

from qiniu import Auth, BucketManager
from demo.qiniu_utils import *


class QiniuService:

    name: str = None
    config = {}

    logger = None  # LoggingService
    q: Auth = None
    bucket: BucketManager = None

    def __init__(self, name='pic', **kwargs) -> None:
        super().__init__()
        self.name = name
        # self.config = get_settings(name)
        # self.logger = kwargs.get('logger') if kwargs.get('logger') is not None else LoggingService(logfile='chatglm.log')

        self.config = qiniu_config.get(name)

        access_key = self.config['access_key']
        secret_key = self.config['secret_key']
        bucket_name = self.config['bucket']
        bucket_domain = 'https://s.laoyaoba.com'

        q = Auth(access_key, secret_key)
        bucket = BucketManager(q)
        self.q = q
        self.bucket = bucket

    def fetch_image(self, images: list, path: str = None):
        result = []
        for image in images:
            # key = 'tmp/' + image.split('/')[-1]
            ext = get_extension_from_url(image, '.jpg')
            key = get_key(calculate_md5(image) + ext, path)

            ret, info = self.bucket.fetch(image, bucket_name, key)  # type: dict, ResponseInfo
            assert info.status_code == 200, 'fetch is fail'

            info2: dict = get_image_info(info)
            pic_info: dict = fetch_and_get_image_info(bucket_domain, key)
            assert info2['fsize'] == pic_info['size']
            del pic_info['size']
            info2.update(pic_info)

            result.append({
                'key': calculate_md5(image),
                'url': image,
                'meta': info2
            })

        return result
