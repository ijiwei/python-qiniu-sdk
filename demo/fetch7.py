"""
功能描述
:author wjh
:date 2024-09-07
"""

from demo.qiniu_utils import *


# 示例使用:
url = 'https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/107b26b8f8334a148e4ad617cb5215aa~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1726319060&x-signature=TEqdxnhSt6%2FuK%2BbqK%2FSShUrOJCs%3D'
extension = get_extension_from_url(url)
print(f"File extension is: {extension}")
