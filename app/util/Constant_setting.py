import os
import subprocess
import psycopg2
from app.application import app, env

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))

# 根据环境加载相应的配置文件
if env == 'dev':
    from app.config.config_dev import Config
elif env == 'uat':
    from app.config.config_uat import Config
elif env == 'prod':
    from app.config.config_prod import Config

class Constant_cmd():
    def __init__(self,userid,case_id,job_id):
        self.userid = userid
        self.case_id =case_id
        self.job_id = job_id
        self.cmd_td = Config.get_cmd_path(userid,case_id,job_id)
        self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


class Constant_cmd_api():
    def __init__(self,user_id,job_id):
        self.user_id = user_id
        self.job_id = job_id
        self.cmd_td = Config.get_cmd_path_api(job_id,user_id)


class Constant_cmd_data_batch():
    def __init__(self,user_id,case_id):
        self.user_id = user_id
        self.case_id = case_id
        self.cmd_td = Config.get_cmd_path_batch(user_id,case_id)
        self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)



class Constant_db():
    def __init__(self):
        self.config = Config
        self.db = psycopg2.connect(**self.config.DATABASE)
