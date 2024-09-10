"""
功能描述
:author wjh
:date 2024-09-10
"""

import requests
import os
from PIL import Image
import cairosvg
from io import BytesIO

def download_image(url, local_filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        return local_filename
    else:
        print(f"Failed to download image: {response.status_code}")
        return None

def get_image_info(filepath):
    try:
        # 先尝试用 Pillow 打开文件（如果不是 SVG）
        with Image.open(filepath) as img:
            return {
                "size": os.path.getsize(filepath),
                "format": img.format,
                "width": img.width,
                "height": img.height,
                "colorModel": img.mode
            }
    except (OSError, IOError):
        # 如果出现错误，可能是 SVG 文件，使用 cairosvg 处理
        return handle_svg(filepath)

def handle_svg(filepath):
    # 使用 cairosvg 将 SVG 转换为 PNG 并在内存中处理
    png_image_data = cairosvg.svg2png(url=filepath)
    img = Image.open(BytesIO(png_image_data))
    return {
        "size": len(png_image_data),
        "format": "png",
        "width": img.width,
        "height": img.height,
        "colorModel": img.mode
    }

def process_image(url):
    local_filename = url.split('/')[-1]
    local_filepath = download_image(url, local_filename)

    if local_filepath:
        info = get_image_info(local_filepath)

        # 删除文件
        os.remove(local_filepath)

        return info
    return None

# 示例使用
image_url = "https://s.laoyaoba.com/bianjifagao/ab504a7d91bb7e54a41e4f94f2076607/403724be377ac13d772143a8dc719db2.svg"
image_info = process_image(image_url)
print(image_info)

image_url = "https://s.laoyaoba.com/bianjifagao/00085685cba1b18ceed294d5f992ed2a/7e75af1c5f8b9b5bb6b6c513a29ae9b5.jpg"
image_info = process_image(image_url)
print(image_info)


