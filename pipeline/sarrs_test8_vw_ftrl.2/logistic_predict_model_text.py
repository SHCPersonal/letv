#!/usr/bin/python
import sys

model_dict={}
dict_path=sys.argv[1]
for line in open(dict_path):
    sp = line.strip().split(':')
    if len(sp) == 2 and sp[0].isdigit():    
        key = sp[0]
        value = float(sp[1])
        model_dict[key]=value

for line in sys.stdin:
    sp = line.strip().split('|', 1)
    sum = 0
    label = sp[0].split(' ')[2]
    feature_str = sp[1].strip(' ').split(' ')
    for item in feature_str:
        key,tag,value = item.rpartition(':')
        if key in model_dict:
            sum = sum + float(value) * model_dict[key]
    print str(sum) + ' ' + label
