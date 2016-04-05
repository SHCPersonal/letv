#!/bin/bash
cd `dirname $0`
source /etc/profile

x=$1
#inpath=/user/rec/ctr_predict/data/test
inpath=$2
user_profile=$3
outpath=$4
today_date=`date -d '1 days ago' +%Y%m%d`

hadoop fs -rm -r -skipTrash $outpath/${x}_train


hadoop_binary=hadoop                                                                                             
hdfs_bin_dir=/data/rec/ctr_predict/bin/

cmd="./simple_mapreduce_test
     --auto_run
     --num_mapper=100
     --num_reducer=30
     --input_format=text
     --output_format=text
     --hdfs_output_dir=$outpath/${x}_train
     --hdfs_input_paths=$inpath/*,$user_profile/*
     --enable_multi_mapper_output=false
     --hdfs_bin_dir=$hdfs_bin_dir
     --hadoop_binary=$hadoop_binary
     --lib_jars=./custom_format_1_1_2.jar
     --uploading_files=../rec_media_doc_info.txt,../recvid_rate.txt
     --compatible_mod=false
     --compress_map_output=false
     --compress_mapper_out_value=false
     --fileoutput_compress=false
     --shuffle_input_buffer_percent=0.5
     --feature_builder_type=SarrsExtraLabelFeatureBuilder
     "
echo $cmd
$cmd
