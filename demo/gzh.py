"""
功能描述
:author wjh
:date 2024-09-08
"""
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import RemoteConnection
from jwtools.io_util import *

url = 'https://mp.weixin.qq.com/s?__biz=MzU5NzE0NjE0MQ==&mid=2247805678&idx=2&sn=e66086c6dc8680c205b68f6a6428d5cf&chksm=ff86048ef1812d376b1eba6c91678480646db9d47f73505d4a26b4abe0f82631f7422dac7d57&scene=126&sessionid=1725761056#rd'

content_xpath = '//div[@id="js_content" or @id="js_share_notice" or @class="wx_video_play_opr" or @class="rich_media_content"]'


def get_webdriver():
    opt = webdriver.ChromeOptions()
    opt.add_argument("no-sandbox")
    opt.add_argument("--disable-extensions")
    # opt.add_argument("--headless")
    return webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=opt)


def get_gzh_images(webdriver, xpath: str):
    if webdriver is None:
        driver = get_webdriver()
        driver.implicitly_wait(10)
    else:
        driver = webdriver

    driver.get(url)

    # write_text_to_file("1.thml", driver.page_source)
    element = driver.find_element(By.XPATH, xpath)

    result = []
    images = element.find_elements(By.XPATH, './/img')
    for image in images:
        html = image.get_attribute('outerHTML')
        src = image.get_attribute('src')
        data_src = image.get_attribute('data-src')
        if not src:
            continue

        result.append(data_src)

    if webdriver is None:
        driver.close()

    return result


# list = get_gzh_images(None, content_xpath)

list = [
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fyb9A8SX4moUK5lJ4C7gMicRnhMONwp262avUZrjZkXk3CA5trnUJ6SvhQ8gf16ibYTvArI4UOGs5Kw/640?wx_fmt=other&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVKaMXhoypUicbWxeXS8ibPbfdsh2VLOUrUUibtAon5YHC9HdF8QxkLVPbA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVvOGTxUVBhVibOmfMboQrViaqyCiar09ibSw28iah9ibfDicj29Uv2sNKeEE3A/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVfe1M1HUHnCyvxq4wBZaIUHnBBEw6RlXQOHXtxWibQ6vo4eTL43ebCicQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVPkuozz7GjBZ2ibCaNiaw6c3GvCxKGMe2ZhLvpp3q47GtYfd0j6d1GcnQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVVKzNxZJuTd3KcItRSdMpJicbtEqzFQyVvuaSfb9EI4Oej0bYZTfb4kA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVfDfKlZm78ET1M6nm1XRV8ickdCyDg4tNQEY1sw14kcje69rZiaKFkXEw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVTPSlQKj6iccz22MpjKw088egRxgRoO4zjZQZlQ0IAStYxLkpFzPAcmA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVB80SicsMiauqH8pvEUDIu6VjeATKuJAyoBQDDpZdmWGg0O45yMMWJasQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVWkviaJkibQzo1qdvhAaJI8k6uviad6NHkDMujnvKOcpuN6YdB9XBuGocg/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVsKcncez8tcpGDLuq5H7vSiaZk7Qic03FibD2QqsahRKwvTesWh24KE9Yw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVA0NWnVicQicDKGibR7XtnpTkul5ib4IK1Ov8mHmZ5U7icQhzOVAROwF6IFA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAV9509J0tSm9hJUdNUDhuFe1icQZs3jlrKvsKxQajTydia8zrfWw0D2UOw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAV3ABx3RqYBasfQEYYEVau5nIS6KmEfm0yEaicrCWKDyGian7hNicTXSafw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVURvDYLcOEbz3ubtKpicXYIXSBoMmWib10GOchOTvxB1wKu1uOaUj2FOw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVFQSrhDFc0f5yBOzUTdsicjptexRpV67IvLPbkGnu7wtlbErbibh8tpbA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVWWZcrc42Tzbf612e4WNHV1Lkdr5aPYhcTicicgHgopzqj72fViaN9dcAg/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVJXtH2TLBSJTcVZKoIp1NY9ibOsKIQibnBUDEZzxYx6GC5vlXNicicXs8sw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVwB1hbIjicVaBd18aBia3oM9YsX4VoUqfT6g67RrqrGCAXMDow1Ua5Gnw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVgCzguxajwo5DchRowub5JV5Vu38a1q1mEMhn4bdZELerk3xVcx5VtQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVxo2oliapGHHWYIkyDYKz5uk00e64aTBSPjFocOIPIjQw0HH6ic0FOB0A/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVtTSMbqjokmVYK5iahc1GQpvk2uJMFW0x6VV89Bmf2vGFVjfZiaQrJqGg/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVKDlh1ENNltHDKOB17pydPNwcxQEr6RChvx0dbQRSq5vzzB46HSdB5w/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVI8NNOyb2gP67ltVGDhEMaSDiaWw0EV1jXtmwGciaQqDZCCGGgNrwbDVA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVwY90YSm3xPnLOpWvjqyBkfxouZ6fricIhbKwzgUh5quFSmgoodCvic2g/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVZ4BVx7TlcZzzuKMzFTN1mnuQekicDd9Da9tfMGenP4IbWNC5ke7rv0A/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVdxWv3VnaOneh1oeuUjFibfEQVaDlShwMeXeOkhD2sibKMr1mdTia0VFsA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVgrz5ZQQeS8C0Z4ibUFt0AVHicLCkejn2EmndMWDhJdFalKTZiaztlydeA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVS27kP7oRK37FlvRWl1L4RIZxEvB1Gk1w1YEibd2Ef5dwZoicZJVoE16w/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVBZACdwLQPkwEGPIUBvvA7NibbLQyXiaicbDmduxMqkVRZYDBBT4IbnXbw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVKGfmg4uM1Ib36mpch6ZIN0BjZVUicSiahofbhJClEqfWfVyaGgbS364Q/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVdJQiaHLdYMUu0qnZiclAMTgheMJo4uYfkAibh5PTToblUZSJcTjywQscA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVjIuDnhATZWa0oZicno2wGiaIOwFH0VI7jbRWjfwXvO9zF7mzRfWtAShg/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVLheyrXWnXPY1dcqI7kg4JE3OYzcN0qrwVFpesWIoecI1R5ndas8dqQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAV0agqbV9Jud5Wia4QBuiaW3jRcVdb5LagGt5crb7El0nCTrSx2vvXkrqQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVgpf4ywa0txAz27Pd78aw9NRc1qFibHpjSWpN4gKIfUia2uQ56gRjVVzg/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVFkr2ZiaON6qibbnOetX3to6q9gPicyJEjot7EXuhn4IOa40Cs1B2JuUug/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVX9ClS1oKdy2LuE7mWfMmoEf8N9fKARqOd90ab56L0x4ogoic6uBiajIA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_png/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVyv3j4OAiaGoEKuURckEU1bBdm075LVgNCzUJibEZTgfQHyKEqTpKhTqQ/640?wx_fmt=png&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVqsKB0lEIo7GhficT1XHmGSNCZJPS1l1w4BFtaJjtPzh9VLYJLbAfUyw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVmnyy2ZyoLiaia3BPhB8fnGeY6byfaMdcXzJ3qk9Huyg5Vicf1VbP6lzdg/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVro3iaOcOfhDicXkPxiapiaYH1ahyyEGlEEic8965yK1pGISdVAV2P0Z8rFw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVWd94jibchqTKqbp3tkXw5uwwSiciamAOu18QibXPClBkGa5sCkrVN32fJQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVAlA1s0aob3cibO0BSZnEdMkucHYyqDqA324zic0x2ykhTkCbL2EYRFQw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVNIcF6mfhrFxUibT8I2xIEQ9EmOQ2knuoXICp5vmr4dE5htHCBqSibfIQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVjsaJpemibic01viafoEGqBLoeJvxKaaMKduDTbBicibicauwhuBkYbTeqYgw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVUNSAtxTKducicYfb7CqQzHWuicptvd0rFRWibhkvEgnuQleia1oKNibOT3Q/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVl4xhA9l9ZsF59OUoCaxiaeDwiaWQtlicuCsE7WcibhZeT8GcOGnmpnBYEw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAV4PdIKic20lDEjz4eune8SvHQtQRib3SiahIfUgBOLjqQzWYTTyRopm0UA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVq75PlXlloRhv336Oia3zceYbevreCiaricvTxedesYfUaRu6lu16ncia0w/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVFB6ziaN0h7S2MkJOS0pAVoHHX5ABxzlIYFafRW288qLwCZx8QPY0m6g/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVb7MEnarAGnJ79kZ6iaq6L2F4V4yLMU64icobK3zIjbn3x18z3wPnESFw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVQV6ExHmfXZFZxrGMetA3QbicBaamDrVnUrl2kBkzmkiciaW9f1jHsCJOw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVDRTBhRvvD9m89Sf1qwRHrw4ucgz1RqMQSphQc64LuJCumC4pokbicnw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVLibH3gqdLHOyXYZskPXPIYZ4KKSwL6BqYzLsUPCpyWWg8gcH7jLATqw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVAFlyggfpSwOaOT4AWpoO7mVbmOeCB4jT7ESc0fYB3ibTZYxlDmQSQicQ/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAV9tIKRorIibJZ0N9UiaQhnTMuofc6ru52VtBKL9bfuDd7qMa5EMxIRd6g/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVzU5olycIog3DpJkfaaYwecyOAVHnPFstfiauFHLG9XMkVj3lJK3WBicA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVD41uWicQMRX7ibPNSmwpvt8qgdOdnLlyInVIu3GUUDGicC6doKXJicniciag/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAV3nGbYArnibNy7Pp5CeQMYoF6my5zGnRYIyjuypmTFhP4po8tyX9YZJw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAVKicvHvQ6uS8pV4B0EuypKC306ssbM7sKUBpn8He9ueP9qzLlLbgplGA/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/qfHfmEUr8fzAHRB5f6ia0gzJ48Z3xgsAV3nBx2PtT6CW7WOyb4ic1gazFpRptxFAS9TuzFRcnFq1mKFOU7VNhrSw/640?wx_fmt=jpeg&from=appmsg',
    'https://mmbiz.qpic.cn/mmbiz_png/qfHfmEUr8fxgHRzibRRyoRFLTVzvicvPOic3vzmBMvYAWuMSPeB89v8b46owvOs1qzIsrRNNHe4ggsgu1wZNdsqAA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1',
    'https://mmbiz.qpic.cn/mmbiz_png/qfHfmEUr8fx0O4lyLicFwP5LAVY1I6KzE5MA3HDeyhsY11o8rlTjAGIsLOwypmTTJyzKvbrEO0sa1POVl48TPXg/640?wx_fmt=jpeg&wxfrom=5&wx_lazy=1&wx_co=1'
]

print(list)

from demo.qiniu_utils import *
from demo.qiniu_service import QiniuService

qs = QiniuService(name='pic')
data = qs.fetch_image(list, 'tmp2/gzh/')
print(data)

# filter
data = [image for image in data if image.get('meta', {}).get('width', 0) > 100]
print(data)