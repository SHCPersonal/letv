#!/usr/bin/python

import sys

user_list={}
for line in open("local_unique_user.txt"):
	sp=line.strip().split('\t')
	user_list[sp[0]]=1


for line in sys.stdin:
	sp=line.strip().split('\t',1)
	uid=sp[0][2:]
	if not uid in user_list:
		continue
	user_profile=sp[1]

	print uid+'\t'+user_profile
	

