#!/usr/bin/python
import sys
import urlparse
import math

class KV(object):
    def __init__(self):
        self.key=''
        self.value=0.0
    
    def __lt__(self,other):
        return self.value > other.value

score_idx=int(sys.argv[1])

itemcf_dict={}
for line in sys.stdin:
    sp = line.strip().split('\t')
    f1,f2 = sp[0].split('_')
    kv2 = KV()
    kv2.key=f1
    kv2.value=float(sp[score_idx])
    if f2 in itemcf_dict:
        itemcf_dict[f2].append(kv2)
    else:
        itemcf_dict[f2]=[kv2]


    kv1 = KV()
    kv1.key = f2
    kv1.value=float(sp[1])
    if f1 in itemcf_dict:
        itemcf_dict[f1].append(kv1)
    else:
        itemcf_dict[f2]=[kv1]


for key,value in itemcf_dict.items():
    value.sort()
    total=0.0
    for kv in value:
        total = total + kv.value

    res = []
    for kv in value:
        res.append(kv.key + ':' + str(kv.value/total))
    print key + '\t' + '\t'.join(res)

