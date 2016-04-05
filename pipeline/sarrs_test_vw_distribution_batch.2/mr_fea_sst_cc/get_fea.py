#!/usr/bin/python
from __future__ import division
import sys
import itertools
import time
import string
import sys
import os
import math
sys.path.append("./")
reload(sys)
#import feature_build 

# the user profile parser

def dict2str(dict):
	str_res=""
	for key in dict.keys():
		if len(str_res) == 0:
			str_res = key+":"+str(dict[key])
		else :
			str_res = str_res + "\t" + key + ":" + str(dict[key])
	return str_res
def list2str(list):
	str_res=""
	for key in list:
		if len(str_res) == 0:
			str_res = key+":1"
		else :
			str_res = str_res + "\t" + key + ":1" 
	return str_res

# load the vedio feature

vid_value_dict={}
vid_pid_dict={}

for line in open("./rec_media_doc_info.txt"):
	try:
		vid,pid,value=line.strip().split("\t")
	except:
		sys.abort()
		continue
	vid_value_dict[vid]=value
	if pid and pid != "NULL":
		vid_pid_dict[vid]=pid
	

#read the vid ctr information
vid_ctr_dict={}

for line in open("./recvid_rate.txt"):
	try:
		vid,rate,fenzi,fenmu,rate_value,rate_log,rate_buckt,click_value,click_log,click_buckt,exp_value,exp_log,exp_buckt=line.strip().split(" ")
	except:
		continue

	vid_ctr_dict[vid]=line.strip().replace(" ","?")


# read  the user activity log for training sample
user_activity_log=[]

os.popen('chmod 755 ./happy_to_see_recommender_feature_builder')
user_profile={}
for line in sys.stdin:

	#print "read stdin"
	try:
		sp=line.strip().split('\t')
		if len(sp) < 2:
			continue 
		if sp[-1] == "user_activity_log":
			user_activity_log.append(line)
		else:
			user_profile[sp[0]]=sp[1]
	except:
		sys.abort()
		continue

# construct the feature

def my_split(str):
	list=[]
	count = 0
	a=""
	b=""
	c=str
	while (len(c) > 0):
		a,b,c = c.partition('\t')
		list.append(a)
		count=count+1
	return list

for line in user_activity_log:
        try:
                sp=my_split(line.strip())
                uid,reid,label,uid_1,lc,vid,pid,cid,rec_vid,index,time_str=sp[:11]
        except:
		sys.abort()
                continue
	out_list=[]
	temp_list=[]
	
	ctr_line=""
	id=""
	if uid in user_profile:
		user_profile_str=user_profile[uid]
	else:
		continue
	if rec_vid and len(rec_vid) > 1 and rec_vid in vid_value_dict:
		media_doc_info_str=vid_value_dict[rec_vid]
		id=rec_vid
		if id in vid_ctr_dict:
			ctr_line=vid_ctr_dict[id]
	elif vid and len(vid) > 1 and  vid in vid_value_dict:
		media_doc_info_str=vid_value_dict[vid]
		id = vid
		if id in vid_ctr_dict:
			ctr_line=vid_ctr_dict[id]
	elif pid and len(pid) > 1 and pid in vid_value_dict:
		media_doc_info_str=vid_value_dict[pid]
		id = pid
		if id in vid_ctr_dict:
			ctr_line=vid_ctr_dict[id]
	else:
		continue
	if len(ctr_line) == 0:
		ctr_line="test"
	var = os.popen('./happy_to_see_recommender_feature_builder '+uid+" "+user_profile_str+" "+id+" "+media_doc_info_str+" "+ctr_line+" "+time_str).read()
	#print var
	if (len(var) == 0):
		sys.stderr.write(line)
		sys.stderr.write(user_profile_str)
		sys.stderr.write(media_doc_info_str)
		sys.abort()
	#history, feature = var.strip().split('\t', 1)

	print reid + '\t'  + var
	#print var



