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

filename_re=re.compile(r"filename=\"(.*?)\"")

class base_AAAI():
    def __init__(self,outpath=u"F:/会议论文下载/AAAI/"):
        # 基础的url
        self.FRONT_URL = "https://aaai.org/Library/AAAI/"
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
                        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                        "referer":"https://aaai.org/Library/conferences-library.php",
                        "Host":"www.aaai.org"
                        }

        #self.headers["cookie"]=cookies
        self.id_list=[ pdfid.replace(".pdf","").split("-")[0] for pdfid in os.listdir(outpath)]
        self.outpath=outpath
        print(self.id_list)

    def crawl(self,year_list=["aaai19contents.php"]):
        for year in year_list:
            self.headers["User-Agent"] = random.choice(self.user_agent)
            url=self.FRONT_URL+year
            res = None
            while (not res):
                try:
                    res = requests.get(url, headers=self.headers)
                    print(u"主页面获取成功......")
                except requests.exceptions.SSLError:
                    print(u"主页面获取失败......")
                    time.sleep(300)
                    print(u"主页面重新获取......")
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            pdfurllist = self.get_pdfurl(soup_string)
            for pdfurl in pdfurllist:
                print(pdfurl + "开始下载....")
                downflag = self.download_pdf(pdfurl,url)
                print(pdfurl + "处理完毕....")
                if (downflag):
                    print(pdfurl + u"的pdf已经下载完毕")
                    time.sleep(random.randint(5, 15))
            print(str(year) + u"的页面内容已经下载完毕........")

    def download_pdf(self,pdf_url,pre_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        self.headers["refer"]=pre_url
        fileid=pdf_url.split("/")[-2]
        if (fileid in self.id_list):
            downflag = False
        else:
            readflag = False
            while (not readflag):
                try:
                    res_pdf = requests.get(pdf_url, headers=self.headers, timeout=(5, 25))
                    readflag = True
                    filename=self.outpath+filename_re.findall(res_pdf.headers["Content-Disposition"])[0]
                    with open(filename, "wb") as w:
                        w.write(res_pdf.content)
                except requests.exceptions.RequestException:
                    print(pdf_url + u"出现超时....")
                    time.sleep(random.randint(120, 240))
                    print(pdf_url + u"重新下载....")
            downflag = True
        return downflag

    def get_pdfurl(self,maindiv):
        pdf_plist=maindiv.find_all("p",attrs={"class" :"left"})
        for a_wrap in pdf_plist:
            pdfa_list=a_wrap.select("a")
            for pdfa in pdfa_list:
                if("pdf" in pdfa.get_text().lower()):
                    yield pdfa.get("href")


class base_old_AAAI():
    def __init__(self,outpath=u"F:/会议论文下载/AAAI/"):
        # 基础的url
        self.FRONT_URL = "https://aaai.org/Library/AAAI/"
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
                        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                        "referer":"https://aaai.org/Library/conferences-library.php",
                        "Host":"www.aaai.org"
                        }

        #self.headers["cookie"]=cookies
        self.id_list=[ pdfid.replace(".pdf","").split("-")[0] for pdfid in os.listdir(outpath)]
        self.outpath=outpath
        print(self.id_list)

    def crawl(self,year_list=["aaai18contents.php","aaai17contents.php","aaai16contents.php","aaai15contents.php"]):
        for year in year_list:
            self.headers["User-Agent"] = random.choice(self.user_agent)
            self.headers["refer"] = "https://aaai.org/Library/conferences-library.php"
            url=self.FRONT_URL+year
            res = None
            while (not res):
                try:
                    res = requests.get(url, headers=self.headers)
                    print(u"主页面获取成功......")
                except requests.exceptions.SSLError:
                    print(u"主页面获取失败......")
                    time.sleep(300)
                    print(u"主页面重新获取......")
                except requests.exceptions.ConnectionError:
                    print(pdf_main_url+u" pdf页面获取失败......")
                    time.sleep(300)
                    print(pdf_main_url+u" pdf页面重新获取......")
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            pdfurllist = self.get_pdfurl(soup_string)
            for pdfurl in pdfurllist:
                print(pdfurl + u"开始下载....")
                downflag = self.download_pdf(pdfurl,url)
                print(pdfurl + u"处理完毕....")
                if (downflag):
                    print(pdfurl + u"的pdf已经下载完毕 "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                    time.sleep(random.randint(5, 15))
            print(str(year) + u"的页面内容已经下载完毕........")
            time.sleep(15)

    def download_pdf(self,pdf_url_wrap,pre_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        self.headers["refer"] = pre_url
        fileid=pdf_url_wrap.split("/")[-1]
        if (fileid in self.id_list):
            downflag = False
        else:
            time.sleep(10)
            res = None
            pdf_main_url=pdf_url_wrap.replace("view","viewPaper").replace("http://","https://")
            while (not res):
                try:
                    res = requests.get(pdf_main_url, headers=self.headers)
                    print(pdf_main_url+u" pdf页面获取成功......")
                except requests.exceptions.SSLError:
                    print(pdf_main_url+u" pdf页面获取失败......")
                    time.sleep(300)
                    print(pdf_main_url+u" pdf页面重新获取......")
                except requests.exceptions.ConnectionError:
                    print(pdf_main_url+u" pdf页面获取失败......")
                    time.sleep(300)
                    print(pdf_main_url+u" pdf页面重新获取......")
            soup_string=BeautifulSoup(res.text, "html.parser")
            pdf_url=soup_string.select("a[class=action]")[0].get("href").replace("view","viewFile")
            print(pdf_url+u"文件地址获取成功！")
            time.sleep(random.randint(0,10))
            readflag = False
            while (not readflag):
                try:
                    res_pdf = requests.get(pdf_url, headers=self.headers, timeout=(5, 25))
                    readflag = True
                    filename=self.outpath+filename_re.findall(res_pdf.headers["Content-Disposition"])[0]
                    with open(filename, "wb") as w:
                        w.write(res_pdf.content)
                except requests.exceptions.RequestException:
                    print(pdf_url + u"出现超时....")
                    time.sleep(random.randint(120, 240))
                    print(pdf_url + u"重新下载....")
            downflag = True
        return downflag

    def get_pdfurl(self,maindiv):
        pdf_plist=maindiv.find_all("p",attrs={"class" :"left"})
        for a_wrap in pdf_plist:
            pdfa_list=a_wrap.select("a")
            if(pdfa_list):
                yield pdfa_list[0].get("href")


if __name__=="__main__":
    emnlp_ba=base_old_AAAI(outpath=u"F:/会议论文下载/AAAI/")
    emnlp_ba.crawl(year_list=["aaai17contents.php","aaai16contents.php","aaai15contents.php"])

