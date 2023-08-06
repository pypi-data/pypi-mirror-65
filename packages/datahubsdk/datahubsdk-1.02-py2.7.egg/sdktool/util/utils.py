import os,boto3,requests,json,time,hashlib
from Config import *

class BasicConfig(object):
    def __init__(self):
        pass

    @staticmethod
    def get_client():
        session = boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        client = session.client(service_name="s3", region_name=region_name, endpoint_url=endpoint)
	return client

    @staticmethod
    def get_resource():
        session = boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        resource = session.resource(service_name="s3", region_name=region_name, endpoint_url=endpoint)
	return resource

    @staticmethod
    def deal_post(url,datas):
        # print url,datas
        r = requests.post(url,json.dumps(datas))
        if r.status_code != 200:
            return r.status_code
        else:
            return r.text

    @staticmethod
    def deal_get(url):
        # print url
        r = requests.get(url)
        if r.status_code != 200:
            return r.status_code
        else:
            # print r.text
            return json.loads(r.text)

    @staticmethod
    def calsize(fp):
        fsize = os.path.getsize(fp)
        result = round(float(fsize)/(1024*1024), 1)
        if result > 1024:
            return str(round(float(fsize)/(1024*1024*1024), 1)) + "GB"
        return str(result) + "MB"

    @staticmethod
    def path2id(path):
        if path.isdigit():
            return path
        path = "/".join(path.split("/")[:2])
        url = prefix + "/projects/single?projectIdOrPath=" + path
        # print url
        r = BasicConfig.deal_get(url)
        return str(r['data'].get("project_id"))

    @staticmethod
    def calhash(fp):
        if os.path.isfile(fp+".hash"):
            hash_code = open(fp+".hash",'r').read().strip()
            return hash_code
        f = open(fp,'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        return hash_code

    @staticmethod
    def usage():
        print "if you have any question,plz ask zhangyuhao25@jd.com"

class FileConfig(object):
    def __init__(self):
        pass
    
    @staticmethod
    def globalconfig(k,v):
        fp,content = FileConfig.openconfig('global.json')
        content[k] = v
        json.dump(content,fp)
        print fp,content
        fp.close()

    @staticmethod
    def operationconfig(file_path,op):
        fp,content = FileConfig.openconfig('basic.json')
        a={}
        a["op"] = op
        a["fp"] = file_path
        a["hash"] = BasicConfig.calhash(file_path)
        content["fp_list"].append(a)
        json.dump(content,fp)
        # print fp,content
        fp.close()

    @staticmethod
    def openconfig(infile):
        # fcntl.flock(fp, fcntl.LOCK_EX)
        dir = os.getcwd() + "/.store"
        if not os.path.isdir(dir):
            os.mkdir(dir)
        file_path = dir + "/" + infile
        if not os.path.isfile(file_path):   
            fp = open(file_path,'w+')
            if "global" in infile.split("/")[-1]:  
                return fp,{}
            elif "basic" in infile.split("/")[-1]:
                return fp,{"fp_list":[]}
        else:
            fp = open(file_path,'r+')
            a=json.load(fp)
            fp.seek(0)
            fp.truncate()
            return fp,a

    # @staticmethod
    # def closeConfig(fp):
    #     # fcntl.flock(fp, fcntl.LOCK_UN)
    #     fp.close()
