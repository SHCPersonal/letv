#!/usr/bin/python
import sys

for line in sys.stdin:
    sp=line.strip().split(' ')
    #print sp
    try:
        print sp[1][-1] + ' ' + sp[0]
    except:
        continue
