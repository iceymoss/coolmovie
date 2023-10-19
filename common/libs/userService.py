import random,string, hashlib, base64


class UserService():

    # 密码加密
    def genePwd(pwd, salt):
        m = hashlib.md5() #生成md5实例
        str = "%s-%s"%(base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()
    # 生成盐值
    @staticmethod
    def geneSalt(lenght=16):
        key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(lenght)]
        return ("".join(key_list))
