# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, make_response, redirect
from common.libs.Helper import ops_renderErrJSON, ops_renderJSON
from common.libs.userService import UserService
from common.models.user import User
from application import db, global_db, app


# 用户模块
member_page = Blueprint("member_page", __name__)


@member_page.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("/member/reg.html")
    req = request.values
    nickname = req["nickname"] if "nickname" in req else ""
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""
    login_pwd2 = req["login_pwd2"] if "login_pwd2" in req else ""

    if login_name is None or len(login_name) < 1:
        return ops_renderErrJSON(msg="账号不能为空")

    if login_pwd is None or len(login_pwd) < 6:
        return ops_renderErrJSON("密码不能小于6位")

    if login_pwd != login_pwd:
        return ops_renderErrJSON(msg="输入密码不一致")

    # 登录账号不能重复
    user = global_db.query(User).filter_by(login_name=login_name).first()
    if user:
        return ops_renderErrJSON(msg="账号已存在，请更换账号")

    # 写入数据库
    user = User()
    user.nickname = nickname
    if nickname is None:
        user.nickname = login_name
    user.login_name = login_name
    user.login_salt = UserService.geneSalt(8)
    user.login_pwd = UserService.genePwd(login_pwd, user.login_salt)

    global_db.add(user)
    global_db.commit()

    res = {"code": 0,
           "msg": {"nickname": nickname, "login_name": login_name, "login_pwd": login_pwd, "login_pwd2": login_pwd2},
           "token": "difhdanf3rudifndf.dfrhindfidf89er.49fhdigjaihg8qa"}
    return ops_renderJSON(data=res)


@member_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("/member/login.html")

    req = request.values
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""

    # 校验参数
    if login_name is None or len(login_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的账号")

    if login_pwd is None or len(login_pwd) < 6:
        return ops_renderErrJSON("密码不能小于6位")

    # 查检查账号
    user = global_db.query(User).filter_by(login_name=login_name).first()
    if user is None:
        return ops_renderErrJSON(msg="请输入正确的账号")

    # 验证密码
    pwd = UserService.genePwd(login_pwd, user.login_salt)
    if user.login_pwd != pwd:
        return ops_renderErrJSON(msg="密码错误")

    if user.status != 1:
        return ops_renderErrJSON(msg="当前账号已禁用，请联系管理员")

    resp = make_response(ops_renderJSON(msg="登录成功"))
    # 设置cookie
    resp.set_cookie(app.config["AUTH_COOKIE_NAME"], "%s#%s"%(UserService.geneAuthCode(user), user.id), 60*60*24)

    return resp

@member_page.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return resp