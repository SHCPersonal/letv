#!/usr/bin/python
import sys

model_dict={}
dict_path=sys.argv[1]
for line in open(dict_path):
    sp = line.strip().split('\t')
    key = sp[0]
    value = float(sp[1])
    model_dict[key]=value

for line in sys.stdin:
    sp = line.strip().split('\t')
    sum = 0
    label = sp[0]
    for item in sp[1:]:
        key,tag,value = item.rpartition(':')
        if key in model_dict:
            sum = sum + float(value) * model_dict[key]
    print sp[0] + ' ' + str(sum)
