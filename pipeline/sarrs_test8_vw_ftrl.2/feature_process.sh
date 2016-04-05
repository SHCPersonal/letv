#!/bin/bash

cd `dirname $0`
source /etc/profile

inpath=
user_profile=
outpath=
training_date=
#sst_file_source='rec@10.130.91.79:/home/rec/data/recommendation/mobile_recommender/data/rec_media_doc_info.dat'
#sst_file_source='rec@10.180.92.86:/letv/home/rec/deploy/video_pipeline/pipeline/data/repo/media_doc_info.sst'
sst_file_source='rec@10.200.91.72:/home/rec/data/recommendation/leview/engine/dynamic_data/media_doc_info.sst'

mode=''
pt='0003'
rec_area='rec_0027'
pipeline='pipeline'
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
else
	echo $#
	echo $@
	echo 'wrong argv'
	exit
fi

today_date=$training_date
inpath=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/data/training_sample
user_profile=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/data/user_profile
outpath=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train

echo "copy the rec sst file"
rm -rf rec_meida_doc_info.sst
hadoop fs -get /data/rec/video_pipeline/adapter/mediadocinfo/full/media_doc_info_${today_date}*.sst rec_media_doc_info.sst
if [ ! -f rec_media_doc_info.sst ]
then
    echo "can not get the sst file from hadoop"
    scp $sst_file_source ./rec_media_doc_info.sst
else
    echo "get the sst file from hadoop"
fi
hadoop fs -cat $inpath/part* | awk -F "\t" '{print $8; print $6; print $5}' | sort -u > vid_list.txt
./media_doc_info_parser.py rec_media_doc_info.sst vid_list.txt
rm -rf rec_media_doc_info.sst

hadoop fs -rm -r -skipTrash $outpath/mr_fea*_train
hadoop fs -mkdir -p $outpath

echo "1"

hadoop fs -getmerge /data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/data/session_ctr full_rate.txt
awk '$4 > 20 {print $1, $2, $3, $4}' full_rate.txt | python ctr_feature_normalize.py > recvid_rate.txt

echo "2"
#local feature
#for x in `ls |grep ^fea_`
#do
#	echo $x
#	cd $x
	#hadoop fs -cat $inpath/part* | ./get_fea.py part-00000 &
#	cd ..
#done

echo "3"
# hdfs feature
for x in `ls |grep ^mr_fea_`
do
	echo $x
	cd $x
	./run_mapreduce_bin.sh $x $inpath $user_profile $outpath
	cd ../
done
wait
#check_status

######### put local_fea on hdfs ############
#for x in `ls |grep ^fea_`
#do
#	echo $x
#	hadoop fs -rm -r -skipTrash $outpath/mr_${x}_train
#	hadoop fs -mkdir $outpath/mr_${x}_train
#	hadoop fs -put -f $x/part-00000 $outpath/mr_${x}_train
#	rm $x/part-00000
#done

############特征合并 #######
hadoop fs -rm -r -skipTrash $outpath/merge
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=180 -input $outpath/mr_*_train -output $outpath/merge -mapper ./mapper_merge_fea.py  -reducer ./reducer_merge_fea.py -file mapper_merge_fea.py -file reducer_merge_fea.py

hadoop fs -rm -r -skipTrash $outpath/statistic/count_fea
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0 -D mapred.reduce.tasks=120 -input $outpath/merge -output $outpath/statistic/count_fea -mapper ./mapper_count_fea.py  -reducer ./reducer_count_fea.py -file mapper_count_fea.py -file reducer_count_fea.py
#hadoop fs -cat  $outpath/statistic/count_fea/part* > count_fea
