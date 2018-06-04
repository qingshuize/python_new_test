#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import subprocess
import os,requests
from pyPdf import PdfFileWriter, PdfFileReader
from cStringIO import StringIO
from reportlab.pdfgen import canvas
from peewee import *
import signal
import datetime

qmpnews_db = MySQLDatabase(
    host='47.94.38.128',
    port=3306,
    database='qmpnews',
    user="qmpnews",
    passwd="q1a#9nB@88RePws",
    charset='utf8'
)


def after_timeout():  # 超时后的处理函数
    print("timeout!!!.")

#超长时间处理
def timeout_error(interval,callback):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(interval)  # 设置 num 秒的闹钟
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError as e:
                print(e)
                callback()
        return to_do
    return wrap


def update_flag(url):
    sql='update mf_file_list set is_watermark=1 where url=%s'
    qmpnews_db.execute_sql(sql,[url])
    print('update flag ok!')

def decompress_pdf(temp_buffer):
    temp_buffer.seek(0)  # Make sure we're at the start of the file.

    process = subprocess.Popen(['pdftk.exe',
                                '-',  # Read from stdin.
                                'output',
                                '-',  # Write to stdout.
                                'uncompress'],
                                stdin=temp_buffer,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return StringIO(stdout)


class PDF_watermark_handle(object):

    def __init__(self):

        self.pic_x = 96  # 水印图片宽
        self.pic_y = 96  # 水印图片高
        # self.path='/alidata1/www/pdf1.qimingpian.com/'
        self.path = '/Users/qmp/Desktop/'


    ##图片水印
    def create_pic_watermark(self,img,watermark_file,pdf_w,pdf_h):

        c = canvas.Canvas(watermark_file, pagesize=(pdf_w,pdf_h))
        c.setFillAlpha(0.13)  # 设置透明度
        #变形旋转效果
        c.drawImage(self.path+img, float(pdf_w) / 2 - self.pic_x / 2, 0, self.pic_x, self.pic_y)
        c.save()

    #处理加密pdf文件
    def solve_encrypt(self,pdf_input,pdf_file):

        if pdf_input.getIsEncrypted():
            print('该PDF文件被加密了.')
            # 尝试用空密码解密
            try:
                pdf_input.decrypt('')
            except Exception:
                print('尝试解密失败.')
                return False
            else:
                print(pdf_file+'首次解密成功.')


    def get_pdf_size(self,pdf_input,i):

        try:
            print(pdf_input.flattenedPages)
            [_, _, x, y] = list(pdf_input.flattenedPages[i].get('/MediaBox'))
            if x == 0 or y==0:
                [x, _, _, y] = list(pdf_input.flattenedPages[i].get('/CropBox'))

        except Exception as e:
            print(e)
            [_, _, x, y] = list(pdf_input.flattenedPages[i].get('/CropBox'))
        print(x, y)
        return x,y

    #@timeout_error(20,after_timeout)
    def add_watermark(self,pdf_file, watermark_file,outdir,num):
        try:
            if os.path.exists(self.path+pdf_file):
                pdf_output = PdfFileWriter()
                input_s = open(self.path + pdf_file, 'rb')
                pdf_input = PdfFileReader(input_s)

                # with open(self.path+pdf_file, 'rb') as input_file:
                #     input_buffer = StringIO(input_file.read())
                # try:
                #     pdf_input = PdfFileReader(input_buffer)
                # except utils.PdfReadError as e:
                #     print(e)
                #     pdf_input=decompress_pdf(input_buffer)
                # print(pdf_input)

                #加密检测
                self.solve_encrypt(pdf_input,pdf_file)

                # 获取页数
                pageNum = pdf_input.getNumPages()

                print('页码总数：'+str(pageNum))
                if not os.path.exists(self.path+outdir):
                    os.makedirs(self.path+outdir)
                out_file=pdf_file.replace('.pdf','（加水印）.pdf')
                if not os.path.exists(self.path+outdir+out_file):
                    # # 给每一页打水印
                    for i in range(pageNum):
                        page = pdf_input.getPage(i)
                        print(i)
                        if i<num:
                            #针对每页格式不同，制作相应格式的水印pdf
                            w,h=self.get_pdf_size(pdf_input,i)
                            self.create_pic_watermark('qmp_logo1.png',watermark_file,w,h)
                            print('create watermark ok!')
                            s = open(watermark_file, 'rb')
                            pdf_watermark = PdfFileReader(s)
                            page.mergePage(pdf_watermark.getPage(0))
                        page.compressContentStreams()  # 压缩内容
                        pdf_output.addPage(page)

                    output_s = open(self.path+outdir+out_file, 'wb')
                    pdf_output.write(output_s)

                    # update_flag('http://pdf1.qimingpian.com/announcement/'+pdf_file)
                    print('add watermark ok!')
                    output_s.close()
                else:
                    print('加水印文件已存在.')
                input_s.close()
            else:
                print('原文件不存在！')
        except Exception as e:
            print(file_pdf+': '+e.message)
            # if e.message.startswith('EOF'):
            #     print('eof!!!!')
            # elif e.message.endswith('decrypted'):
            #     print('decrypted!!!')
            return e.message

    def get_url_content(self,url):
        res=requests.get(url)
        if res.status_code==200:
            file_pdf = url.split('/')[-1]
            with open(self.path + file_pdf, 'w') as f:
                f.write(res.content)
            print(file_pdf+' save ok!')
            print(os.path.getsize(self.path + file_pdf))
            return file_pdf
        else:
            return False



def pdf_test(pdf_name):
    path='/Users/qmp/Desktop/'
    if os.path.exists(path + pdf_name):
        try:
            pdf_input = PdfFileReader(open(path + pdf_name, 'rb'))
            page=pdf_input.getNumPages()
            print(page)
            for i in range(5):
                [_,_,X,Y]=media_size=pdf_input.flattenedPages[i].get('/MediaBox')
                if X==0 or Y==0:
                    print(media_size)
                    print('\n')
        except Exception as e:
            print(e)




if __name__ == '__main__':

    #加水印之后的输出文件夹
    # out_dir='announcement/'
    out_dir = 'output1/'

    pdf_obj=PDF_watermark_handle()

    sql='SELECT url FROM mf_file_list WHERE `del_flag` = 0 AND `open_flag` = 1 AND `source_flag` = 1 and is_watermark=1 and url like "%%announcement%%pdf" ORDER BY report_date desc limit 50'
    # cusor=qmpnews_db.execute_sql(sql)
    # ress=cusor.fetchall()
    ress=[x for x in os.listdir('/Users/qmp/Desktop/') if x.endswith('.pdf')]
    # ress=['5b0e6f7830150.pdf']
    # error_list=[]
    for s in ress:

        # url=s[0].encode('utf8').replace('real','raw')
        # file_pdf=url.split('/')[-1]
        #
        # if not os.path.exists('/Users/qmp/Desktop/'+file_pdf):
        #     pdf_obj.get_url_content(url)
        # else:
            # pass
        file_pdf=s
        print(file_pdf)
        pdf_test(file_pdf)
        # # commands.getoutput('cp announcement/%s announcement_raw/%s'%(file_pdf,file_pdf))
        # # print('copy ok!')
        # print('开始时间：'+str(datetime.datetime.now()))
        # #pdf添加水印保存
        # error_info=pdf_obj.add_watermark(file_pdf,'watermark_img1.pdf',out_dir,3)
        # if error_info  !='file has not been decrypted':
        #     error_list.append([file_pdf,error_info])

    # print(len(error_list))
    # # error_set=set(error_list)
    # # error_dict={}
    # # for x in error_set:
    # #     error_dict[x]=error_list.count(x)
    # # print(error_dict)
    #
    # for m,n in error_list:
    #     print(m+':'+n)