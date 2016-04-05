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
    for key, group in groupby(data, itemgetter(0)):
      label=key.rsplit("&&", 1)[1]
      fea=''
      for k, line in group: 
        fea = fea + '\t' + line
      print label + fea

 
if __name__ == "__main__":
    main()
	
