#!/usr/bin/python
import sys
import random
import time
random.seed(time.time())

def ParseSingleClkDetail(detail):
    ret = {}
    for item in detail.split('&'):
        try:
            k,v = item.split('=')
            ret[k] = v
        except:
            continue
    return ret

user_dict={}
for line in open("user_list.txt"):
	line = line.strip() 
	if line and line not in user_dict:
		user_dict[line] = 1


p=1.0
for line in sys.stdin:
    sp=line.strip().split("\x01")
    reid,uid,lc,vid,pid,cid,time_str,recom_str,type,clk_detail = sp[:10]
    rec_list=list(set(recom_str.strip().split("-")))[:4]
    if clk_detail=='-':
        clk_list=[]
    else:
        clk_list=[ParseSingleClkDetail(meta).get('vid',"NULL") for meta in clk_detail.split()]
    clk_set=set(clk_list)
    for index,rec_vid in enumerate(rec_list,start=1):
        if rec_vid.isdigit()==False:
            continue
        
        label='1' if rec_vid in clk_set else '0'
        
        if label=="0" and random.random()>p:
            continue
        
        new_reid=reid+"_"+rec_vid+"&&"+label
	if not uid or uid == "-":
		uid = lc

	if uid and uid != "-" and uid in user_dict:	
        	print "\t".join([new_reid,label,uid,lc,vid,pid,cid,rec_vid,str(index),time_str,"user_activity_log"])
            
            
    
    
