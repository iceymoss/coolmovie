# -*- coding: utf-8 -*-
from flask import Flask
from flask_script import Manager
import pymysql
import os

# from flask_sqlalchemy import SQLAlchemy


app = Flask( __name__ )

manager = Manager( app )

# 读取配置文件
app.config.from_pyfile( "config/base_setting.py" )


# 连接数据库
db = None
connection = None
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456789',
    database='school'
)

db = connection.cursor()
