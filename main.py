# pdf_2.py

# 导入库
import re

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator

# 提供初始密码
password = ''
# 没有密码可以初始密码
# document.initialize()

#打开pdf文件
fp = open('./data/paper/2987443.2987455.pdf','rb')

#从文件句柄创建一个pdf解析对象
parser = PDFParser(fp)

#创建pdf文档对象，存储文档结构
document = PDFDocument(parser)

#创建一个pdf资源管理对象，存储共享资源
rsrcmgr = PDFResourceManager()

laparams = LAParams()

#创建一个device对象
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

#创建一个解释对象
interpreter = PDFPageInterpreter(rsrcmgr, device)

#处理包含在文档中的每一页
str =""
flag = False
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    layout = device.get_result()

    for x in layout:
        # 获取文本对象
        if isinstance(x, LTTextBox):
            if 'REFERENCES' in x.get_text():
                flag = True
            if flag:
                str = str + x.get_text()

print(str)
pattern = '\[.*\]'
for i in re.split(pattern,str):
    # if re.findall(pattern,i) != None:
        print(i)

