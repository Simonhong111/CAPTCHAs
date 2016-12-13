# !/usr/bin/env python
# coding=utf-8
import os
from PIL import Image,ImageFont,ImageDraw,ImageFilter
import random
import string
font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf',25)

for i in range(901,1001):
    # Img = Image.new("RGBA", (256,144),(255,255,255))
    # Draw = ImageDraw.ImageDraw(Img, "RGBA")
    # Draw.setfont(Font)
    # x=random.randint(0,999999)
    # x=str(x)
    # Draw.text((20, 25), x, fill='black')
    # 图片宽度
    width = 28
    # 图片高度
    height = 28
    size = width, height  # 宽， 高

    # 背景颜色
    bgcolor = (255, 255, 255)
    # 生成背景图片
    image = Image.new('RGB', (width, height), bgcolor)
    # 字体颜色
    fontcolor = (0, 0, 0)
    # 产生draw对象，draw是一些算法的集合
    draw = ImageDraw.Draw(image)
    # 画字体,(0,0)是起始位置
    draw.text((3, 0), 'A', font=font, fill=fontcolor)
    # 释放draw
    del draw
    保存原始版本
    image = image.filter(ImageFilter.BLUR)
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 700,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    image1 = image.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    # image2 = image.filter(ImageFilter.BLUR)  # 滤镜，边界加强（阈值更大）
    a=str(i)
    p='pic'+a+'.png'
    image2.save(p)