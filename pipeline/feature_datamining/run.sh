#!/bin/bash
cd `dirname $0`
source /etc/profile

count_threshold=1
data_start=
if [ $# -ge 1 ]
then
	if [ $# -ge 1 ]
	then
		data_start=$1
	fi
else
	echo $#
	echo $@
	echo 'wrong argv'
	exit
fi


rm -f media_info.txt dictionary_info.txt
mysql -h 117.121.54.220 -P 3308 -u tuijian_read -p"f6w6FSewb2v5gpcy7PGT" -e "use mms;select concat('4_',id), sub_category from con_video_info where can_search = 1 and play_platform != '' and not isnull(play_platform) and site like '%650001%'  and source_id!=200003" > media_info.txt
mysql -h 117.121.54.220 -P 3308 -u tuijian_read -p"f6w6FSewb2v5gpcy7PGT" -e "use mms;select concat('1_',id), sub_category from con_album_info where can_search = 1 and play_platform != '' and not isnull(play_platform) and site like '%650001%'  and source_id!=200003" >> media_info.txt
mysql -h 117.121.54.220 -P 3308 -u tuijian_read -p"f6w6FSewb2v5gpcy7PGT" -e "use mms;select id, value from db_dictionary_info" > dictionary_info.txt

# statistic

server_log_path=/data/rec/log/server_log/online_by_day/*/*/sarrs_*/*
cnt=0
total=0
server_log_path_with_input=""
mining_date=$data_start
while [ $cnt -lt 60 ]
do
    mining_date=`date -d $mining_date' -1 day' +%Y%m%d`
    server_log_path_one_day=/data/rec/log/server_log/online_by_day/$mining_date/*/sarrs_*/*
    server_log_path_with_input=$server_log_path_with_input' -input '$server_log_path_one_day
    cnt=`expr $cnt + 1`
done
echo $server_log_path_with_input

user_activity_output_path=/data/rec/ctr_predict/data_mining/feature_mining/user_activity_output_path/


hadoop fs -rm -r -skipTrash $user_activity_output_path
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=100 $server_log_path_with_input -output $user_activity_output_path -mapper mapper_user_activity.py -reducer reducer_user_activity.py -file mapper_user_activity.py -file reducer_user_activity.py -file media_info.txt -file dictionary_info.txt
rm -f user_weight.txt
hadoop fs -cat ${user_activity_output_path}part* | awk -F '\t' '{print $1"\t"$4}' | sort -u > user_weight.txt

feature_distribution_in_people=/data/rec/ctr_predict/data_mining/feature_mining/feature_distribution_in_people/
hadoop fs -rm -r -skipTrash $feature_distribution_in_people
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=100 -input $user_activity_output_path -output $feature_distribution_in_people -mapper mapper_feature_in_people_distribution.py -reducer reducer_feature_in_people_distribution.py  -file mapper_feature_in_people_distribution.py -file reducer_feature_in_people_distribution.py
rm -f feature_count.txt
hadoop fs -cat ${feature_distribution_in_people}part* | awk -F '\t' '{print $1"\t"$2"\t"$3}' > feature_count.txt


# item cf

itemcf_pair=/data/rec/ctr_predict/data_mining/feature_mining/itemcf_pair/
hadoop fs -rm -r -skipTrash $itemcf_pair
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=100 $server_log_path_with_input -output $itemcf_pair -mapper mapper_user_activity.py -reducer reducer_item_pair_gen.py -file mapper_user_activity.py -file reducer_item_pair_gen.py -file media_info.txt -file dictionary_info.txt

itemcf_res=/data/rec/ctr_predict/data_mining/feature_mining/itemcf_res/
hadoop fs -rm -r -skipTrash $itemcf_res
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=100 -input $itemcf_pair -output $itemcf_res -mapper mapper_output_throught.py -reducer reducer_itemcf_gen.py -file mapper_output_throught.py -file reducer_itemcf_gen.py -file user_weight.txt -file feature_count.txt

post process

cnt=1
while [ $cnt -lt 15 ]
do
    hadoop fs -cat {$itemcf_res}part* | python result_postprocess.py $cnt > res_{$cnt}.txt
    cnt=`expr $cnt + 1`
done
