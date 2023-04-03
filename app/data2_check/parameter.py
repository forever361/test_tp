import ast
import configparser
import json
import os
import sys

from app.data2_check.commom.Constant_t import Constant_id
from app.useDB import ConnectSQL
from app.util.SSH import mySSH
from app.util.crypto_ECB import AEScoder

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)


# user_path = '{}/userinfo/{}/'.format(configPath, user_id)
# data_conn_path = user_path + '/' + 'data_conn.txt'
# data_db_path = user_path + '/' + 'data_db.csv'
# print(user_path)

class Parameter_common():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        with open(data_conn_path, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            # print(111,configreader_dict)
            self.source_type = configreader_dict['Source TYPE']
            self.target_type = configreader_dict['Target TYPE']



class Parameter_db():

    def parse_parameter_file(seft):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        with open(data_db_path, "r") as f:
            return [i.split(',') for i in f.readlines() if i[0] not in ('#', '\n','')]

class Parameter_or_ali():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        with open(data_conn_path, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            self.Source_conn = configreader_dict['Source conn']
            self.Target_conn = configreader_dict['Target conn']

            list_s = []
            list_t = []
            lists = self.Source_conn.split(",")
            listt = self.Target_conn.split(",")
            for i in lists:
                list_s.append(i.strip())
            for i in listt:
                list_t.append(i.strip())

            self.host = list_s[0]
            self.user = list_s[1]
            self.pwd = AEScoder().decrypt(list_s[2])

            self.access_id = listt[0]
            self.secret_access_key = AEScoder().decrypt(listt[1] )
            self.project = listt[2]
            self.endpoint = listt[3]


class Parameter_ali_ali():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        with open(data_conn_path, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            self.Source_conn = configreader_dict['Source conn']
            self.Target_conn = configreader_dict['Target conn']

            list_s = []
            list_t = []
            lists = self.Source_conn.split(",")
            listt = self.Target_conn.split(",")
            for i in lists:
                list_s.append(i.strip())
            for i in listt:
                list_t.append(i.strip())

            self.access_id_s = list_s[0]
            self.secret_access_key_s = AEScoder().decrypt(list_s[1])
            self.project_s = list_s[2]
            self.endpoint_s = list_s[3]

            self.access_id_t = listt[0]
            self.secret_access_key_t = AEScoder().decrypt(listt[1] )
            self.project_t = listt[2]
            self.endpoint_t = listt[3]


class Parameter_or_or():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        with open(data_conn_path, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            self.Source_conn = configreader_dict['Source conn']
            self.Target_conn = configreader_dict['Target conn']

            list_s = []
            list_t = []
            lists = self.Source_conn.split(",")
            listt = self.Target_conn.split(",")
            for i in lists:
                list_s.append(i.strip())
            for i in listt:
                list_t.append(i.strip())

            self.host_s = list_s[0]
            self.user_s = list_s[1]
            self.pwd_s =   AEScoder().decrypt(list_s[2])

            self.host_t = listt[0]
            self.user_t = listt[1]
            self.pwd_t =  AEScoder().decrypt(listt[2])


class Parameter_pg_ali():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        with open(data_conn_path, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            self.Source_conn = configreader_dict['Source conn']
            self.Target_conn = configreader_dict['Target conn']

            list_s = []
            list_t = []
            lists = self.Source_conn.split(",")
            listt = self.Target_conn.split(",")
            for i in lists:
                list_s.append(i.strip())
            for i in listt:
                list_t.append(i.strip())

            self.host = list_s[0]
            self.port = list_s[1]
            self.db = list_s[2]
            self.user = list_s[3]
            self.pwd = AEScoder().decrypt(list_s[4] )

            self.access_id_t = listt[0]
            self.secret_access_key_t =  AEScoder().decrypt(listt[1])
            self.project_t = listt[2]
            self.endpoint_t = listt[3]

            # print(self.host ,self.port ,self.db ,self.user ,self.pwd )
            # print(self.access_id_t ,self.secret_access_key_t ,self.project_t ,self.endpoint_t )


class Parameter_pg_pg():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        data_conn_ssh= user_path + '/' + 'data_ssh.txt'
        with open(data_conn_path, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            self.Source_conn = configreader_dict['Source conn']
            self.Target_conn = configreader_dict['Target conn']

            list_s = []
            list_t = []
            lists = self.Source_conn.split(",")
            listt = self.Target_conn.split(",")
            for i in lists:
                list_s.append(i.strip())
            for i in listt:
                list_t.append(i.strip())

            if list_s[3] == "[remote]":
                with open(data_conn_ssh, "r", encoding="utf-8") as f:
                    configreader2 = f.readlines()
                    conf= ast.literal_eval(configreader2[0])
                    # print(111,conf[0])
                    j= (conf[0])
                    host = j['host'].strip()
                    username = j['username'].strip()
                    port = j['port'].strip()
                    password = AEScoder().decrypt(j['password'].strip())
                    exec_command_account = j['exec_command_account'].strip()
                    exec_command_pwd = j['exec_command_pwd'].strip()

                    print(111,host)
                    print(222,username)
                    print(333,password)
                    print(444, exec_command_account)
                    print(555, exec_command_pwd)

                    test = mySSH(host=host, username=username, password=password)
                    test.connect()
                    # 执行命令并获取命令结果
                    stdin1, stdout1, stderr1 = test.connection.exec_command(exec_command_account)
                    stdin2, stdout2, stderr2 = test.connection.exec_command(exec_command_pwd)

                    uid_result = str(stdout1.read(), 'UTF-8').strip()
                    psw_result = str(stdout2.read(), 'UTF-8').strip()


                    self.host_s = list_s[0]
                    self.port_s = list_s[1]
                    self.db_s = list_s[2]
                    self.user_s = uid_result
                    self.pwd_s = psw_result

                    self.host_t = list_t[0]
                    self.port_t = list_t[1]
                    self.db_t = list_t[2]
                    self.user_t = list_t[3]
                    self.pwd_t = AEScoder().decrypt(list_t[4])

            elif self.Target_conn == "remote":
                pass
            else:

                self.host_s = list_s[0]
                self.port_s = list_s[1]
                self.db_s = list_s[2]
                self.user_s = list_s[3]
                self.pwd_s = AEScoder().decrypt(list_s[4] )

                self.host_t = list_t[0]
                self.port_t = list_t[1]
                self.db_t = list_t[2]
                self.user_t = list_t[3]
                self.pwd_t = AEScoder().decrypt(list_t[4] )

class Parameter_file_ali():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        data_conn_path = user_path + '/' + 'data_conn.txt'
        data_db_path = user_path + '/' + 'data_db.csv'
        with open(data_conn_path, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            self.Source_conn = configreader_dict['Landingserver conn']
            self.Target_conn = configreader_dict['Target conn']

            list_s = []
            list_t = []
            lists = self.Source_conn.split(",")
            listt = self.Target_conn.split(",")
            for i in lists:
                list_s.append(i.strip())
            for i in listt:
                list_t.append(i.strip())

            self.host_s = list_s[0]
            self.user_s = list_s[1]
            self.pwd_s = AEScoder().decrypt(list_s[2])

            self.access_id_t = listt[0]
            self.secret_access_key_t =  AEScoder().decrypt(listt[1])
            self.project_t = listt[2]
            self.endpoint_t = listt[3]

class Parameter_tmp():
    def __init__(self):
        user_id = Constant_id().cookie_id
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        temp = user_path + '/' + 'temp.txt'
        with open(temp, "r", encoding="utf-8") as f:
            configreader = f.readlines()
            configreader_dict = ast.literal_eval(configreader[0])
            self.select_rule = configreader_dict['select_rule']
        print(self.select_rule)


if __name__ == "__main__":
    Parameter_file_ali()