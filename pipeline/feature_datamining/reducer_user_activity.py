#!/usr/bin/python
from __future__ import division
import sys
import itertools
import time
import string
import sys
import os
import math
from itertools import groupby
from operator import itemgetter
import sys, json, datetime, uuid, os
 

dictionary_info={}
for line in open('dictionary_info.txt'):
    sp = line.strip().split('\t')
    dictionary_info[sp[0]] = sp[1]

media_doc_info_dict={}
class Media_doc_info(object): 
    def __init__(self):
        self.subcategory=[]

for line in open("media_info.txt"):
    sp = line.strip().split('\t')
    if len(sp) < 2:
        continue
    id = sp[0]
    media_doc_info = Media_doc_info()
    media_doc_info.subcategory = sp[1].split(',')
    media_doc_info_dict[id] = media_doc_info


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)
  
        
def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    for uid, group in groupby(data, itemgetter(0)):
        feature_dict={}
        visit_count = 0
        for uid, info in group:
            sp = info.strip().split('\t')
            if len(sp) < 2:
                continue
            if sp[1] in media_doc_info_dict:
                media_doc_info = media_doc_info_dict[sp[1]]
                for sub_category in media_doc_info.subcategory:
                    if sub_category not in dictionary_info:
                        continue
                    if dictionary_info[sub_category] in feature_dict:
                        feature_dict[dictionary_info[sub_category]] = feature_dict[dictionary_info[sub_category]] + 1
                    else:
                        feature_dict[dictionary_info[sub_category]] = 1
            visit_count = visit_count + 1
        for k,v in feature_dict.items():
            print uid + '\t' + k + '\t' + str(v) + '\t' + str(visit_count)
 
if __name__ == "__main__":
    main()

