#encoding=utf-8

import sys
import requests
import urllib
import urllib2
import time
import random
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )

class BDTieba_tie:
    # 初始化
    def __init__(self):
        # 问号以前的url
        self.FRONT_URL = "http://tieba.baidu.com"
        #请求头构造
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

    # 开始入口
    def start(self, tie_url):
        # 起始url
        url = tie_url
        # 查找所有url
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(url,headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        content_generator = self.get_tietext(soup_string)
        for content in content_generator:
            yield content
        next_url = self.get_nexturl(soup_string.find_all("li" ,{"class":"l_pager pager_theme_5 pb_list_pager"}))
        num = 1
        print("**********帖子的第" + str(num) + "页执行完毕**********")
        while(next_url):
            time.sleep(60 + random.randint(0, 60))
            self.headers["User-Agent"]=random.choice(self.user_agent)
            res = requests.get(next_url,headers=self.headers)
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            content_generator = self.get_tietext(soup_string)
            for content in content_generator:
                yield content
            num += 1
            print("**********帖子第" + str(num) + "页执行完毕**********")
            next_url = self.get_nexturl(soup_string.find_all("li" ,{"class":"l_pager pager_theme_5 pb_list_pager"}))


    # 获取页面帖子url
    def get_tietext(self, soup_string):
        div_list = soup_string.find_all("div" ,{"class":"l_post l_post_bright j_l_post clearfix  "})
        for div in div_list:
            t_name=self.get_empty(div.select("li[class=d_name]"))
            content=self.get_empty(div.find_all("div",{"class":"d_post_content j_d_post_content  "}))
            time_string=self.get_empty(div.select("span[class=tail-info]"),-1)
            yield "\t".join([t_name,time_string,content])

    def get_empty(self,list,index=0):
        if(len(list)==0):
            return ""
        else:
            return list[index].get_text()


    def get_nexturl(self,page_string):
        a_list=page_string[0].select("a")
        last_a=a_list[-1]
        last_string=last_a.get_text()
        if(last_string=="尾页"):
            next_a=a_list[-2]
            next_url=self.FRONT_URL+next_a.get("href").replace("amp;","")
            return next_url
        else:
            return ""

if __name__=="__main__":
    bd_spider=BDTieba_tie()
    content_generator=bd_spider.start("https://tieba.baidu.com/p/4142238698")
    for content in content_generator:
        print(content)