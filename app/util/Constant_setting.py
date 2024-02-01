import os
import subprocess
import psycopg2

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))


# class Constant_cmd():
#     def __init__(self,userid):
#         self.userid = userid
#         self.cmd_td = '/root/miniconda3/envs/tp/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
#         self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# class Constant_cmd():
#     def __init__(self,userid):
#         self.userid = userid
#         self.cmd_td = '/Users/kun/miniconda3/envs/myenv/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
#         self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


class Constant_cmd():
    def __init__(self,userid):
        self.userid = userid
        self.cmd_td = '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
        self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# class Constant_cmd_api():
#     def __init__(self,user_id,job_id):
#         self.user_id = user_id
#         self.job_id = job_id
#         self.cmd_td = '/Users/kun/miniconda3/envs/myenv/bin/python3.6 {}/api_check/runapi.py {} {}'.format(configPath,
#                                                                                                        job_id, user_id)

# class Constant_cmd_api():
#     def __init__(self,user_id,job_id):
#         self.user_id = user_id
#         self.job_id = job_id
#         self.cmd_td = 'D:/software/miniconda3/envs/tanos/python.exe {}/api_check/runapi.py {} {}'.format(configPath, job_id,user_id)


class Constant_cmd_api():
    def __init__(self,user_id,job_id):
        self.user_id = user_id
        self.job_id = job_id
        self.cmd_td = '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/api_check/runapi.py {} {}'.format(configPath, job_id,user_id)


class Constant_cmd_data_batch():
    def __init__(self,user_id,case_id):
        self.user_id = user_id
        self.case_id = case_id
        self.cmd_td = '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/data2_check_batch/run_or_mx.py  {} {}'.format(configPath, user_id,case_id)




class Constant_db():
    def __init__(self):
        self.db = psycopg2.connect(database="test_frame", user="postgres",password="postgres",
                                     host="8.134.189.98", port="3433")
# class Constant_db():
#     def __init__(self):
#         self.db = psycopg2.connect(database="test_frame", user="cdi", password="Cdi2021@",
#                                      host="pgm-1hl07vmgn0rd297653280.pgsql.rds.ali-ops.cloud.cn.hsbc", port="3433")