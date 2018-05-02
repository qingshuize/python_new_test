#coding:utf8
from cStringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import *
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
import re
from peewee import *
from hashlib import md5
import requests
import os
import urllib2

path = '/Users/qmp/Desktop/'

URL_db = MySQLDatabase(
    host='47.94.38.128',
    database='shujujiance',
    user="shujujiance_pyt",
    passwd="f5W1vg##e1cf",
    charset='utf8'
)


def try_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            print('Error!')

    return wrapper


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

if __name__ =='__main__':
    # file_list=['1204342691.pdf','1204352020.PDF']
    # sql='select id,title,pdf_source_link from mf_neeq_total where company="" or company is null and pdf_source_link like "%%%%pdf" order by id limit 10'
    # sql='select code,pdf_source_link from mf_neeq_total inner join mf_capital_information where ipo_code=code and ipo_type="已挂牌" and category="公开转让说明书" limit 5,3'
    sql='select id,company,pdf_source_link from mf_neeq_total where code="" and title regexp "券商公告" order by id desc limit 1'
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

        pdfTotxt(path+pdf_name,path+file_name+'.txt')

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