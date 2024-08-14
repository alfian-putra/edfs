#!/usr/bin/python3

import os
import sys

edfs_home = os.environ["EDFS_HOME"]
lib_dir = os.path.join(edfs_home, "lib/")

sys.path.append(edfs_home)
sys.path.append(lib_dir)

from core import EDFS
from init import INIT 

edfs = EDFS()
init = INIT()

command=sys.argv[1]
arg_length=len(sys.argv)

if command=="ls":
    """
    3 scenaryo :
        edfs ls
        edfs ls <dir>
        edfs ls -r
        edfs ls -r <dir>
    """
    if arg_length==2:
        edfs._iterate(edfs.ls())
    elif (arg_length==3) and (not sys.argv[2]=="-r"):
        edfs._iterate(edfs.ls(sys.argv[2]))
    elif (arg_length==3) and (sys.argv[2]=="-r"):
        edfs._iterate(edfs.lsr())
    elif (arg_length==4) and (sys.argv[2]=="-r"):
        edfs._iterate(edfs.lsr(sys.argv[3]))
elif command=="init":
    if len(sys.argv) == 2:
        init.init_cluster()
    else:
        print("Invalid argument !")
elif command=="mkdir":
    if not arg_length==3:
        raise Exception("Invalid argument !")
    else:
        edfs.mkdir(sys.argv[2])
elif command=="rm":
    if arg_length==3 or arg_length==4:
        if sys.argv[2]=="-f":
            edfs.remove_file(sys.argv[3])
        elif edfs.is_exist(sys.argv[2]):
            edfs.remove_file(sys.argv[2])
        else:
            raise Exception("File not found !")
    else:
        raise Exception("Invalid argument !")
elif command=="put":
    if not arg_length==4:
        raise Exception("Invalid argument !")
    else:
        edfs.add_file(sys.argv[2],sys.argv[3])
elif command=="get":
    if not arg_length==4:
        raise Exception("Invalid argument !")
    else:
        edfs.get_file(sys.argv[2],sys.argv[3])
    pass