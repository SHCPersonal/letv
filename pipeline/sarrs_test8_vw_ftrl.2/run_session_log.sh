#!/bin/bash
cd `dirname $0`
source /etc/profile 


function check_result(){
    if [ $? -ne 0 ]
    then
        echo 'check result false'
        exit
    fi
}



mode=''
pt='0003'
rec_area='rec_0027'
pipeline='pipeline'
end=
if [ $# -ge 4 ]
then
	if [ $# -ge 1 ]
	then
		training_date=$1
	fi
	if [ $# -ge 2 ]
	then
		pt=$2
	fi
	if [ $# -ge 3 ]
	then
		rec_area=$3
	fi
	if [ $# -ge 4 ]
	then
		pipeline=$4
	fi
	if [ $# -ge 5 ]
	then
		end=$5
	fi

else
	echo $#
	echo $@
	echo 'wrong argv'
	exit
fi

today_date=$training_date
yesterday_date=`date -d $training_date' -1 day' +%Y%m%d`
user_profile_date=`date -d $training_date' -1 day' +%Y%m%d`
tomorrow_date=`date -d $training_date' +1 day' +%Y%m%d`


hadoop_binary=hadoop 
hdfs_bin_dir=/data/rec/ctr_predict/bin/
session_log_data=/data/rec/log_analyze/expose_click/protobuf/1_${today_date}_${tomorrow_date}
hadoop_work_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/data 
hadoop_work_last_day_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$user_profile_date/data
hadoop_work_user_activity_path=$hadoop_work_path/training_sample
hadoop_work_unique_user_path=$hadoop_work_path/unique_user
input_user_profile=/data/rec/profile/inc/$user_profile_date/
output_user_profile=$hadoop_work_path/user_profile
echo "user profile path:"
echo $input_user_profile

if [ $today_date -lt 20151202 ]
then 
	server_log_path=/data/rec/log/server_log/online_by_day/${today_date}-*/sarrs_log*
else 
	server_log_path=/data/rec/log/server_log/online_by_day/${today_date}/*/sarrs_*/*
fi

echo "server_log_path"
echo $server_log_path

server_click_log_path=$hadoop_work_path/server_click_log

#setup the folder
hadoop fs -mkdir -p $hadoop_work_user_activity_path

hadoop fs -rm -r -skipTrash $server_click_log_path
hadoop fs -cat $server_log_path | python mapper_server_log_parser.py | sort -u > server.log
hadoop fs -mkdir $server_click_log_path
hadoop fs -put server.log $server_click_log_path/part-00000


mysql -h 117.121.54.220 -P 3308 -u tuijian_read -p"f6w6FSewb2v5gpcy7PGT" -e "use mms;select id,pid from con_video_info where pid is not null" > vid_info.txt

hadoop fs -rm -r -skipTrash $hadoop_work_user_activity_path
hadoop fs -mkdir $hdfs_bin_dir
cmd="./new_session_log_extractor
     --auto_run
     --num_mapper=100
     --num_reducer=20
     --input_format=kv_text
     --output_format=text
     --hdfs_output_dir=$hadoop_work_user_activity_path
     --hdfs_input_paths=$session_log_data,$server_click_log_path
     --enable_multi_mapper_output=false
     --hdfs_bin_dir=$hdfs_bin_dir
     --hadoop_binary=$hadoop_binary
     --lib_jars=./custom_format_1_1_2.jar
     --uploading_files=./vid_info.txt
     --compatible_mod=false
     --compress_map_output=false
     --compress_mapper_out_value=false
     --fileoutput_compress=false
     --shuffle_input_buffer_percent=0.5
     "
echo $cmd
$cmd
hadoop fs -cat $hadoop_work_user_activity_path/part* | awk -F '\t' '{print $3; print $4}' | sort -u > local_unique_user.txt

hadoop fs -rm -r -skipTrash $output_user_profile
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=0 -input $input_user_profile/* -output $output_user_profile -mapper ./mapper_get_userprofile.py -file ./mapper_get_userprofile.py -file ./local_unique_user.txt

hadoop fs -cat  $output_user_profile/part* | awk -F '\t' '{print $1}' > user_list.txt

#--uploading_files=../rec_media_doc_info.txt,../recvid_rate.txt,../itemcf.txt

start_date=`date -d $training_date' -7 day' +%Y%m%d`
end_date=`date -d $training_date' +0 day' +%Y%m%d`
session_log_data_batch=/data/rec/log_analyze/expose_click/protobuf/7_${start_date}_${end_date}
echo "ctr data path:"
echo $session_log_data_batch
session_log_ctr=$hadoop_work_path/session_ctr

cmd="./session_log_ctr_aggregator
      --auto_run
      --num_mapper=100
      --num_reducer=50
      --hdfs_server=hadoopNN1.com
      --hdfs_host=hdfs://webdm-cluster
      --hdfs_port=9000
      --input_format=kv_text
      --output_format=text
      --hdfs_output_dir=$session_log_ctr
      --hdfs_input_paths=$session_log_data_batch
      --enable_multi_mapper_output=false
      --hdfs_bin_dir=$hdfs_bin_dir
      --hadoop_binary=$hadoop_binary
      --lib_jars=./custom_format_1_1_2.jar
      --compatible_mod=false
      --compress_map_output=false
      --compress_mapper_out_value=false
      --fileoutput_compress=false
      --shuffle_input_buffer_percent=0.5
    "
#echo $cmd
#$cmd
#hadoop fs -getmerge $hadoop_work_path/session_ctr full_rate.txt
#awk '$4 > 20 {print $1, $2, $3, $4}' full_rate.txt | python ctr_feature_normalize.py > recvid_rate.txt
hadoop fs -rm -r -skipTrash $session_log_ctr
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -input $hadoop_work_last_day_path/training_sample -output $session_log_ctr -mapper mapper_item_ctr.py -reducer reducer_item_ctr.py -file mapper_item_ctr.py -file reducer_item_ctr.py
