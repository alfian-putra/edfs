#!/usr/bin/python3

from yaml_parser import CONFIG


class URL():
    def __init__(self):
        self.config = CONFIG() 
    
    def datanode_download_block(self, datanode_host, block_name):
        host = datanode_host
        port = self.config.datanode_port
        api = "/api/downloads/" + block_name
        return f"http://{host}:{port}{api}"
        
    
    def datanode_upload_block(self, datanode_host, block_name):
        host = datanode_host
        port = self.config.datanode_port
        api = "/api/uploads/" + block_name
        return f"http://{host}:{port}{api}"   
    
    def datanode_remove_block(self, datanode_host, block_name):
        host = datanode_host
        port = self.config.datanode_port
        api = "/api/remove/" + block_name
        return f"http://{host}:{port}{api}"  

    def nameserver_json(self, json_file):
        host = self.config.nameserver_host
        port = self.config.nameserver_port
        api = "/api/metadata/" + json_file
        return f"http://{host}:{port}{api}"



#u = URL()

#print(u.datanode_download_block("localhost", "block_name"))