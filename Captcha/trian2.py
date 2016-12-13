# !/usr/bin/env python
# coding=utf-8
import os
from PIL import Image,ImageFont,ImageDraw
import random
import string
font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf',25)

for i in range(101,201):
    newImage = Image.new('RGB',(width,height),bgcolor)
    #  newImage = image.rotate(45)
    # load像素
    image=Image.open('pic1.png')
    newPix = newImage.load()
    pix = image.load()
    offset = 0
    # if img[width,height]==0:
    s = image.size
    # newImage.show()
    print(s)
    for y in range(s[0]):
        offset += 0.15
        for x in range(s[1]):
            if pix[y,x] != 255:
                # 新的x坐标点
                newx = x + offset
                # 你可以试试如下的效果
                # newx = x + math.sin(float(y)/10)*10
                if newx < width:
                    # 把源像素通过偏移到新的像素点
                    newPix[newx, y] = pix[x, y]
    a=str(i)
    p='pic'+a+'.png'
    image.save(p)