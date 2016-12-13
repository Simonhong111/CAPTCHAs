# !/usr/bin/env python
# coding=utf-8

import cv2

image = cv2.imread('BW_202.bmp')  # 读取图像
image2 = image.copy()  # 复制图像
for i in range(0, image.shape[0]):  # image.shape表示图像的尺寸和通道信息(高,宽,通道)
    for j in range(0, image.shape[1]):
        image2[i, j] = 255 - image[i, j]
#
# cv2.imshow('image1', image)
# cv2.imshow('image2', image2)

cv2.imwrite("sa1220252.jpg", image2)  # 保存图像

cv2.waitKey(0)  # 按键继续
cv2.destroyAllWindows()  # 释放窗口

