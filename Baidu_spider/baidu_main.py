#encoding=utf-8

import sys
from Baidu_spider import BDTieba_search


reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
    tieba_word=["足球"]
    keyword_search=["梅西"]
    bd_spider = BDTieba_search()
    for tbw in tieba_word:
        for key in keyword_search:
            content_generator = bd_spider.start(tb_name=tbw, keyword=key)
            w = open("C:/Users/IAO-XY/Desktop/lz_spider/spider_result/baidu/"+tbw+"_"+key+".txt", "wt")
            for content in content_generator:
                w.write(content + "\n")
                w.flush()
            w.close()

if __name__=="__main__":
    main()