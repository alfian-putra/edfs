#!/usr/bin/python3

import os
import sys
import hashlib
import json

pwd = os.getcwd()
edfs_home = os.environ["EDFS_HOME"]
#add pythonpath
sys.path.append(pwd)
sys.path.append(edfs_home)
import yaml

from json_parser import METADATA, HOSTMAP, FILEMAP
from yaml_parser import CONFIG
from block_handler import BLOCK
from url_builder import URL
from connection_handler import CONN

block_handler = BLOCK()
url_handler = URL()


#json_data = JSON(json_file)
#print(json_data)
#print("\n\n"+repr(json_data.data[0]))

#this will parsing the metadata of a file
class CORE():
    def __init__(self): 
        self.metadata = METADATA()
        self.filemapping = FILEMAP()
        self.config = CONFIG()
        self.con = CONN()

    # json functionality
    def print_json(self):
        print(self.metadata)
        return
    def init_json():
        pass
    def get_json():
        pass
    def set_json():
        pass
    
    # CORE functionality
    def is_exist(self, filename):
        for i in range(0, len(self.metadata.content)):
            if self.metadata.content[i]['name']==filename:
                return True
        return False
    def is_parent_dir_exist(self, filepath):
        filepath = filepath[:filepath.rfind("/")] + "/"
        #print("tes : "+filepath)
        self.is_exist(filepath)
    ## item name
    def add(self, item):
        self.add_to_json(item)

#add functionality to core obnject
class EDFS(CORE):
    def __init__(self):
        CORE.__init__(self)
    
    def _iterate(self, ls):
        for item in ls:
            print(item)

    # utility function
    def generate_md5(self,file_path):
        #print(file_path)
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()

    # json functionality
    def add_file(self, filename, edfspath):
        f = filename.split("/")[len(filename.split("/")) -1]
        
        edfs_file = os.path.join(edfspath, f) if edfspath[len(edfspath) -1]=="/" else edfspath
        edfs_path = edfs_file
        # if edfs_path exist throw error
        if self.is_exist(edfs_file):
            raise Exception(f"file {edfs_file} already exist !")
            return False

        ##  put json data of a local file to json
        ### check if parent dir of edfs exist
        if self.is_parent_dir_exist(edfs_file):
            raise Exception(f"parent dir does not exist !")
            return False
        
        ### check local file exist
        if not os.path.exists(filename):
            raise Exception(f"{filename} not found !")
            return False
        
        ### check filename is a file 
        if not os.path.isfile(filename):
            raise Exception(f"{filename} not a file !")
            return False

        ### add to json
        md5_file = self.generate_md5(filename)

        metadata_data = '{"name" : "'+edfs_file+ \
                '", "type" : "file",'+ \
                '"md5" : "'+ md5_file+ \
                '", "block" : '+ block_handler.to_chunk(filename, edfs_file, self.config.blocksize, self.config.datanode_host)+ \
                '}'
        #print("tes >>> " + metadata_data)
        #print(type(json.loads(metadata_data)))
        #PENDING >> 
        self.metadata.append_data(metadata_data)
        #print(self.metadata)

    #filename = fullpath filename in edfs
    def remove_file(self, filename):
        def _remove_block(json_data):
            for i in json_data["block"]:
                host = i 
                for j in json_data["block"][host]:
                    url = self.con.remove(host, j)
            return

        for i in range(0, len(self.metadata.content) ):
            if self.metadata.content[i]['name']==filename:
                ##remove block
                _remove_block(self.metadata.content[i])

                self.metadata.remove_data(i)
        for i in range(0, len(self.filemapping.content) ):
            if self.filemapping.content[i]['name']==filename:
                self.filemapping.remove_data(i)
        return 

    def get_file(self, filename, localpath):
        block_handler.to_file(filename, localpath)
    
    def lsr(self, *args):
        if len(args) < 1 :
            return self.lsr("/")
        else:
            dir = args[0]
            lsdir = []
            for i in range(0, len(self.metadata.content)):
                if dir == self.metadata.content[i]['name'][0:len(dir)]:
                    lsdir.append(self.metadata.content[i]['name'])
            lsdir.sort()
            #self._iterate(lsdir)
            return lsdir

    def ls(self, *args):
        rtrnls =[]
        if len(args) < 1 :
            deep_dir = 1
            ls = self.lsr("/")
            for i in ls:
                if len(i.split("/")) <= deep_dir+2:
                    if  not i.split("/")[len(i.split("/")) -1]=="/":
                        rtrnls.append(i)
        else:
            dir = args[0]
            deep_dir =  len(dir.split("/"))
            ls = self.lsr(dir)
            for i in ls:
                if len(i.split("/")) <= deep_dir+1:
                    rtrnls.append(i)
        rtrnls.sort()
        #self._iterate(rtrnls)
        return rtrnls
    
    def mkdir(self, dir):
        if not dir[len(dir)-1] == "/":
            dir += "/"
        if self.is_exist(dir):
            raise Exception("Directory exist !")
        deep = dir.count("/")
        data = ""
        for item in self.metadata.content:
            if item["type"]=="directory":
                if (item["name"] in dir) and \
                (item["name"].count("/") == (deep -1)):
                    data = '{ "name" : "'+ dir +'", "type" : "directory"}'
        
        if len(data)==0:
            raise Exception("Parent dir not found !")

        self.metadata.append_data(data)

#print("testiiiing")
#print(config.nameserver['host'])
#ocore = EDFS()
#ocore.print_json()
#ocore.add_file("t", "/")
#ocore.add_file("10.txt", "/")
#ocore.print_json()
#ocore.remove_file("/t")
#ocore.print_json()
#ocore.get_file("/10.txt", "~/playground/python/edfs/0.1.0/")
#print(ocore.ls())
#ocore.mkdir("/dir2/dir4")
#ocore.print_json()
#ocore.ls()
#ocore.lsr()
#ocore.mkdir("/dir2/dir4/tes/tess")
#print("\n\n")
#print(ocore.is_exist("/none"))
#print("\n\n")
#print(ocore.is_exist("/f1"))
