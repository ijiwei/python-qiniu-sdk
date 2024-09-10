"""
功能描述
:author wjh
:date 2024-09-10
"""


import requests
import os
from PIL import Image
from io import BytesIO
import cairosvg

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
        with Image.open(filepath) as img:
            return {
                "size": os.path.getsize(filepath),
                "format": img.format,
                "width": img.width,
                "height": img.height,
                "colorModel": img.mode
            }
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

def handle_svg(filepath):
    # Convert SVG to PNG in memory for metadata extraction
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
        try:
            # 试图直接使用 Pillow 获取图片信息
            info = get_image_info(local_filepath)
        except OSError:
            # 如果是 SVG 或者其他无法直接打开的格式，则尝试将其作为 SVG 处理
            info = handle_svg(local_filepath)

        # 删除文件
        os.remove(local_filepath)

        return info
    return None

# 示例使用
# image_url = "https://s.laoyaoba.com/bianjifagao/00085685cba1b18ceed294d5f992ed2a/7e75af1c5f8b9b5bb6b6c513a29ae9b5.jpg"
image_url = "https://s.laoyaoba.com/bianjifagao/ab504a7d91bb7e54a41e4f94f2076607/403724be377ac13d772143a8dc719db2.svg"
image_info = process_image(image_url)

print(image_info)
