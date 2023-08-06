import random,pprint,os,fcntl,time
from util.Config import *
from util.utils import BasicConfig

MAX = 100*100*100*10
FNAME = 'test0324del.txt'

def genfile():
    fp = open(FNAME,'w+')
    for i in range(MAX):
        fp.write(str(random.randint(0,MAX)) + "\n")
    fp.close()

# genfile()
def cc():
    # api = prefix + "/projects/single?projectIdOrPath="
    # r = BasicConfig.deal_get(api+"18")
    # print r
    # r = BasicConfig.path2id("datahub_search/full_data")
    # path = os.getcwd() + "/gg.json"
    # print path
    # fp = open(path,'a+')
    # fcntl.flock(fp, fcntl.LOCK_EX)
    # fp.write(str(time.time()))
    # time.sleep(10)
    # fp.write(str(time.time()))
    # fcntl.flock(fp, fcntl.LOCK_UN)
    # fp.close()
    print BasicConfig.calhash('test0312small.txt')
cc()
    
