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
            return text

    device.close()
    retstr.close()

if __name__ =='__main__':
    # file_list=['1204342691.pdf','1204352020.PDF']
    sql='select id,title,pdf_source_link from mf_neeq_total where company="" or company is null and pdf_source_link like "%%%%pdf" order by id limit 10'
    cur=URL_db.execute_sql(sql)
    res=cur.fetchall()
    # for file_name in file_list:
    path='/Users/qmp/Desktop/'
    for x in res:
        id=x[0]
        title=x[1]
        file_link=x[2]
        file_name=md5(file_link).hexdigest()+'.pdf'
        ress=requests.get(file_link)
        with open(path+file_name,'w') as f:
            f.write(ress.content)
        text=pdf_to_text(path+file_name)
        print(50 * '*' + 'content' + 50 * '*')
        # print(text)
        # used_text=re.findall('[证券|公司]代码：(.*)\W+[证券|公司]简称：(.*)公告编号',text)[0]
        # print(used_text)
        # code=used_text[0].strip()
        # print(code)
        # short=used_text[1].strip()
        # print(short)

        regexp=re.compile('\s+1?')
        used_text=regexp.split(text)[0]
        print(used_text)
        print(50 * '*' + 'used_text'+50 * '*')
        # regexp_1 = re.compile('\n+')
        # used_lines_text = regexp_1.split(text)[0]
        # print(used_lines_text)
        # regexp_1 = re.compile('\n{2}')
        # # used_lines_text = regexp_1.split(used_text)[0]
        # used_lines_text = '\n'.join(regexp_1.split(used_text)[6:])
        # print(used_lines_text)