import base64
import hashlib
import random
import string


class UserService():

    @staticmethod
    def genAuthCode ( user_info =None):
        m= hashlib.md5()
        str = "%s-%s-%s"%(user_info.id,user_info.login_name,user_info.login_pwd)
        m.update(str.encode("utf-8"))
        return m.hexdigest()


    @staticmethod
    def genPwd ( pwd,salt):
        m= hashlib.md5()
        str = "%s-%s"%(base64.encodebytes(pwd.encode("utf-8")),salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()


    @staticmethod
    def genSalt ( lenth =16):
      keylist =  [random.choice( (string.ascii_letters+string.digits)) for i in range(lenth)]
      return ("".join(keylist))
