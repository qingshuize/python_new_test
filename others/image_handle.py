#coding:utf8
from PIL import Image
# from pytesser import pytesser
import pytesseract
from log_tool import *
import cv2
from tqdm import tqdm,trange

def Image_handle():
    img=Image.open('/Users/qmp/Desktop/5.jpg')

    #把彩色图像转化为灰度图像。RBG转化到HSI彩色空间，采用I分量
    img1= img.convert('L')

    #二值化处理
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = img1.point(table, '1')
    out.show()

    # print pytesser.image_file_to_string('/Users/qmp/Desktop/img.jpeg')
    print(pytesser.image_to_string(out))


def get_text():
    text = pytesseract.image_to_string(Image.open('/Users/qmp/Desktop/5.jpg'), lang='chi_sim')
    print(text)


# 图片打马赛克
@try_error
def Mosaic_img(path, name, (t_row, t_col)):
    """
    program1

    """
    img = cv2.imread(path + name)

    # 复制图片
    # img_copy = img.copy()
    # cv2.imwrite(path + 'copy_1.jpg', img_copy)
    # logging.debug('save copy image!!')

    # 对图片全部打马赛克并保存
    row = img.shape[0]
    col = img.shape[1]
    logging.debug('Origin size:(%s,%s)' % (row, col))
    for i in trange(1):
        img1 = cv2.resize(img[::t_row, ::t_col], (row, col))
        logging.debug('Mosaic size:(%s,%s)' % (t_row, t_col))
        cv2.imwrite(path + 'mosaic_1.jpg', img1)
        logging.debug('save image success!!')



if __name__ == '__main__':
    # Image_handle()
    get_text()