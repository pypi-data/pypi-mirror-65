import os,sys,json
import boto3
from util.utils import BasicConfig
from util.Config import *
import pprint

class Checkout(object):
    def __init__(self,version,erp,id,mnt_path="",dst=""):
        self.version = version
        self.id = id
        self.prefix_url = prefix + "/projects/single?projectIdOrPath="
        self.erp = erp        
        self.mnt_path = mnt_path
        self.dst = dst

    def get_prefix(self):
        url = self.prefix_url + self.id
        r = BasicConfig.deal_get(url)
        if isinstance(r, int) or r['code'] != "200":
            return r
        group, project = r['data'].get(
            "group_name", ""), r['data'].get("project_name", "")
        return group + "/" + project + "/"

    def checkout(self):
        if self.id.isdigit():
            prefix_path = self.get_prefix()
            project_id = self.id
        else:
            project_id = BasicConfig.path2id(self.id)
        url = prefix+"/projects/"+project_id+"/deploy/checkout?erp="+self.erp+"&ref="+self.version
        r = BasicConfig.deal_get(url)
        result = {}
        for item in r['meta']:
            for k,v in item.items():
                try:
                    v = json.loads(v)
                    filepath,cfspath = prefix_path + v.get("filePath"),v.get("cfspath")
                    if filepath and cfspath:
                        # print filepath + "\t" + cfspath
                        result[filepath] = cfspath
                except:
                    pass
        return result

    def checkout_sl(self):
        r = self.checkout()
        # if self.dst.startswith("."):
        #     self.dst += os.getcwd() + self.dst.lstrip("./") + "/"
        dir = "/".join(self.dst.split("/")[:-1])
        if not os.path.exists(dir):
            os.mkdir(dir)
        for k,v in r.items():
            src,dst = os.path.join(self.mnt_path,v),os.path.join(self.dst,k)
            self.soft_link(src,dst)

    #softlink needs to be done by YWers
    def soft_link(self,src,dst):
        if os.path.islink(dst):
            os.unlink(dst)
        else:
            dir = "/".join(dst.split("/")[:-1])
            if not os.path.exists(dir):
                os.makedirs(dir)
            os.symlink(src,dst)

# a=Checkout(version="master",erp="zhangyuhao25",id="5",mnt_path="/mnt/cfs/",dst="/home/admin/zyh/test")
# r = a.checkout()
# for k,v in r.items():
#     print k,v
# a.checkout_sl()

