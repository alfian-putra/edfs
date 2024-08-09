import requests
import os

from url_builder import URL
from yaml_parser import CONFIG

class CONN():
    def __init__(self):
        self.url_builder = URL()
        self.conf = CONFIG()
    
    def upload(self, host, filename):
        url = self.url_builder.datanode_upload_block(host, filename.split("/")[len(filename.split("/")) -1])
        files = {'file': open(filename, 'rb')}  # Specify the file you want to upload .split("/")[len(filename.split("/")) -1]
        print(url)
        response = requests.post(url, files=files)

        if not response.status_code == 200 :
            raise Exception("connection failed : " + str(response.status_code))
        
        return

    def download(self, host, edfsfile, topath):
        fulledfs = edfsfile
        edfsfile = edfsfile.split("/")[len(edfsfile.split("/")) -1]
        tofile = os.path.join(topath, edfsfile)
        #print(tofile)
        url = self.url_builder.datanode_download_block(host, edfsfile)
        print(url)
        response = requests.get(url)

        if response.status_code == 200 :
            with open(tofile, "wb") as file:
                file.write(response.content)
        else:
            raise Exception("connection failed : " + str(response.status_code))
        
        return
    
    def nameserver_json(self, jsonname):
        url = self.url_builder.nameserver_json(jsonname)
        print(url)
        response = requests.get(url)
        return response.content
    
    def remove(self, host, blockname):
        url = self.url_builder.datanode_remove_block(host, blockname)
        print(url)
        response = requests.get(url)

        #if not response.status_code == 200 :
        #    raise Exception("connection failed : " + str(response.status_code))
        
        return