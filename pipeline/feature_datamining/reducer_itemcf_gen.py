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
 
user_weight={}
for line in open('user_weight.txt'):
    sp = line.strip().split('\t')
    user_visit_cnt=int(sp[1])
    user_weight[sp[0]]=1/math.log(user_visit_cnt + 1)
feature_count={}
for line in open('feature_count.txt'):
    sp = line.strip().split('\t')
    if int(sp[1]) < 100:
        continue
    feature_count[sp[0]]=[int(sp[1]), int(sp[2])]


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)
  
        
def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    for pair, group in groupby(data, itemgetter(0)):
        f1,f2=pair.split('_')
        if f1 not in feature_count or f2 not in feature_count:
            continue
        score1=0.0
        score2=0.0
        score3=0.0
        score4=0.0
        score5=0.0

        score6=0.0
        score7=0.0
        for pair, info in group:
            sp = info.strip().split('\t')
            if len(sp) < 5:
                continue
            score1 = score1 + 1
            score2 = score2 + float(sp[1])
            score3 = score3 + float(sp[2])
            score4 = score4 + float(sp[3])
            score5 = score5 + float(sp[4])

            score6 = score6 + user_weight[sp[0]]
            score7 = score7 + user_weight[sp[0]] * float(sp[1])
        f1,f2=pair.split('_')
        base1_0 = math.sqrt(feature_count[f1][0])
        base1_1 = math.sqrt(feature_count[f1][1])
        base2_0 = math.sqrt(feature_count[f2][0])
        base2_1 = math.sqrt(feature_count[f2][1])

        print pair + '\t' + str(score1/(base1_0 * base2_0)) + '\t' + str(score2/(base1_0 * base2_0)) + '\t' + str(score3/(base1_0 * base2_0)) + '\t'+ str(score4/(base1_0 * base2_0)) + '\t' + str(score5/(base1_0 * base2_0)) + '\t' + str(score6/(base1_0 * base2_0)) + '\t' + str(score7/(base1_0 * base2_0)) + '\t' + str(score1/(base1_1 * base2_1)) + '\t' + str(score2/(base1_1 * base2_1)) + '\t' + str(score3/(base1_1 * base2_1)) + '\t' + str(score4/(base1_1 * base2_1)) + '\t' + str(score5/(base1_1 * base2_1)) + '\t' + str(score6/(base1_1 * base2_1)) + '\t' + str(score7/(base1_1 * base2_1))

 
if __name__ == "__main__":
    main()

