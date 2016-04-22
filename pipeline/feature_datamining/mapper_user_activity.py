#!/usr/bin/python
import sys
import urlparse

for line in sys.stdin:
    sp = line.strip().split('\t')
    if len(sp) < 3:
        continue
    if not sp[2].startswith("action=click"):
        continue
    query = urlparse.parse_qs(urlparse.urlparse("http://www.baidu.com/index?"+sp[2]).query)
    if not  "rec_id" in query or len(query["rec_id"]) == 0:
        continue
    if not "key" in query or len(query["rec_id"]) == 0:
        continue
    rec_id = query["rec_id"][0]
    key = query["key"][0]
    if "lc" in query and len(query["lc"]) > 0:
        lc = query["lc"][0]
    else:
        lc = ""
    if "aid" in query and len(query["aid"]) > 0:
        aid = query["aid"][0]
    else:
        aid = ""
    if "chid" in query and len(query["chid"]) > 0:
        chid = query["chid"][0]
    else:
        chid = ""
    if len(lc) > 1 and len(key) > 1:
        str_size = len(lc)
        i = 0
        while i < str_size:
            if lc[i].isalpha() or lc[i].isdigit():
                i = i + 1
                continue
            break
        if i != str_size:
            lc = lc[:i]
        print lc + '\t' + sp[0] + '\t' + key + '\t' + aid + '\t' + chid

