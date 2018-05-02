#coding:utf8
import comtypes.client
import os
path='/Users/qmp/Desktop/'

def init_ppt():
    ppt=comtypes.client.CreateObject('Powerpoint.Application')
    ppt.Visible=1
    return ppt

def PPT2pdf(ppt,input,output,formatType=32):
    if output[-3:]!='pdf':
        output=output+'.pdf'
    deck=ppt.Presentations.Open(input)
    deck.SaveAs(output,formatType)
    deck.close()

def Convert_in_folder(ppt,path):
    files=os.listdir(path)
    pptfiles=[f for f in files if f.endswith(('.ppt','pptx'))]
    for pptfile in pptfiles:
        fullpath=os.path.join(path,pptfile)
        PPT2pdf(ppt,fullpath,fullpath)

if __name__ == '__main__':
    ppt=init_ppt()
    ppt.Convert_in_folder(ppt,path)
    ppt.Quit()
