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
        self.category=''
        self.area=''

    def build_category_subcategory_area(self, dictionary_info):
        res=[]
        if len(self.category) == 0:
            return res
        for sub in self.subcategory:
            category_name = dictionary_info[self.category]
            subcategory_name = ''
            if sub in dictionary_info:
                subcategory_name = dictionary_info[sub]
            area_name = ''
            if self.area in dictionary_info:
                area_name = dictionary_info[self.area]
            feature = category_name+'/'+subcategory_name+'/'+area_name
            res.append(feature)
        return res

    def build_category_subcategory(self, dictionary_info):
        res=[]
        if len(self.category) == 0:
            return res
        for sub in self.subcategory:
            category_name = dictionary_info[self.category]
            subcategory_name = ''
            if sub in dictionary_info:
                subcategory_name = dictionary_info[sub]
            feature = category_name+'/'+subcategory_name
            res.append(feature)
        return res

    def build_category_area(self, dictionary_info):
        res=[]
        if len(self.category) == 0:
            return res
        category_name = dictionary_info[self.category]
        area_name = ''
        if self.area in dictionary_info:
            area_name = dictionary_info[self.area]
        feature = category_name + '/' + area_name
        res.append(feature)
        return res


    def build_category(self, dictionary_info):
        res=[]
        if len(self.category) == 0:
            return res
        res.append(dictionary_info[self.category])
        return res

    def build_subcategory(self, dictionary_info):
        res=[]
        for sub in self.subcategory:
            if sub in dictionary_info:
                subcategory_name = dictionary_info[sub]
                res.append(subcategory_name)
        return res



for line in open("media_info.txt"):
    sp = line.strip().split('\t')
    if len(sp) < 2:
        continue
    id = sp[0]
    media_doc_info = Media_doc_info()
    if sp[1] != 'NULL':
        media_doc_info.subcategory = sp[1].strip(',').split(',')
    if sp[2] != 'NULL':
        media_doc_info.category=sp[2]
    if sp[3] != 'NULL':
        media_doc_info.area=sp[3].strip(',').split(',')[0]
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
                res_list=media_doc_info.build_category_area(dictionary_info)
                for feature_name in res_list:
                   
                    j = i + 1
                    while j < group_size:
                        info_1 = temp_group[j]
                        sp_1 = info_1.strip().split('\t')
                        if len(sp_1) < 2:
                            continue
                        if sp_1[1] in media_doc_info_dict:
                            media_doc_info_1 = media_doc_info_dict[sp_1[1]]
                            res_list1=media_doc_info.build_category_area(dictionary_info)
                            for feature_name_1 in res_list1:
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

