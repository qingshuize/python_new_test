#coding:utf8
from cStringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import *
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from peewee import *
from hashlib import md5
import requests
import os
import urllib2
from log_tool import *

path = '/Users/qmp/Desktop/'

URL_db = MySQLDatabase(
##
)



@try_error
def pdf_to_text(DataIO,Save_path):
    # 来创建一个pdf文档分析器
    parser = PDFParser(DataIO)
    # 创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr = PDFResourceManager()
        # 设定参数进行分析
        laparams = LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 处理每一页
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                try:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        with open('%s' % (Save_path), 'a') as f:
                            # 参数a，表示不会覆盖，直接追加写，和w不一样
                            f.write(x.get_text().encode('utf-8') + '\n')
                        print('convert txt ok!')
                except:
                    print "Failed!"

@try_error
#将一个pdf转换成txt
def pdfTotxt(filepath,outpath):
    try:
        fp = file(filepath, 'rb')
        outfp=file(outpath,'w')
        #创建一个PDF资源管理器对象来存储共享资源
        #caching = False不缓存
        rsrcmgr = PDFResourceManager(caching = False)
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams,imagewriter=None)
        #创建一个PDF解析器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                      password='',caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)
        #关闭输入流
        fp.close()
        #关闭输出流
        device.close()
        outfp.flush()
        outfp.close()
    except Exception as e:
         print("Exception:%s",e)


@try_error
def del_file(filename):
    for x in filename:
        os.remove(path+x)
        print('delete file %s ok!'%x)

from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Songti', '/Library/Fonts/Songti.ttc'))


#文字水印
def create_word_watermark(content):

    c=canvas.Canvas('watermark_word.pdf')
    c.setFont("Songti", 20)

    c.rotate(30)
    c.skew(10,0)
    c.saveState()

    c.drawString(200, 100, content.decode('utf8'))
    # c.drawText(content.decode('utf8'))
    # 保存水印文件
    c.save()
    pdf_watermark = PdfFileReader(open("watermark_word.pdf","rb"))
    return pdf_watermark



##图片水印
def create_pic_watermark(img):
    f_pdf = 'watermark_img.pdf'
    w_pdf = 25 * cm
    h_pdf = 30 * cm
    c = canvas.Canvas(f_pdf, pagesize=(w_pdf, h_pdf))
    c.setFillAlpha(0.1)  # 设置透明度
    print(c.drawImage(img,  8* cm, 1*cm, 5 * cm, 5 * cm))  # 这里的单位是物理尺寸
    c.save()
    pdf_watermark = PdfFileReader(open('watermark_img.pdf', 'rb'))
    return pdf_watermark

def solve_encrypt(pdf_input):
    # PDF文件被加密了
    if pdf_input.getIsEncrypted():
        print('该PDF文件被加密了.')
        # 尝试用空密码解密
        try:
            pdf_input.decrypt('')
        except Exception as  e:
            print('尝试用空密码解密失败.')
            return False
        else:
            print('用空密码解密成功.')



def add_watermark(pdf_file_in, pdf_watermark,pdf_file_out,max_page=None):
    pdf_output = PdfFileWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input_stream)

    # 获取PDF文件的页数
    pageNum = pdf_input.getNumPages()

    for i in range(pageNum):
        page = pdf_input.getPage(i)
        if i < max_page:
            page.mergePage(pdf_watermark.getPage(0))
            page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
    output_stream = open(os.path.join(pdf_file_out, os.path.basename(pdf_file_in)), 'wb')
    pdf_output.write(output_stream)
    output_stream.close()
    input_stream.close()
    return True


def Pdf_test():
    path = './'
    file_list = os.listdir(path)
    for file in file_list:
        try:
            if file.endswith('.pdf'):
                print(file)
                input = PdfFileReader(open(path + file, "rb"))
                title = input.getDocumentInfo().title
                print("title: %s" % title)
                number = input.getNumPages()
                print('total pages:%s' % number)
                content = ""
                for i in range(3):
                    #     page=input.getDocumentInfo()
                    info = input.getPage(i)
                    # print(info.getContents())
                    extractedText = info.extractText()
                    content += extractedText + "\n"
                    print(content)
                    #     print(info)
                    #     use_info=re.findall('[.]+',str(info))
                    #     print(use_info)
        except Exception as e:
            print(e)





if __name__ =='__main__':
    pdf_watermark = create_pic_watermark(path + 'qmp_logo.png')  # 图片水印
    pdf_watermark1 = create_word_watermark('666')  # 文字水印

    # file_list=['1204342691.pdf','1204352020.PDF']
    sql = 'select id,company,pdf_source_link from mf_neeq_total order by size desc limit 1'
    cur=URL_db.execute_sql(sql)
    res=cur.fetchall()
    # for file_name in file_list:

    for x in res:
        # id=x[0]
        # title=x[1]
        code=x[0]
        com=x[1]
        file_link=x[2]
        print(code)
        print(com)
        print(file_link)

        #直接从url获取
        # html = urllib2.urlopen(urllib2.Request(file_link)).read()
        # DataIO = StringIO(html)
        # pdf_to_text(DataIO, path+'b2.txt')


        file_name=md5(file_link).hexdigest()
        pdf_name=file_name+'.pdf'
        ress=requests.get(file_link)
        if not os.path.exists(path+pdf_name):
            with open(path+pdf_name,'w') as f:
                f.write(ress.content)

        add_watermark(path +pdf_name,pdf_watermark,path+'output',3) #添加前三页水印

                # pdfTotxt(path+pdf_name,path+file_name+'.txt')

        # html_name=file_name+'.html'
        # if not os.path.exists(path+html_name):
        #     # os.system('pdf2htmlEX --zoom 1 %s %s' % (path+pdf_name,path+html_name))
        #     commands.getoutput('pdf2htmlEX --zoom 1 %s --dest-dir %s %s' % (path+pdf_name,path,html_name))
        #     print('ok!')
        # i=0
        # while i<3:
        #     if not os.path.exists(path + file_name + '.txt'):
        #         Path = open(path+pdf_name, 'rb')
        #         pdf_to_text(Path,file_name)
        #         i+=1
        #
        # if os.path.exists(path + file_name + '.txt'):
        #     with open(path+file_name+'.txt','r') as f:
        #         print(50 * '*' + 'content' + 50 * '*')
        #         text=f.read()
        #
        #         use_info = re.findall(r'8\d{5}', text)
        #         use_info=list(set(use_info))
        #         print(use_info)
        #         if use_info:
        #             if len(use_info)==1:
        #                 update_sql='update mf_neeq_total set code=%s where company=%s'
        #                 URL_db.execute_sql(update_sql,[use_info[0],com])
        #                 print('update ok!')
        #                 del_file([file_name+'.txt',file_name+'.pdf'])
        # else:
        #     print('%s txt file not exist!'%file_name)



        # with open(path+html_name,'r') as fp:
        #     text=fp.read()
        #     print(os.path.exists(path+html_name))
        #     search_info=re.findall(r'主办券商(\W+)证券',text)   ##查找主办券商
        #     print(len(set(search_info)))
        #     if search_info:
        #         for info in set(search_info):
        #             print(info)
        # for detail in search_info:
            # print(detail.split('：')[-1]+'证券股份有限公司')
        # print(text)



        # used_text=re.findall('[证券|公司]代码：(.*)\W+[证券|公司]简称：(.*)公告编号',text)[0]
        # print(used_text)
        # code=used_text[0].strip()
        # print(code)
        # short=used_text[1].strip()
        # print(short)


        # print(50 * '*' + 'used_text'+50 * '*')
        # regexp_1 = re.compile('\n+')
        # used_lines_text = regexp_1.split(text)[0]
        # print(used_lines_text)
        # regexp_1 = re.compile('\n{2}')
        # # used_lines_text = regexp_1.split(used_text)[0]
        # used_lines_text = '\n'.join(regexp_1.split(used_text)[6:])
        # print(used_lines_text)
