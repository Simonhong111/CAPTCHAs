
# coding: utf-8

# In[1]:

from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import math
import numpy as np
import cv2

# In[2]:

'''基本功能'''
#图片宽度
width = 28
#图片高度
height = 35
size=width, height   # 宽， 高

#背景颜色
bgcolor = (255,255,255)
#生成背景图片
image = Image.new('RGB',(width,height),bgcolor)

#加载字体
font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf',25)
#字体颜色
fontcolor = (0,0,0)
#产生draw对象，draw是一些算法的集合
draw = ImageDraw.Draw(image)
#画字体,(0,0)是起始位置
draw.text((6,0),'A',font=font,fill=fontcolor)
#释放draw
del draw
#保存原始版本
# image = image.filter(ImageFilter.BLUR)
params = [1 - float(random.randint(1, 2)) / 100,
          0,
          0,
          0,
          1 - float(random.randint(1, 10)) / 100,
          float(random.randint(1, 2)) / 500,
          0.001,
          float(random.randint(1, 2)) / 500
          ]
image = image.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
image.save('A_1.jpeg')
'''演示扭曲，需要新建一个图片对象'''
a = Image.open('A_1.jpeg')
# def cha():
#     draw.text((6, 0), 'A', font=font, fill=fontcolor)
#     return character

# #新图片
newImage = Image.new('RGB',(width,height),bgcolor)
#  newImage = image.rotate(45)
# load像素



newPix = newImage.load()
pix = image.load()
offset = 0
# if img[width,height]==0:
s = image.size
# newImage.show()
print(s)
for y in range(s[0]):
    offset += 0.5
    for x in range(s[1]):
        if pix[y,x] != 255:
            # 新的x坐标点
            newx = x + offset
            # 你可以试试如下的效果
            # newx = x + math.sin(float(y)/10)*10
            if newx < width:
                # 把源像素通过偏移到新的像素点
                newPix[newx, y] = pix[x, y]

# image.save('kasjkakj.jpg')

# for y in range(0,height):
#     offset += 0.4
#     for x in range(0,width):
#         #新的x坐标点
#         newx = x + offset
#         #你可以试试如下的效果
#         #newx = x + math.sin(float(y)/10)*10
#         if newx < width:
#             #把源像素通过偏移到新的像素点
#             newPix[newx,y] = pix[x,y]

# #保存扭曲后的版本
# image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）
newImage.save('A_2.jpeg')



'''形变一下'''
#x1 = ax+by+c
#y1 = dx+ey+f
newImage = image.transform((width+0,height+0), Image.AFFINE, (1,-0.2,0,-0.1,1,0))
newImage.save('A_3.jpeg')


'''画干扰线，别画太多，免得用户都看不清楚'''        
#创建draw，画线用
draw = ImageDraw.Draw(newImage)
#线的颜色
linecolor= (0,0,0)
for i in range(0,15):
    #都是随机的
    x1 = random.randint(0,width)
    x2 = random.randint(0,width)
    y1 = random.randint(0,height)
    y2 = random.randint(0,height)
    draw.line([(x1, y1), (x2, y2)], linecolor)            

#保存到本地
newImage.save('A_4.jpeg')