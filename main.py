import PDFanalysis
import get_reference
pdf = PDFanalysis.PdfAnanlysis('./data/paper/2987443.2987455.pdf')
result=[]

# for i in pdf.reference():
#     print(i)
co= 0
for i in pdf.reference():
    # print(i)
    flag = False
    # if ":/" not in i :
    list = i.split('.')
    for j in list :
        if j.count(" ") > 3:
            if get_reference.get(j):
                flag = True
                co+=1
    if flag:
        print(i)
        result.append(i)
# print(result)
print(co)