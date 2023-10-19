# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from common.libs.Helper import ops_gender
from common.models.user import User
from application import db, global_db

# 蓝图优化
index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():

    context = {}
    return ops_gender("index.html", context)


