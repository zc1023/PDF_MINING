import PDFanalysis

pdf = PDFanalysis.PdfAnanlysis('./data/paper/2987443.2987455.pdf')
for i in pdf.reference():
    print(i)