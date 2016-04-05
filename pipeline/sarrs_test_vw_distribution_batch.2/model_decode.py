#sunhaochuan 20150921
import sys

id_key_dict={}
dict_path=sys.argv[1]
for line in open(dict_path):
    sp = line.strip().split('\t')
    id = int(sp[1])
    id_key_dict[id]=sp[0]

for line in sys.stdin:
    sp=line.strip().split(':')
    if len(sp) == 2 and sp[0].isdigit():
        print id_key_dict[int(sp[0])] + '\t' + sp[1] + '\t0\t0\t0\t0'
        
