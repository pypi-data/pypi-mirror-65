import paramiko
import stat
from pyprobar import probar, bar
from guang.Utils.toolsFunc import yaml_load, yaml_dump
import os


class Cloud:
    def __init__(self, config_path="config.yaml"):
        param_dict = yaml_load(config_path)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(**param_dict)
        self.sftp = self.client.open_sftp()

        self.remote_res = {"path": [], "abspath": [], "dir": []}
        self.local_res = {"path": [], "abspath": [], "dir": []}
        self.cwd = os.getcwd()
        self.remote_cwd = self.sftp.getcwd()


    def local_walk(self, local_path, one=1):
        """custommized os.walk()
        return a dict with `path` `abspath` and `dir`.

        """
        if one == 1:
            self.local_root = os.path.abspath(local_path)

        path_list = os.listdir(local_path)
        for idx, _path in enumerate(path_list):
            path = os.path.join(local_path, _path)
            if os.path.isfile(path):  # file
                self.local_res["abspath"].append(os.path.abspath(path))
            elif os.path.isdir(path):  # dir
                self.local_res["dir"].append(os.path.abspath(path))
                self.local_walk(path, one=2)
            else:
                print(f"{path} can't recognise, skipped")

        return self.local_res

    def remote_walk(self, remote_path, one=1):
        """
        return a dict with `path` `abspath` and `dir`.

        """
        if one == 1:
            self.remote_root = remote_path
        path_attr = self.sftp.listdir_attr(remote_path)

            # S_ISLNK(st_mode)：是否是一个连接.
            # S_ISREG(st_mode)：是否是一个常规文件.
            # S_ISDIR(st_mode)：是否是一个目录
            # S_ISCHR(st_mode)：是否是一个字符设备.
            # S_ISBLK(st_mode)：是否是一个块设备
            # S_ISFIFO(st_mode)：是否 是一个FIFO文件.
            # S_ISSOCK(st_mode)：是否是一个SOCKET文件

        for i in path_attr:

            path = os.path.join(remote_path, i.filename).replace('\\', '/')

            if stat.S_ISDIR(i.st_mode):  # dir
                self.remote_res["dir"].append(path)
                self.remote_walk(path, one=2)
            elif stat.S_ISREG(i.st_mode):

                self.remote_res["abspath"].append(path)
                self.remote_res["path"].append(i.filename)

            else:
                print(f"{path} can't recognise, skipped")

        if one == 1:
            self.sftp.chdir()
        return self.remote_res

    #     def remove_except(self, except_path, path_type='dir'):
    #         """remove except directory from self.path_res
    #         path_type: `dir` or `file`
    #         """
    #         for ex in except_path:
    #             if path_type is "dir":
    #                 for j in self.path_res["dir"]:
    #                     if ex == j[-len(ex):]:
    #                         self.path_res["dir"].remove(j)
    #             elif path_type is "file":
    #                 for idx, j in enumerate(self.path_res["path"]):
    #                     if ex == j[-len(ex):]:
    #                         self.path_res["path"].remove(j)
    #                         self.path_res["abspath"].pop(idx)
    #             else:
    #                 print(f"{path} can't recognise, skipped")

    def get_remote_path(self, path_type='dir'):
        """path_type: `relpath`, `abspath`, `dir`, `reldir`
        """
        L = len(self.remote_root)
        if path_type == "dir":
            return self.remote_res["dir"]

        elif path_type == "reldir":
            abs_dir = self.remote_res["dir"]
            rel_dir = [i.replace(i[:L+1], '') for i in abs_dir]
            # rel_dir = [i.replace(self.remote_root, '') for i in abs_dir]
            # rel_dir = [i[1:] if i[0] is '/' else i for i in rel_dir]
            return rel_dir

        elif path_type == "relpath":
            abspath = self.remote_res["abspath"]
            relpath = [i.replace(i[:L+1], '') for i in abspath]

            return relpath

        elif path_type == "abspath":
            return self.remote_res["abspath"]
        else:
            raise ValueError("parameter path_type is illegal")

    def get_local_path(self, path_type='dir'):
        """path_type: `relpath`, `abspath`, `reldir`, `dir`
         """
        L = len(self.local_root)
        if path_type == "reldir":
            reldir = []
            for res_dir in self.local_res["dir"]:
                reldir.append(res_dir.replace(res_dir[:L+1], ''))
            return reldir

        elif path_type == 'dir':
            return self.local_res["dir"]

        elif path_type == "relpath":
            abspath = self.local_res["abspath"]
            relpath = [i.replace(i[:L+1], '') for i in abspath]
            return relpath

        elif path_type == "abspath":
            return self.local_res["abspath"]
        else:
            raise ValueError("parameter path_type is illegal")

    def create__local_dir(self, dirs):
        for i in dirs:
            if os.path.exists(i):
                pass
            else:
                os.makedirs(i)
                print(f"{i} not exist, is creating")
        print('\n')

    def create_remote_dir(self, dirs):
        for i in dirs:
            try:
                self.sftp.stat(i)
            except:
                # self.sftp.mkdir(i) # sftp.mkdir can't create malti-layer directories
                self.client.exec_command(f"mkdir -p {i}")
                print(f"{i} not exist, is creating")
        print('\n')


    def judge_update(self, remote, local, load = "download"):
        """ Judge  if the file is synchronized with remote file and local's.
        `load` options: "download" ,"upload"
        return True if update else False
        """

        if load == "download":
            remote_stat = self.sftp.stat(remote)
            remote_size, remote_time = remote_stat.st_size, remote_stat.st_mtime
            try:
                local_stat = os.stat(local)
                local_size, local_time = local_stat.st_size, local_stat.st_mtime
                if remote_time >= local_time and remote_size != local_size:
                    return True
                else:
                    return False
            except:
                return True
        elif load == "upload":
            local_stat = os.stat(local)
            local_size, local_time = local_stat.st_size, local_stat.st_mtime
            try:
                remote_stat = self.sftp.stat(remote)
                remote_size, remote_time = remote_stat.st_size, remote_stat.st_mtime
                if remote_time <= local_time and remote_size != local_size:
                    return True
                else:
                    return False
            except:
                return True


    def download(self):

        _dir = self.get_remote_path('reldir')
        _dir = [os.path.join(self.local_root, i).replace("\\", '/') for i in _dir]
        self.create__local_dir(_dir)

        _remote = [i.replace('\\', '/') for i in self.get_remote_path('abspath')]
        _local = [os.path.join(self.local_root, i).replace("\\", '/') for i in self.get_remote_path('relpath')]

        # split _remote and _local here, and then add multiple threads
        idx = 0
        for remote, local in zip(_remote, _local):
            if self.judge_update(remote, local, "download"):
                print(f"local file:{os.path.basename(local)} will be updated", end='')
                self.sftp.get(remote, local)
            bar(idx, len(_local))
            idx += 1

    def upload(self):

        _dir = self.get_local_path("reldir")
        _dir = [os.path.join(self.remote_root, i).replace("\\", '/') for i in _dir]
        self.create_remote_dir(_dir)

        _local = [i.replace('\\', '/') for i in self.get_local_path("abspath")]
        _remote = [os.path.join(self.remote_root, i).replace('\\', '/') for i in self.get_local_path("relpath")]

        # # split _remote and _local here, and then add multiple threads
        idx = 0
        for local, remote in zip(_local, _remote):
            if self.judge_update(remote, local, "upload"):
                print(f"remote file:{os.path.basename(local)} will be updated", end='')
                self.sftp.put(local, remote)
            bar(idx, len(_local))
            idx += 1


if __name__ == "__main__":
    cloud = Cloud()
    cloud.remote_walk('/home/ubuntu/github/academic-kickstart')

    cloud.local_walk('download')
    # cloud.download() # will download the files under academic-kickstart to `download`
    cloud.upload() # will upload the files under `download`folder to `academic-kickstart`
    # pass
