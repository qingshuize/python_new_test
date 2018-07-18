#coding:utf8
from PIL import Image
import numpy as np
import cv2
import random
import re
import matplotlib.pyplot as plt
PATH='/Users/qmp/Desktop/'


def Roate_image(filein,deg):
    name=filein.split('/')[-1]
    image=Image.open(filein)

    w, h = image.size
    print(w,h)
    # 右旋转12度
    image.resize((h, w), Image.ANTIALIAS)
    im = image.rotate(deg)
    im.save(PATH+'out/'+name)
    # # 右旋转45度, 并裁剪一块
    # im = im.rotate(-30)
    # x = 50
    # y = 50
    # w = 150
    # h = 150
    # region = im.crop((x, y, x + w, y + h))
    # region.save("./rotate-r30-crop.jpeg")


def scope_more(image):
    origin_w,origin_h=image.size
    # 图片拉伸操作
    x_s = 800
    y_s = origin_w * origin_h / x_s
    out = image.resize((x_s, y_s), Image.ANTIALIAS)
    out.show()
    return out

#矩形规则形状裁剪图片
def Scope_image(x1,x2,x3,x4):
    raw_image=Image.open(PATH+'pic1.jpg')
    image=np.array(raw_image)
    print(image.shape)
    origin_w,origin_h=image.shape[:-1]
    print(origin_w,origin_h)
    print(image[100,100])




    out=raw_image
    # out=scope_more(raw_image)
    x_list=map(lambda x:x[0],[x1,x2,x3,x4])
    print(x_list)
    x_min = min(x_list)
    x_max=max(x_list)
    print(x_max)

    y_list = map(lambda x: x[1], [x1, x2, x3, x4])
    print(y_list)
    y_min = min(y_list)
    y_max = max(y_list)
    print(y_max)

    # #等比例缩放
    # image.thumbnail(handle_size,Image.ANTIALIAS)  # 等比例缩放
    # image.save(PATH+"pic1.thumbnail","JPEG")
    # image.show()

    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
    定位四个点A,B,C,D,则A(x,y),B(x+w,y),C(x,y+h),D(x+w,y+h)
    '''
    # if x>=0 and x+w<=origin_w and y>=0 and y+h<=origin_h:
    # region = out.crop((x_min, y_min, x_max, y_max))
    # print(region.size)
    # copy_region=array(region)
    # for i in range(origin_w-w):
    #     for j in range(origin_h-h):
    #         if i<x or i>x+w or j<y or j>j+h:
    #             copy_region[i,j]=array([0,0,0])
    # out_image = Image.fromarray(copy_region)
    #
    # out_image.save(PATH+'pic2_s.jpg')
    # print('image scope ok!')
# else:
#     print('input size error!')


def getPngPix(img_src,pixelX,pixelY):
    img_src = img_src.convert('RGBA')
    str_strlist = img_src.load()
    data = str_strlist[pixelX,pixelY]
    img_src.close()
    return data

#调整图片亮度，alpha为调整倍率
def image_light(image_file,alpha):
    Img = cv2.imread(image_file)
    image_name = image_file.split('/')[-1]
    w, h = Img.shape[:-1]
    for i in range(w):
        for j in range(h):
            Img[i,j,0]=int(Img[i,j,0]* alpha)
            Img[i, j, 1] = int(Img[i, j, 1] * alpha)
            Img[i, j, 2] = int(Img[i, j, 2]* alpha)
    cv2.namedWindow('img')
    cv2.imshow('img', Img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def get_w_h(size):
    for x in range(1,size):
        y=x
        if size-x*y<=2:
            return x,y

def ResizeImage(filein, fileout):
    img = Image.open(filein)
    x,y=img.size
    print(x,y)


    #Image.BILINEAR
    #Image.ANTIALIAS
    w,h=240,360
    # img.thumbnail((x*5,y*5), Image.BILINEAR)
    out = img.resize((w, h), Image.ANTIALIAS)  # resize image with high-quality
    # print(img.size)
    out.save(fileout,quality=100)


#图片截取任意四边形投影处理
def AffineTransform(image_file,point_info):
    Img = cv2.imread(image_file)
    image_name=image_file.split('/')[-1]
    w,h=Img.shape[:-1]
    print(w,h)
    #图片标准输出尺寸
    standard_w, standard_h = 1000,800
    # standard_w,standard_h=get_w_h(w*h)
    print(standard_w,standard_h)
    SrcPointsA=np.float32(point_info)

    CanvasPointsA=np.float32([[0,0],[0,standard_h],[standard_w,0],[standard_w,standard_h]])
    # AffineMatrix = cv2.getAffineTransform(np.array(SrcPointsA),
    #                                       np.array(CanvasPointsA))
    # print 'AffineMatrix:\n', AffineMatrix
    # AffineImg = cv2.warpAffine(Img, AffineMatrix, (Img.shape[1], Img.shape[0]))
    # cv2.imshow('AffineImg', AffineImg)
    # cv2.imwrite(PATH + 'handle_pic.png', AffineImg)

    ##投影，四个点坐标
    PerspectiveMatrix = cv2.getPerspectiveTransform(np.array(SrcPointsA), np.array(CanvasPointsA))
    PerspectiveImg = cv2.warpPerspective(Img, PerspectiveMatrix, (standard_w,standard_h))
    cv2.imshow('PerspectiveImg', PerspectiveImg)
    cv2.imwrite(PATH + 'out/Perspective_%s_1.png'%image_name, PerspectiveImg)

    print('%s handle save success!!!'%image_name)

from scipy import ndimage
from pylab import *

def Image_reflect(image_file):
    im = array(Image.open(image_file).convert('L'))
    H = array([[1.4, 0.05, -100], [0.05, 1.5, -100], [0, 0, 1]])
    # print(H[:2, :2])
    im2 = ndimage.affine_transform(im, H[:2, :2], (H[0, 2], H[1, 2]))
    figure()
    imshow(im2)
    show()

def Image_size_handle(file):
    image = cv2.imread(file)
    print(image.size)
    a=image.shape
    x,y=image.shape[:-1]
    print(x,y)
    #cv2.INTER_AREA
    #cv2.INTER_CUBIC
    #INTER_LANCZOS4
    #INTER_LINEAR
    #INTER_NEAREST

    p_h,p_w=get_w_h(image.size)
    p1 = cv2.resize(image, (p_w,p_h),
                    interpolation=cv2.INTER_AREA)

    cv2.imshow('sss',p1)
    x_rate=int(p_w/200)
    print(x_rate)
    p2=cv2.resize(p1, (int(x/4),int(y/4)),
                    interpolation=cv2.INTER_AREA)
    cv2.imwrite(PATH +'output/Perspective_test_3.png', p2)
    # im = Image.open(file)
    # w, h = im.size
    # print w,h
    #
    # if w > 310:
    #     h_new = 310 * h / w
    #     w_new = 310
    #     out = im.resize((w_new, h_new), Image.ANTIALIAS)
    #     new_path=PATH+'output/'
    #     out.save(new_path)


def pyramid_handel():
    s=cv2.imread(PATH+'a.jpg')
    x, y = s.shape[:-1]
    # G=s.copy()
    # gpA=[G]
    # lpA=[]
    # cv2.imshow('g',G)
    # image_o = G
    # G = cv2.pyrDown(G)
    # GE = cv2.pyrUp(G)
    # L = np.subtract(image_o, GE)
    # gpA.append(G)
    # lpA.append(L)
    # cv2.imshow('lpA', L)
    # cv2.imshow('上采样+拉普拉斯', L + GE)
    # cv2.imshow('upsample', GE)
    # cv2.waitKey()
    # MSE(image_o, L + GE)
    # p = cv2.resize(s, (200,300),
    #interpolation=cv2.INTER_AREA)

    # s0 = cv2.resize(s, (int(x*3), int(y*3)),
    #                                 interpolation=cv2.INTER_AREA)
    # s0=cv2.pyrUp(s)
    s1=cv2.pyrDown(s)
    # plt.imshow(s)
    # s2=cv2.pyrDown(s1)
    # s2 = cv2.resize(s1, (250, 200),
    #                 interpolation=cv2.INTER_AREA)
    cv2.imwrite(PATH + 'caculate.png', s1)

def tranform_style(filein,n):
    img = cv2.imread(filein)
    name=filein.split('/')[-1]
    rows, cols = img.shape[:-1]
    recyle_img=np.rot90(img,n)
    print(rows,cols)
    # # 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
    # # 可以通过设置旋转中心，缩放因子，以及窗口大小来防止旋转后超出边界的问题
    # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), degree, 0.6)
    # # 第三个参数是输出图像的尺寸中心
    # dst = cv2.warpAffine(img, M, (cols, rows))
    # while (1):
    #     cv2.imshow('img', dst)
    #     if cv2.waitKey(1) & 0xFF == 27:
    #         break
    # cv2.destroyAllWindows()
    cv2.imwrite(PATH + 'out/roate_%s_%s'%(n,name), recyle_img)

if __name__ == '__main__':
    #截取图片四个顶点坐标
    # point_list = [(0, 0), (0, 1280), (960, 0), (960, 1280)]
    point_list = [(183, 1141), (1, 2079), (1683, 1042), (1858, 2062)]
    # point_list = [(62, 468), (39, 1017), (918, 488), (945, 1004)]
    # point_list=[(890,140),(196,138),(920,590),(256,726)]
    # point_list = [(0, 0), (0, 1280), (960, 0), (960, 1280)]
    # Scope_image(x1, x2, x3, x4)
    # Scope_image(x, y, w, h)
    # getPngPix()
    # matchImg(open(path+'pic1.jpg'), open(path+'pic1_s.jpg'), confidencevalue=0.5)
    # AffineTransform(PATH+'7.jpg',point_list)
    # image_light(PATH+'pic2.jpeg',1.02)
    # Image_reflect(PATH+'pic.jpeg')
    # Roate_image(PATH+'4.jpeg',90)
    # ResizeImage(PATH + 'a.jpg',PATH+'output/' + 'resize_a.jpg')
    # Image_size_handle(PATH+'5.jpg')
    # pyramid_handel()
    # tranform_style(PATH+'4.jpeg',2)
