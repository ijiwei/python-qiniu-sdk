# -*- coding: utf-8 -*-
# flake8: noqa

from demo.qiniu_service import QiniuService

# key = 'tmp/t1.jpg'

images = [
    'https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/107b26b8f8334a148e4ad617cb5215aa~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1726319060&x-signature=TEqdxnhSt6%2FuK%2BbqK%2FSShUrOJCs%3D',
    'https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/7a1204e2b84dd53be6b340d2e2d10ce8~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1726319060&x-signature=0oEC%2FXMk8mTaei6JKtLVv3pfejo%3D',
]


qs = QiniuService(name='pic')
data = qs.fetch_image(images)
print(data)
