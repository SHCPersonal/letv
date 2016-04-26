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
        feature_dict={}
        visit_count = 0
        for uid, info in group:
            sp = info.strip().split('\t')
            if len(sp) < 2:
                continue
            if sp[1] in media_doc_info_dict:
                media_doc_info = media_doc_info_dict[sp[1]]
                res_list=media_doc_info.build_category_area(dictionary_info)
                for feature in res_list:
                    if feature in feature_dict:
                        feature_dict[feature] = feature_dict[feature] + 1
                    else:
                        feature_dict[feature] = 1
            visit_count = visit_count + 1
        for k,v in feature_dict.items():
            print uid + '\t' + k + '\t' + str(v) + '\t' + str(visit_count)
 
if __name__ == "__main__":
    main()

