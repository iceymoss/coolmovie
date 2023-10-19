# -*- coding: utf-8 -*-
from application import app


# 拦截器，请求到服务器前拦截，做对应鉴权
@app.before_request
def before_request():
    app.logger.info("--------before_request--------")
    return


# 拦截器，请求过服务器后拦截，做流量统计等
@app.after_request
def after_request(response):
    app.logger.info("--------after_request--------")
    return response
