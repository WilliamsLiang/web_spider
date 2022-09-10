#encoding=utf-8

import sys
import requests
import random
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Base_RANK():
    def __init__(self):
        # 基础的url
        self.FRONT_URL = "http://www.qianmu.org"
        self.user_agent = [
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
        ]
        self.headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Connection": "keep-alive",
                        "Host":"www.qianmu.org",
                        "Upgrade-Insecure-Requests":"1",
                        "Accept-Language":"zh-CN,zh;q=0.9",
                        "Cache-Control":"max-age=0",
                        }

    def crawl(self,url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(url, headers=self.headers)
        html_text = res.text
        data_josn=self.parse_html(html_text)
        return data_josn

    def parse_html(self,html_text):
        data_json={"HeardTitle":"","RowData":[]}
        soup_string = BeautifulSoup(html_text, "html.parser")
        div_list = soup_string.select("div[class=rankItem]")
        h2_tag=None
        table_tag=None
        for div in div_list:
            tmp_h2=div.select("h2")
            tmp_table=div.select("table")
            if(tmp_h2):
                h2_tag=tmp_h2[0]
            if(tmp_table):
                table_tag=tmp_table[0]
        data_json["HeardTitle"]=self.parse_h2(h2_tag)
        data_json["RowData"]=self.parse_table(table_tag)
        return data_json

    def parse_h2(self,h2_tag):
        """
        获取表格标题
        """
        return h2_tag.get_text()

    def parse_table(self,table_tag):
        """
        获取表格数据
        """
        rowData=[]
        tr_list=table_tag.select("tr")
        for tr in tr_list:
            line="\t".join([td.get_text() for td in tr.select("td")])
            rowData.append(line)
        return rowData


if __name__=="__main__":
    acmspider = Base_RANK()
    data_json = acmspider.crawl(url="http://www.qianmu.org/ranking/904.htm")
    w=open(u"C:/Users/sfe_williamsL/Desktop/大学排行榜.txt","wt")
    w.write(data_json["HeardTitle"]+"\n")
    for line in data_json["RowData"]:
        w.write(line+"\n")
    w.close()