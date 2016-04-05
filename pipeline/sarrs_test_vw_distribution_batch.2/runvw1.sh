#!/bin/bash
mapper=`printenv mapred_task_id | cut -d "_" -f 5`
rm -f temp.cache
chmod 755 vw
date +"%F %T Start training mapper=$mapper" > /dev/stderr
echo $mapred_map_tasks > /dev/stderr
echo $mapreduce_job_submithost > /dev/stderr
echo $mapred_output_dir > /dev/stderr
echo $mapreduce_task_output_dir > /dev/stderr
echo $mapreduce_map_input_file > /dev/stderr
vwcmd="./vw --total 300 --node $mapper --cache_file temp.cache --span_server 10.148.12.11 --noconstant --l1 0.1 --l2 0.1 --loss_function=logistic --holdout_off"
mapred_job_id=`echo $mapred_job_id | tr -d 'job_'`
gdcmd="$vwcmd -b 24 --unique_id $mapred_job_id --passes 10 --adaptive -d /dev/stdin -f tempmodel"
mapred_job_id=`expr $mapred_job_id \* 2` #create new nonce
bfgscmd="$vwcmd --unique_id $mapred_job_id --bfgs --mem 5 --passes 50 -f model --readable_model model.text -i tempmodel"
if [ "$mapper" == '000000' ]; then
    echo "gd training "$gdcmd > /dev/stderr
    $gdcmd > mapperout 2>&1
    if [ $? -ne 0 ]; then
      date +"%F %T Failed mapper=$mapper cmd=$gdcmd" > /dev/stderr
      exit 1
    fi
    echo "bfgs training "$bfgscmd > /dev/stderr
    $bfgscmd >> mapperout 2>&1
    if [ $? -ne 0 ]; then
      date +"%F %T Failed mapper=$mapper cmd=$gdcmd" > /dev/stderr
      exit 1
    fi
    outfile=$mapreduce_task_output_dir/model
    outfile_readable=$mapreduce_task_output_dir/model.text
    mapperfile=$mapreduce_task_output_dir/mapperout
    found=`hadoop fs -lsr | grep $mapreduce_task_output_dir | grep mapperout`
    if [ "$found" != "" ]; then
      hadoop fs -rm -r $mapperfile
    fi
    found=`hadoop fs -lsr | grep $mapreduce_task_output_dir | grep model`
    if [ "$found" != "" ]; then
      hadoop fs -rm -r $outfile
    fi
    date +"%F %T outfile=$outfile" > /dev/stderr
    hadoop fs -put model $outfile
    hadoop fs -put model.text $outfile_readable
    hadoop fs -put mapperout $mapperfile
else
    $gdcmd
    if [ $? -ne 0 ]; then
      date +"%F %T Failed mapper=$mapper cmd=$gdcmd" > /dev/stderr
      exit 1
    fi
    $bfgscmd
    if [ $? -ne 0 ]; then
      date +"%F %T Failed mapper=$mapper cmd=$gdcmd" > /dev/stderr
      exit 1
    fi
fi
date +"%F %T Done mapper=$mapper" > /dev/stderr
