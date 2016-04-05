import sys
import os

#cmd1="hadoop fs -cat /user/rec/ctr_predict/pipeline/0003/rec_0027/20151022/train/mr_fea_sst_train/part-00049 | head -n 10 > py.txt"
cmd1="hadoop fs -cat /user/rec/ctr_predict/pipeline/0003/rec_0027/20151022/train/merge/part-00000 | head -n 100 > py.txt"
#cmd2="hadoop fs -cat /user/rec/ctr_predict/pipeline/0003/rec_0027/20151022/train/tmp_mr_fea_sst_cc/part-00049 | head -n 10 > cc.txt"
cmd2="hadoop fs -cat /user/rec/ctr_predict/pipeline/0003/rec_0027/20151022/train/merge_test1/part-00000 | head -n 100 > cc.txt"
os.system(cmd1)
os.system(cmd2)

#dict_py={}
#for line in open("py.txt"):
#	sp = line.strip().split('\t')
#	dict_py[sp[0]]=sp[1:]
#	dict_py[sp[0]].sort()

#dict_cc={}
#for line in open("cc.txt"):
#	sp = line.strip().split('\t')
#	dict_cc[sp[0]]=sp[1:]
#	dict_cc[sp[0]].sort()

f_py=open("py.s","w")
f_cc=open("cc.s","w")
#for k in dict_cc.keys():
#	if k in dict_py:
#		for item in dict_py[k]:
#			f_py.write(k+'\t'+item+'\n')
#		for item in dict_cc[k]:
#			f_cc.write(k+'\t'+item+'\n')

for line in open("py.txt"):
	sp=line.strip('').split('\t')
	sp.sort()
	for item in sp:
		f_py.write(item+'\n')
for line in open("cc.txt"):
	sp=line.strip().split('\t') 
	sp.sort()
	for item in sp:
		f_cc.write(item+'\n')
	
