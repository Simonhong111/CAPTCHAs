
# coding: utf-8

# In[1]:

from PIL import Image,ImageOps  


# In[2]:

from pylab import *


# In[3]:

im=Image.open('test.jpg')


# In[4]:

im_grey=im.convert('L')


# In[5]:

im_peak=im_grey.convert('1')
# im_peak.show()


# In[6]:

# from PIL import ImageFilter,ImageEnhance

# im_filter=im_peak.filter(ImageFilter.MedianFilter)
# for j in range(1):
#     im_filter=im_filter.filter(ImageFilter.MedianFilter)
    
# im_filter.show()


# In[7]:

#import os, sys


# In[8]:

#import scipy.io as scio 


# In[9]:

#dataFile = 'C://Users//hzy//Desktop//BW.mat'  


# In[10]:

#data = scio.loadmat(dataFile)  


# In[11]:

#imshow(data)
#show()


# In[12]:

# import cv2


# In[13]:

# im= ImageOps.invert(image) 
# im.save('im.jpg')


# In[14]:

from multiprocessing import Queue


# In[15]:

def cfs(im,x_fd,y_fd):

    xaxis=[]
    yaxis=[]
    pix=im.load()
    visited =set()
    q=Queue.Queue()
    q.put((x_fd, y_fd))
    visited.add((x_fd, y_fd))
    offsets=[(1, 0), (0, 1), (-1, 0), (0, -1)]#四邻域

    while not q.empty():
        x,y=q.get()

        for xoffset,yoffset in offsets:
            x_neighbor,y_neighbor=x+xoffset,y+yoffset

            if (x_neighbor,y_neighbor) in (visited):
                continue  # 已经访问过了

            visited.add((x_neighbor, y_neighbor))

            try:
                if pix[x_neighbor, y_neighbor]==0:
                    xaxis.append(x_neighbor)
                    yaxis.append(y_neighbor)
                    q.put((x_neighbor,y_neighbor))

            except IndexError:
                pass

    xmax=max(xaxis)
    xmin=min(xaxis)
    #ymin,ymax=sort(yaxis)

    return xmax,xmin

#搜索区块起点
def detectFgPix(im,xmax):

    l,s,r,x=im.getbbox()
    pix=im.load()
    for x_fd in range(xmax+1,r):
        for y_fd in range(x):
            if pix[x_fd,y_fd]==0:
                return x_fd,y_fd

def CFS(im):

    zoneL=[]#各区块长度L列表
    zoneBE=[]#各区块的[起始，终点]列表
    zoneBegins=[]#各区块起点列表

    xmax=0#上一区块结束黑点横坐标,这里是初始化
    for i in range(5):

        try:

            x_fd,y_fd=detectFgPix(im,xmax)
            xmax,xmin=cfs(im,x_fd,y_fd)
            L=xmax-xmin
            zoneL.append(L)
            zoneBE.append([xmin,xmax])
            zoneBegins.append(xmin)

        except TypeError:
            return zoneL,zoneBE,zoneBegins

    return zoneL,zoneBE,zoneBegins


# In[16]:

#求出图片的垂直投影直方图
def VerticalProjection(im):

    VerticalProjection={}
    l,s,r,x=im.getbbox()

    pix=im.load()

    for x_ in range(r):

        black=0
        for y_ in range(x):

            if pix[x_,y_]==0:
                black+=1

        item=str(x_)
        VerticalProjection[item]=black

    return VerticalProjection

#========>VERTICALPROJECTION ABOVE


# In[17]:

def zonexCutLines(zoneL,zoneBegins):

    Dmax=21  #最大字符长度
    Dmin=11  #最小字符长度
    Dmean=15.5  #平均字符长度

    zonexCutLines=[]

    for i in range(len(zoneL)):

            xCutLines=[]     
            if zoneL[i]>Dmax:

                num=round(float(zoneL[i])/float(Dmean))
                num_int=int(num)

                if num_int==1:
                    continue

                for j in range(num_int-1):
                    xCutLine=zoneBegins[i]+Dmean*(j+1)
                    xCutLines.append(xCutLine)
                zonexCutLines.append(xCutLines)

            else:
                continue

    return zonexCutLines


# In[18]:

def yVectors_sorted(zoneBE,VerticalProjection):

    yVectors_dict={}
    yVectors_sorted=[]
    for zoneBegin,zoneEnd in zoneBE:
        L=zoneEnd-zoneBegin
        Dmean= 15.5  #基于人工统计的平均字符长度值
        num=round(float(L)/float(Dmean))#区块长度L除以平均字符长度Dmean四舍五入可得本区块字符数量
        num_int=int(num)

        if num_int>1:#当本区块字符数量>1时候，可以认为出现字符粘连，是需要切割的区块

            for i in range(zoneBegin,zoneEnd+1):

                i=str(i)
                yVectors_dict[i]=VerticalProjection[i]#扣取需要切割的区块对应的垂直投影直方图的部分
            #对扣取部分进行重排并放入yVectors_sorted列表中   
            yVectors_sorted.append(sorted(yVectors_dict.iteritems(),key=lambda d:d[1],reverse=False))

    return yVectors_sorted


# In[19]:

def get_dropsPoints(zoneL,zonexCutLines,yVectors_sorted):

    Dmax=21
    Dmean=15.5
    drops=[]
    # yVectors_sorted__=[]
    # xCutLines=[]


    h=-1

    for j in range(len(zoneL)):
        yVectors_sorted_=[]

        if zoneL[j]>Dmax:

            num=round(float(zoneL[j])/float(Dmean))
            num_int=int(num)

            #容错处理
            if num_int==1:
                continue

            h+=1
            yVectors_sorted__=yVectors_sorted[h]
            xCutLines=zonexCutLines[h]

            #分离
            yVectors_sorted_x=[]
            yVectors_sorted_vector=[]
            for x,vector in yVectors_sorted__:
                yVectors_sorted_x.append(x)
                yVectors_sorted_vector.append(vector)

            for i in range(num_int-1):

                for x in yVectors_sorted_x:

                    x_int=int(x)
                    #d表示由Dmean得出的切割线和垂直投影距离的最小点之间的距离
                    d=abs(xCutLines[i]-x_int)

                    #d和Dmean一样也需要人工设置
                    if d<4:
                        drops.append(x_int)#x是str格式的 
                        break 

        else:

            #print '本区块只有一个字符'
            continue

    return drops


# In[20]:

def get_Wi(im,Xi,Yi):

    pix=im.load()
    #statement
    n1=pix[Xi-1,Yi+1]
    n2=pix[Xi,Yi+1]
    n3=pix[Xi+1,Yi+1]
    n4=pix[Xi+1,Yi]
    n5=pix[Xi-1,Yi]

    if n1==255:
        n1=1
    if n2==255:
        n2=1
    if n3==255:
        n3=1
    if n4==255:
        n4=1
    if n5==255:
        n5=1

    S=5*n1+4*n2+3*n3+2*n4+n5

    if S==0 or S==15:
        Wi=4

    else:
        Wi=max(5*n1,4*n2,3*n3,2*n4,n5)

    return Wi

def situations(Xi,Yi,Wi):

    switcher={

        1: lambda:(Xi-1,Yi),
        2: lambda:(Xi+1,Yi),
        3: lambda:(Xi+1,Yi+1),
        4: lambda:(Xi,Yi+1),
        5: lambda:(Xi-1,Yi+1),
    }

    func=switcher.get(Wi,lambda:switcher[4]())
    return func()

#改进型就是在drops滴水起点的获取方式和经典不一样
def dropPath(im,drops):

    l,s,r,x=im.getbbox()    
    path=[]
    zonePath=[]    
    for drop in drops:

        Xi=drop
        Yi=0
        limit_left=drop-4#左约束
        limit_right=drop+4#右约束

        while Yi!=x-1:
            Wi=get_Wi(im,Xi,Yi)
            Xi,Yi=situations(Xi,Yi,Wi)

            if Xi==limit_left or Xi==limit_right:
                Xi,Yi=path[-1]#若触碰到约束边界，就回退到上一次的坐标

            if Yi>2:
                #如果遇到当前水滴位置坐标和上或者上上次的坐标一样，则设置为权重4，即垂直向下从n0挪动到n2的位置
                if path[-2]==(Xi,Yi) or path[-1]==(Xi,Yi):
                    Xi,Yi=situations(Xi,Yi,4)

            path.append((Xi,Yi))
        zonePath.append(path)
    return zonePath

#主函数
def DropCUT(im):

    pix=im.load()
    drops=drops(im)
    zonePath=dropPath(im,drops)
    for path in zonePath:
        for x,y in path:
            pix[x,y]=255#令滴水路径上的所有坐标都染上白色

    return im


# In[21]:

im1=DropCUT(im)
im.save('test2.jpg')


# In[22]:

# tesseract test.jpg output-l eng -psm 7 

