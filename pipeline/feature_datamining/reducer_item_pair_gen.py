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
        
        temp_group=[]
        for uid_t, info in group:
            temp_group.append(info)

        feature_dict={}
        vid_dict={}
        visit_count = 0
        group_size=len(temp_group)
        visit_count = group_size
        i = 0
        j = 0

        while i < group_size:
            info = temp_group[i]
            sp = info.strip().split('\t')
            if len(sp) < 2:
                continue
            if sp[1] in media_doc_info_dict:
                media_doc_info = media_doc_info_dict[sp[1]]
                for sub_category in media_doc_info.subcategory:
                    if sub_category not in dictionary_info:
                        continue
                   
                    j = i + 1
                    while j < group_size:
                        info_1 = temp_group[j]
                        sp_1 = info_1.strip().split('\t')
                        if len(sp_1) < 2:
                            continue
                        if sp_1[1] in media_doc_info_dict:
                            media_doc_info_1 = media_doc_info_dict[sp_1[1]]
                            for sub_category_1 in media_doc_info_1.subcategory:
                                if sub_category_1 not in dictionary_info:
                                    continue
                                feature_name = dictionary_info[sub_category]
                                feature_name_1 = dictionary_info[sub_category_1]
                                if feature_name < feature_name_1 :
                                    output_key = feature_name + '_' + feature_name_1
                                elif feature_name_1 < feature_name :
                                    output_key = feature_name_1 + '_' + feature_name
                                else :
                                    continue
                                if output_key in feature_dict:
                                    feature_dict[output_key] = feature_dict[output_key] + 1
                                    vid_dict[output_key].add(sp[1])
                                    vid_dict[output_key].add(sp_1[1])
                                else:
                                    feature_dict[output_key] = 1
                                    vid_dict[output_key]=set([sp[1],sp_1[1]])
                                    
 
                        j = j + 1
            i = i + 1
        for pair,value in feature_dict.items():
            vid_count = len(vid_dict[pair])
            score1 = float(value) / vid_count
            score2 = float(value * value) / vid_count
            print pair + '\t' + uid + '\t' + str(value) + '\t' + str(vid_count) + '\t' + str(score1) + '\t' + str(score2) 
 
if __name__ == "__main__":
    main()

