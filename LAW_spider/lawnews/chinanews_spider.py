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

getnexta=re.compile(r'<a href="(.*?)">下一页</a>')

class chinanews_spider():
    def __init__(self, cookies, outpath=u"C:/Users/sfe_williamsL/Desktop/文本相似性计算/新闻数据/",webtype="xingshianjian"):
        # 基础的url
        self.FRONT_URL = "http://www.chinalawnews.cn/"
        self.TARGET_URL = self.FRONT_URL+webtype+"/"
        """
        参数类型：
        user_id:URL中的ID
        hrml_title:请求地址TITLE
        client_id:第一次请求的ID
        """
        #self.AJAX_GETURL = "https://dl.acm.org/tab_about.cfm?id={user_id}&type=proceeding&sellOnline=0&parent_id={user_id}&parent_type=proceeding&toctitle=&tocissue_date=&notoc=0&usebody=tabbody&tocnext_id=&tocnext_str=&tocprev_id=&tocprev_str=&toctype=&_cf_containerId=cf_layoutareaprox&_cf_nodebug=true&_cf_nocache=true&_cf_clientid={client_id}&_cf_rc=1"
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
            "Content-Type": "text / html",
            "Host": "www.chinalawnews.cn"
        }
        self.crawlINFO=chinanew_info(outpath=outpath,fronturl=self.FRONT_URL)
        self.outpath = outpath
        self.id_list = [infoid.replace(".txt", "") for infoid in os.listdir(outpath)]
        print(self.id_list)

    def crawl(self, pre_num=5):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(self.TARGET_URL, headers=self.headers)
        html_text = res.content.decode("utf-8")
        soup_string = BeautifulSoup(html_text, "html.parser")
        infourllist = self.get_infourl(soup_string)
        for infourl in infourllist:
            downflag = self.store_info(infourl)
            print(infourl + "处理完毕....")
            if (downflag):
                print(infourl + "的新闻数据已经下载完毕")
                time.sleep(random.randint(0, 10))
        next_url=self.get_nexturl(soup_string)
        print("第1个页面内容已经下载完毕........")
        new_num = pre_num - 1
        while (new_num != 0 and next_url != ""):
            # 第二次请求获取PDF列表
            self.headers["User-Agent"] = random.choice(self.user_agent)
            res = requests.get(self.TARGET_URL+next_url, headers=self.headers)
            html_text = res.content.decode("utf-8")
            soup_string = BeautifulSoup(html_text, "html.parser")
            infourllist = self.get_infourl(soup_string)
            for infourl in infourllist:
                downflag = self.store_info(infourl)
                print(infourl + "处理完毕....")
                if (downflag):
                    print(infourl + "的新闻数据已经下载完毕")
                    time.sleep(random.randint(0, 10))
            next_url = self.get_nexturl(soup_string)
            print("第" + str(pre_num - new_num + 1) + "个页面内容已经下载完毕........")
            new_num = new_num - 1


    def store_info(self, info_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        fileid = info_url.split("/")[-1].replace(".html","")
        if (fileid in self.id_list):
            downflag = False
        else:
            self.crawlINFO.crawel(info_url)
            downflag = True
        return downflag

    def get_nexturl(self,soup_string):
        apages=soup_string.select("div[class=dede_pages]")[0]
        a_list=[_.get("href") for _ in apages.select("a") if("下一页" in _.get_text())]
        if(a_list):
            return a_list[0]
        else:
            return ""

    def get_infourl(self, maindiv):
        main_div = maindiv.select("div[id=mian]")[0]
        juti_list= main_div.select("div[class=juti_list]")
        for url in juti_list:
            yield url.select("a")[0].get("href")

class chinanew_info():
    def __init__(self,outpath=u"C:/Users/sfe_williamsL/Desktop/文本相似性计算/新闻数据/",fronturl="http://www.chinalawnews.cn/"):
        # 基础的url
        self.FRONT_URL = fronturl
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
            "Content-Type": "text / html",
            "Host": "www.chinalawnews.cn"
        }
        self.outpath = outpath

    def crawel(self,url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(self.FRONT_URL+url, headers=self.headers)
        html_text = res.content.decode("utf-8")
        soup_string = BeautifulSoup(html_text, "html.parser")
        store_info = self.parse_html(soup_string)
        fileid = url.split("/")[-1].replace(".html", "")
        filename = self.outpath + fileid + ".txt"
        f = open(filename,"wt")
        f.write(store_info)
        f.close()

    def parse_html(self,soup_string):
        article_info=soup_string.select("div[id=artical]")[0]
        headerinfo="<header>"+article_info.select("h1")[0].get_text()+"</header>"
        maindiv_info=article_info.select("div[id=artical_real]")[0]
        abstract_info="<abstract>"+maindiv_info.select("div[class='dy_box ss_none']")[0].get_text().replace("\r","").replace("\n\n","\n")+"</abstract>"
        main_info="<content>"+maindiv_info.select("div[id=main_content]")[0].get_text().replace("\r","").replace("\n\n","\n")+"</content>"
        all_info="\n".join([headerinfo,abstract_info,main_info])
        return all_info

if __name__=="__main__":
    #cookies = "__cfduid=d8d304e58cab2d74fd097f3e4c9af01ab1562507918; _ga=GA1.2.368478941.1562507920; CFP=1; _fbp=fb.1.1568542539206.470111739; IP_CLIENT=1795640; SITE_CLIENT=3011566; __cflb=2874915494; CFID=75945022; CFTOKEN=414fdc4b8db198c7%2D4BB2A536%2D0C7C%2D5AA7%2DF056E18400A56563; _gid=GA1.2.2129928846.1570367065; picked=3331212,prox; AK=expires%3D1570369171%7Eaccess%3D%2F10%2E1145%2F3340000%2F3331212%2F%2A%7Emd5%3D5dbe175e97ceaa7ec49861d8a0991545; cffp_mm=444; JSESSIONID=D48FFDA4278B409720C0B3FEF1B2A8D6.dl; __atuvc=0%7C37%2C42%7C38%2C52%7C39%2C25%7C40%2C8%7C41; __atuvs=5d9ab066b2e0ff30000"
    acmspider = chinanews_spider(cookies="",outpath=u"C:/Users/sfe_williamsL/Desktop/文本相似性计算/新闻数据/")
    acmspider.crawl(pre_num=20)
