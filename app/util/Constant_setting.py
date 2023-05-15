import os
import subprocess

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))

# class Constant_cmd( ):
#     def __init__(self,userid):
#         self.userid =userid
#         self.cmd_td = 'python {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
#         self.retcode = subprocess.Popen(self.cmd_td, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# class Constant_cmd():
#     def __init__(self,userid):
#         self.userid = userid
#         self.cmd_td = '/hsbc/tac/app/anaconda3/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
#         self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class Constant_cmd():
    def __init__(self,userid):
        self.userid = userid
        self.cmd_td = '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath, self.userid)
        self.retcode = subprocess.Popen(self.cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)