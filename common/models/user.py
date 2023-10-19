# coding: utf-8
from application import db
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


# 创建 User 类以映射表结构
class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(30), nullable=False)
    login_name = Column(String(20), nullable=False)
    login_pwd = Column(String(32), nullable=False)
    login_salt = Column(String(32), nullable=False, comment='登录密码随机数')
    status = Column(Integer, default=1, nullable=False, comment='状态 0：无效， 1：有效')
    updated_time = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    created = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

