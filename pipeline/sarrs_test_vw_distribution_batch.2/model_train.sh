#!/bin/bash
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
inpath=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/mr_fea_sst_cc_train
inpath=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/mr_fea_sst_cc_train
merge_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/merge
count_fea_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/statistic/count_fea
encode_fea_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area/$today_date/train/encode
model_path=/data/rec/ctr_predict/$pipeline/$pt/$rec_area


# 1.encode the training data
echo "1.encode the training data"
rm -f key_id.dict
rm -f key_id.dict.new
hadoop fs -get $model_path/key_id.dict
if [ ! -f key_id.dict ]
then
    touch key_id.dict
fi
echo $count_fea_path/part*
hadoop fs -cat $count_fea_path/part* | awk -F "\t" '$2>100 {print $0}' | python ./key_convert.py key_id.dict
key_num=`wc -l model_key | awk '{print $1}'`
if [ $key_num -lt 10000 ]
then
	echo 'too few modle key in training data (less than 10000)'
	exit
fi
hadoop fs -rm -r -skipTrash $encode_fea_path
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapred.output.compress=0  -Dmapreduce.input.fileinputformat.split.minsize=1024 -D mapreduce.tasktracker.map.tasks.maximum=30 -D mapred.reduce.tasks=0 -Dmapreduce.map.memory.mb=3000 -input $inpath -output $encode_fea_path -mapper ./mapper_encode_fea.py -file ./mapper_encode_fea.py -file ./model_key -file ./key_id.dict.local


# predict next day
if [ -f model.binary ]
then
    echo "predict the next day"
    hadoop fs -cat $encode_fea_path/part* | ./vw -t --hash strings -i model.binary -p predict.res
    cat predict.res | python ./predict_parser.py > local_out
    echo $training_date >> new_result.txt
    echo "vw predict" >> new_result.txt
    cat local_out | ./scoreKDD.py >> new_result.txt
    rm -rf predict.res local_out


    rm -rf detail_predict_feature.txt
    hadoop fs -cat $merge_path/part* |./ftrl/ftrl_predict_std model local_out
    echo $training_date >> new_result.txt
    echo "no_vw predict" >> new_result.txt
    cat local_out|./scoreKDD.py >> new_result.txt
    rm -rf detail_predict_feature.txt local_out
fi
###########################
:<<BLOCK
# 2.training the model
echo "2.training the model"
init=
bit_precision='-b 24'
rm -f model.binary
rm -f model.binary.new
rm -f model.text
rm -f model.text.new
hadoop fs -get $model_path/model.binary
if [ -f model.binary ]
then
    init='-i model.binary'
    bit_precision=''
fi
rm -rf model.binary.new model.text.new temp.cache
echo "init: $init"
echo "bit_precision: "$bit_precision

ftrl="./vw $bit_precision --ftrl --cache_file temp.cache --l1 0.2 --l2 0.1 --ftrl_alpha 0.05 --ftrl_beta 1.0 --passes 2 --noconstant --hash strings $init --loss_function logistic -f model.binary.new --readable_model model.text.new"
sgd="./vw -b 31 --cache_file temp.cache --l1 0.2 --l2 0.1 --passes 1 --hash strings $init --loss_function logistic model.binary.new --readable_model model.text.new"
bfgs="./vw -b 31 --bfgs --cache_file temp.cache --l1 0.2 --l2 0.1 --passes 10 --hash strings $init --loss_function logistic -f model.binary.new --readable_model model.text.new"
hadoop fs -cat $encode_fea_path/part* | $ftrl

file_num=`wc -l model.text.new | awk '{print $1}'`
if [ ! -f model.text.new -o $file_num -lt 1000 ]
then
	echo 'wrong model'
	exit
fi
BLOCK


# 3. mv the temp data
echo "3. mv the temp data"
#mv model.binary.new model.binary
#mv model.text.new model.text
mv key_id.dict.new key_id.dict

:<<BLOCK
# 4. use vw to do predict
echo "4. use vw to do predict"
hadoop fs -cat $encode_fea_path/part* | ./vw -t --hash strings -i model.binary -p predict.res
cat predict.res | python ./predict_parser.py > local_out
echo $training_date" vw predict">> result.txt
cat local_out | ./scoreKDD.py >> result.txt
rm -rf predict.res local_out

# 5. decode the model
echo "5. decode the model"
cat model.text | python ./model_decode.py key_id.dict > model

# 6. use no-vw to do predict
echo "6. use no-vw to do predict"
rm -rf detail_predict_feature.txt
hadoop fs -cat $merge_path/part* |./ftrl/ftrl_predict_std model local_out
echo $training_date" non_vw predict">> result.txt
cat local_out|./scoreKDD.py >> result.txt
rm -rf detail_predict_feature.txt local_out

rm -rf detail_predict_feature.txt
hadoop fs -cat $merge_path/part* | python logistic_predict.py model > local_out
echo $training_date" linear predict">> result.txt
cat local_out|./scoreKDD.py >> result.txt
rm -rf detail_predict_feature.txt local_out

BLOCK

#hadoop fs -put -f model.binary $model_path/$today_date/${today_date}_model.binary
#hadoop fs -put -f model.binary $model_path/model.binary
#hadoop fs -put -f model.text $model_path/$today_date/${today_date}_model.text
#hadoop fs -put -f model.text $model_path/model.text
hadoop fs -put -f key_id.dict $model_path/$today_date/${today_date}_key_id.dict
hadoop fs -put -f key_id.dict $model_path/key_id.dict
#hadoop fs -put -f model $model_path/$today_date/${today_date}_model
#hadoop fs -put -f model $model_path/model
#hadoop fs -put -f recvid_rate.txt $model_path/$today_date/${today_date}_recvid_rate.txt
#hadoop fs -put -f recvid_rate.txt $model_path/recvid_rate.txt
