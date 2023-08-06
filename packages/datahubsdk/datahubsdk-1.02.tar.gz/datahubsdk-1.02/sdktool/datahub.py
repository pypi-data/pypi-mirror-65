# -*- coding: UTF-8 -*-    
from sdktool.util.utils import *
from sdktool.upload import *
from sdktool.checkout import *
# from util.utils import *
# from upload import *
# from checkout import *
from optparse import OptionParser
import json,pprint,traceback,sys,ConfigParser,fcntl

import logging
logging.basicConfig(level=logging.ERROR,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

reload(sys)
sys.setdefaultencoding('utf8')

def getusage():
    usage1 = "usage: %prog [Options] arg1 [Options] arg2 ..."
   
def demoArgs():
    parser = OptionParser(usage=getusage())
    # parser.add_option("-f", "--config", action="store", dest='config',help="加载配置文件")
    # parser.add_option("-p", "--put", action="store_true", dest='put',help="将配置文件里的信息用DataOps管理")
    # parser.add_option("-g", "--get", action="store_true", dest='get',help="获取当前bucket下所有的文件真实cfs路径")
    # parser.add_option("-k", "--keyword", action="store", dest='keyword',help="当-g生效时，查询匹配关键词的路径")   
    parser.add_option("-c", "--checkout",action="store",dest="version",help="根据version来checkout")
    parser.add_option("--project",action="store",dest="project",help="project_id,checkout时必须")
    parser.add_option("-s", "--softlink",action="store_true",dest="softlink",help="checkout需要创建软链")
    parser.add_option("--mnt",action="store",dest="mnt",help="挂载路径，创建软链必须")
    parser.add_option("--dst",action="store",dest="dst",help="checkout 路径")
    parser.add_option("--command",action="store",dest="command",help="命令行参数配置")

    #OpertationConfig
    parser.add_option("--add",action="store",dest="add",help="同git add，添加文件以逗号,分割")
    parser.add_option("--rm",action="store",dest="rm",help="同git rm，删除文件以逗号,分割")
    parser.add_option("--commit",action="store_true",dest="commit",help="同git commit")
    parser.add_option("-m","--message",action="store",dest="message",help="同git message")
    
    #globalConfig
    parser.add_option("--config",action="store_true",dest='config',help="global config配置")
    parser.add_option("--dataunit",action="store",dest='dataunit',help="设置dataunit")
    parser.add_option("--partition",action="store",dest='partition',help="设置partition")
    parser.add_option("--erp", action="store", dest='erp',help="所有涉及到DataOps的操作，erp是必须的！")
    parser.add_option("--projectpath",action="store",dest="projectpath",help="项目路径prefix")
    

    (ori, args) = parser.parse_args()
    if ori.config:
        if ori.dataunit:
            FileConfig.globalconfig("dataunit",ori.dataunit)
            logging.info("dataunit信息已指定")
        if ori.partition:
            FileConfig.globalconfig("partition",ori.partition)
            logging.info("partition信息已指定")
        if ori.erp:
            FileConfig.globalconfig("erp",ori.erp)
            logging.info("erp信息已指定")
        if ori.projectpath:
            FileConfig.globalconfig("projectpath",ori.projectpath)
            logging.info("projectpath信息已指定")
        return
    
    if ori.add or ori.rm:
        if ori.add:
            FileConfig.operationconfig(ori.add,"add")
        if ori.rm:
            FileConfig.operationconfig(ori.rm,"rm")
        return

    if ori.commit:
        if not ori.message:
            logging.error("请提交commit message")
            return
        try:
            fp_global = open(os.getcwd() + "/.store/global.json",'r+')
            fp_basic = open(os.getcwd() + "/.store/basic.json",'r+')
            fp_list = json.load(fp_basic).get("fp_list")
            gconfig = json.load(fp_global)
            a=Upload(gconfig=gconfig,fp_list=fp_list,message=ori.message)
            a.commit()
        except Exception,e:
            logging.error(str(traceback.print_exc()) + "请保证制定了正确的config信息和文件")
            return


    if ori.command:
        config = ConfigParser.ConfigParser()
        config.read(ori.command)
        tmp = config.items("command")
        o={}
        for item in tmp:
            o[item[0]] = item[1]
    else:
        o = vars(ori)
        
    # checkout
    if o.get("version"):
        if not o.get("project") or not o.get("erp"):
            logging.error("提示：checkout版本时，project和erp是必须的")
            return
        if o.get("softlink"):
            if not o.get("mnt"):
                logging.error("提示：创建软链时，挂载路径prefix是必须的")
            else:
                c=Checkout(version=o.get("version"),erp=o.get("erp"),id=str(o.get("project")),mnt_path=o.get("mnt"),dst=o.get("dst"))
                c.checkout_sl()
        else:
            c=Checkout(version=o.get("version"),erp=o.get("erp"),id=str(o.get("project")),mnt_path="",dst="")
            c.checkout()
        return
    
    # #checkin
    # if o.get("config"):
    #     try:
    #         with open(o.get("config"),'r') as f:
    #             fp_list = json.load(f).get("fp_list")
    #             if o.get("put"):
    #                 if not o.get("erp"):
    #                     logging.error("提示：上传文件终止！注意，当上传文件时ERP是必须的！")
    #                     return
    #                 a=Upload(erp=o.get("erp"),fp_list=fp_list)
    #                 a.put_file()
    #     except Exception,e:
    #         print traceback.print_exc()
    #         logging.error("Please make sure the config.json file is correct!")
    #     return
    
    # listall
    if o.get("get"):
        a=Upload()
        a.get_objects(o.get("keyword"))
        return
    
demoArgs()
    
    
    