#!/usr/bin/python
#coding=utf-8
from __future__ import division
import sys
sys.path.append("../lib")
#sys.path.append("../lib/thrift_python")
sys.path.append("../lib/site-packages/proto")
sys.path.append("../python_module")
sys.path.append("../gen-py")
reload(sys)

from serving.mediadocinfo.ttypes import *
import pysst
#from ttypes import *
from thrift_util import *

if len(sys.argv) < 2:
	print "usage: ./check_key.py *.sst key"
	sys.exit()

old_sst = pysst.SSTReader(sys.argv[1])
print "sst_before_gen_time",old_sst.GetMetaData("sst_before_gen_time")

# get one key result.
print FromStringToThrift(MediaDocInfo, old_sst.Get(sys.argv[2]))


