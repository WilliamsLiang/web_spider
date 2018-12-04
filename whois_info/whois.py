# -*- coding: utf-8 -*-
import sys
import re
import requests
import random
import json
import urllib2
import time
import random

reload(sys)
sys.setdefaultencoding("utf-8")

remail=re.compile(r"Registrar Abuse Contact Email: (.*?)\r{0,1} ")
rephone=re.compile(r"Registrar Abuse Contact Phone: (.*?)\r{0,1} ")
rest_prov=re.compile(r"Registrant State/Province: (.*?)\r{0,1} ")
re_count=re.compile(r"Registrant Country: (.*?)\r{0,1} ")
reg_host = re.compile(u'https?://[^/]+')
reg_url = re.compile(u'(https?://.*?)[#\t]')
cookie_sub=re.compile(ur'whois.html\?domain=.*?&')

headers={
    "Host":"cloud.baidu.com",
    "Origin":"https://cloud.baidu.com",
    'Content-Type':'application/json'
}

user_agents=[
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]

def get_url(line):
    datas=line.split("\t")
    url = reg_url.findall(line)
    if len(url) == 0:
        return ""
    url=url[0]
    if(len(datas)<2):
        return ""
    thost_list = reg_host.findall(url)
    if len(thost_list)== 0:
        return ""
    url_host=thost_list[0]
    thost=url_host.split("/")[-1]
    return thost

def whois_format(result): 
    who_json=json.loads(result)
    success_code=who_json["success"]
    if(not success_code):
        return ""
    else:
        who_data=who_json[u"result"][u"data"]
        registname=who_data[u"registrantName"]
        registemail=who_data[u"registrantEmail"]
        sponsor=who_data[u"sponsoringRegistrar"]
        date=who_data[u"registrationDate"]
        server_name="|".join(who_data[u"nameServer"])
        rowdata=" ".join(who_data[u"rawData"])
        mail_all=re.findall(remail,rowdata)
        if (len(mail_all)!=0):
            exmail=mail_all[0]
        else:
            exmail=""
        phone_all=re.findall(rephone,rowdata)
        if (len(phone_all)!=0):
            phone=phone_all[0]
        else:
            phone=""
        state_all=re.findall(rest_prov,rowdata)
        if(len(state_all)!=0):
            state=state_all[0]
        else:
            state=""
        country_all=re.findall(re_count,rowdata)
        if(len(country_all)!=0):
            country=country_all[0]
        else:
            country=""
        return "\t".join([date,registname,registemail,sponsor,exmail,phone,state,country,server_name])

def log_host(path):
    loghost=set([])
    f=open(path,"rt")
    for line in f.readlines():
        datas=line.split("\t")
        if(len(datas)<2):
            continue
        host=datas[0]
        if(host not in loghost):
            loghost.add(host)
    f.close()
    return loghost

def save_whois(input_path,out_path,cookies):
    global headers
    ajax_url="https://cloud.baidu.com/api/bcd/whois/detail"
    loghost=log_host(out_path)
    f=open(input_path,"rt")
    erro_num=0
    for line in f.readlines():
        if(erro_num==10):
            continue
        c_url=get_url(line)
        if(c_url==""):
            continue
        if(c_url in loghost):
            continue
        datas={
            "domain": c_url,
            "type": "NORMAL"
        }
        referer="https://cloud.baidu.com/product/bcd/whois.html?domain={url}&track=cp:aladdin%7Ckw:154".format(url=c_url)
        headers["Referer"]=referer.format(url=c_url)
        random_agent = random.choice(user_agents)
        headers["User-Agent"]=random_agent
        post_data=json.dumps(datas)
        req_cookie=cookies.format(do_url=c_url)
        headers["Cookie"]=req_cookie
        req  = urllib2.Request(ajax_url, post_data, headers)
        try:
            result=urllib2.urlopen(req).read()
            erro_num=0
        except Exception:
            print("---------erro---------")
            erro_num+=1
            continue
        w=open(out_path,"at")
        try:
            infoline=whois_format(result)
            if(infoline==""):
                time.sleep(5+random.randint(0,5))
                continue
            w.write(c_url+"\t"+infoline+"\n")
        except Exception:
            w.write(c_url+"\tnull\n")
        w.close()
        print("*******"+c_url+"*******")
        time.sleep(5+random.randint(0,5))

if __name__=="__main__":
    input_path="result_keyword_multi_all.txt"
    out_path="result.txt"
    inter_cookies=""#cookies的设置
    re_co=re.findall(cookie_sub,inter_cookies)[0]
    cookies=inter_cookies.replace(re_co,"whois.html?domain={do_url}&")
    save_whois(input_path,out_path,cookies)