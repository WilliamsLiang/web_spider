#encoding=utf-8

from njaulibparse.searchinfo import searchinfo

if __name__=="__main__":
    bi=searchinfo()
    list_info=["F2","G2"]
    num_info=[2575,1]
    for i in range(len(list_info)):
        classinfo=list_info[i]
        num=num_info[i]
        tl=bi.start(class_id=classinfo,doc_type="01",start_num=num)
        w=open("result/"+classinfo+"_book.txt","at")
        for t in tl:
            w.write(t+"\n")
            w.flush()
        w.close()