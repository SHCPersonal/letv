#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import base64

sys.path.append("../lib")
#sys.path.append("../lib/thrift_python")
sys.path.append("../lib/site-packages/proto")
sys.path.append("../python_module")
sys.path.append("../gen-py")
reload(sys)
sys.setdefaultencoding( "utf-8" )


from thrift_util import *
from serving.mediadocinfo.ttypes import *
import pysst

def feature_map_parse(feature_dict):
	category=''
	subcategory=''
	actor=''
	director=''
	guest=''
	compere=''
	leword=''
	tag=''

	for key in feature_dict.keys():
		if key.startswith("CATEGORY_"):
			category=category+key[9:]+','
		elif key.startswith("SUBCATEGORY_"):
			subcategory=subcategory+key[12:]+','
		elif key.startswith("ACTOR_"):
			actor=actor+key[6:]+','
		elif key.startswith("DIRECTOR_"):
			director=director+key[9:]+','
		elif key.startswith("GUEST_"):
			guest=guest+key[6:]+','
		elif key.startswith("COMPERE_"):
			compere=compere+key[8:]+','
		elif key.startswith("LEWORD_"):
			keword=leword+key[7:]+','
		elif key.startswith("TAG_"):
			tag=tag+key[4:]+','

	return category+'\t'+subcategory+'\t'+actor+'\t'+director+'\t'+guest+'\t'+compere+'\t'+leword+'\t'+tag


def media_doc_info_parse(source_file, output_file, error_file, vid_dict):
	print source_file
	f_out = open(output_file, 'w')
	if not f_out:
		print "failed to open output file!"
		return
	f_error = open(error_file, 'w')
	if not f_error:
		print "failed to opend error file"
		return

	source_sst = pysst.SSTReader(source_file)
	media_doc_info_list = []
	while source_sst.IterValid():
		k = source_sst.GetCurKey()
		if not k in vid_dict:
			source_sst.IterNext()
			continue
		value=source_sst.GetCurValue()
		#v = FromStringToThrift(MediaDocInfo, value)
		source_sst.IterNext()
		try:
			f_out.write(k+'\t0\t'+base64.b64encode(value))
			#f_out.write(k+'\t0\t'+)
			f_out.write('\n')
			pass
		except:
			print sys.exc_info()
			f_error.write("bad value:"+value+'\n')
	return media_doc_info_list

sst_file_path = sys.argv[1]
vid_list = sys.argv[2]
vid_dict={}
for line in open(vid_list):
	vid_dict[line.strip()]=1

out_file_path = "rec_media_doc_info.txt"
error_file_path = "error.txt"
res_list = media_doc_info_parse(sst_file_path,out_file_path, error_file_path, vid_dict)



