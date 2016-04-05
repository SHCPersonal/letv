#!/bin/bash

cd `dirname $0`
echo $0
source /etc/profile

training_date=
mode=''
pt='0003'
rec_area='rec_0027'
pipeline='pipeline'
model_file=model
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
	echo 'wrong argv in the predict.sh'
	exit
fi

today_date=$training_date
inpath=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/merge


rm detail_predict_feature.txt
hadoop fs -get $inpath/part-00001 detail_predict_feature.txt
cat detail_predict_feature.txt |./ftrl/ftrl_predict_std $model_file local_out
echo $training_date >> new_result.txt
cat local_out|./scoreKDD.py >> new_result.txt
                                                     
