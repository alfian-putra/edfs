#!/usr/bin/python3

import os
import sys
import subprocess

from yaml_parser import CONFIG
from connection_handler import CONN

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
        data = '{ "files" : []}'
        fullpath = os.path.join(self.conf.edfs_home,"metadata/metadata.json")
        self._write_to_file(fullpath, data)

    def _init_json_hostmapping(self):
        data = '{ "hosts" : []}'
        fullpath = os.path.join(self.conf.edfs_home,"metadata/hostmapping.json")
        self._write_to_file(fullpath, data)

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

    def init_cluster(self):
        self.init_dir()
        self.init_json()

class UPDATE():
    def __init__(self):
        self.conf = CONFIG()
        self.con_handler = CONN()
        
    def update_json(self):
        lsjson = ["filemapping", "hostmapping","metadata"]

        def _read_json_api(filename):
            return self.con_handler.nameserver_json(filename).decode("utf-8")

        def _write_to_json(filename, content):
            filename = filename + ".json"
            f = open(filename, "w")
            f.write(content)
            f.close()
            return
        
        def _json_name(name):
            return os.path.join(self.conf.edfs_home,"metadata/", name)

        for n in lsjson:
            fullpath = _json_name(n)
            data = _read_json_api(n)
            _write_to_json(fullpath, data)

    def update_config(self):
        datanode = self.conf.datanode_host
        env_path = os.path.join(self.conf.edfs_home, "conf/edfs_env.sh")
        conf_path = os.path.join(self.conf.edfs_home, "conf/edfs_config.yaml")

        for host in datanode:
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
