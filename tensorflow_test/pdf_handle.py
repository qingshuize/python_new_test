#coding:utf8
from cStringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re
from peewee import *
from hashlib import md5
import requests
import os
import commands
URL_db = MySQLDatabase(
    host='47.94.38.128',
    database='shujujiance',
    user="shujujiance_pyt",
    passwd="f5W1vg##e1cf",
    charset='utf8'
)


def pdf_to_text(path):

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()

    device = TextConverter(rsrcmgr, retstr,codec='utf-8',laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    with open(path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, set()):
            interpreter.process_page(page)
            text = retstr.getvalue()
            # print(text)
            print(50 * '*' + 'convert end' + 50 * '*')
            yield text

    device.close()
    retstr.close()

if __name__ =='__main__':
    # file_list=['1204342691.pdf','1204352020.PDF']
    # sql='select id,title,pdf_source_link from mf_neeq_total where company="" or company is null and pdf_source_link like "%%%%pdf" order by id limit 10'
    sql='select code,pdf_source_link from mf_neeq_total inner join mf_capital_information where ipo_code=code and ipo_type="已挂牌" and category="公开转让说明书" limit 5,3'
    cur=URL_db.execute_sql(sql)
    res=cur.fetchall()
    # for file_name in file_list:
    path='/Users/qmp/Desktop/'
    for x in res:
        # id=x[0]
        # title=x[1]
        code=x[0]
        file_link=x[1]
        print(code)
        print(file_link)
        file_name=md5(file_link).hexdigest()
        pdf_name=file_name+'.pdf'
        ress=requests.get(file_link)
        if not os.path.exists(path+pdf_name):
            with open(path+pdf_name,'w') as f:
                f.write(ress.content)
        # text=pdf_to_text(path+file_name)
        html_name=file_name+'.html'
        if not os.path.exists(path+html_name):
            # os.system('pdf2htmlEX --zoom 1 %s %s' % (path+pdf_name,path+html_name))
            commands.getoutput('pdf2htmlEX --zoom 1 %s --dest-dir %s %s' % (path+pdf_name,path,html_name))
        # print(50 * '*' + 'content' + 50 * '*')

        with open(path+html_name,'r') as fp:
            text=fp.read()
            print(os.path.exists(path+html_name))
            search_info=re.findall(r'主办券商(\W+)证券',text)
            print(len(search_info))
            if search_info:
                for info in search_info:
                    print(info)
        # for detail in search_info:
            # print(detail.split('：')[-1]+'证券股份有限公司')
        # print(text)
        # used_text=re.findall('[证券|公司]代码：(.*)\W+[证券|公司]简称：(.*)公告编号',text)[0]
        # print(used_text)
        # code=used_text[0].strip()
        # print(code)
        # short=used_text[1].strip()
        # print(short)

        # regexp=re.compile('\s+1?')
        # used_text=regexp.split(text)[0]
        # print(used_text)
        # print(50 * '*' + 'used_text'+50 * '*')
        # regexp_1 = re.compile('\n+')
        # used_lines_text = regexp_1.split(text)[0]
        # print(used_lines_text)
        # regexp_1 = re.compile('\n{2}')
        # # used_lines_text = regexp_1.split(used_text)[0]
        # used_lines_text = '\n'.join(regexp_1.split(used_text)[6:])
        # print(used_lines_text)