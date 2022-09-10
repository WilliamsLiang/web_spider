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

class base_qimizi():
    def __init__(self,outpath=u"C:/Users/sfe_williamsL/Desktop/tmp_qimizi.txt"):
        # 基础的url
        self.BASE_URL = "http://www.wxsy.net"
        self.FRONT_URL="http://www.wxsy.net/novel/"
        """
        参数类型：
        user_id:URL中的ID
        hrml_title:请求地址TITLE
        client_id:第一次请求的ID
        """
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
                        "Host":"www.wxsy.net",
                        }
        self.outpath=outpath

    def crawl(self,main_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        url=self.FRONT_URL+main_url
        print(url)
        res = None
        while (not res):
            try:
                res = requests.get(url, headers=self.headers,timeout=5)
                print("主页面获取成功......")
            except requests.exceptions.SSLError:
                print("主页面获取失败......")
                time.sleep(300)
                print("主页面重新获取......")
            except requests.exceptions.RequestException:
                print("主页面获取超时......")
                time.sleep(300)
                print("主页面重新获取......")
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        div_list=soup_string.select("div[class='pt-chapter-cont-detail full']")[0]
        a_list=[self.BASE_URL+a.get("href") for a in div_list.select("a")]
        w=open(self.outpath,"wt")
        for url in a_list:
            content=self.get_content(url)
            w.write(content+"\n\n\n")
            time.sleep(random.randint(0,10))
            w.flush()
        w.close()

    def get_content(self,pdf_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        print(pdf_url)
        res = None
        while (not res):
            try:
                res = requests.get(pdf_url, headers=self.headers, timeout=5)
                print("内容页面获取成功......")
            except requests.exceptions.SSLError:
                print("内容页面获取失败......")
                time.sleep(300)
                print("内容页面重新获取......")
            except requests.exceptions.RequestException:
                print("内容页面获取超时......")
                time.sleep(300)
                print("内容页面重新获取......")
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        main_div=soup_string.select("div[class='size16 color5 pt-read-text']")[0]
        print(pdf_url + "的页面内容已经下载完毕........")
        content_text="\n".join([p.get_text() for p in main_div.select("p")])
        return content_text


if __name__=="__main__":
    #cookie="_ga=GA1.2.424395814.1574509679; _gid=GA1.2.1136203319.1574509679; OptanonAlertBoxClosed=2019-11-23T11:48:18.772Z; trackid=26dcdba14e02435285e27a19a; event-tracker=d6660756-baca-4e3c-a419-2c37044ffddd; event-tracker-session=c04dff58-61ab-4b2b-8ba4-c894a77aeb92; OptanonConsent=landingPath=NotLandingPage&datestamp=Sat+Nov+23+2019+19%3A57%3A52+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=3.6.19&groups=1%3A1%2C0_110775%3A1%2C2%3A1%2C0_110776%3A1%2C3%3A1%2C0_110777%3A1%2C4%3A1%2C0_110774%3A1%2C0_112699%3A1%2C0_132599%3A1%2C0_132598%3A1%2C0_132601%3A1%2C0_132600%3A1%2C0_132603%3A1%2C0_132602%3A1%2C0_118607%3A1&AwaitingReconsent=false; __gads=ID=1f8f9584ea8398a2:T=1574510273:S=ALNI_MbyoyLbxINaQfUTw6AZAxA9vCRYMg; sim-inst-token=1:3991465546-3000162591-3000803042-3002351942-3000202650-3001312038-3991438083-3000115770-3000203264-3000882202-3001144869:1574540334245:af526ad7"
    emnlp_ba=base_qimizi(outpath=u"C:/Users/sfe_williamsL/Desktop/tmp_qimizi.txt")
    emnlp_ba.crawl("4676/")

