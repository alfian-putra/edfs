#!/usr/bin/python3

import os
import sys
import subprocess
import shutil
import tarfile

edfs_home = os.environ["EDFS_HOME"]
lib_path = os.path.join(edfs_home, "lib")
#add pythonpath
sys.path.append(edfs_home)
sys.path.append(lib_path)

from lib.yaml_parser import CONFIG
from lib.connection_handler import CONN

# INIT
# init dir
# init json
# distribute datanode
#   - create tmp dir "datanode"
#   - copy all in this dir to datanode dir
#   - remove bin
#     ignored file in datanode
#   - pack datanode to datanode.tar.gz
#   - unpack using ssh datanode/* to edfs_home

class INIT():
    def __init__(self):
        self.conf = CONFIG()
        self.con_handler = CONN()

    def _write_to_file(self, filename, content):
        f = open(filename, "w")
        f.write(content)
        f.close()
        return

    def _init_json_filemapping(self):
        data = '{ "files" : []}'
        fullpath = os.path.join(self.conf.edfs_home,"metadata/filemapping.json")
        self._write_to_file(fullpath, data)

    def _init_json_metadata(self):
        data = '{ "files" : [ { "name": "/" , "type": "directory" } ]}'
        fullpath = os.path.join(self.conf.edfs_home,"metadata/metadata.json")
        self._write_to_file(fullpath, data)

    def _init_json_hostmapping(self):
        data = '{ "hosts" : []}'
        fullpath = os.path.join(self.conf.edfs_home,"metadata/hostmapping.json")
        self._write_to_file(fullpath, data)

    def init_all_host(self):
        # ssh
        def _ssh(host,cmd):
            cmd = f"ssh root@{host} {cmd}"
            run_cmd = subprocess.run(cmd.split(" "))
        
        for host in self.conf.datanode_host:
            _ssh(host, "yum install -y python3-pip")
            _ssh(host, f"pip3 install -r {self.conf.edfs_home}/requirements")

    def init_datanode_tarbal(self):
        #create dir
        def create_dir(dirname): 
            if not os.path.exists(dirname):
                os.mkdir(dirname)

        #copy dir or file
        def copy_dir(target, dest):
            try:
                shutil.copytree(target, dest)
            except Exception as err:
                print(err)

        #copy dir or file
        def copy_file(target, dest):
            try:
                shutil.copyfile(target, dest)
            except Exception as err:
                print(err)

        #delete dir or file
        def remove(target):
            os.remove(target)

        #this dir
        parent_dir = os.getcwd()

        #datanode build dir
        datanode_builddir = os.path.join(parent_dir, "datanode/")

        #list needed package
        ls_pkg = ["bin","conf","example","lib","data","log","metadata","pid"]
        ls_file = ["requirements"]

        #ignored file in datanode
        ls_datanode_ignore = ["bin/nameserver", "bin/edfs.py"]

        # 1. create build dir
        create_dir(datanode_builddir)

        # 2. copy dir to build dir
        for i in  ls_pkg:
            fullpath = os.path.join(parent_dir, i)
            full_datanode_builddir = os.path.join(datanode_builddir,i)
            copy_dir(fullpath, full_datanode_builddir)

        # 3. copy file
        for i in  ls_file:
            fullpath = os.path.join(parent_dir, i)
            full_datanode_builddir = os.path.join(datanode_builddir,i)
            copy_file(fullpath, full_datanode_builddir)

        # 4. datanode : remove unused
        for i in ls_datanode_ignore:
            fullpath = os.path.join(datanode_builddir,i)
            remove(fullpath)

        # 5. create tarbal
        tarbal = tarfile.open("datanode.tar.gz", "w")
        for elm in ls_pkg:
            fullpath = os.path.join("datanode/",elm)
            tarbal.add(fullpath)
        for elm in ls_file:
            fullpath = os.path.join("datanode/",elm)
            tarbal.add(fullpath)

        tarbal.close()
        shutil.rmtree("datanode/")
    
    def distribute_datanode(self):
        # scp host
        def _scp(host,file):
            cmd = f"scp {file} root@{host}:/opt"
            run_cmd1 = subprocess.run(cmd.split(" "))

        # ssh
        def _ssh(host,cmd):
            cmd = f"ssh root@{host} {cmd}"
            run_cmd = subprocess.run(cmd.split(" "))

        def distribute_to_host(host):
            # create edfs path dir in datanode host
            _ssh(host, f"mkdir -p {self.conf.edfs_home}")
            # scp tarbal to /opt (/opt/datanode.tar.gz)
            _scp(host, "datanode.tar.gz")
            # ssh tar -xvf /opt/datanode.tar.gz
            _ssh(host, "tar -xvf /opt/datanode.tar.gz -C /opt/")
            # ssh cp -r /opt/datanode/* {edfs_home}
            _ssh(host, f"cp -r /opt/datanode/* {self.conf.edfs_home}")
            # ssh rm -rf /opt/datanode/ datanode.tar.gz
            _ssh(host, "rm -rf /opt/datanode /opt/datanode.tar.gz")            

        for host in self.conf.datanode_host:
            if host==self.conf.nameserver_host:
                continue
            distribute_to_host(host)
        

    def init_dir(self):
        ls = ["data","metadata","log","pid"]
        for d in ls:
            fullpath = os.path.join(self.conf.edfs_home, d)
            if not os.path.exists(fullpath):
                os.mkdir(fullpath)

    def init_json(self):
        self._init_json_filemapping()
        self._init_json_metadata()
        self._init_json_hostmapping()
        self.init_datanode_tarbal()

    def init_cluster(self):
        try:
            self.init_dir()
            self.init_json()
            self.distribute_datanode()
            self.init_all_host()
        except Exception as e:
            print(f"ERROR : {e}")
        else:
            print("Init complete !")
        finally:
            run_cmd = subprocess.run("rm -rf datanode datanode.tar.gz".split(" "))

class UPDATE():
    def __init__(self):
        self.conf = CONFIG()
        self.con_handler = CONN()
        
    def update_json(self):
        lsjson = ["filemapping", "hostmapping","metadata"]

        #def _read_json_api(filename):
        #    return self.con_handler.nameserver_json(filename).decode("utf-8")

        def _write_to_json(filename):
            filename = filename + ".json"
            for host in self.conf.datanode_host:
                if host==self.conf.nameserver_host:
                    continue
                cmd = f'scp {filename} root@{host}:{filename}'
                run_cmd = subprocess.run(cmd.split(" "))

            return
        
        def _json_name(name):
            return os.path.join(self.conf.edfs_home,"metadata/", name)

        for n in lsjson:
            fullpath = _json_name(n)
            #data = _read_json_api(n)
            print(fullpath)
            _write_to_json(fullpath)

    def update_config(self):
        datanode = self.conf.datanode_host
        env_path = os.path.join(self.conf.edfs_home, "conf/edfs_env.sh")
        conf_path = os.path.join(self.conf.edfs_home, "conf/edfs_config.yaml")

        for host in datanode:
            if host==self.conf.nameserver_host:
                continue
            cmd1 = f'scp {env_path} root@{host}:{env_path}'
            run_cmd1 = subprocess.run(cmd1.split(" "))

            cmd2 = f'scp {conf_path} root@{host}:{conf_path}'
            run_cmd2 = subprocess.run(cmd2.split(" "))

    def update(self):
        self.update_config()
        self.update_json()
        

_init = INIT()
_update = UPDATE()

if len(sys.argv)==2:
    if sys.argv[1]=="init":
        _init.init_cluster()
    elif sys.argv[1]=="update":
        _update.update()
else :
    print("USAGE : {init | update}")
