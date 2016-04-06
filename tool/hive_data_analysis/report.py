
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

field_format="reid, bkt, pageid, fragid,is_ex, is_clk, uid, lc, vid, pid, cid, time_str, recom_str, type, clk_detail"

cmd1 = "hadoop fs -cat /user/rec/ctr_predict/pipeline/0003/rec_0027/20151029/data/recommend_user_activity_log/000000_0 | head -n 1000"
cmd2 = 'mysql -h 117.121.54.220 -P 3308 -u tuijian_read -p"f6w6FSewb2v5gpcy7PGT" -e "use mms;select id,SOURCE_ID,VIDEO_TYPE,PID,PORDER,MID,NAME_CN,SUB_TITLE,DESCRIPTION,TAG,CATEGORY,SUB_CATEGORY,EPISODE,BTIME,ETIME, WATCHING_FOCUS,DURATION,SCORE,RELEASE_DATE,AREA,CREATE_TIME,UPDATE_TIME,UPDATE_UID  from con_video_info where play_platform is not null and id in '
cmd3 = "hive -e \"select %s from dm_rec.tbl_engine_join_day where dt = '20160405' and pt = '0003' and area='rec_0027' and is_ex > 0 and fragid in ('4464','4459','3563') and bkt = '110\:1'\"" % field_format

user_profile={}
for line in open("../../pythonmapreduce/local_user_profile.txt"):
	sp = line.strip().split('\t')
	user_profile[sp[0]]=line


data=os.popen(cmd3).readlines()

for line in data:
	if not line:
		continue

	"%s" % field_format =line.strip().split('\t')
	if len(sp) < 9:
		continue

	table = table+"<tr>"
	table = table+td_template % ("user_id:" + uid)
	table = table+"</tr>"
	table = table + "<tr>"
	table = table + td_template % ("lc:" + lc)
	table = table + "</tr>"

	sql = cmd2 + "(" +sp[7].replace("-",",") + ")\""
	for line1 in os.popen(sql).readlines():
		sp1=line1.strip().split('\t')
		table = table + "<tr>"
		for item in sp1:
			table = table+ td_template % item
		table = table + "</tr>"
	table = table + "<tr>"
	table = table + (td_template%sp[9])
	table = table + "</tr>"


table=table+"</table>"
title="report"

page = html_head + (head_template % title) + "<body>" + table + "</body>"+html_tail

print page
