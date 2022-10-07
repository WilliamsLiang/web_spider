#encoding=utf-8

import sys
import re
import requests
import urllib
import time
import random
from bs4 import BeautifulSoup
from njaulibparse.bookinfo import bookinfo


class searchinfo():
    def __init__(self):
        # 基础的url
        self.BASE_URL = " http://libweb.njau.edu.cn/browse/cls_browsing_book.php?s_doctype={doc_type}&cls={class_type}"
        self.PAGE_NUM = "&page={page_num}"
        # 问号以前的url
        self.FRONT_URL = "http://libweb.njau.edu.cn"
        # 请求头构造
        self.user_agent = [
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
        ]
        self.headers = {"Host": "tieba.baidu.com",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Upgrade-Insecure-Requests": "1",
                        "Connection": "keep-alive"
                        }

        self.bookinfo_crawel=bookinfo()

    def start(self,class_id="",doc_type="all",start_num=1):
        # 起始url
        url = self.BASE_URL.format(class_type=urllib.quote(class_id), doc_type=urllib.quote(doc_type))
        if(start_num!=1):
            url = url + self.PAGE_NUM.format(page_num=start_num)
        # 查找所有url
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        content_generator = self.get_resultinfo(soup_string)
        for content in content_generator:
            yield content
        max_value = self.get_maxindex(soup_string)
        print("**********  '" + class_id + "'类别书籍的第"+str(start_num)+"页执行完毕**********")
        for num in range(start_num+1,max_value+1):
            next_url = url + self.PAGE_NUM.format(page_num=num)
            self.headers["User-Agent"] = random.choice(self.user_agent)
            res = requests.get(next_url, headers=self.headers)
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            content_generator = self.get_resultinfo(soup_string)
            for content in content_generator:
                yield content
            print("**********  '" + class_id + "'类别书籍的第" + str(num) + "页执行完毕**********")

    def get_resultinfo(self, soup_string):
        div_list = soup_string.select("div[class=list_books]")
        for div in div_list:
            other_url=div.select("a")[0].get("href")
            other_info=self.bookinfo_crawel.get_maininfo(other_url)
            book_title=div.select("a")[0].get_text()
            yield "\t".join([book_title,other_info])

    def get_maxindex(self,soup_string):
        value_list=soup_string.select("option")
        max_value=max([int(vo.get("value")) for vo in value_list])
        return max_value

if __name__=="__main__":
    bi=searchinfo()

    tl=bi.start(class_id="TP3")
    for t in tl:
        print(t)