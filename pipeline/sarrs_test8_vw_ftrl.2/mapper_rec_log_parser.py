#!/usr/bin/python
import sys
import urlparse
import time


for line in sys.stdin:
    sp = line.strip().split('\t')
    if len(sp) < 3:
        continue
    if not sp[2].startswith("action=logrec"):
        continue
    try:
        time_raw_str=sp[0].split('.', 1)[0]
        time_str=str(time.mktime(time.strptime(time_raw_str,'%Y/%m/%d-%H:%M:%S')))
    except:
        continue
    query = urlparse.parse_qs(urlparse.urlparse("http://www.baidu.com/index?"+sp[2]).query)
    if not  "reid" in query or len(query["reid"]) == 0:
        continue
    if not "ids" in query or len(query["ids"]) == 0:
        continue
    rec_id = query["reid"][0]
    ids = query["ids"][0]
    rec_key = ids.strip().split(',')
    for key in rec_key:
        if len(key) > 1:
            print rec_id + '\t' + key + '\t' + time_str + '\trec_log_tag'

