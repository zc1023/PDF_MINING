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


class PdfAnanlysis:
    def __init__(self, flie,password=""):
        self.file = flie
        self.password = password

    def reference(self):
        with open(self.file,'rb') as fp:
            parser = PDFParser(fp)
            document = PDFDocument(parser,self.password)
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr,laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr,device)

            str = ""
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
            pattern = '\[.*\]'
            return re.split(pattern,str)


if __name__ == '__main__':
    pdf = PdfAnanlysis('./data/paper/2987443.2987455.pdf')
    for i in pdf.reference():
        print(i)
