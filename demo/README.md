图片基本信息（imageInfo）
https://developer.qiniu.com/dora/1269/pictures-basic-information-imageinfo

示例：
http://dn-odum9helk.qbox.me/resource/gogopher.jpg?imageInfo

测试 url：
https://finance.sina.com.cn/stock/relnews/us/2024-09-06/doc-incnfpnk4614820.shtml

返回

```json

{
  size: 214513,
  format: "jpeg",
  width: 640,
  height: 427,
  colorModel: "ycbcr",
  orientation: "Top-left"
}

```



在七牛云的图片处理服务中，除了 `?imageInfo` 获取图片元数据信息外，你还可以使用一系列参数对图片进行操作和处理。这些参数称为 **图片处理操作符**。常见的操作包括图片缩放、裁剪、旋转、格式转换等。

以下是七牛云图片处理服务中常用的一些参数：

### 1. `imageInfo` 
获取图片的元数据信息（宽度、高度、格式等）。
```url
http://<bucket_domain>/<image_key>?imageInfo
```

### 2. `exif`
获取图片的 EXIF 信息（如果图片带有 EXIF 数据）。
```url
http://<bucket_domain>/<image_key>?exif
```

### 3. `imageView2`
用于对图片进行缩略图操作（包括缩放、裁剪等）。
```url
http://<bucket_domain>/<image_key>?imageView2/<mode>/w/<width>/h/<height>/q/<quality>/format/<format>
```

- `mode`：缩放模式（取值范围 0-5）：
  - `0`：限定缩略图的宽高，放大和缩小图片。
  - `1`：限定缩略图的宽高，按照宽高比例进行缩放。
  - `2`：限定缩略图的宽高，居中裁剪。
  - `3`：限定缩略图的宽度，高度自适应。
  - `4`：限定缩略图的高度，宽度自适应。
  - `5`：强制将图片缩放到指定的宽高，可能导致图片变形。
- `w`：宽度（像素值）。
- `h`：高度（像素值）。
- `q`：图片质量（1-100）。
- `format`：转换后的图片格式（如 `jpg`、`png` 等）。

#### 示例：
将图片缩放到宽 300px，高 400px：
```url
http://<bucket_domain>/<image_key>?imageView2/1/w/300/h/400
```

### 4. `imageMogr2`
高级图片处理接口，可以进行图片的缩放、裁剪、旋转、格式转换等操作。
```url
http://<bucket_domain>/<image_key>?imageMogr2/auto-orient/thumbnail/<size>/gravity/<gravity>/crop/<width>x<height>/rotate/<angle>/format/<format>/blur/<radius>x<sigma>
```

- `auto-orient`：根据图片 EXIF 信息自动旋转图片。
- `thumbnail`：指定缩放尺寸，支持按比例缩放，如 `100x100!`。
- `gravity`：指定裁剪的对齐方式，如 `center`、`northwest`、`southeast` 等。
- `crop`：指定裁剪区域，如 `300x400` 表示裁剪 300x400 的区域。
- `rotate`：旋转角度。
- `format`：转换后的图片格式（如 `jpg`、`png` 等）。
- `blur`：模糊处理，参数为 `<radius>x<sigma>`。

#### 示例：
将图片缩放到宽 200px 并旋转 90 度：
```url
http://<bucket_domain>/<image_key>?imageMogr2/thumbnail/200x/rotate/90
```

### 5. `watermark`
为图片添加水印，支持文字和图片水印。
```url
http://<bucket_domain>/<image_key>?watermark/2/text/<base64_encoded_text>/font/<base64_encoded_font>/fontsize/<fontsize>/fill/<fill_color>/dissolve/<opacity>/gravity/<gravity>/dx/<x_offset>/dy/<y_offset>
```

- `text`：Base64 编码的水印文字。
- `font`：Base64 编码的字体。
- `fontsize`：文字大小。
- `fill`：水印颜色（如 `#FFFFFF` 表示白色）。
- `dissolve`：水印的透明度（1-100）。
- `gravity`：水印位置（如 `center`、`northwest`、`southeast` 等）。
- `dx`、`dy`：水平和垂直边距。

#### 示例：
在图片的右下角添加 "Hello World" 的文字水印：
```url
http://<bucket_domain>/<image_key>?watermark/2/text/aGVsbG8gd29ybGQ=/font/dmVyZGFuYS5ib2xk/fontsize/500/fill/I0ZGRkZGRg==/gravity/southeast/dx/10/dy/10
```

### 6. `imageAve`
获取图片的平均色值。
```url
http://<bucket_domain>/<image_key>?imageAve
```

#### 示例：
```url
http://<bucket_domain>/<image_key>?imageAve
```
返回示例：
```json
{
    "RGB": "0x997c66"
}
```

### 7. `imageMogr2/strip`
去除图片的元信息（如 EXIF 数据等）。
```url
http://<bucket_domain>/<image_key>?imageMogr2/strip
```

### 8. `imageMogr2/blur`
对图片进行模糊处理。
```url
http://<bucket_domain>/<image_key>?imageMogr2/blur/<radius>x<sigma>
```

- `radius`：模糊半径。
- `sigma`：标准差，用来控制模糊效果。

#### 示例：
对图片进行模糊处理，模糊半径为 10，标准差为 20：
```url
http://<bucket_domain>/<image_key>?imageMogr2/blur/10x20
```

### 9. `imageMogr2/format`
将图片转换为指定格式。
```url
http://<bucket_domain>/<image_key>?imageMogr2/format/<format>
```

- `format`：目标格式（如 `jpg`、`png`、`gif` 等）。

#### 示例：
将图片转换为 PNG 格式：
```url
http://<bucket_domain>/<image_key>?imageMogr2/format/png
```

### 10. `imageView2/q`
调整图片的压缩质量。
```url
http://<bucket_domain>/<image_key>?imageView2/q/<quality>
```

- `quality`：图片的质量（1-100），数值越高图片质量越好，文件体积越大。

#### 示例：
将图片质量调整为 80：
```url
http://<bucket_domain>/<image_key>?imageView2/q/80
```

---

### 总结
通过这些参数，你可以对图片进行各种处理操作，包括缩放、裁剪、旋转、加水印、格式转换、模糊处理等。这些参数可以组合使用，从而满足各种不同的图片处理需求。

常用组合包括：
- 缩放图片并加水印
- 裁剪图片并转换格式
- 获取图片元数据信息和平均色值