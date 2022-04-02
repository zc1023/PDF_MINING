import os

from src import get_reference
# get_reference.get_reference('ndss2021_3B-2_24008_paper.pdf')
for root, dirs, files in os.walk('data/paper'):
    print(root)
    print(dirs)
    print(files)
# get_reference.mulit_get_reference('ndss2021_3B-2_24008_paper.pdf',threadcont= 20 )

# with open("./data/reference/ndss2021_3B-2_24008_paper/ Yin Zhang and Vern Paxson","r") as f:
#     str = f.read()
#     print(str)
#     list = f.readlines()
#     print(list)