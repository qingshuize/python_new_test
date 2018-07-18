#coding:utf8
from PIL import Image
# from pytesser import pytesser
import pytesseract
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


if __name__ == '__main__':
    # Image_handle()
    get_text()