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
 
def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)
        
def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    for feature_name, group in groupby(data, itemgetter(0)):
        count=0
        list=[]
        total=0
        for feature_name, info in group:
            sp = info.split(':')
            #if len(sp) != 3:
            #    continue
            uid,feature_count,use_weight=sp
            count = count + 1
            total = total + int(feature_count)
            list.append(info)
        print feature_name + '\t' + str(count) + '\t' + str(total) + '\t' + '\t'.join(list)
 
if __name__ == "__main__":
    main()

