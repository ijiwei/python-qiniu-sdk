# -*- coding: utf-8 -*-
# flake8: noqa

from demo.qiniu_service import QiniuService
import requests

image_info_url = 'https://s.laoyaoba.com/tmp/bb88-c6db3c308874b7bb0fab8f0208781c8a.png?imageInfo'
response = requests.get(image_info_url)

print(response.content)
