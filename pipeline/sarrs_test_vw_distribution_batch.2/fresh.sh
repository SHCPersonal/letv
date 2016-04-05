rm -f new_session_log_extractor
wget http://10.11.144.116:8002/source/tp/build64_release/shared/pipeline/algorithm/ya_item_cf/mapreduce/new_session_log_extractor
chmod 755 new_session_log_extractor

rm -f session_log_ctr_aggregator
wget http://10.11.144.116:8002/source/tp/build64_release/shared/pipeline/algorithm/ya_item_cf/mapreduce/session_log_ctr_aggregator
chmod 755 session_log_ctr_aggregator
