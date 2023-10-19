from application import app


class UrlManager(object):

    # 获取绝对路径
    @staticmethod
    def buildUrl(path):
        config_domain = app.config['DOMAIN']
        return "%s%s"%( config_domain['www'],path )


    # 拼接相对路径
    @staticmethod
    def buildStaticUrl(path):
        path = "/static" + path
        return UrlManager.buildUrl(path)