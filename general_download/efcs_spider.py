#encoding=utf-8

import sys
import re
import requests
import time
import random
import os
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )


pdftitle=re.compile(r"ftid=(\d+?)&")

class Base_EFSA():
    def __init__(self,outpath=u"C:/Users/sfe_williamsL/Desktop/会议论文下载/wsdm/"):
        # 基础的url
        self.FRONT_URL = "https://efsa.onlinelibrary.wiley.com"
        """
        参数类型：
        user_id:URL中的ID
        hrml_title:请求地址TITLE
        client_id:第一次请求的ID
        """
        self.RESULT_URL="https://efsa.onlinelibrary.wiley.com/action/doSearch?AllField={query_word}"
        # 请求头构造
        self.user_agent = [
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
        ]
        self.headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Connection": "keep-alive",
                        "Content-Type": "text / html;charset = UTF - 8",
                        "refer":"https://efsa.onlinelibrary.wiley.com/"
                        }

    def crawl(self,query_word,pre_num=5):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        url=self.RESULT_URL.format(query_word=query_word.replace(" ","+"))
        res = requests.get(url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        pre_url=self.is_next(soup_string)
        for ul in soup_string.select("ul"):
            for info in ul.select("div[class='item__body']"):
                title=info.select("span[class='hlFld-Title']")[0].get_text()
                author=info.select("span[class='hlFld-ContribAuthor']")[0].get_text()
                journal=info.select("a[class='publication_meta_serial']")[0].get_text()
                volume=info.select("a[class='publication_meta_volume_issue']")[0].get_text()
                date=info.select("p[class='meta__epubDate']")[0].get_text().replace("\r","").replace("\n","").strip()
                yield "\t".join([title,author,journal,volume,date])
        while(pre_url!=""):
            self.headers["User-Agent"] = random.choice(self.user_agent)
            res = requests.get(pre_url, headers=self.headers)
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            pre_url = self.is_next(soup_string)
            for ul in soup_string.select("ul"):
                for info in ul.select("div[class='item__body']"):
                    title = info.select("span[class='hlFld-Title']")[0].get_text()
                    author = [a.get_text() for a in info.select("span[class='hlFld-ContribAuthor']")]
                    journal = info.select("a[class='publication_meta_serial']")[0].get_text()
                    volume = info.select("a[class='publication_meta_volume_issue']")[0].get_text()
                    date = info.select("p[class='meta__epubDate']")[0].get_text().replace("\r","").replace("\n","").strip()
                    yield "\t".join([title, author, journal, volume, date])


    def is_next(self,maindiv):
        pre_a=maindiv.select("a[title='Next page']")
        if(pre_a):
            pre_url=pre_a[0].get("href")
            return pre_url
        else:
            pre_url=""
            return pre_url

if __name__=="__main__":
    cookies = "__cfduid=d8d304e58cab2d74fd097f3e4c9af01ab1562507918; _ga=GA1.2.368478941.1562507920; CFP=1; _fbp=fb.1.1568542539206.470111739; IP_CLIENT=1795640; SITE_CLIENT=3011566; AK=expires%3D1569583631%7Eaccess%3D%2F10%2E1145%2F3330000%2F3326734%2F%2A%7Emd5%3D5a5b0a23a35ea57942b6c99d7b76b980; JSESSIONID=183FA878A7105BECA4C60AA5F074DBB3.cfusion; CFID=161588552; CFTOKEN=67939e4f73ba9201%2DCD6C9827%2DC044%2D883C%2D3A33BE96DC37BF47; __cflb=2605054591; cffp_mm=0; __atuvc=0%7C36%2C0%7C37%2C42%7C38%2C52%7C39%2C1%7C40; __atuvs=5d901d4d5c8bcd98000"
    acmspider = Base_EFSA()
    text_list=acmspider.crawl(query_word="genetically modified")
    for text in text_list:
        print(text)