# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
# from common.models.user import User

# 蓝图优化
index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    return "hello, world"
