#encoding=utf-8

import sys
from Baidu_spider import BDTieba_search


reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
    tieba_word=["穿山甲","野生","养生","中药","药材","文玩"]
    keyword_search=["穿山甲","川山甲","山甲","山甲片","山甲粉","山甲珠","亚洲甲片","穿山甲爪子","鳞片","穿山甲鳞片","穿山甲鳞片粉","穿山甲药酒","穿山甲种苗","养殖穿山甲","收购山甲片","出售山甲片","收山甲片","穿山甲手链","山甲珠串"]
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