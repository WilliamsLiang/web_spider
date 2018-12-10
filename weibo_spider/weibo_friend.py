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

cookies=""

class weibo_friend:
    def __init__(self,user_id,out_path="result.txt",log_path="weibo.txt"):
        #weibo基础的url
        self.BaseUrl = "https://weibo.cn"
        self.FansUrl = "https://weibo.cn/{user_id}/fans"
        self.FollowerUrl = "https://weibo.cn/{user_id}/follow"
        #用户的id
        self.user_id=""
        #加载已存在的路径
        self.out_path = out_path
        self.log_path=log_path
        #爬虫headers设置
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
            'Cookie':cookies
        }
        # 构建已获取到信息人员的字典
        self.urlkey_info = {}
        self.idkey_info = {}
        self.is_log = {}
        #获取该账号下的所有关注和粉丝
        self.load_log()
        main_user = self.generate_user(self.BaseUrl + "/" + user_id)
        self.main_user = main_user

    def load_log(self):
        f = open(self.log_path, "rb")
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
            next_user_object = self.generate_user(next_url,username=next_name,userid=next_id)
            f_num = int(datas[6])
            main_object.add_friend(next_user_object)
            self.is_log[main_object.get_id()]=f_num
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
        time.sleep(30+random.randint(0,30))
        return user_object

    def generate_user(self,url,username="",userid=""):
        user_object=None
        if (not user_object):
            user_object = self.urlkey_info.get(url, None)
        if(not user_object):
            user_object=self.idkey_info.get(userid,None)
        if(username=="" and userid=="" and (not user_object)):
            user_object=self.create_user(url)
        if(not user_object):
            user_object=weibo_user(userid,username,url)
            self.idkey_info[userid]=user_object
            self.urlkey_info[url]=user_object
        return user_object

    def get_relation(self,user,level=1):
        now_num=len(user.get_friends())
        if(now_num == self.is_log.get(user.get_id(),-1)):
            friend_list=user.get_friends()
        else:
            friend_list=self.follower_and_fans(user)
        yield user
        if(level==0):
            pass
        else:
            for f_id in friend_list.keys():
                next_user=friend_list[f_id]
                next_generator=self.get_relation(next_user,level=level-1)
                for next_object in next_generator:
                    yield next_object

    def follower_and_fans(self,user):
        fans_url=self.get_user(user,self.FansUrl)
        followers_url=self.get_user(user,self.FollowerUrl)
        friends=[url for url in followers_url if url in fans_url]
        for furl in friends:
            self.modify_user(furl,user)
        time.sleep(180 + random.randint(0, 120))
        return user.get_friends()

    def modify_user(self,furl,user):
        if(not self.urlkey_info.get(furl,None)):
            othuser=self.create_user(furl)
        else:
            othuser=self.urlkey_info[furl]
        print("\t".join([user.get_info(),othuser.get_info()]))
        user.add_friend(othuser)

    def get_user(self,user,dest_url):
        url = dest_url.format(user_id=user.get_id())
        url_list=[]
        self.headers["User-Agent"] = random.choice(self.user_agent)
        res = requests.get(url, headers=self.headers)
        html_text = res.text
        soup_string = BeautifulSoup(html_text, "html.parser")
        content_generator = self.get_userurl(soup_string)
        url_list+=content_generator
        next_page = extract_nextpage.findall(html_text)
        num = 1
        print(user.get_info() + "  " +url+"第1页抓取完毕")
        while (next_page):
            time.sleep(240 + random.randint(0, 120))
            next_url = self.BaseUrl + next_page[0]
            self.headers["User-Agent"] = random.choice(self.user_agent)
            res = requests.get(next_url, headers=self.headers)
            html_text = res.text
            soup_string = BeautifulSoup(html_text, "html.parser")
            content_generator = self.get_userurl(soup_string)
            url_list+=content_generator
            num += 1
            print(user.get_info() + "  " + next_url + "第"+str(num)+"页抓取完毕")
            next_page = extract_nextpage.findall(html_text)
        return url_list

    def get_userurl(self,soup_string):
        div_list = soup_string.select("table")
        url_list=[]
        for div in div_list:
            a_list=div.select("a")
            url=a_list[0].get("href")
            url_list.append(url)
        return list(set(url_list))

    def Crawl(self,level=1):
        relation_generator=self.get_relation(self.main_user,level)
        w=open(self.out_path,"wb")
        for user_object in relation_generator:
            print("---------"+user_object.get_info()+"处理完毕 ----------")
            friend_num=len(user_object.get_friends())
            for key,friend in user_object.get_friends().items():
                w.write("\t".join([user_object.get_info(),friend.get_info(),str(friend_num)])+"\n")
                w.flush()
        w.close()


if __name__=="__main__":
    wf=weibo_friend("")# user's url
    wf.Crawl(level=1)