#
#sunhaochuan 20150923
cd `dirname $0`
source /etc/profile

training_date=
mode=''
pt='0003'
rec_area='rec_0027'
pipeline='pipeline'
lambda1=0.5

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
		lambda1=$5
	fi
else
	echo $#
	echo $@
	echo 'wrong argv'
	exit
fi

today_date=$training_date
#inpath=/user/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/merge
inpath=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/*/train/merge
#count_fea_path=/user/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/statistic/count_fea
count_fea_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/*/train/statistic/count_fea
model_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area

ftrl=./ftrl/ftrl_train_std_model_based

rm -f model
#hadoop fs -get $model_path/model model
echo 'start to get count'
hadoop fs -cat $count_fea_path/part* | awk -F "\t" '$2>100 {print $0}' > model_key
echo 'finish getting count'
key_num=`wc -l model_key | awk '{print $1}'`
if [ $key_num -lt 10000 ]
then
	echo 'too few modle key in training data (less than 10000)'
	exit
fi

touch model
./prepair_model.py model model_key > new_model
mv new_model model
hadoop fs -cat $inpath/part* | $ftrl new_model model --alpha=0.05 --lambda1=$lambda1 --lambda2=10 --thread=2
#check_status
file_num=`wc -l new_model|awk '{print $1}'`
if [ $file_num -lt 1000 ]
then
	echo 'wrong model'
	exit
else
	awk '$2!=0{print $0}' new_model > model
fi

#hadoop fs -put -f model $model_path/$today_date/${today_date}_model
hadoop fs -put -f model $model_path/model
hadoop fs -put -f recvid_rate.txt $model_path/recvid_rate.txt

rm -rf detail_predict_feature.txt
hadoop fs -get $inpath/part-00001 detail_predict_feature.txt
cat detail_predict_feature.txt |./ftrl/ftrl_predict_std model local_out
echo $training_date >> result.txt
cat local_out|./scoreKDD.py >> result.txt

#copy the model and ohter data file to target
#scp ./model rec@10.130.91.79:/home/rec/data/recommendation/mobile_recommender_ctr_predict/data/personalized_ctr_predict_model.dat
#scp ./recvid_rate.txt rec@10.130.91.79:/home/rec/data/recommendation/mobile_recommender_ctr_predict/data/recvid_rate.txt
