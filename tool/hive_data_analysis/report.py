
import time

page=""
table='<table border="1">'
html_head='<html>'
html_tail='</html>'

head_template='''
 <head>
        <title>%s</title>
    <style>img{float:left;margin:5px;}</style>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
 </head>'''
td_template='''
<td>%s</td>
'''

import os
import sys

field_format="reid,bkt,pageid,fragid,is_ex,is_clk,uid,lc,vid,pid,cid,time_str,recom_str,type,clk_detail"

cmd1 = "hadoop fs -cat /user/rec/ctr_predict/pipeline/0003/rec_0027/20151029/data/recommend_user_activity_log/000000_0 | head -n 1000"
cmd2 = 'mysql -h 117.121.54.220 -P 3308 -u tuijian_read -p"f6w6FSewb2v5gpcy7PGT" -e "use mms;select id,pid,SOURCE_ID,VIDEO_TYPE,PID,PORDER,NAME_CN,SUB_TITLE,TAG,CATEGORY,SUB_CATEGORY,EPISODE,BTIME,ETIME,DURATION,SCORE,RELEASE_DATE,AREA,CREATE_TIME,UPDATE_TIME,UPDATE_UID  from con_video_info where play_platform is not null and id in '
cmd3 = "hive -e \"select %s from dm_rec.tbl_engine_join_hour where dt = '20160407' and pt = '0003' and area='rec_0027' and is_ex > 0 and is_clk > 0 and fragid in ('4464','4459','3563') and bkt = '110\:1'\"" % field_format



data=os.popen(cmd3).readlines()


f = open('a.txt', 'w')
for line in data:
  f.write(line)

limit = 0
for line in data:
    if limit >= 1000:
      continue
    limit = limit + 1
    if not line:
        continue

    sp = line.strip().split('\t')
    format_sp = field_format.split(',')
    if len(sp) != len(format_sp):
      continue
    
    idx = 0
    value={}
    while(idx < len(format_sp)):
      value[format_sp[idx]] = sp[idx];
      idx = idx + 1
    x = time.localtime(int(value['time_str']))
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',x)

    table = table+"<tr>"
    table = table+td_template % ("user_id:" + value['uid'])
    table = table + td_template % ("lc:" + value['lc'])
    table = table + "</tr>"
    table = table + "<tr>"
    table = table + td_template % ('is_ex' + value['is_ex'])
    table = table + td_template % ('is_clk' + value['is_clk'])
    table = table + td_template % (time_str)
    table = table + "</tr>"

    sql = cmd2 + "(" +value['recom_str'].replace("-",",") + ")\""
    for line1 in os.popen(sql).readlines():
        sp1=line1.strip().split('\t')
        table = table + "<tr>"
        for item in sp1:
            table = table+ td_template % item
        table = table + "</tr>"
    table = table + "<tr>"
    table = table + (td_template%value['clk_detail'])
    table = table + "</tr>" 


table=table+"</table>"
title="report"

page = html_head + (head_template % title) + "<body>" + table + "</body>"+html_tail


f1 = open('index.html', 'w')
f1.write(page)
f1.close()
