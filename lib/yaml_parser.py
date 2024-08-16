#!/usr/bin/python3

import os
import sys

from json_parser import JSON

pwd = os.getcwd()

edfs_home = os.environ["EDFS_HOME"]
edfs_config = os.path.join(edfs_home, "conf", "edfs_config.yaml")
#print(edfs_config)
#print(edfs_home)
#add pythonpath
sys.path.append(pwd)
sys.path.append(edfs_home)

import yaml

class CONFIG():
    def __init__(self):
        #os environment (edfs env)
        self.edfs_home = os.environ["EDFS_HOME"]
        #yaml
        self.config = self.parsing_yaml(edfs_config)
        self.nameserver_host = self.config['nameserver_host']
        self.nameserver_port = self.config['nameserver_port']
        self.blocksize = self.config['blocksize']
        self.datanode_port = self.config['datanode_port']
        self.datanode_host = self.config['datanode_host']

        self.nameserver = {'host' : self.nameserver_host, 'port': self.nameserver_port}
        self.data = {'blocksize' : self.blocksize}
        self.datanode = {'port' : self.datanode_port, 'host':self.datanode_host}
    def parsing_yaml(self, file):
        with open(file, 'r') as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
        return data
    def __str__(self):
        return repr(self.config)

#c = CONFIG(edfs_config)
#print(c)
#print(c.nameserver['host'])
