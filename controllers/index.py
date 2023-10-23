# -*- coding: utf-8 -*-
import random
from flask import Blueprint, request, redirect
from sqlalchemy import desc, between
from common.libs.Helper import ops_gender
from common.libs.Helper import iPagenation
from common.libs.UrlManager import UrlManager
from common.models.user import User
from application import db, global_db
from common.models import movie



# 蓝图优化
index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    req = request.values

    # 获取最新数据
    order_by_f = str(req['order']) if ("order" in req and req['order']) else "lastest"
    page = 1
    if 'p' in req and req['p']:
        page = int(req['p'])

    query = global_db.query(movie.Movie)
    print("参数：", order_by_f)

    page_params = {
        'total_count': int(query.count()),
        "page_size": 30,
        'page': page,
        'url': "/?"
    }

    pages = iPagenation(page_params)
    # 0 - 30,30 - 60 ,60 - 90
    offset = (page - 1) * page_params['page_size']
    limit = page * page_params['page_size']

    if order_by_f == "hot":
        query = query.order_by(desc(movie.Movie.view_counter))
    else:
        query = query.order_by(movie.Movie.pub_date.desc(), movie.Movie.id.desc())
    list_movie = query.offset(offset).limit(limit).all()
    # for item in list_movie:
    #     print("返回", item.__str__())
    return ops_gender("index.html", { "data":list_movie,"pages":pages })

@index_page.route("/info")
def get_movieinfo():
    req = request.values
    movie_id = int(req["id"]) if ("id" in req and req["id"]) else 0
    if movie_id < 1:
        return redirect(UrlManager.buildUrl("/"))

    info = global_db.query(movie.Movie).filter_by(id=movie_id).first()
    if info is None:
        return redirect(UrlManager.buildUrl("/"))

    # 增加点击量
    info.view_counter += 1
    recommend = info.view_counter

    # 提交更改到数据库
    global_db.commit()

    # 获取推荐内容
    start = recommend-100
    end = recommend+100
    recommend_list = global_db.query(movie.Movie).filter(movie.Movie.view_counter.between(start, end)).all()
    sampled_elements = random.sample(recommend_list, 4)
    return ops_gender("info.html", {"info": info, "recommend_list": sampled_elements})


