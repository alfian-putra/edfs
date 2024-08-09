#!/usr/bin/python3
import json
import os

json_path = os.path.join(os.getcwd(), "../metadata")
metadata_json_file = os.path.join(json_path, "metadata.json")
hostmapping_json_file = os.path.join(json_path, "hostmapping.json")
filemapping_json_file = os.path.join(json_path, "filemapping.json")

class JSON():
    def __init__(self, json_path):
        # Opening JSON file
        f = open(json_path)
        # returns JSON object as
        # a dictionary
        self.data = json.load(f)
        self.json_path = json_path
    def __str__(self):
        return json.dumps(self.data, indent=2)
    

    ### def as_dict(self):
    ###     return self.data

class METADATA(JSON):
    def __init__(self):
        JSON.__init__(self, metadata_json_file)
        self.content = self.data["files"]
    
    def append_data(self, new_data):
        try:
            self.content.append(json.loads(new_data))
        except Exception as e:
            return str(e)
        

        self.update_file()
        return 
    
    def remove_data(self, idx):
        self.content.pop(idx)
        self.update_file()
        return

    def update_file(self):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

class FILEMAP(JSON):
    def __init__(self):
        JSON.__init__(self, filemapping_json_file)
        self.content = self.data["files"]
    
    def append_data(self, new_data):
        try:
            self.content.append(json.loads(new_data))
        except Exception as e:
            return str(e)
        

        self.update_file()
        return 
    
    def remove_data(self, idx):
        self.content.pop(idx)
        self.update_file()
        return

    def update_file(self):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

class HOSTMAP(JSON):
    def __init__(self):
        JSON.__init__(self, hostmapping_json_file)
        self.content = self.data["blocks"]
    
    def append_data(self, new_data):
        try:
            self.content.append(json.loads(new_data))
        except Exception as e:
            return str(e)
        
        self.update_file()
        return 

    def update_file(self):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

