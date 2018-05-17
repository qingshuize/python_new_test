#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os,requests
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from hashlib import md5

#添加中文字体库
pdfmetrics.registerFont(TTFont('Songti', '/Library/Fonts/Songti.ttc'))
pdfmetrics.registerFont(TTFont('Arial Unicode', '/Library/Fonts/Arial Unicode.ttf'))

class PDF_watermark_handle(object):

    def __init__(self):
        # 这里的单位是cm
        self.pdf_w = 25 * cm    #pdf宽
        self.pdf_h = 30 * cm    #pdf高
        self.pic_x=4 * cm       #水印图片宽
        self.pic_y=4 * cm       #水印图片高
        self.path='/Users/qmp/Desktop/'

    #文字水印
    def create_word_watermark(self,content,mark_name):

        c=canvas.Canvas(self.path+'%s.pdf'%mark_name)
        # c.setStrokeColorRGB(1, 1, 0.3)
        c.setFillColorRGB(0.92, 0.92, 0.92)
        c.setFont("Arial Unicode", 13)
        # c.rotate(9)
        # c.skew(10, -10)
        # # c.saveState()
        # c.restoreState()
        # c.translate(-0,- 0)
        c.rotate(-13)
        c.skew(10, 0)
        c.saveState()
        for i in range(-10,30,5):
            for j in range(-20,50,2):
                c.drawString(i*cm, j*cm, content.decode('utf8'))

        # c.drawCentredString(0, 0,content.decode('utf8'))
        # 保存水印文件
        c.save()


    ##图片水印
    def create_pic_watermark(self,img):
        f_pdf = 'watermark_img.pdf'
        c = canvas.Canvas(f_pdf, pagesize=(self.pdf_w, self.pdf_w))
        c.setFillAlpha(0.09)  # 设置透明度
        #变形旋转效果
        # c.rotate(14)
        # c.skew(10, 5)
        # c.saveState()
        # for i in range(0,50,10):
            # for j in range(0,50,8):
        c.drawImage(img,  9* cm, 0.5*cm, self.pic_x, self.pic_y)
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



    def add_watermark(self,pdf_file, watermark_file,outdir):
        pdf_output = PdfFileWriter()
        input_s = open(self.path+pdf_file, 'rb')
        pdf_input = PdfFileReader(input_s)
        pdf_watermark = PdfFileReader(open(self.path+watermark_file, 'rb'))

        #加密检测
        self.solve_encrypt(pdf_input)

        # 获取页数
        pageNum = pdf_input.getNumPages()

        # 给每一页打水印
        for i in range(pageNum):
            page = pdf_input.getPage(i)
            page.mergePage(pdf_watermark.getPage(0))
            page.compressContentStreams()  # 压缩内容
            pdf_output.addPage(page)
        if not os.path.exists(self.path+outdir):
            os.makedirs(self.path+outdir)
        output_s = open(self.path+outdir+pdf_file, 'wb')
        pdf_output.write(output_s)
        output_s.close()
        input_s.close()
        return self.path+outdir+pdf_file

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




if __name__ == '__main__':
    pass
#     path='/Users/qmp/Desktop/'
#
#     #加水印之后的输出文件夹
#     out_dir='output'
#
#     pdf_obj=PDF_watermark_handle()
#
#     #制作文字水印
#     pdf_obj.create_word_watermark('你是谁？')
#
#     #制作图片水印
#     pdf_obj.create_pic_watermark(path+'qmp_logo.png')
#
#     # url='http://pdf1.qimingpian.com/announcement/5af515ae557ce.pdf'
#     # file_pdf=url.split('/')[-1].strip()
#     #
#     # if not os.path.exists(path+file_pdf):
#     #     res = requests.get(url)
#     #     with open(path+file_pdf,'w') as f:
#     #         f.write(res.content)
#     #     print(file_pdf)
#
#     #pdf添加水印保存
#     file_pdf='1.pdf'
#     pdf_obj.add_watermark(file_pdf,'./watermark_img.pdf',out_dir)