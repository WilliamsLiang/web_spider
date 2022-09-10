#encoding=utf-8
import sys
import re
import requests
import time
import random
import os
from bs4 import BeautifulSoup

class base_ACL():
    def __init__(self,outpath=u"F:/会议论文下载/ACL/"):
        # 基础的url
        self.BASE_URL = "https://aclanthology.org/"
        self.FRONT_URL = "https://aclanthology.org/events/"
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
        self.id_list=[ pdfid.replace(".bib",".txt") for pdfid in os.listdir(outpath)]
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
            for url_list in pdfurllist:
                bib_url,pdf_url,video_url,ppt_url = url_list
                print(bib_url + "开始下载....")
                downflag = self.download_pdf(bib_url,pdf_url,video_url,ppt_url)
                print(bib_url + "处理完毕....")
                if (downflag):
                    print(bib_url + "的pdf已经下载完毕")
                    time.sleep(random.randint(2,8))
            print(str(year) + "年的"+c_name+"页面内容已经下载完毕........")

    def get_list(self,re_list):
        if(not re_list):
            return ""
        else:
            return re_list[0]

    def get_bibtext(self,bibtext):
        title_re = re.compile('[\s]title = "([\s\S]*?)"')
        author_re = re.compile('[\s]author = "([\s\S]*?)"')
        abstract_re = re.compile('[\s]abstract = "([\s\S]*?)"')
        title = self.get_list(title_re.findall(bibtext))
        author = self.get_list(author_re.findall(bibtext)).replace("and","|").replace("\r","").replace("\n","")
        absract = self.get_list(abstract_re.findall(bibtext))
        return title,author,absract
        

    def download_bib(self,bib_url):
        file_name = bib_url.replace(".bib",".txt")
        bib_url = self.BASE_URL + bib_url
        readflag=False
        while(not readflag):
            try:
                res_pdf = requests.get(bib_url, headers=self.headers,timeout=(5,25))
                readflag=True
                title,author,absract = self.get_bibtext(res_pdf.text)
                with open(self.outpath+file_name, "wt",encoding="utf-8") as w:
                    w.write("\n".join([title,author,absract]))
            except requests.exceptions.RequestException:
                print(bib_url + "出现超时....")
                time.sleep(random.randint(20,60))
                print(bib_url + "重新下载....")

    def download_pdf(self,bib_url,pdf_url,video_url,ppt_url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        pdf_file = pdf_url.split("/")[-1]
        video_file = video_url.split("/")[-1]
        ppt_file = ppt_url.split("/")[-1]
        bib_file = bib_url.split("/")[-1]
        file_list = [_ for _ in [video_file,ppt_file] if("." in _)]
        zip_list = [[m,n] for m,n in zip([pdf_file,video_file,ppt_file],[pdf_url,video_url,ppt_url]) if("." in m)]
        tmp_flag = True
        for f in file_list:
            if(f not in self.id_list):
                tmp_flag = False
        if ((bib_file.replace(".bib",".txt") in self.id_list) and tmp_flag):
            downflag = False
        else:
            if(bib_file.replace(".bib",".txt") not in self.id_list):
                self.download_bib(bib_url)
            if(not tmp_flag):
                for fname,furl in zip_list:
                    readflag=False
                    while(not readflag):
                        try:
                            res_pdf = requests.get(furl, headers=self.headers,timeout=(5,25))
                            readflag=True
                            with open(self.outpath+fname, "wb") as w:
                                w.write(res_pdf.content)
                        except requests.exceptions.RequestException:
                            print(furl + "出现超时....")
                            time.sleep(random.randint(20,60))
                            print(furl + "重新下载....")
            downflag = True
        return downflag

    def get_url(self,aurl_list):
        if(not aurl_list):
            return ""
        else:
            a = aurl_list[0]
            return a.get("href")
        

    def get_pdfurl(self,maindiv):
        pdf_plist = maindiv.find_all("p",attrs={"class" :"d-sm-flex align-items-stretch"})
        for a_wrap in pdf_plist:
            pdfa_url = self.get_url(a_wrap.find_all("a",attrs={"title" :"Open PDF"}))
            videoa_url = self.get_url(a_wrap.find_all("a",attrs={"title" :"Video"}))
            ppt_url = self.get_url(a_wrap.find_all("a",attrs = {"title" :"Presentation"}))
            bib_url = self.get_url(a_wrap.find_all("a",attrs = {"title" :"Export to BibTeX"}))
            if(not bib_url):
                continue
            yield bib_url,pdfa_url,videoa_url,ppt_url

if __name__=="__main__":
    #ba = base_ACL(outpath=u"F:/会议论文下载/ACL/")
    #ba.crawl("acl", year_list=[2019, 2018, 2017, 2016, 2015])
    # ba.crawl("acl", year_list=[2019])
    emnlp_ba=base_ACL(outpath=u"G:/acl/")
    emnlp_ba.crawl("acl",year_list=[2021,2020,2019,2018,2017,2016])
    #emnlp_ba.crawl("emnlp", year_list=[2019])

