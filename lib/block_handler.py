#!/usr/bin/python3

import os
import shutil

from yaml_parser import CONFIG
from connection_handler import CONN
from json_parser import FILEMAP, METADATA
from url_builder import URL


class BLOCK():
    def __init__(self):
        self.config = CONFIG()
        self.filemapping = FILEMAP()
        self.metadata = METADATA()
        self.connect = CONN()
        self.url_builder = URL()
        #print("edfs home")
        #print(self.config.edfs_home)
        self.data_path = os.path.join(self.config.edfs_home, "data")
        self.tmp_data_path = os.path.join(self.data_path, ".tmp")
        #print(self.data_path)
        #print(self.tmp_data_path)
        #print("///////////")
    # chunk file into a part
    # file : local file 
    # tmp : tmp dir is in <edfs-home>/data/.tmp
    # blockSize : blockSize
    # lsHost : list host 

    # this function will return :
    # {"h1" : ["chunk1","chunk2"], "h2" : ["chunk2"]}
    def to_chunk(self, file, full_edfs_filepath, blockSize, lsHost):
           #fullpath=os.path.join(os.getcwd(), "GFG.txt")
           f = open(file, "rb")

           #blocksize to kilobyte
           blockSize = int(blockSize)
           blockSize *= (1024*1024)
           #print(type(blockSize))
           #print(str(blockSize))

           #create tmp dir
           if not os.path.exists(self.tmp_data_path):
               os.mkdir(self.tmp_data_path)
           data = f.read(blockSize)
           ls = {}
           all_block = []
           idx_host = 0
           max_idx_host = len(lsHost)
           idx_chunk = 0

           for x in lsHost:
               ls[x] = []

           # h : host
           # c : chunk to add
           #def add_to_dict(h, c):
           #    if not h in ls:
           #        print("s")
           #        ls[h] = []
           #    ls[h] = ls[h].append(c)
           def writeTmpBlock(filename, content):
               fullpath = os.path.join(self.tmp_data_path, filename)
               f = open(fullpath, "wb")

               f.write(content)
               f.close()

           while data:
               #print(repr(ls))
               #print("host" + str(idx_host))
               print("FILEBLOCK >> " + file)
               file = file.split("/")[len(file.split("/")) -1]
               chunk_name = file + str(idx_chunk)
               
               writeTmpBlock(chunk_name, data)
               all_block.append(chunk_name)
               #print(chunk_name)
               #print(data)
               #if not idx_host in lsHost:
               #    lsHost[idx_host] = []
               # print("lsHost : "+repr(ls[lsHost[idx_host]]))
               ls[lsHost[idx_host]].append(chunk_name)
               
               #distribute block
               fullpath = os.path.join(self.tmp_data_path, chunk_name)
               self.connect.upload(lsHost[idx_host], fullpath)

               data = f.read(blockSize)
               idx_chunk += 1
               idx_host = idx_host +1 if idx_host < max_idx_host -1 else 0
           #print(repr(ls))  
            
           #os.listdir(self.tmp_data_path)
           shutil.rmtree(self.tmp_data_path)

           filemap_data = '{ "name" : "'+ full_edfs_filepath+ \
                          '" , "block" :' + repr(all_block).replace("'",'"')+ \
                          '}'
            
           #print("FILEMAPPING -->> "+filemap_data)
           self.filemapping.append_data(filemap_data)
           return repr(ls).replace("'",'"')

    def to_file(self, file, targetdir_or_file):
        #create tmp dir
        if not os.path.exists(self.tmp_data_path):
            os.mkdir(self.tmp_data_path)
        
        def _collect_block(edfs_filename, json_data, targetdir):
            for i in json_data["block"]:
                host = i 
                for j in json_data["block"][host]:
                    url = self.connect.download(host, j, targetdir)
            return

        def _target_filename(target, edfsfile):
            if "~" in target:
                target = os.path.expanduser(target)
            if not os.path.isfile(target):
                if os.path.isdir(target):
                    edfsfile = edfsfile.split("/")[len(edfsfile.split("/")) -1]
                    if os.path.isfile(os.path.join(target, edfsfile)):
                        raise Exception(os.path.join(target, edfsfile) + " Already exists")
                    return os.path.join(target, edfsfile)
                else :
                    raise Exception(f"{target} is not a directory or a file.")
            return target
        
        def _reunite_block(blockdir, blockls, tofile):
            print("BLOCKDIR >> "+blockdir)
            target_file = open(tofile, "ab")
            #print(repr(blockls))
            for i in blockls:
                print("PRINT I >>"+i)
                ffile = os.path.join(blockdir, i)
                print("FFILE "+ffile)
                f = open(ffile, "rb")
                target_file.write(f.read())
                f.close()
            target_file.close()

            return
        
        # 1. download all block
        # 2. check target file
        # 3. reunite block to target file
        metadata_block_data = ""
        #print(file)
        for item in self.metadata.content:
            #print(item["name"] +" "+file+" "+ str(item["name"] == file))
            if item["name"] == file:
                metadata_block_data = item
        
        filemap_block_data = ""
        #print(file)
        for item in self.filemapping.content:
            #print(item["name"] +" "+file+" "+ str(item["name"] == file))
            if item["name"] == file:
                filemap_block_data = item["block"]

        _collect_block(file, metadata_block_data, self.tmp_data_path)

        file_target = _target_filename(targetdir_or_file, file)

        _reunite_block(self.tmp_data_path, filemap_block_data, file_target)

        shutil.rmtree(self.tmp_data_path)



