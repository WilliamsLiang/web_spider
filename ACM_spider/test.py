#encoding=utf-8

import sys
import re
import requests
import urllib
import urllib2
import time
import random
from bs4 import BeautifulSoup
from base_spider.sigir_spider import sigir_download

reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
    cookies="__cfduid=d8d304e58cab2d74fd097f3e4c9af01ab1562507918; _ga=GA1.2.368478941.1562507920; _gid=GA1.2.117468789.1562739715; CFP=1; JSESSIONID=F2D0C5ABBCD14C96CCDA0BD6F07D99C0.dl; CFID=58351575; CFTOKEN=18943ef18c6a5a4f%2DBC2138DE%2DF35E%2DC66E%2D709D4D9B8897D299; IP_CLIENT=1795640; SITE_CLIENT=3011566; __cflb=2874915494; cffp_mm=0; __atuvc=16%7C28; __atuvs=5d26d05272ed2c48001"
    acmspider=sigir_download(cookies)
    acmspider.crawl(url="https://dl.acm.org/citation.cfm?id=3209978&picked=prox")

if __name__=="__main__":
    main()
