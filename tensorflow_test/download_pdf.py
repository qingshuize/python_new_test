#coding:utf8
import requests
from hashlib import md5
import time

def download():
    headers={
        'Host':'ipo.csrc.gov.cn',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
        'Connection':'keep-alive',
        'Cookie':'BIGipServerpool_IPO=845457600.20480.0000; acw_tc=AQAAAH4TeAWHkwcAFrybJ88lduA3N1ta'
    }
    # url='http://ipo.csrc.gov.cn/pdfdownload.action?blockType=intention&ipoCode=731042634&xmlId=3&pdfBatch=%2Fxbrl2%2Fexhibitxbrl%2F%2F792573957%2F10198%2FCN-731042634-GA0101-20180126-31.pdf'
    url1='http://www.hkexnews.hk/APP/SEHK/2018/2018011501/Documents/SEHK201801300030_c.pdf'
    res=requests.get(url1,stream=True)
    path='/Users/qmp/Desktop/'
    file_name=md5(url1).hexdigest()+'.pdf'
    with open(path+file_name,'wb') as f:
        # f.write(res.content)
        # for x in res.raw:
        #     f.write(x)
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
                # time.sleep(0.1)


def download1():
    url='http://ipo.csrc.gov.cn/pdfdownload.action?blockType=intention&ipoCode=731042634&xmlId=3&pdfBatch=%2Fxbrl2%2Fexhibitxbrl%2F%2F792573957%2F10198%2FCN-731042634-GA0101-20180126-31.pdf'
    path = '/Users/qmp/Desktop/'
    res = requests.get(url)
    res.raise_for_status()
    playFile = open(path+'test.pdf', 'wb')
    for chunk in res.iter_content(100000):
        if chunk:
            playFile.write(chunk)
    playFile.close()


if __name__ == '__main__':

    download()
    # download1()




#
# import sys
# import requests
# import threading
# import datetime
#
# # 传入的命令行参数，要下载文件的url
# url = sys.argv[1]
#
#
# def Handler(start, end, url, filename):
#     headers = {'Range': 'bytes=%d-%d' % (start, end)}
#     r = requests.get(url, headers=headers, stream=True)
#
#     # 写入文件对应位置
#     with open(filename, "r+b") as fp:
#         fp.seek(start)
#         var = fp.tell()
#         fp.write(r.content)
#
#
# def download_file(url, num_thread=3):
#     r = requests.head(url)
#     try:
#         file_name = sha1(url).hexdigest()+'.pdf'
#         print(file_name)
#         file_size = int(
#             r.headers['content-length'])  # Content-Length获得文件主体的大小，当http服务器使用Connection:keep-alive时，不支持Content-Length
#     except:
#         print("检查URL，或不支持对线程下载")
#         return
#
#     # 创建一个和要下载文件一样大小的文件
#     fp = open(file_name, "wb")
#     fp.truncate(file_size)
#     fp.close()
#
#     # 启动多线程写文件
#     part = file_size // num_thread  # 如果不能整除，最后一块应该多几个字节
#     for i in range(num_thread):
#         start = part * i
#         if i == num_thread - 1:  # 最后一块
#             end = file_size
#         else:
#             end = start + part
#
#         t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
#         t.setDaemon(True)
#         t.start()
#
#     # 等待所有线程下载完成
#     main_thread = threading.current_thread()
#     for t in threading.enumerate():
#         if t is main_thread:
#             continue
#         t.join()
#     print('%s 下载完成' % file_name)
#
#
# if __name__ == '__main__':
#     start = datetime.datetime.now().replace(microsecond=0)
#     download_file(url)
#     end = datetime.datetime.now().replace(microsecond=0)
#     print("用时: ",end)
#     print(end - start)