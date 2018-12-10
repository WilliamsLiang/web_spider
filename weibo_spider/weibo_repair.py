#encoding=utf-8

import sys
import re
import requests
import time
import random
from bs4 import BeautifulSoup
from weibo_user import weibo_user

reload(sys)
sys.setdefaultencoding( "utf-8" )

extract_id=re.compile(r"/(\d*?)[/\b]")
extract_username=re.compile(r"(.*?)\s")
extract_nextpage=re.compile(ur'<div><a href="(.*?)">下页</a>')


class weibo_repair:
    def __init__(self,input_path,out_path="weibo_new.txt"):
        #weibo基础的url
        self.BaseUrl = "https://weibo.cn"
        self.FansUrl = "https://weibo.cn/{user_id}/fans"
        self.FollowerUrl = "https://weibo.cn/{user_id}/follow"
        #用户的id
        self.user_id=""
        #爬虫headers设置
        self.cookies=""

        self.user_agent = [
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
        ]
        self.headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'weibo.cn',
            'Upgrade-Insecure-Requests': '1',
            'Cookie':self.cookies
        }
        #构建已获取到信息人员的字典
        self.urlkey_info={}
        self.idkey_info={}
        #获取该账号下的所有关注和粉丝
        self.input_path=input_path
        self.out_path=out_path
        #加载一个日志
        self.log={}
        self.load_log()

    def load_log(self):
        f = open(self.out_path, "rb")
        for line in f.readlines():
            line = line.decode("utf-8").replace("\r", "").replace("\n", "")
            datas = line.split("\t")
            if(len(datas)<6):
                continue
            mainuser_name = datas[0]
            mainuser_id = datas[1]
            mainuser_url = datas[2]
            main_object = self.generate_user(mainuser_url,username=mainuser_name,userid=mainuser_id)
            next_name=datas[3]
            next_id=datas[4]
            next_url = datas[5]
            next_object = self.generate_user(next_url,username=next_name,userid=next_id)
            url_key = "\t".join([main_object.get_url(), next_object.get_url()])
            self.log[url_key] = self.log.get(url_key, 0) + 1
        f.close()

    def create_user(self,url):
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        table_info = soup_string.select("table")
        if (table_info):
            href_id = table_info[0].select("a")[0].get("href")
            user_id = extract_id.findall(href_id)[0]
            user_info = table_info[0].select("span[class=ctt]")[0]
            username = extract_username.findall(user_info.get_text().replace(u'\xa0', u' '))[0]
        else:
            myuser = soup_string.select("div[class=ut]")[0]
            username = myuser.contents[0]
            href_id = myuser.select("a")[1].get("href")
            user_id = extract_id.findall(href_id)[0]
        user_object=self.generate_user(url,username,user_id)
        time.sleep(60+random.randint(0,60))
        print(user_object.get_info())
        return user_object

    def generate_user(self,url,username="",userid=""):
        user_object=None
        if(not user_object):
            user_object=self.idkey_info.get(userid,None)
        if(not user_object):
            user_object=self.urlkey_info.get(url,None)
        if(username=="" and userid=="" and (not user_object)):
            user_object=self.create_user(url)
        if(not user_object and username!="" and userid!=""):
            user_object=weibo_user(userid,username,url)
            self.idkey_info[userid]=user_object
            self.urlkey_info[url]=user_object
        return user_object

    def modify_user(self,furl,user):
        othuser=self.create_user(furl)
        user.add_friend(othuser)

    def modify(self):
        f = open(self.input_path,"rb")
        w = open(self.out_path, "ab")
        for line in f.readlines():
            line=line.decode("utf-8").replace("\r","").replace("\n","")
            datas=line.split("\t")
            if(len(datas)<4):
                continue
            username=datas[0]
            user_id=datas[1]
            user_url=datas[2]
            next_url = datas[3]
            url_key="\t".join([user_url,next_url])
            if(self.log.get(url_key,0)):
                continue
            user_object = weibo_user(user_id, username, user_url)
            next_user_object=self.generate_user(next_url)
            w.write("\t".join([user_object.get_info(),next_user_object.get_info()])+"\n")
            w.flush()
        w.close()
        f.close()


if __name__=="__main__":
    wf=weibo_repair("weibo.txt")
    print("****加载结束***")
    wf.modify()