#!/usr/bin/pytho
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
    if len(rec_id) > 0 and len(key) > 1:
        print rec_id + '\t' + key + '\t' + lc + '\t' + aid + '\t' + chid + '\tserver_log_tag'

