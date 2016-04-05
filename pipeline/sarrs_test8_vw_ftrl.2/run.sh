#!/bin/bash
cd `dirname $0`
source /etc/profile

start_date=
end_date=
pipeline='pipeline'
if [ $# -ge 5 ]
then
	if [ $# -ge 1 ]
	then
		start_date=$1
	fi
	if [ $# -ge 2 ]
	then
		end_date=$2
	fi
	if [ $# -ge 3 ]
	then
		pt=$3
	fi
	if [ $# -ge 4 ]
	then
		rec_area=$4
	fi
	if [ $# -ge 5 ]
	then
		pipeline=$5
	fi
else
	echo $#
	echo $@
	echo 'wrong argv'
	exit
fi

date_array=()
i=0
total=0
training_date=$start_date
while [ $training_date -le $end_date ]
do
	date_array[$i]=$training_date
    echo $training_date
	let i++
	training_date=`date -d $training_date' +1 day' +%Y%m%d`
done

echo "total $i days"

for date_item in ${date_array[@]}
{
	echo $date_item
    ./run_session_log.sh $date_item $pt $rec_area $pipeline
    ./feature_process.sh $date_item $pt $rec_area $pipeline
    #./predict.sh $date_item $pt $rec_area $pipeline
    ./model_train.sh $date_item $pt $rec_area $pipeline
}


