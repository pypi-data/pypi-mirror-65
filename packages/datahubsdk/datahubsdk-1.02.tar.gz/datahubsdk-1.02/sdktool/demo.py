from util.utils import *
from upload import *
from checkout import *


def demoUp():
    with open("basic.json",'r') as f:
        fp_list = json.load(f).get("fp_list")
    a=Upload(erp='zhangyuhao25',fp_list=fp_list)
    # get all files in the bucket
    a.get_objects()
    # put file in the format AS fp_list above
    a.put_file()


def demoDown():
    a = Checkout(version="master", erp="zhangyuhao25",
                 id="1", mnt_path="/mnt/cfs/")
    result = a.checkout()
    for k, v in result.items():
        print k, v


def demoDel():
    pass


if __name__ == '__main__':
    BasicConfig.usage()
    # demoUp()
    # demoDown()
    # demoDel()
