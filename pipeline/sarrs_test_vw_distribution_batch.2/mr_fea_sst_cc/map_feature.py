#!/usr/bin/python
from __future__ import division
import sys
import time

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

for line in sys.stdin:
	try: 
		sp=my_split(line.strip())
		if len(sp) < 2:
			continue
		if sp[-1] == 'user_activity_log':
		#	print sp[:4]
			reid, label, uid, lc = sp[:4]
		#	print "a"
			if len(uid.strip()) == 0 or uid == '-':
				uid = lc
			if len(uid.strip()) != 0 and uid != '-':
				print uid+"\t"+line
		else:
			 print line
	except:
		continue
	
