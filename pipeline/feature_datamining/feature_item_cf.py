#!/usr/bin/python
import sys
import urlparse
import math

class Feature_info(object):
    def __init__(self):
        self.count = 0
        self.total = 0
        self.user_list = []
        self.name = ""

features=[]
user_weight_dict={}

for line in sys.stdin:
    sp = line.strip().split('\t')
    feature_info = Feature_info()
    feature_info.count = int(sp[1])
    if feature_info.count < 1000:
        continue
    for item in sp[2:]:
        uid,visit,user_weight = item.strip().split(':')
        feature_info.total = feature_info.total + int(visit)
        feature_info.user_list.append(uid+':'+visit)
        user_weight_dict[uid] = int(user_weight)
    feature_info.name = sp[0]
    features.append(feature_info)


feature_size = len(features)

i = 0
j = 0
while i < feature_size - 1:
    j = i + 1
    while j < feature_size:
        base_dict = {}
        intersection_count = 0
        intersection_total = 0
        for item in features[i].user_list:
            uid,weight  = item.strip().split(':')
            base_dict[uid]=int(weight)
        for item in features[j].user_list:
            uid,weight = item.strip().split(':')
            if uid in base_dict:
                intersection_count = intersection_count + 1
        score = intersection_count / (math.sqrt(features[i].count) * math.sqrt(features[j].count))
        print features[i].name + '\t' + features[j].name + '\t' + str(score)
        j = j + 1
    i = i + 1

                    


