# coding = utf8

import re
import requests
import time
import random
import os
from bs4 import BeautifulSoup

import logging

file_handler = logging.FileHandler('./log.txt',mode='wt', encoding='utf-8')
logging.basicConfig(level=logging.INFO,
                    handlers={file_handler},
                    format='%(message)s')

class Base_AllenAI():
    def __init__(self,outpath=u"E:/计算机论文/Allen AI/"):
        # 基础的url
        self.FRONT_URL = "https://www.semanticscholar.org"
        """
        参数类型：
        user_id:URL中的ID
        hrml_title:请求地址TITLE
        client_id:第一次请求的ID
        """
        self.REQUEST_URL="https://allenai.org/papers?q={query}"
        self.PAGE_NUM = "&o={page_num}1"
        self.BASE_info = "{info_url}\t{title}\t{conf}\t{abstract}\t{down_flag}"
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
                        # "Content-Type": "text / html;charset = UTF - 8"
                        }

        self.outpath=outpath
        self.id_list=[ pdfid.replace(".pdf","") for pdfid in os.listdir(outpath)]
        print(self.id_list)

    def crawl(self,query,pre_num=1):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        url = self.REQUEST_URL.format(query=query)
        print(url)
        #第一次请求获取相关论文列表
        res = requests.get(url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        max_page = self.allPage(soup_string)
        if(pre_num<=1):
            url_list = self.get_paperlist(soup_string)
            for url in url_list:
                print(url)
                pdf_url = self.get_info(url)
                if(pdf_url):
                    print(pdf_url + "开始下载....")
                    downflag = self.download_pdf(pdf_url)
                    print(pdf_url + "处理完毕....")
                    if(downflag):
                        print(pdf_url + "的pdf已经下载完毕")
                        time.sleep(random.randint(0,10))
            print("第1个页面内容已经下载完毕........")
            pre_num = pre_num+1
        while(pre_num<=max_page):
            url = self.REQUEST_URL.format(query=query) + self.PAGE_NUM.format(page_num=(pre_num-1))
            print(url)
            #第一次请求获取相关论文列表
            res = requests.get(url, headers=self.headers)
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            url_list = self.get_paperlist(soup_string)
            for url in url_list:
                print(url)
                pdf_url = self.get_info(url)
                if(pdf_url):
                    print(pdf_url + "开始下载....")
                    downflag = self.download_pdf(pdf_url)
                    print(pdf_url + "处理完毕....")
                    if(downflag):
                        print(pdf_url + "的pdf已经下载完毕")
                        time.sleep(random.randint(0,10))
            print("第"+str(pre_num)+"个页面内容已经下载完毕........")
            pre_num = pre_num+1

    def get_paperlist(self,soup_string):
        ul_soup = soup_string.find_all(attrs={"class": "ant-list-items"})
        for ul in ul_soup:
            a_soup_list = ul.select("h2 > a")
            for a_soup in a_soup_list:
                yield a_soup.get("href")

    def allPage(self,soup_string):
        navi_list = soup_string.find_all("ul",class_="ant-pagination")
        for ul_navi in navi_list:
            li_list = ul_navi.find_all("li")
            num_list = [int(li.get("title")) for li in li_list if(li.get("title").isdigit())]
        return max(num_list)

    def get_firstText(self,tmp_list):
        if(tmp_list):
            return tmp_list[0].get_text()
        else:
            return ""

    def get_info(self,info_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(info_url, headers=self.headers)
        print(res.status_code)
        if(res.status_code==301 or res.status_code==302):
            html = requests.get(info_url, headers=self.headers, allow_redirects=False)
            new_url = html.headers['Location']
            res = requests.get(new_url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        title = self.get_firstText(soup_string.find_all("h1"))
        year_info = self.get_firstText(soup_string.find_all("span",attrs={"data-selenium-selector": "year-and-venue"}))
        abstract = self.get_firstText(soup_string.find_all("span",attrs={"data-selenium-selector": "text-truncator-text"}))
        pdf_url = soup_string.find_all("meta",attrs={"name":"citation_pdf_url"})
        if(pdf_url):
            pdf_url = pdf_url[0].get("content")
        else:
            pdf_url = None
        log_info = self.BASE_info.format(info_url=info_url,title=title,conf=year_info,abstract=abstract,down_flag=pdf_url)
        logging.info(log_info)
        return pdf_url

    def download_pdf(self,pdf_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        pdf_id = pdf_url.split("/")[-1].replace(".pdf","")
        print(pdf_id)
        if(pdf_id in self.id_list):
            downflag=False
        else:
            if(".pdf" not in pdf_url):
                downflag=False
                return downflag
            filename=self.outpath+pdf_id+".pdf"
            res_pdf = requests.get(pdf_url, headers=self.headers)
            with open(filename, "wb") as w:
                w.write(res_pdf.content)
            downflag=True
        return downflag


if __name__=="__main__":
    acmspider = Base_AllenAI(outpath=u"E:/计算机论文/Allen AI/")
    acmspider.crawl("commonsense",pre_num=1)