
from progressbar import *
from upyun import *
import os, requests, time, sqlite3



# 源仓库配置
st1_name = "wxywebbg"
st1_operator = "tesy"
st1_password = "rZCXcDpkBxUsHvyH6ULjAhFbWpmmNope"
st1_link = "https://bf.wxydejoy.top"

# 目标仓库配置
st2 = True
st2_name = ""
st2_operator = ""
st2_password = ""
st2_link = ""

# 本地配置
local = True
local_dir = "local/"  # 本地相对路径


# 继承原upyun类

# class UpYun(object):
#     def __init__(self, service, username=None, password=None,
#                  auth_server=None, timeout=None, endpoint=None,
#                  chunksize=None, debug=False, read_timeout=None,
#                  encrypt_pwd=None):

class ProgressBarHandler(object):
    def __init__(self, totalsize, params):
        widgets = [params, Percentage(), ' ',
                   Bar(marker='=', left='[', right=']'), ' ',
                   ETA(), ' ', FileTransferSpeed()]
        self.pbar = ProgressBar(widgets=widgets, maxval=totalsize).start()

    def update(self, readsofar):
        self.pbar.update(readsofar)

    def finish(self):
        self.pbar.finish()



class Myupy(UpYun):
    # 列举仓库所有目录
    # [{'name': '404.html', 'type': 'N', 'size': '34388', 'time': '1633352699'}, {'name': 'CNAME', 'type': 'N', 'size': '12', 'time': '1633352700'}
    finallist = []
    dirlist = ['']
    conn = sqlite3.connect('file.db')
    cur = conn.cursor()
    

    def list_all(self, now_dir="/"):
        if 'upyun_storage_log' in now_dir:
            return
        for i in self.getlist(now_dir):
            if i["type"] == "N":
                i["name"] = now_dir + i["name"]
                self.finallist.append(i)
            else:
                j = i
                self.dirlist.append(now_dir + j['name'])
                # j['name'] = now_dir + j['name']
                self.list_all(now_dir=now_dir + i["name"] + "/")

        # {'name': '/page/10/index.html', 'type': 'N', 'size': '50752', 'time': '1633352724'},
    def mkdir_all(self):

        for i in self.dirlist:
            if not os.path.exists(local_dir+i):
                os.makedirs(local_dir+i)


    def download_all(self,local_dir):
        for i in self.finallist:
            with open(local_dir+i["name"], 'wb') as f:
                up.get(i["name"], f, handler=ProgressBarHandler, params='Uploading ')


    def async_download(self):
        pass

up = Myupy(st1_name, st1_operator, st1_password)

res = up.list_all()
up.mkdir_all()
up.download_all(local_dir)

# print(os.getcwd())


# print(type(res), res, up.finallist)
# print(up.dirlist)