#!/bin/bash
cd `dirname $0`
source /etc/profile

x=$1
#inpath=/user/rec/ctr_predict/data/test
inpath=$2
user_profile=$3
outpath=$4
today_date=`date -d '1 days ago' +%Y%m%d`

hadoop fs -rm -r -skipTrash $outpath/${x}_train


hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=300 -input $inpath/* -input $user_profile/* -output $outpath/${x}_train -mapper ./map_feature.py -reducer ./get_fea.py -file map_feature.py  -file get_fea.py -file ../rec_media_doc_info.txt -file ../recvid_rate.txt -file ./happy_to_see_recommender_feature_builder
