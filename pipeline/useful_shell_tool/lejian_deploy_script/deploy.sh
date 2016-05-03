#!/bin/bash

#set -x
iplist=("10.180.91.218")
version="v2"
dt=`date +%Y%m%d`

for ip in $iplist
do
echo $ip
echo $dt

#servingroot
serving_root_binary_name=serving_root_${dt}_$version
experiment_file_name=experiment.conf_${dt}_$version
run_shell_file_name=run_serving_root.sh_${dt}_$version
scp serving_root/bin/serving_root rec@$ip:~/data/recommendation/leview/serving_root/bin/${serving_root_binary_name}
scp serving_root/conf/experiment.conf rec@$ip:~/data/recommendation/leview/serving_root/conf/${experiment_file_name}
scp serving_root/conf/leview_detail_parameter.conf rec@$ip:~/data/recommendation/leview/serving_root/conf/
scp serving_root/sbin/run_serving_root.sh rec@$ip:~/data/recommendation/leview/serving_root/sbin/${run_shell_file_name}
ssh rec@$ip "cd ~/data/recommendation/leview/serving_root/bin/; rm -f serving_root; ln -s ${serving_root_binary_name} serving_root"
ssh rec@$ip "cd ~/data/recommendation/leview/serving_root/conf/; mv experiment.conf ${experiment_file_name}_backup; ln -s ${experiment_file_name} experiment.conf"
ssh rec@$ip "cd ~/data/recommendation/leview/serving_root/sbin/; mv run_serving_root.sh ${run_shell_file_name}_backup; ln -s ${run_shell_file_name} run_serving_root.sh"

#restart
ssh rec@$ip "cd ~/data/recommendation/leview/serving_root/sbin/; sh restart.sh"


#engine
engine_binary_name=sarrs_rec_${dt}_$version
engine_conf_name=server.cfg_${dt}_$version
engine_flags_name=engine.flags_${dt}_$version
engine_run_shell_file_name=run_sarrs_rec.sh_${dt}_${version}
scp engine/bin/sarrs_rec rec@$ip:~/data/recommendation/leview/engine/bin/${engine_binary_name}
scp engine/conf/server.cfg rec@$ip:~/data/recommendation/leview/engine/conf/${engine_conf_name}
scp engine/conf/engine.flags rec@$ip:~/data/recommendation/leview/engine/conf/${engine_flags_name}
scp engine/sbin/run_sarrs_rec.sh rec@$ip:~/data/recommendation/leview/engine/sbin/${engine_run_shell_file_name}
ssh rec@$ip "cd ~/data/recommendation/leview/engine/bin/; rm -f sarrs_rec; ln -s ${engine_binary_name} sarrs_rec"
ssh rec@$ip "cd ~/data/recommendation/leview/engine/conf/; mv server.cfg ${engine_conf_name}_backup; ln -s ${engine_conf_name} server.cfg"
ssh rec@$ip "cd ~/data/recommendation/leview/engine/conf/; mv engine.flags  ${engine_flags_name}_backup; ln -s ${engine_flags_name} engine.flags"
ssh rec@$ip "cd ~/data/recommendation/leview/engine/sbin/; mv run_sarrs_rec.sh ${engine_run_shell_file_name}_backup; ln -s ${engine_run_shell_file_name} run_sarrs_rec.sh"


scp engine/data/category_area_feature_count.txt rec@$ip:~/data/recommendation/leview/engine/data/
scp engine/data/category_feature_count.txt rec@$ip:~/data/recommendation/leview/engine/data/
scp engine/data/category_subcategory_area_feature_count.txt rec@$ip:~/data/recommendation/leview/engine/data/
scp engine/data/category_subcategory_feature_count.txt rec@$ip:~/data/recommendation/leview/engine/data/
scp engine/data/subcategory_feature_count.txt rec@$ip:~/data/recommendation/leview/engine/data/

#restart
ssh rec@$ip "cd  ~/data/recommendation/leview/engine/sbin/; sh restart.sh"

done



