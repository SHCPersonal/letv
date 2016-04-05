#!/usr/bin/python
import sys
import random
import time
import urlparse

for line in sys.stdin:
	sp=line.strip().split("\t")
	if (sp[:-1] == "user_activity_log"):
		reid=sp[0].split('_', 1)[0]
		print reid + '\t' + line
	else:
		if sp[2].startwith("action=click&"):
			result=urlparse.urlparse("http://www.baidu.com/?"+sp[2])
			params=urlparse.parse_qs(result.query,True)
			
