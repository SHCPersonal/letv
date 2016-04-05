#!/usr/bin/python
 
from itertools import groupby
from operator import itemgetter
import sys, json, datetime, uuid, os
 
def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)
        
def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    for key, group in groupby(data, itemgetter(0)):
        #if (len(group) != 2):
        #    print key + '\t' + len(group)
        #if (group[0] != group[1]):
        #    print key + '@' + group[0] + '@' + group[1]
 	print key
if __name__ == "__main__":
    main()
