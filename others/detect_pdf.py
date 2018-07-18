#coding:utf8

import traceback, tempfile
from PyPDF2 import PdfFileReader
import requests
import time
path='/Users/qmp/Desktop/'
from peewee import *
URL_db = MySQLDatabase(
    ###

#
# def isValidPDF_bytes(pdfBytes):
#     bValid = True
#     try:
#         fp = tempfile.TemporaryFile()
#         fp.write(pdfBytes)
#         reader = PdfFileReader(fp)
#         fp.close()
#         if reader.getNumPages() < 1:  # 进一步通过页数判断。
#             bValid = False
#     except:
#         bValid = False
#         print('*' + traceback.format_exc())

    # return bValid

import io, traceback,os
from PyPDF2 import PdfFileReader


def isValidPDF_bytes(pdfBytes):
    bValid = True
    try:
        b = io.BytesIO(pdfBytes)
        reader = PdfFileReader(b)
        if reader.getNumPages() < 1:  # 进一步通过页数判断。
            bValid = False
    except Exception as e:
        # pass
        bValid = False
        # print(e)
        # print('*' + traceback.format_exc())

    return bValid


# 参数为bytes类型数据。利用临时文件。
def isValidPDF_bytes1(pdfBytes):
    bValid = True
    try:
        fp = tempfile.TemporaryFile()
        fp.write(pdfBytes)
        reader = PdfFileReader(fp)
        # if reader.isEncrypted:
        #     try:
        #         reader.decrypt('')
        #         print('File Decrypted (PyPDF2)')
        #     except:
        #         command = ("cp " + filename +
        #                    " temp.pdf; qpdf --password='' --decrypt temp.pdf " + filename
        #                    + "; rm temp.pdf")
        #         os.system(command)
        #         print('File Decrypted (qpdf)')
        #         fp = open(filename)
        #         pdfFile = PdfFileReader(fp)
        # else:
        #     print('File Not Encrypted')
        fp.close()
        if reader.getNumPages() < 1:  # 进一步通过页数判断。
            bValid = False
    except:
        bValid = False
        print('*' + traceback.format_exc())

    return bValid

if __name__ =='__main__':
    sql='select id,qmp_url from mf_hk_zhaogu where qmp_url like "%%%%ganggu%%%%" and link_is_real=0 order by id desc limit 10'
    cur = URL_db.execute_sql(sql)
    res = cur.fetchall()
    for x in res:
        id = x[0]
        url = x[1]
        res=requests.get(url)
        time.sleep(0.1)
        print(isValidPDF_bytes(res.content))
        if not isValidPDF_bytes(res.content):
            print('id:'+str(id))
            print('link:'+url)
            # update_sql='update mf_hk_zhaogu set qmp_url=null where id=%s'
            # URL_db.execute_sql(update_sql,[id])
            # print('update success!')
