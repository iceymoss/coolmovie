# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from common.models.user import User
from application import db, global_db

# 蓝图优化
index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    return render_template("index.html")
    # user = global_db.query(User).filter_by(id=1).first()
    # print(user)
    # if user:
    #     return f"User ID: {user.id}, Nickname: {user.nickname}"
    # else:
    #     return "User not found"


