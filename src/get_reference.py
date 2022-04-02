import os.path
import re
import threading
import time
from lxml import etree
import requests
import random
from src import PDFanalysis
from collections import deque
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
PROXIES = [
    {'ip_port': '111.11.228.75:80', 'user_pass': ''},
    {'ip_port': '120.198.243.22:80', 'user_pass': ''},
    {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
    {'ip_port': '101.71.27.120:80', 'user_pass': ''},
    {'ip_port': '122.96.59.104:80', 'user_pass': ''},
    {'ip_port': '122.224.249.122:8088', 'user_pass': ''},
]
dblp = 'https://dblp.org/search?q='
def get_url(url:str):
    i = 0
    while (i < 2):
        # double try to reduce the impact of network fluctuations
        try:
            time.sleep(random.random())
            # random dormancy against the anti-repilte policy
            r = requests.get(url, headers={'User-agent': USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]},
                             #proxies=PROXIES[random.randint(0, len(PROXIES) - 1)], #free proxies,unstable and unnecessary
                             timeout=5)
            if r.status_code == 200:
                return r.text
        except:
            i += 1
    return ''

def get_data(reference:str):
    try:
        html = etree.HTML(get_url(dblp+ reference))
        link = html.xpath('//nav[@class = "publ"]/ul/li[2]/div[1]/a/@href')
        # got the reference address
        return link
    except:
        return []

def get_bib(url:str,file:str):
    # save bib
    context = get_url(url)
    with open(file,'w') as f:
        f.write(context)

def get_reference(dp,paper):
    while dp:
        reference  = dp.pop()
        list = get_data(reference)
        pattern = "[^a-zA-Z0-9. ]"
        reference = re.sub(pattern, '', reference)
        if list != []:
            # remove '.pdf' in flie name,the download address is only different from the page suffix
            get_bib(list[0].replace('html?view=bibtex', 'bib?param=1'), './data/reference/' + paper[0:-4] + '/' + reference)

class my_thread(threading.Thread):
    def __init__(self,paper,dp):
        threading.Thread.__init__(self)
        self.paper = paper
        self.dp = dp
    def run(self):
        get_reference(self.dp,self.paper)

# use threat to save time
def mulit_get_reference(paper:str,threadcont = 10):
    if not os.path.exists('./data/reference/'+paper[0:-4]+'/'):
        os.makedirs('./data/reference/'+paper[0:-4]+'/')
    pdf = PDFanalysis.PdfAnanlysis('./data/paper/'+paper)
    references = []
    for i in pdf.reference():

        list = i.split('.')
        for j in list:
            if j.count(" ") > 5:
                # remove impossibe reference
                references.append(j)
    dp = deque(references)

    threads=[]
    for i in range(threadcont):
        thread = my_thread(paper,dp)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    get_reference('ndss2021_3B-2_24008_paper.pdf')