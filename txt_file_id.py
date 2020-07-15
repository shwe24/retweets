#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:44:35 2020

@author: ashutosh
"""
import configparser
import pymysql
from pymongo import MongoClient
import os

def get_config():
    cf = configparser.ConfigParser()
    dirname = os.path.dirname
    path = os.path.join(dirname(dirname((__file__))), 'conf', 'config.cfg')
    #print("Config path: ",path)
    cf.read(path)
    return cf

def get_mongodb_client(env=None):
    cf = get_config()
    if not env:
        db_env = 'dev'
    else:
        db_env = env
    sec = 'mongodb_{0}'.format(db_env)
    db_host = cf.get(sec, 'host')
    db_port = cf.getint(sec, 'port')
    db_user = cf.get(sec, 'user')
    db_pwd = cf.get(sec, 'password')
    db_name = cf.get(sec, 'db_name')
    uri = 'mongodb://{}:{}@{}:{}/?authSource={}'.format(db_user, db_pwd, db_host, db_port, db_name)
    client = MongoClient(uri)
    return client


client = get_mongodb_client()
datalake = client['datalake']
col=datalake['list_memberships']
x=col.find()
file1= open("t_id.txt",'w')
for data in x:
    file1.writelines(data['id_str']+"\n")
file1.close()