
from progressbar import *
from upyun import *
import os, requests, time, sqlite3


# 只下载和上传，不删除，也就是说不需要删除权限

# 源仓库配置
st1_name = "wxywebbg"
st1_operator = "tesy"
st1_password =
st1_link = "https://bf.wxydejoy.top"

# 目标仓库配置
st2 = True
st2_name = "wxyundf"
st2_operator = "tesy"
st2_password =
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
    download_ed = []  # 本地的
    download_now = [] # 刚下的


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


    def down_now_update(self):
        str_list = []
        for i in self.download_now:
            str_list.append(i['name']+'\n')

        if not os.path.exists('file.txt'):
            f = open('file.txt', 'w')
            f.writelines(str_list)
            f.close()
        else:
            f = open('file.txt', 'a+')
            f.writelines(str_list)
            f.close()


    def down_befor_update(self):
        if os.path.exists('file.txt'):
            f = open('file.txt', 'r')
            self.download_ed = f.readlines()
            f.close()


    def sync_download(self,local_dir):
        self.finallist = []
        self.download_ed = []
        self.list_all() # 获取全部文件列表 finallist     [{'name': '/page/10/index.html', 'type': 'N', 'size': '50752', 'time': '1633352724'},
        self.down_befor_update() # download_ed 获取本地文件列表
        print(self.finallist,self.download_ed)
        self.mkdir_all() # 创建文件夹
        for i in self.finallist:
            if i['name']+'\n' not in self.download_ed:
                with open(local_dir + i["name"], 'wb') as f:
                    up.get(i["name"], f, handler=ProgressBarHandler, params='Downloading ')
                    self.download_now.append(i)
        self.down_now_update()

    def sync_upload(self,local_dir):
        self.sync_download(local_dir)
        res2 = Myupy(st2_name, st2_operator, st2_password)
        res2.finallist = [] # remote
        self.download_ed = [] # local
        res2.list_all()  # 获取全部文件列表 finallist     [{'name': '/page/10/index.html', 'type': 'N', 'size': '50752', 'time': '1633352724'},
        self.down_befor_update()  # download_ed 获取本地文件列表
        res2list = []
        if res2.finallist != []:
            for i in self.finallist:
                res2list.append(i['name'])

        for i in self.download_ed:
            if i.replace('\n','') not in res2list:
                with open(local_dir + i.replace('\n',''), 'rb') as f:
                    res2.put(i.replace('\n',''), f)












up = Myupy(st1_name, st1_operator, st1_password)

up.sync_upload(local_dir)




#up.download_all(local_dir)

#print(up.finallist)
# up.down_update()
# print(os.getcwd())


# print(type(res), res, up.finallist)
# print(up.dirlist)
