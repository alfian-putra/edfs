#!/usr/bin/python3

import os
import sys


edfs_home = os.environ["EDFS_HOME"]
lib_dir = os.path.join(edfs_home, "lib/")

sys.path.append(lib_dir)
sys.path.append(edfs_home)

from flask import Flask, flash, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from yaml_parser import CONFIG

config = CONFIG()
UPLOAD_FOLDER = os.path.join(config.edfs_home, "data/")

app = Flask(__name__)


@app.route('/api/uploads/<filename>', methods=['GET', 'POST'])
def upload_file(filename):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print("FILE __>>" + filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            #return redirect(url_for('download_file', name=filename))
    return ''' 
    '''

@app.route('/api/uploads/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@app.route('/api/downloads/<filename>')
def return_file(filename):
    fullPath = os.path.join(UPLOAD_FOLDER, filename)
    print(fullPath)
    try:
        return send_file(fullPath, download_name=filename)
    except Exception as e:
        return str(e)

@app.route('/api/remove/<filename>')
def rm_file(filename):
    fullPath = os.path.join(UPLOAD_FOLDER, filename)
    print(fullPath)
    os.remove(fullPath)
    return ""




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=config.datanode_port)