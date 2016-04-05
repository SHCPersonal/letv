#!/usr/bin/python
from __future__ import division
import sys
from math import log
import string

max_click_value=0
max_click_log=0
max_exp_value=0
max_exp_log=0
max_rate_value=0
max_rate_log=0

frequent_click=[]
frequent_exp=[]
frequent_rate=[]

data=[]
for line in sys.stdin:
	data.append(line)

for line in data:	
	sp=line.split()
	rate=string.atof(sp[1])
	click=string.atof(sp[2])
	exp=string.atof(sp[3])
	if (click > max_click_value):
		max_click_value=click
	frequent_click.append(click)
	if (log(click+1) > max_click_log):
		max_click_log=log(click+1)
	if (exp > max_exp_value):
		max_exp_value=exp
	frequent_exp.append(exp)
	if (log(exp+1) > max_exp_log):
		max_exp_log=log(exp+1)
	if (rate > max_rate_value):
		max_rate_value=rate
	frequent_rate.append(rate)
	if (abs(log(rate+0.0000001)) > max_rate_log):
		max_rate_log=abs(log(rate+0.0000001))

frequent_click.sort()
frequent_exp.sort()
frequent_rate.sort()

#print frequent_click
#print frequent_exp
#print frequent_rate

len_click=int(len(frequent_click)/20)
len_exp=int(len(frequent_exp)/20)
len_rate=int(len(frequent_rate)/20)

#print len_click
#print len_exp
#print len_rate

def print_buckt(frequent, len):
	cnt=0
	idx=len-1
	res=""
	while (cnt < 19):
		cnt=cnt+1
		idx=idx+len
		res = res + str(frequent[idx]) + " "
	return res
	
#print print_buckt(frequent_click, len_click)
#print print_buckt(frequent_exp, len_exp)
#print print_buckt(frequent_rate, len_rate)


def get_buckt(num, frequent, len):
	cnt=0
	idx=len-1
	while(cnt < 19 and num > frequent[idx]):
		cnt=cnt+1
		idx = idx + len
	return cnt

for line in data:
	sp=line.split()
	print line.strip('\n') + ' ' + str(string.atof(sp[1])/max_rate_value) + ' ' + str(abs(log(string.atof(sp[1])+0.0000001)/max_rate_log)) + ' ' + str(get_buckt(string.atof(sp[1]), frequent_rate, len_rate)) + ' ' + str(string.atof(sp[2])/max_click_value) + ' ' + str(abs(log(string.atof(sp[2])+1)/max_click_log)) + ' ' + str(get_buckt(string.atof(sp[2]), frequent_click, len_click)) + ' ' + str(string.atof(sp[3])/max_exp_value) + ' ' + str(abs(log(string.atof(sp[3])+1)/max_exp_log)) + ' ' + str(get_buckt(string.atof(sp[3]), frequent_exp, len_exp))
