import sys
sys.path.append("./")
reload(sys)

import feature_build 

str_list=["abc","eefe","sssse"]
tmplll=feature_build.TmpData()
tmplll.append("abc")
tmplll.append("ddd")
p=feature_build.PythonUtil()
res=feature_build.PythonUtil.test(p, tmplll)
print res
