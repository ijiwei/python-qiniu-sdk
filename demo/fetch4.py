# -*- coding: utf-8 -*-
# flake8: noqa

from demo.qiniu_service import QiniuService


key = 'tmp/t1.jpg'

images = [
    'https://n.sinaimg.cn/spider20240906/521/w850h471/20240906/bb88-c6db3c308874b7bb0fab8f0208781c8a.png',
    'https://n.sinaimg.cn/spider20240906/514/w850h464/20240906/5324-72bd1f35ace5406b9e7b6da192bb53c2.png',
    'https://n.sinaimg.cn/spider20240906/562/w850h512/20240906/dd2b-08d321279244d3c6d2cf297b0f6ebe18.png',
    'https://n.sinaimg.cn/spider20240906/635/w850h585/20240906/187b-ee7593ba0a5b277336856e03571d7ab2.png',
    'https://n.sinaimg.cn/finance/d3f34f8d/20240626/fireicon.png',
    'https://n.sinaimg.cn/news/42f7389d/20190523/JiJin300x250.jpg'
]


qs = QiniuService(name='pic')
data = qs.fetch_image(images)
print(data)
