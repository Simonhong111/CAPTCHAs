# !/usr/bin/env python
# coding=utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
img=cv2.imread('1.jpg')
GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh1=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)
# ret,thresh2=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY_INV)
# ret,thresh3=cv2.threshold(GrayImage,127,255,cv2.THRESH_TRUNC)
# ret,thresh4=cv2.threshold(GrayImage,127,255,cv2.THRESH_TOZERO)
# ret,thresh5=cv2.threshold(GrayImage,127,255,cv2.THRESH_TOZERO_INV)
# titles = ['Gray Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5]
image = [thresh1]

# for i in range(6):
#    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#    plt.title(titles[i])
#    plt.xticks([]),plt.yticks([])
# plt.show()
cv2.imwrite('1F.jpg',img)