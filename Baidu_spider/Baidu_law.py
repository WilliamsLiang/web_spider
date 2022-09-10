#encoding=utf-8

import sys
import re
import requests
import urllib
import urllib2
import time
import random
import json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )

del_param=re.compile(r"\?.*")

class Baidu_law:

    # 初始化
    def __init__(self,cookies):

        # 基础的url
        self.BASE_URL = "https://duxiaofa.baidu.com/law/predictajax/get_inference"
        #请求头构造
        self.user_agent = [
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
        ]
        self.headers = {"Host": "duxiaofa.baidu.com",
                   "Accept": "application/json, text/plain, */*",
                   "Upgrade-Insecure-Requests": "1",
                   "Connection": "keep-alive",
                    "Referer": "https://duxiaofa.baidu.com / list?searchType = inference",
                    "Origin":"https://duxiaofa.baidu.com"
                   }
        self.headers["Cookie"]=cookies

    # 开始入口
    def start(self,conten_list):
        for content in conten_list:
            self.headers["User-Agent"] = random.choice(self.user_agent)
            params={"type":"general","wd":content}
            res=requests.post(self.BASE_URL, json.dumps(params))
            tmp_dict=json.loads(res.text)
            print("\t".join(tmp_dict["data"]["inference"]["value"]))


if __name__=="__main__":
    content_list=[]
    f = open(u"C:/Users/sfe_williamsL/Desktop/毕业论文/data/test.txt", "rb")
    tmp_data = []
    for line in f.readlines():
        datas = line.decode("utf-8").split("\t")
        if (len(datas) < 2):
            continue
        query_id = datas[0]
        content = datas[4]
        content_list.append(content)
    f.close()
    bd_spider=Baidu_law(cookies="BAIDUID=889BBBC8B00A20C46788524061D79397:FG=1; BIDUPSID=889BBBC8B00A20C46788524061D79397; PSTM=1561361030; BDUSS=2d4ZGNLZGY1bzZiZ3RrRUhNWUdyMmpMY0FaVUNXSWRpOE9xMGpydUlkMVdIemhkSVFBQUFBJCQAAAAAAAAAAAEAAAAcZLwyV2xpbW92ZWN5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFaSEF1WkhBdb; MCITY=-%3A; Hm_lvt_ac8fb11c31cd3cf585523fd58e170e95=1571576188,1572929558,1573122805; delPer=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=3; H_PS_PSSID=1469_21096_29568_29221; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lpvt_ac8fb11c31cd3cf585523fd58e170e95=1573288375")
    bd_spider.start(content_list)
