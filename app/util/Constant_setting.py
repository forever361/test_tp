import os
import subprocess
import psycopg2

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))


# class Constant_cmd():
#     def __init__(self,userid):
#         self.userid = userid
#         self.cmd_td = '/root/miniconda3/envs/tp/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
#         self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

class Constant_cmd():
    def __init__(self,userid):
        self.userid = userid
        self.cmd_td = '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
        self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


class Constant_db():
    def __init__(self):
        self.db = psycopg2.connect(database="test_frame", user="postgres",password="postgres",
                                     host="47.113.185.98", port="5353")

# class Constant_db():
#     def __init__(self):
#         self.db = psycopg2.connect(database="test_frame", user="cdi", password="Cdi2021@",
#                                      host="pgm-1hl07vmgn0rd297653280.pgsql.rds.ali-ops.cloud.cn.hsbc", port="3433")