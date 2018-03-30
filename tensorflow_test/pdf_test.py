#coding:utf8
from pyPdf import PdfFileWriter,PdfFileReader
import os
import re
def main():
    path = '/Users/qmp/Desktop/'
    file_list=os.listdir(path)
    for file in file_list:
        try:
            if file.endswith('.pdf'):
                print(file)
                input = PdfFileReader(open(path+file, "rb"))
                title=input.getDocumentInfo().title
                print("title: %s" % title)
                number=input.getNumPages()
                print('total pages:%s'%number)
                content = ""
                for i in range(3):
                #     page=input.getDocumentInfo()
                    info=input.getPage(i)
                    # print(info.getContents())
                    extractedText = info.extractText()
                    content += extractedText + "\n"
                    print(content)
                #     print(info)
                #     use_info=re.findall('[.]+',str(info))
                #     print(use_info)
        except Exception as e:
            print(e)

if __name__=='__main__':
    main()