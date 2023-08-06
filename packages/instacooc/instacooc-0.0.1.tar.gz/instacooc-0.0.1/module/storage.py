# -*- coding: utf-8 -*-
import configparser
import pymysql

config = configparser.ConfigParser()
config.read('src/config.ini')

def connect():
    return pymysql.connect(host = config['InstagrammysqlDB']['host'],
                           user = config['InstagrammysqlDB']['user'],
                           password = config['InstagrammysqlDB']['pass'],
                           database = config['InstagrammysqlDB']['db'])

