#!/usr/bin/python
import sys
ori_dict={}
for line in open(sys.argv[1]):
	fea,wgszn=line.strip().split("\t",1)
	ori_dict[fea]=wgszn

zstr='0\t0\t0\t0\t0'
model_key={}
for line in open(sys.argv[2]):
	fea,count=line.strip().split("\t")
	if fea not in ori_dict and fea not in model_key:
		model_key[fea]=0
		print fea+"\t"+zstr

for key,value in ori_dict.iteritems():
	if key!='':
		print key+"\t"+value

