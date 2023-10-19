# # # -*- coding: utf-8 -*-
from application import app
from controllers import index
from controllers.index import index_page
# #
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension( app )

'''
拦截器处理 和 错误处理器
'''
from interceptors.Auth import *
from interceptors.errorHandler import *

# 注册路由
app.register_blueprint( index.index_page,url_prefix = "/api" )