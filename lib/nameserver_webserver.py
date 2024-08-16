#!/usr/bin/python3
import os
import json
import sys

edfs_home = os.environ["EDFS_HOME"]
lib_dir = os.path.join(edfs_home, "lib/")

sys.path.append(lib_dir)
sys.path.append(edfs_home)

from flask import Flask, render_template, jsonify
from flask import url_for
from yaml_parser import CONFIG

config = CONFIG()
app = Flask(__name__, static_url_path='/static')

@app.route('/api/metadata/<jsonFile>', methods=['GET'])
def updateJsonMap(jsonFile):
    jsonFileExtension = "../metadata/" + jsonFile + ".json"
    jsonFullPath = os.path.join(os.getcwd(), jsonFileExtension)

    if not os.path.isfile(jsonFullPath):
        raise Exception(f"Data not Found {jsonFileExtension}")
    
    f = open(jsonFullPath)

    return jsonify(json.load(f))
    ## return app.send_static_file(jsonFullPath)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=config.nameserver_port)
