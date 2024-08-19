# EDFS | Example Distributed File System

### NOTE

This project is example of how hdfs work this project content such thing :

1. initialize cluster 
1. put file into edfs
1. get file from edfs
1. make dir in edfs
1. delete file or dir in edfs

### Getting started

This project run properly on fedora 40, but it is possible to run this project in another linux distribution. In this scenaryo i use this environment :

| Name | Specification | Amount |
|---|---|---|
|VM| Fedora v40, python v3.12 | 2 |

data :

| Name | hostname | ip |
|---|---|---|
|VM1| n20.playground.id | 192.168.124.20 |
|VM1| n21.playground.id | 192.168.124.21 |


#### 1. Preparing host

create ssh passwordless from nameserver host to accessing all datanode
    
    root@fedora:~# ssh-keygen -t rsa -m PEM -b 3072
    Generating public/private rsa key pair.
    Enter file in which to save the key (/root/.ssh/id_rsa): 
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /root/.ssh/id_rsa
    Your public key has been saved in /root/.ssh/id_rsa.pub
    The key fingerprint is:
    SHA256:qEIO/5tOVzPdBJuo3H7nyAeEa0TuaK1aV2qqeoYlE7k root@fedora
    The key's randomart image is:
    +---[RSA 3072]----+
    |          .      |
    |        .. +     |
    |   .   o..o .    |
    |  o  . ++..o     |
    |. .o  +=Soo .    |
    | =E ..oo==.      |
    |  +=o.oo= ...    |
    |  .+o+.+ o +.    |
    |  .=B+.   o..    |
    +----[SHA256]-----+

    root@fedora:~# ssh-copy-id -i /root/.ssh/id_rsa.pub root@<datanode-host>

Make sure that nameserver can accessing root user from datanode

    echo "PermitRootLogin yes" /etc/ssh/sshd_config
    sudo systemctl restart sshd

Make sure every host can accessing each other by using hostname (add to /etc/hosts):

    192.168.124.20   n20.playground.id
    192.168.124.21   n21.playground.id


#### 2. Installing Nameserver & Initializing Cluster

pull this git to dir that will be used for installation, in this example i use /opt

    cd /opt
    git clone https://github.com/alfian-putra/edfs.git
    cd /opt/edfs

configure the edfs_env.sh

    vi conf/edfs_env.sh

    export EDFS_HOME="/opt/edfs/"

configure the edfs_config.yaml

    vi conf/edfs_config.yaml

    # nameserver host
    nameserver_host: n20.playground.id

    # nameserver port
    nameserver_port: 8080

    # blocksize in mb
    blocksize: 1

    # datanode port
    datanode_port: 3000

    # datanode host list
    datanode_host :
        - n20.playground.id
        - n21.playground.id

init the cluster :

    source conf/edfs_env.sh ; ./init.py init

in nameserver host run the nameserver

    source conf/edfs_env.sh ; bin/nameserver start

in every datanode host run the datanode

    source /opt/edfs/conf/edfs_env.sh ; /opt/edfs/bin/datanode start

#### 3. Practicing

listing all file :

    bin/edfs.py ls /

make a dir :

    bin/edfs.py mkdir /example

put file to edfs :

    bin/edfs.py put example/10.txt /example/

get file to local file :

    bin/edfs.py get /example/10.txt /opt
