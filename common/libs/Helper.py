from flask import jsonify, g, render_template


# 统计模板渲染，放入全局变量
def ops_gender(templates, context={}):
    print("全局变量：",g.current_user)
    if "current_user" in g:
        context["current_user"] = g.current_user
    return render_template(templates, **context)


def ops_renderJSON(code=200, msg="操作成功", data={}):
    resp = {"code": code, "msg": msg, "data": data}
    return jsonify(resp)


def ops_renderErrJSON(msg="系统繁忙，请稍后再试", data={}):
    return ops_renderJSON(code=-1, msg=msg, data=data)
