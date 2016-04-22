#!/usr/bin/python
import sys
import urlparse


for line in sys.stdin:
    sp = line.strip().split('\t')
    if len(sp) < 4:
        continue
    #if int(sp[2]) < 2:
    #    continue
    # feature_name uid feature_count user_visit_count
    print sp[1] + '\t' + sp[0] + ':' + sp[2] + ':' + sp[3]
