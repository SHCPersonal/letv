#!/bin/bash
cd `dirname $0`
source /etc/profile 

#sunhaochuan, 20150916
#description

#the day before today
training_date=

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


#start to collect the training data
today_date=$training_date 
echo $today_date
user_profile_date=`date -d $training_date' -1 day' +%Y%m%d` 
echo $user_profile_date
hadoop_work_path=/user/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/data
hadoop_work_user_activity_path=$hadoop_work_path/recommend_user_activity_log
hadoop_work_unique_user_path=$hadoop_work_path/unique_user
input_user_profile=/user/resys/profile/inc/$user_profile_date/0/
output_user_profile=$hadoop_work_path/user_profile
#firstly collect user activity log form database data_rec, table tbl_engine_join_day

hadoop fs -mkdir -p $hadoop_work_user_activity_path
if [ -n "$end" ]
then
	today_date=`date -d $end' days ago' +%Y%m%d`
	hive_sql="use data_rec; INSERT OVERWRITE DIRECTORY '$hadoop_work_user_activity_path' select reid, uid, lc, vid, pid, cid, time_str, recom_str, type, clk_detail  from tbl_engine_join_day where cast (dt as int) between '$today_date' and pt = '$pt' and area='$rec_area' and is_ex = 1"
else

	hive_sql="use data_rec; INSERT OVERWRITE DIRECTORY '$hadoop_work_user_activity_path' select reid, uid, lc, vid, pid, cid, time_str, recom_str, type, clk_detail  from tbl_engine_join_day where dt = '$today_date' and pt = '$pt' and area='$rec_area' and is_ex = 1"
fi


echo "Start the job with the SQL as below:"
echo "$hive_sql"
echo 
echo hive -e "$hive_sql" hadoop_cmd="jar /usr/local/hadoop/lib/hadoop-mapred-1.1.2.jar org.apache.hadoop.streaming.HadoopStreaming  -D mapred.output.compress=0 -D mapred.reduce.tasks=0 -input $hadoop_work_user_activity_path/* -output $hadoop_work_unique_user_path -mapper ./get_unique_user.py  -file get_unique_user.py" hadoop fs -rm -r -skipTrash $hadoop_work_unique_user_path hadoop fs -mkdir -p $hadoop_work_path/$today_date

echo "Start to collect unique user hadoop job with cmd as below:"
echo "$hadoop_cmd"
echo
echo

hadoop jar /usr/local/hadoop/lib/hadoop-mapred-1.1.2.jar org.apache.hadoop.streaming.HadoopStreaming  -D mapred.output.compress=0 -input $hadoop_work_user_activity_path/* -output $hadoop_work_unique_user_path -mapper ./get_unique_user_mapper.py -reducer ./get_unique_user_reducer.py  -file get_unique_user_mapper.py -file get_unique_user_reducer.py

hadoop fs -getmerge $hadoop_work_unique_user_path ./local_unique_user.txt

hadoop fs -rm -r -skipTrash $output_user_profile
hadoop jar /usr/local/hadoop/lib/hadoop-mapred-1.1.2.jar org.apache.hadoop.streaming.HadoopStreaming  -D mapred.output.compress=0 -D mapred.reduce.tasks=0 -input $input_user_profile/* -output $output_user_profile -mapper ./mapper_get_userprofile.py -file ./mapper_get_userprofile.py -file ./local_unique_user.txt

hadoop fs -cat  $output_user_profile/part* | awk -F '\t' '{print $1}' > user_list.txt

#cd  ../test
hadoop fs -rm -r -skipTrash $hadoop_work_path/training_sample
# thirdly format the user activity log
hadoop jar /usr/local/hadoop/lib/hadoop-mapred-1.1.2.jar org.apache.hadoop.streaming.HadoopStreaming  -D mapred.output.compress=0 -D mapred.reduce.tasks=0 -input  $hadoop_work_user_activity_path/* -output $hadoop_work_path/training_sample -mapper ./mapper_sample.py  -file mapper_sample.py -file user_list.txt


