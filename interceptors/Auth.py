# -*- coding: utf-8 -*-
from application import app, global_db
from flask import request,g
from common.models.user import User
from common.libs.userService import UserService


# 拦截器，请求到服务器前拦截，做对应鉴权
@app.before_request
def before_request():
    app.logger.info("--------before_request--------")
    user_info = check_login()
    app.logger.info(user_info)
    print("返回数据：",str(user_info))
    g.current_user = None
    if user_info:
        print("存在", user_info)
        # 放到flask的全局变量中
        g.current_user = user_info
    return


# 拦截器，请求过服务器后拦截，做流量统计等
@app.after_request
def after_request(response):
    app.logger.info("--------after_request--------")
    return response


def check_login():
    # 获取cookie
    cookies = request.cookies
    cookie_name = app.config["AUTH_COOKIE_NAME"]
    auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    if auth_cookie is None:
        # 没有cookie拦截器不通过
        return False

    # 获取信息
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    # 根据id查数据库
    try:
        user_info = global_db.query(User).filter_by(id=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    # 验证cookie是否有效
    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False
    return user_info









