#!/usr/bin/python
import sys
old_reid=""
old_list=[]
for line in sys.stdin:
	sp=line.strip().split("\t",1)
	if len(sp)!=2:
		continue
	else:
		reid,fea=sp
	if reid==old_reid:
		old_list.append(fea)
	else:
		if old_reid!="":
			try:
				label=old_reid.rsplit("&&",1)[1]
				print label+"\t"+"\t".join(old_list)
			except:
				continue
		old_list=[fea]
		old_reid=reid
label=old_reid.rsplit("&&",1)[1]
print label+"\t"+"\t".join(old_list)
