#!/bin/bash

out_directory=$1
in_directory=$2
model_directory=$3
nmappers=$4
nmappers=100
hadoop fs -rm -r -skipTrash $out_directory 2>&1 > /dev/null 
hadoop fs -rm -r -skipTrash $model_directory 2>&1 > /dev/null
echo $in_directory
echo "hadoop fs -ls $in_directory | awk 'BEGIN{sum = 0} {if(NF > 0) sum += $5;} END{print sum;}'"
total=`hadoop fs -ls $in_directory | awk 'BEGIN{sum = -1} {if(NF > 0) sum += $5;} END{print sum;}'`
echo $nmappers
echo $total
mapsize=`expr $total / $nmappers`
maprem=`expr $total % $nmappers`
mapsize=`expr $mapsize + $maprem`
mapsize=`expr $mapsize + 100`
echo $mapsize

mapper_count=`hadoop fs -ls $in_directory | awk 'BEGIN{sum = 0} {if(NF > 5 && $5 > 1024) sum = sum + 1;} END{print sum;}'`
echo $mapper_count

#./spanning_tree

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -Dmapreduce.input.fileinputformat.split.minsize=$mapsize -Dmapreduce.map.speculative=true -Dmapreduce.job.reduces=$nmappers -input $in_directory -output $out_directory -file ./mapper_batch_fea.py -file ./reducer_batch_fea.py -mapper ./mapper_batch_fea.py -reducer ./reducer_batch_fea.py

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -Dmapreduce.input.fileinputformat.split.minsize=$mapsize -Dmapreduce.map.speculative=true -Dmapreduce.job.reduces=0 -Dmapreduce.map.memory.mb=3000 -Dmapred.child.java.opts="-Xmx100m" -Dmapreduce.task.timeout=600000000 -input $out_directory -output $model_directory -file ./vw -file ./runvw.sh -mapper ./runvw.sh -reducer NONE

#hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -Dmapreduce.input.fileinputformat.split.minsize=$mapsize -Dmapreduce.map.speculative=true -Dmapreduce.job.reduces=0 -Dmapreduce.map.memory.mb=3000 -Dmapred.child.java.opts="-Xmx100m" -Dmapreduce.task.timeout=600000000 -input $in_directory -output $out_directory -file ./mapper_merge_fea.py -mapper ./mapper_merge_fea.py -reducer NONE
