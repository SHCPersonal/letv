#!/usr/bin/python
import sys

key_id_dict={}

for line in open('key_id.dict.local'):
    sp = line.strip().split('\t')
    key_id_dict[sp[0]]=sp[1]

model_key={}
for line in open('model_key'):
    model_key[line.strip()]=1

for line in sys.stdin:
    sp = line.strip().split('\t')
    label=sp[0][-1]
    if label == '0':
        label = '-1'
    res_string = label + ' 1.0 '+sp[0] + '| '
    for feature in sp[1:]:
        pre,mark,post = feature.rpartition(':')
        if  pre in model_key:
            res_string = res_string + ' ' + key_id_dict[pre] + ':' + post
            #res_string = res_string + ' ' + pre + ':' + post

    print res_string

