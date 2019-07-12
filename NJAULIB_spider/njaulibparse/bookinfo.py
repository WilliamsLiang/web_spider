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

class bookinfo():
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
        self.headers = {"Host": "libweb.njau.edu.cn",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Connection": "keep-alive",
                        "Content-Type": "text / html;charset = UTF - 8"
                        }
        self.keyinfo=[u"个人责任者",u"团体责任者",u"丛编项",u"学科主题",u"中图法分类号",u"提要文摘附注"]

    def get_maininfo(self,href_url):
        info_dict = {
            u"个人责任者":"",
            u"团体责任者":"",
            u"丛编项":"",
            u"学科主题": "",
            u"提要文摘附注": "",
            u"中图法分类号": ""
        }
        tie_url = self.FRONT_URL + href_url.replace("../", "/")
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(tie_url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        infodiv = soup_string.select("div[id=item_detail]")[0]
        dl_list=infodiv.select("dl[class=booklist]")
        for dl in dl_list:
            key=dl.select("dt")[0].get_text().replace(":","")
            if(key == u"个人责任者" or key == u"团体责任者"):
                info="".join([ ainfo.get_text() for ainfo in dl.select("dd")[0].select("a")])
                #info=dl.select("dd")[0].select("a")[0].get_text()
            else:
                info = dl.select("dd")[0].get_text()
            if(key in self.keyinfo):
                if(not info_dict.get(key,"")):
                    info_dict[key]=info
                else:
                    info_dict[key]=info_dict[key]+"||"+info
        return tie_url+"\t"+"\t".join([info_dict[key] for key in self.keyinfo])

    def htmlunicode2str(self,unicodestr):
        secondcode=unicodestr[3:5]
        firstcode=unicodestr[5:7]
        code_str="\\x"+firstcode+b"\\x"+secondcode
        return code_str.decode("unicode_internal","ignore")

    def conver_str(self,string):
        html_flag=False
        htmlcode=""
        re_str=""
        for s in string:
            if(s=="&"):
                html_flag=True
                htmlcode=htmlcode+s
            elif(html_flag and s==";"):
                html_flag = False
                htmlcode = htmlcode + s
                re_str=re_str+self.htmlunicode2str(htmlcode)
            elif(html_flag):
                htmlcode=htmlcode+s
            else:
                re_str=re_str+s
        return re_str

if __name__=="__main__":
    bi=bookinfo()
    tl=bi.get_mianinfo("/opac/item.php?marc_no=7a3651533350356672343351353030652f45456941513d3d")
