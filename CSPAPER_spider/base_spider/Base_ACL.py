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


class base_ACL():
    def __init__(self,outpath=u"F:/会议论文下载/ACL/"):
        # 基础的url
        self.FRONT_URL = "https://www.aclweb.org/anthology/events/"
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
                        "Connection": "close",
                        "Content-Type": "text / html;charset = UTF - 8",
                        "accept-language":"zh-CN,zh;q=0.9",
                        "cache-control":"max-age=0",
                        "upgrade-insecure-requests":"1"
                        }

        #self.headers["cookie"]=cookies
        self.id_list=[ pdfid.replace(".pdf","") for pdfid in os.listdir(outpath)]
        self.outpath=outpath
        print(self.id_list)

    def crawl(self,c_name,year_list=[2019,2018,2017,2016,2015]):
        for year in year_list:
            self.headers["User-Agent"] = random.choice(self.user_agent)
            url=self.FRONT_URL+c_name+"-"+str(year)
            self.headers["referer"] = url
            res=None
            while(not res):
                try:
                    res = requests.get(url, headers=self.headers)
                    print("主页面获取成功......")
                except requests.exceptions.SSLError:
                    print("主页面获取失败......")
                    time.sleep(300)
                    print("主页面重新获取......")
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            pdfurllist = self.get_pdfurl(soup_string)
            for pdfurl in pdfurllist:
                print(pdfurl + "开始下载....")
                downflag = self.download_pdf(pdfurl)
                print(pdfurl + "处理完毕....")
                if (downflag):
                    print(pdfurl + "的pdf已经下载完毕")
                    time.sleep(random.randint(10,20))
            print(str(year) + "年的"+c_name+"页面内容已经下载完毕........")

    def download_pdf(self,pdf_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        fileid=pdf_url.split("/")[-1].replace(".pdf","")
        if (fileid in self.id_list):
            downflag = False
        else:
            filename = self.outpath + fileid + ".pdf"
            readflag=False
            while(not readflag):
                try:
                    res_pdf = requests.get(pdf_url, headers=self.headers,timeout=(5,25))
                    readflag=True
                    with open(filename, "wb") as w:
                        w.write(res_pdf.content)
                except requests.exceptions.RequestException:
                    print(pdf_url + "出现超时....")
                    time.sleep(random.randint(120,240))
                    print(pdf_url + "重新下载....")
            downflag = True
        return downflag

    def get_pdfurl(self,maindiv):
        pdf_plist=maindiv.find_all("p",attrs={"class" :"d-sm-flex align-items-stretch"})
        for a_wrap in pdf_plist:
            pdfa_list=a_wrap.find_all("a",attrs={"title" :"Open PDF"})
            if(not pdfa_list):
                continue
            pdfa=pdfa_list[0]
            yield pdfa.get("href")

if __name__=="__main__":
    #ba = base_ACL(outpath=u"F:/会议论文下载/ACL/")
    #ba.crawl("acl", year_list=[2019, 2018, 2017, 2016, 2015])
    # ba.crawl("acl", year_list=[2019])
    emnlp_ba=base_ACL(outpath=u"F:/会议论文下载/EMNLP/")
    emnlp_ba.crawl("emnlp",year_list=[2019,2018,2017,2016,2015])
    #emnlp_ba.crawl("emnlp", year_list=[2019])

