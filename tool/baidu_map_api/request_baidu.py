# -*- coding:utf-8 -*-
import sys
import httplib
import json

def request(parameter):
    conn = httplib.HTTPConnection("api.map.baidu.com")  
    conn.request("GET", parameter)  
    r1 = conn.getresponse()
    return r1.read()
    print r1.status, r1.reason
    return ;
    #200 OK  
    data1 = r1.read()  
    conn.request("GET", "/parrot.spam")  
    r2 = conn.getresponse()  
    print r2.status, r2.reason  
    #404 Not Found  
    data2 = r2.read()  
    conn.close()

#http://www.jb51.net/article/43400.htm
    
class company_detail(object):
    def __init__(self):
        self.id=''
        self.name=''
        self.register=''
        self.address=''
        self.response_data=''
    #the response result from baidu
        self.status=''
        self.lng=''
        self.lat=''
        self.precise=''
        self.confidence=''
        self.level=''
        
    def load_from_line(self, line):
        sp = line.strip().split('\t')
        self.id = sp[0]
        self.name = sp[1]
        self.register = sp[2]
        self.address = sp[3]
    def dump_to_line(self):
        return  self.id+'\t'+self.name+'\t'+self.address+'\t'+str(self.status)+'\t'+str(self.lng)+'\t'+str(self.lat)+'\t'+str(self.precise)+'\t'+str(self.confidence) + '\n'
        
    def ping_baidu_api(self):
        url_format="/geocoder/v2/?address=%s&output=json&ak=VG7BdpOZLwxlaSlSVe21gn2MEbQ8B8Gw"
        request_url = url_format % (self.address)
        dong="栋"
        request_url1 = request_url.replace('#', dong)
        self.response_data = request(request_url1)
        
    def josn_parse(self):
        try:
            j=json.loads(self.response_data) #load function need the input with read() interface
            self.status=j['status']
            self.lng=j['result']['location']['lng']
            self.lat=j['result']['location']['lat']
            self.precise=j['result']['precise']
            self.confidence=j['result']['confidence']
            self.level=j['result']['level']
        except Exception,e:
            print 'Failed to parse the json result: ' + self.address 
            print e


def load_company_address(file_path):
    res = []
    for line in open(file_path):
        com = company_detail()
        com.load_from_line(line)
        res.append(com)
    return res
    
def dump_to_file(res,file_path):
    lines=[]
    for company in res:
        line=company.dump_to_line()
        lines.append(line)
    f = open(file_path, "w")
    f.writelines(lines)
    f.close()
    
company_list=load_company_address("test.txt")
for com in company_list:
    com.ping_baidu_api()
    com.josn_parse()
dump_to_file(company_list, "res.txt")


 
 