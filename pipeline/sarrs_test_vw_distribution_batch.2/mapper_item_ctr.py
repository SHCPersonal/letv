#!/usr/bin/python
from __future__ import division
import sys
import itertools
import time
import string
import sys
import os
import math


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
                reid,label,uid,lc,vid,pid,cid,rec_vid,index,time_str=sp[:10]
        except:
		sys.abort()
                continue
	print rec_vid + '\t' + label
	
