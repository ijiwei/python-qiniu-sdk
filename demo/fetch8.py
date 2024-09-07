"""
功能描述
:author wjh
:date 2024-09-07
"""

from demo.qiniu_utils import *


from urllib.parse import urlparse, unquote
import os

def get_extension_from_url(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    _, ext = os.path.splitext(path)
    return ext if ext else None

# 示例
url1 = "https://n.sinaimg.cn/spider20240906/562/w850h512/20240906/dd2b-08d321279244d3c6d2cf297b0f6ebe18.png"
extension = get_extension_from_url(url1)
print(f"File extension is: {extension}")

import requests
import mimetypes


def get_extension_from_url_or_content_type(url, default_extension='.jpg'):
    # 首先尝试从 URL 解析扩展名
    extension = get_extension_from_url(url)
    if extension and is_valid_extension(extension):
        return extension

    # 如果 URL 中没有扩展名，则通过 Content-Type 推断
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type')
        extension = mimetypes.guess_extension(content_type)
        if extension:
            return extension
        else:
            return default_extension
    except Exception as e:
        print(f"Error fetching Content-Type: {e}")
        return default_extension


# 示例使用复杂 URL
url2 = "https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/107b26b8f8334a148e4ad617cb5215aa~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1726319060&x-signature=TEqdxnhSt6%2FuK%2BbqK%2FSShUrOJCs%3D"
extension = get_extension_from_url_or_content_type(url2)
print(f"File extension is: {extension}")
