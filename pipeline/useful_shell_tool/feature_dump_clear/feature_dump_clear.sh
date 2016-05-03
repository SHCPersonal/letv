#!/bin/bash

#set -x

dt=`date -d ' -1 day' +%Y%m%d`
echo $dt


for ip in `cat iplist.txt`
do
  echo $ip
  ssh rec@$ip "cd ~/data/recommendation/leview/engine/log/feature_dump; du -h;"
  ssh rec@$ip "cd ~/data/recommendation/leview/engine/log/feature_dump; rm -rf $dt;"
done


