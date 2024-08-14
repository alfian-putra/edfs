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
|Host PC | Fedora v40, python v3.12 | 1 |
|VM| Fedora v40, python v3.12 | 2 |

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

#### 2. Installing Nameserver
#### 3. initialize cluster