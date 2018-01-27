#coding:utf8
from cStringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re


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
    file_list=['1204342691.pdf','1204352020.PDF']
    for file_name in file_list:
        text=pdf_to_text('/Users/qmp/Desktop/'+file_name)
        print(50 * '*' + 'content' + 50 * '*')
        # print(text)
        regexp=re.compile('\s+1?')
        used_text=regexp.split(text)[0]
        print(used_text)
        # print(50 * '*' + 'used_text'+50 * '*')
        # regexp_1 = re.compile('\n{2}')
        # # used_lines_text = regexp_1.split(used_text)[0]
        # used_lines_text = '\n'.join(regexp_1.split(used_text)[6:])
        # print(used_lines_text)