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

getid=re.compile(r"citation.cfm\?id=(\d+)?&")
getclientid=re.compile(r"_cf_clientid=\'([A-Za-z0-9]*?)\';")
pdftitle=re.compile(r"ftid=(\d+?)&")

class sigir_download():
    def __init__(self,cookies,outpath="C:/Users/sfe_williamsL/Desktop/ACM_sigir/"):
        # 基础的url
        self.FRONT_URL = "https://dl.acm.org"
        """
        参数类型：
        user_id:URL中的ID
        hrml_title:请求地址TITLE
        client_id:第一次请求的ID
        """
        self.AJAX_GETURL="https://dl.acm.org/tab_about.cfm?id={user_id}&type=proceeding&sellOnline=0&parent_id={user_id}&parent_type=proceeding&toctitle=&tocissue_date=&notoc=0&usebody=tabbody&tocnext_id=&tocnext_str=&tocprev_id=&tocprev_str=&toctype=&_cf_containerId=cf_layoutareaprox&_cf_nodebug=true&_cf_nocache=true&_cf_clientid={client_id}&_cf_rc=1"
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
                        "Content-Type": "text / html;charset = UTF - 8"
                        }

        self.headers["cookie"]=cookies
        self.id_list=[ pdfid.replace(".pdf","") for pdfid in os.listdir(outpath)]
        self.downflag=False
        print(self.id_list)

    def crawl(self,url,pre_num=5):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        originid=getid.search(url).group(1)
        idnum=int(originid)
        #第一次请求获取clientid
        res = requests.get(url, headers=self.headers)
        html_text = res.text
        client_id=getclientid.search(html_text).group(1)
        #第二次请求获取PDF列表
        ajax_url=self.AJAX_GETURL.format(user_id=originid,client_id=client_id)
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(ajax_url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        pre_url=self.is_precontent(soup_string,idnum)
        pdfurllist=self.get_pdfurl(soup_string)
        for pdfurl in pdfurllist:
            self.download_pdf(pdfurl)
            if(self.downflag):
                print(pdfurl + "的pdf已经下载完毕")
                time.sleep(random.randint(0,10))
        print(str(pre_num-pre_num+1)+"个页面内容已经下载完毕........")
        new_num=pre_num-1
        while(new_num!=0 and pre_url!=""):
            self.headers["User-Agent"] = random.choice(self.user_agent)
            originid = getid.search(pre_url).group(1)
            idnum = int(originid)
            # 第一次请求获取clientid
            res = requests.get(pre_url, headers=self.headers)
            html_text = res.text
            client_id = getclientid.search(html_text).group(1)
            # 第二次请求获取PDF列表
            ajax_url = self.AJAX_GETURL.format(user_id=originid, client_id=client_id)
            self.headers["User-Agent"] = random.choice(self.user_agent)
            res = requests.get(ajax_url, headers=self.headers)
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            pre_url = self.is_precontent(soup_string, idnum)
            pdfurllist = self.get_pdfurl(soup_string)
            for pdfurl in pdfurllist:
                self.download_pdf(pdfurl)
                if (self.downflag):
                    print(pdfurl + "的pdf已经下载完毕")
                    time.sleep(random.randint(0,10))
            print(str(pre_num-new_num+1)+"个页面内容已经下载完毕........")
            new_num = new_num - 1

    def download_pdf(self,pdf_url,outpath="C:/Users/sfe_williamsL/Desktop/ACM_sigir/"):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        fileid=pdftitle.search(pdf_url).group(1)
        if(fileid in self.id_list):
            self.downflag=False
        else:
            filename=outpath+fileid+".pdf"
            res_pdf = requests.get(pdf_url, headers=self.headers)
            with open(filename, "wb") as w:
                w.write(res_pdf.content)
            self.downflag=True

    def is_precontent(self,maindiv,originid):
        pre_a=maindiv.select("div[class=small-text]")[0].select("a")[0]
        pre_url=self.FRONT_URL+"/"+pre_a.get("href")
        newid = getid.search(pre_url)
        idnum = int(newid.group(1))
        if(idnum<originid):
            return pre_url
        else:
            return ""

    def get_pdfurl(self,maindiv):
        pdf_alist=maindiv.select("a[name=FullTextPDF]")
        for pdfa in pdf_alist:
            yield self.FRONT_URL+"/"+pdfa.get("href")