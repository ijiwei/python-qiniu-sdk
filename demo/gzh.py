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

url = 'https://mp.weixin.qq.com/s?__biz=MzIxODI2NTY4OQ==&mid=2247523746&idx=1&sn=a6e36d0b9c6aaa14c8e342d84a418ace&chksm=97effc94a0987582e8838205f8edecaab32160b784ba06612d25719346f93cffa629ee2774a1&scene=126&sessionid=1725684824#rd'

content_xpath = '//div[@id="js_content" or @id="js_share_notice" or @class="wx_video_play_opr" or @class="rich_media_content"]'

if os.name == "nt":  # window
    firefox_binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    firefox_executable_path = r"C:\Windows\System32\geckodriver.exe"

    chrome_binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_executable_path = r"C:\Windows\System32\chromedriver.exe"

else:  # linux
    firefox_binary_location = "/usr/bin/firefox"
    firefox_executable_path = "/usr/local/bin/geckodriver"

    chrome_binary_location = "/usr/bin/google-chrome"
    chrome_executable_path = "/usr/local/bin/chromedriver"


def get_webdriver():
    opt = webdriver.ChromeOptions()
    opt.add_argument("no-sandbox")
    opt.add_argument("--disable-extensions")
    # opt.add_argument("--headless")
    return webdriver.Chrome(executable_path=chrome_executable_path, options=opt)


def get_gzh_images(webdriver, xpath: str):
    if webdriver is None:
        driver = get_webdriver()
        driver.implicitly_wait(10)
    else:
        driver = webdriver

    driver.get(url)
    result = []
    images = driver.find_elements(By.XPATH, xpath)
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


list = get_gzh_images(None, content_xpath + '//img')

print(list)

from demo.qiniu_utils import *
from demo.qiniu_service import QiniuService

qs = QiniuService(name='pic')
data = qs.fetch_image(list, 'tmp2/gzh3/')
print(data)

# filter
data = [image for image in data if image.get('meta', {}).get('width', 0) > 100 and image.get('meta', {}).get('height', 0) > 100]
print(data)

# 测试上提交
