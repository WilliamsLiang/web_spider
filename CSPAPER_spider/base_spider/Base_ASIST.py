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

apdfre=re.compile(r'<a href="[/\.0-9A-Za-z]*?">.*?</a>')

class base_ASIST():
    def __init__(self,cookies,outpath=u"F:/会议论文下载/ASIST/"):
        # 基础的url
        self.BASE_URL = "https://asistdl.onlinelibrary.wiley.com"
        #self.FRONT_URL = "http://onlinelibrary.wiley.com/doi/10.1002/pra2.2017.54.issue-1/issuetoc/"
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
                        "refer": "https://asistdl.onlinelibrary.wiley.com/toc/23739231/2018/55/1",
                        }

        self.headers["cookie"]=cookies
        self.id_list=[ pdfid.replace(".pdf","") for pdfid in os.listdir(outpath)]
        self.outpath=outpath
        print(self.id_list)

    def crawl(self,tmp_url,page_num=5):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        self.headers["refer"]=self.BASE_URL
        url = tmp_url
        print(url)
        res = None
        while (not res):
            try:
                res = requests.get(url, headers=self.headers, timeout=5)
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
        pdfurllist = self.get_pdfurl(soup_string, pre_url=url)
        for pdfurl in pdfurllist:
            print(pdfurl + "开始下载....")
            downflag = self.download_pdf(pdfurl,header_url=url)
            print(pdfurl + "处理完毕....")
            if (downflag):
                print(pdfurl + "的pdf已经下载完毕")
                time.sleep(random.randint(0, 10))
        print(url+ "的页面内容已经下载完毕........")
        next_url=self.get_next(soup_string,pre_url=url)
        print(next_url)
        i=0
        while(next_url and i<page_num):
            self.headers["User-Agent"] = random.choice(self.user_agent)
            self.headers["refer"] = self.BASE_URL
            url=next_url
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
            pdfurllist = self.get_pdfurl(soup_string,pre_url=url)
            for pdfurl in pdfurllist:
                print(pdfurl + "开始下载....")
                downflag = self.download_pdf(pdfurl,header_url=url)
                print(pdfurl + "处理完毕....")
                if (downflag):
                    print(pdfurl + "的pdf已经下载完毕")
                    time.sleep(random.randint(5,20))
            print(url + "的页面内容已经下载完毕........")
            next_url = self.get_next(soup_string, pre_url=url)
            i=i+1

    def download_pdf(self,pdf_url,header_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        self.headers["refer"]=pdf_url
        fileid="_".join(header_url.split("/")[-3:])+"_"+"_".join(pdf_url.split("/")[-3:]).replace(".","_").replace(".pdf","")
        pdf_url=pdf_url.replace("/doi/pdf","/doi/pdfdirect")
        if (fileid in self.id_list):
            downflag = False
        else:
            filename = self.outpath + fileid + ".pdf"
            readflag = False
            while (not readflag):
                try:
                    res_pdf = requests.get(pdf_url, headers=self.headers, timeout=(5, 25))
                    readflag = True
                    with open(filename, "wb") as w:
                        w.write(res_pdf.content)
                except requests.exceptions.RequestException:
                    print(pdf_url + "出现超时....")
                    time.sleep(random.randint(120, 240))
                    print(pdf_url + "重新下载....")
            downflag = True
        return downflag

    def get_next(self,soup_string,pre_url=""):
        previous_a=soup_string.select("a[title=Previous]")
        if(previous_a):
            return self.abs_path(previous_a[0].get("href"),pre_url=pre_url)
        else:
            return ""


    def get_pdfurl(self,maindiv,pre_url):
        content_div=maindiv.select("li[class='pdfLink--is-hidden']")
        for content in content_div:
            pdf_alist=content.select("a[title=PDF]")
            for a_soup in pdf_alist:
                yield self.abs_path(a_soup.get("href"),pre_url=pre_url)

    def abs_path(self,rel_url,pre_url=""):
        if(rel_url[0]=="/"):
            return self.BASE_URL+rel_url
        else:
            return pre_url+rel_url

if __name__=="__main__":
    cookie="__cfduid=d8230fd694da6ce5604ac6b0bc5d282a01574493284; SERVER=WZ6myaEXBLFJd7wENI2/+w==; MAID=GogZCrXdu4mnukUS8dQ6rw==; MACHINE_LAST_SEEN=2019-11-22T23%3A15%3A06.270-08%3A00; JSESSIONID=aaaE4X1V4Tdo55446Ad6w; AMCVS_1B6E34B85282A0AC0A490D44%40AdobeOrg=1; AMCV_1B6E34B85282A0AC0A490D44%40AdobeOrg=-1303530583%7CMCIDTS%7C18224%7CMCMID%7C32971698728924915282498990500334240805%7CMCAAMLH-1575098107%7C11%7CMCAAMB-1575098107%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1574500507s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; __gads=ID=59b9b4868a906f33:T=1574493312:S=ALNI_MbTTsLFc588YatFNKtfhamz0opSEg; _sdsat_MCID=32971698728924915282498990500334240805; randomizeUser=0.9720261290876129; _ga=GA1.2.1139542954.1574493308; _gid=GA1.2.1452578297.1574493310; s_cc=true; s_sq=%5B%5BB%5D%5D; QSI_HistorySession=https%3A%2F%2Fasistdl.onlinelibrary.wiley.com%2Ftoc%2F23739231%2F2019%2F56%2F1~1574493326800%7Chttps%3A%2F%2Fasistdl.onlinelibrary.wiley.com%2Ftoc%2F23739231%2F2018%2F55%2F1~1574495254451%7Chttps%3A%2F%2Fasistdl.onlinelibrary.wiley.com%2Ftoc%2F23739231%2F2019%2F56%2F1~1574495524966; _gat_wolga=1"
    emnlp_ba=base_ASIST(cookies=cookie,outpath=u"H:/会议下载/ASIST_spider/")
    emnlp_ba.crawl("https://asistdl.onlinelibrary.wiley.com/toc/23739231/2019/56/1",page_num=5)

