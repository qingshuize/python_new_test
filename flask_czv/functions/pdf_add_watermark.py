#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests,os
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from hashlib import md5

#添加中文字体库
pdfmetrics.registerFont(TTFont('songti', '/mydata/nginx/www/file.com/Fonts/Songti.ttc'))
# pdfmetrics.registerFont(TTFont('Arial Unicode', '/Library/Fonts/Arial Unicode.ttf'))

class PDF_watermark_handle(object):

    def __init__(self,path):

        self.pdf_w = None   #pdf宽
        self.pdf_h = None    #pdf高
        self.pic_x=80       #水印图片宽
        self.pic_y=80       #水印图片高
        self.path=path

    #文字水印
    def create_word_watermark(self,content,mark_name,w,h):

        c=canvas.Canvas('%s'%mark_name)
        # c.setStrokeColorRGB(1, 0, 0.3)
        c.setFillGray(0.5)
        c.setFillColorRGB(1, 0, 0.92)
        c.setFont("songti", 13)
        c.rotate(9)
        # c.skew(10, -10)
        c.saveState()
        # c.restoreState()
        # c.translate(-0,- 0)
        # c.rotate(-13)
        # c.skew(10, 0)
        # c.saveState()
        # for i in range(w,-w,-100):
        #     for j in range(h,-h,-50):
        #         c.drawString(i, j, content.decode('utf8'))

        c.drawCentredString(float(w)/2, float(h)/2,content.decode('utf8'))
        # 保存水印文件
        c.save()


    ##图片水印
    def create_pic_watermark(self,img):
        f_pdf = 'watermark_img.pdf'
        c = canvas.Canvas(f_pdf, pagesize=(self.pdf_w, self.pdf_h))
        c.setFillAlpha(0.13)  # 设置透明度
        #变形旋转效果
        # c.rotate(13)
        # c.skew(10, 5)
        # c.saveState()
        # for i in range(0,50,10):
            # for j in range(0,50,8):
        c.drawImage(img,  float(self.pdf_w)/2-self.pic_x/2, 0, self.pic_x, self.pic_y)
        c.save()

    #处理加密pdf文件
    def solve_encrypt(self,pdf_input):

        if pdf_input.getIsEncrypted():
            print('该PDF文件被加密了.')
            # 尝试用空密码解密
            try:
                pdf_input.decrypt('')
            except Exception as  e:
                print('尝试解密失败.')
                return False
            else:
                print('解密成功.')

    def get_pdf_size(self,pdf_input,i):

        try:
            # print(pdf_input.flattenedPages)
            [_, _, x, y] = list(pdf_input.flattenedPages[i].get('/MediaBox'))
            if x == 0 or y==0:
                [x, _, _, y] = list(pdf_input.flattenedPages[i].get('/CropBox'))

        except Exception as e:
            print(e)
            [_, _, x, y] = list(pdf_input.flattenedPages[i].get('/CropBox'))
        print(x, y)
        return x,y

    def add_watermark(self,link, word,outdir):
        try:
            pdf_file = self.get_url_content(link)
            pdf_output = PdfFileWriter()
            input_s = open(self.path + pdf_file, 'rb')
            pdf_input = PdfFileReader(input_s)
    
            #加密检测
            self.solve_encrypt(pdf_input)
    
            # 获取页数
            pageNum = pdf_input.getNumPages()
    
            w, h = self.get_pdf_size(pdf_input, 0)
            watermark_file='watermark_%s'%pdf_file
            self.create_word_watermark(word, watermark_file, w, h)
            print('create watermark tempalte ok!')
    
            # # 给每一页打水印
            for i in range(pageNum):
                print(i)
                page = pdf_input.getPage(i)
                w, h = self.get_pdf_size(pdf_input, i)
                # self.create_pic_watermark('qmp_logo1.png')
                print('add watermark ok!')
                pdf_watermark = PdfFileReader(open(watermark_file, 'rb'))
                page.mergePage(pdf_watermark.getPage(0))
                page.compressContentStreams()  # 压缩内容
                pdf_output.addPage(page)
            if not os.path.exists(self.path+outdir):
                os.makedirs(self.path+outdir)
            out_file = pdf_file.replace('.pdf', '（加文字水印）.pdf')
            output_s = open(self.path+outdir+out_file, 'wb')
            pdf_output.write(output_s)
            output_s.close()
            input_s.close()
            return self.path+outdir+out_file
        except:
            pass

    def get_url_content(self,url):
        res=requests.get(url)
        if res.status_code==200:
            file_pdf=md5(url).hexdigest()+'.pdf'
            with open(self.path + file_pdf, 'w') as f:
                f.write(res.content)
            print(file_pdf+' save ok!')
            return file_pdf
        else:
            return False




# if __name__ == '__main__':
    # pass
    # path='/Users/qmp/Desktop/'
#
#     #加水印之后的输出文件夹
#     out_dir='./output/'
#
    # pdf_obj=PDF_watermark_handle(path)
#
#     #制作文字水印
#     pdf_obj.create_word_watermark('你是谁？','watermark_word.pdf')
#
#     #制作图片水印
#     pdf_obj.create_pic_watermark('qmp_logo1.png')
#
    # file_pdf=url.split('/')[-1].strip()
    #
    # if not os.path.exists(path+file_pdf):
    #     res = requests.get(url)
    #     with open(path+file_pdf,'w') as f:
    #         f.write(res.content)
    #     print(file_pdf)
#
    #pdf添加水印保存
    # url='http://www.neeq.com.cn/disclosure/2018/2018-10-24/1540369026_955571.pdf'
    # file_pdf='5b177c4d37c4a.pdf'
    # pdf_obj.add_watermark(url,'watermark_word2.pdf',out_dir)
