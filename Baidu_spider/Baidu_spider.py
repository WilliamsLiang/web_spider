#encoding=utf-8

import sys
import re
import requests
import urllib
import urllib2
import time
import random
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )

del_param=re.compile(r"\?.*")

class BDTieba_search:

    # 初始化
    def __init__(self):

        # 基础的url
        self.BASE_URL = "http://tieba.baidu.com/f/search/res?ie=utf-8&kw={tieba}&qw={search}"
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
    def start(self, tb_name="",keyword="",get_type="all"):
        # 起始url
        url = self.BASE_URL.format(tieba=urllib.quote(tb_name),search=urllib.quote(keyword))
        # 查找所有url
        self.headers["refer"] = url
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(url,headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        content_generator = self.switch_get(soup_string,get_type)
        for content in content_generator:
            yield content
        next_page = soup_string.select("a[class=next]")
        num=1
        print("**********" + tb_name + "吧的'" + keyword + "'关键词的第"+str(num)+"页执行完毕**********")
        while(next_page):
            time.sleep(60+random.randint(0,60))
            next_url=self.FRONT_URL+next_page[0].get("href").replace("amp;","")
            self.headers["User-Agent"]=random.choice(self.user_agent)
            res = requests.get(next_url,headers=self.headers)
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            content_generator = self.switch_get(soup_string,get_type)
            for content in content_generator:
                yield content
            num += 1
            print("**********" + tb_name + "吧的'" + keyword + "'关键词的第" + str(num) + "页执行完毕**********")
            next_page = soup_string.select("a[class=next]")
            break

    #选择获取的类型
    def switch_get(self,soup_string,get_type="all"):
        '''
        :param get_type:all url和文本内容, url 只获取帖子链接 , text 帖子摘要
        '''
        if(get_type=="text"):
            return self.get_url_text(soup_string)
        elif(get_type=="url"):
            return self.get_posturl(soup_string)
        elif(get_type=="all"):
            return self.get_all(soup_string)
        else:
            return None

    def get_all(self,soup_string):
        div_list = soup_string.select("div[class=s_post]")
        for div in div_list:
            tie_url = del_param.sub("",self.FRONT_URL+div.select("a[class=bluelink]")[0].get("href"))
            p_title=div.select("span[class=p_title]")[0].get_text()
            p_content=div.select("div[class=p_content]")[0].get_text()
            a_forum=div.select("a[class=p_forum]")[0].get_text()
            user_name=div.select("a")[-1].get_text()
            time_string=div.find_all("font",{"class":"p_green p_date"})[0].get_text()
            yield "\t".join([p_title,p_content,a_forum,user_name,time_string,tie_url])

    # 得到页面的html代码
    def get_url_text(self, soup_string):
        div_list = soup_string.select("div[class=s_post]")
        for div in div_list:
            p_title=div.select("span[class=p_title]")[0].get_text()
            p_content=div.select("div[class=p_content]")[0].get_text()
            a_forum=div.select("a[class=p_forum]")[0].get_text()
            user_name = div.select("a")[-1].get_text()
            time_string = div.find_all("font", {"class": "p_green p_date"})[0].get_text()
            yield "\t".join([p_title,p_content,user_name,time_string,a_forum])

    # 获取页面帖子url
    def get_posturl(self, soup_string):
        div_list = soup_string.select("div[class=s_post]")
        for div in div_list:
            tie_url = del_param.sub("",self.FRONT_URL+div.select("a[class=bluelink]")[0].get("href"))
            yield tie_url


if __name__=="__main__":
    bd_spider=BDTieba_search()
    content_generator=bd_spider.start(tb_name="穿山甲",keyword="穿山甲")
    w=open("test.txt","wt")
    for content in content_generator:
        w.write(content+"\n")
        w.flush()
    w.close()