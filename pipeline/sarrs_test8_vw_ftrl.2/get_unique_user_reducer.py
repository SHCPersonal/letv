#!/usr/bin/python
import sys

old_key=''
old_count=0
for line in sys.stdin:
	key,value=line.strip().split()
	if key==old_key:
		old_count += 1
	else:
		if old_key!='':
			print old_key+"\t"+str(old_count)
		old_key=key
		old_count=1

if old_key!='':
	print old_key+"\t"+str(old_count)	
