import os
import sys
import time
import json
import requests
import pprint
import boto3
from util.utils import BasicConfig
from util.Config import *

'''
format:date/group/project/filename/timestamp.uuid/file
example:20200304/search/knn/knn_blacklist/1583326408.b4fbcfdc00f846cc9d7469de95a4d413/knn_blacklist.txt
'''


class Upload(object):
    def __init__(self,gconfig={}, fp_list=[],message=""):
        self.erp = gconfig.get("erp")
        self.dataunit = gconfig.get("dataunit")
        self.partition = gconfig.get("partition")
        self.projectpath = gconfig.get("projectpath").split(",")
        self.fp_list = fp_list
        self.api_1 = prefix + "/projects/single?projectIdOrPath="
        self.api_2 = prefix + "/projects/meta/upload"
        self.api_3 = prefix + "/projects/dimensions/save"
        self.meta = {"erp": self.erp, "meta": [], "deleted": []}
        self.dimension = {"erp": self.erp, "dimension": []}
        self.message = message

    def genkey(self,fp, hashv, id_one):
        fp_file = fp.split("/")[-1]
        fp_filename = fp_file.split(".")[0]
        today = time.strftime('%Y%m%d', time.localtime())
        ts = str(int(time.time())) + "." + hashv
        r = BasicConfig.deal_get(self.api_1 + str(id_one))
        if isinstance(r, int) or r['code'] != "200":
            return r
        group, project = r['data'].get(
            "group_name", ""), r['data'].get("project_name", "")
        result = "/".join(list((today, group, project,
                          fp_filename, ts, fp_file)))
        return result

    def commit(self):
        resource = BasicConfig.get_resource()
        for item in self.fp_list:
            if item.get("op") == "add":
                if item.get("fp").endswith("/*"):
                    self.put_dir(item, resource)
                else:
                    self.put_single(item, resource)
            # del no need cfs-operation
            if item.get("op") == "del":
                if item.get("fp").endswith("/*"):
                    self.del_dir(item)
                else:
                    self.del_single(item)
        if not self.meta.get("deleted"):
            del self.meta["deleted"]
        # pprint.pprint(self.meta)
        # pprint.pprint(self.dimension)
        r_meta = BasicConfig.deal_post(self.api_2, self.meta)
        r_dimension = 200
        if self.dimension.get("dimension"):
            r_dimension = BasicConfig.deal_post(self.api_3, self.dimension)
        if r_meta == 500 or r_dimension == 500:
            return False
        return True

    # Del Files and dirs
    def del_dir(self, item):
        with open(item.get('hash')) as f:
            lines = f.readlines()
            for line in lines:
                hashv, fp = line.strip().split("\t")
                self.del_single(item, hashv, fp.lstrip("./"))

    def del_single(self,item,hashv='',fp=''):
        if not hashv and not fp:
            fp,hashv = item.get("fp"),item.get("hash")
        for project_path in self.projectpath:
            project_id = BasicConfig.path2id(project_path)
            del_one = {"project_id":project_id,"filePath":os.path.join(project_path,fp)}
            self.meta["deleted"].append(del_one)
       
    # Add Files and dirs   
    def put_dir(self,item,resource):
        # TODO add /*
        with open(item.get('hash')) as f:
            lines = f.readlines()
            for line in lines:
                hashv,fp = line.strip().split()
                self.put_single(item,resource,hashv,fp.lstrip("./"))
    
    def put_single(self,item,resource,hashv="",fp=""):
        if not hashv and not fp:
            fp= item.get("fp")
            hashv = BasicConfig.calhash(os.getcwd() + "/" + fp)
        size = BasicConfig.calsize(fp)
        # For multi projects, one id is needed
        id_one = self.projectpath[0]
        cfs_path = self.genkey(fp,hashv,id_one)
        try:
            t1 = time.time()
            resource.Bucket(bucket).upload_file(fp,cfs_path)
            t2 = time.time()
            print "Upload file " + str(fp) + " costs " + str(t2-t1)
        except:
            return False
        for project_path in self.projectpath:
            project_id = BasicConfig.path2id(project_path)
            meta_item = {"size":size,"filePath":os.path.join(project_path,fp),"hash":hashv,"cfspath":cfs_path,"project_id":project_id}
            if self.dataunit:
                meta_item["dataunit"] = self.dataunit
            if self.partition:
                meta_item["partition"] = self.partition
            self.meta["meta"].append(meta_item)
                                       
    def get_objects(self,query=None):
        resource = BasicConfig.get_resource()
        buckets = resource.Bucket(bucket)
        for item in buckets.objects.all():
            if not query or query in item.key:
                print item.key


# with open("basic.json",'r') as f:
#     fp_list = json.load(f).get("fp_list")
# a=Upload(erp='zhangyuhao25',fp_list=fp_list)
# # a.get_objects("0324")
# a.put_file()
