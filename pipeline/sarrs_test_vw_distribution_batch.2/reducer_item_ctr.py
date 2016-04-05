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
	expose=0.0
	click=0.0
	for key, label in group: 
		expose=expose+1.0
	    	if (label == '1'):
			click=click+1.0
	print key + '\t' + str(click/expose) + '\t' + str(int(click)) + '\t' + str(int(expose))

 
if __name__ == "__main__":
    main()
	
