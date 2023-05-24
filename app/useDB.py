# -*- coding: utf-8 -*-
from app.common.libs.UrlManager import UrlManager
from app.util.Constant_setting import Constant_db
from app.util.log import logg

import psycopg2
import time
import numpy as np

from flask import make_response, request
import urllib3

from app.util.log_util.all_new_log import logger_all


class useDB(object):
    def __init__(self):
        # 连接一个给定的数据库
        # self.conn = psycopg2.connect(database="test_fram",user="cdi",password="Cdi2021@",
        #                              host="pgm-1hl07vmgn0rd297653280.pgsql.rds.ali-ops.cloud.cn.hsbc",port="3433")
        self.conn = Constant_db().db
        # 建立游标，用来执行数据库操作
        self.cursor = self.conn.cursor()

    def search(self, sql):
        print("SEARCH:", sql)
        self.cursor.execute(sql)
        values = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        return values

    def executesql(self, sql):
        print(sql)
        self.cursor.execute(sql)
        self.cursor.close()
        try:
            self.conn.commit()
        except:
            logger_all.error('commit error')
        self.conn.close()

    def executesql_fetch(self, sql):
        print(sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows


class ConnectSQL():
    def __init__(self):
        # 连接一个给定的数据库
        self.conn = Constant_db().db
        # 建立游标，用来执行数据库操作
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_test_case = "create table xcheck.test_case(" \
                           "userid INTEGER NOT NULL," \
                           "name CHARACTER VARYING," \
                           "description text," \
                           "module CHARACTER VARYING," \
                           "status INTEGER," \
                           "id INTEGER NOT NULL DEFAULT nextval('id_seq'::regclass)," \
                           "PRIMARY KEY(id))"
        create_config_target_info = "create table xcheck.config_target_info(" \
                                    "target_id INTEGER NOT NULL DEFAULT nextval('target_id_seq'::regclass)," \
                                    "user_id INTEGER NOT NULL," \
                                    "database_type CHARACTER(50)," \
                                    "target_access_id CHARACTER(100)," \
                                    "target_secret_access_key CHARACTER(100)," \
                                    "target_project CHARACTER(100)," \
                                    "target_endpoint CHARACTER(100)," \
                                    "create_date timestamp without time zone," \
                                    "PRIMARY KEY(target_id))"
        create_config_source_info = "create table xcheck.config_source_info(" \
                                    "source_id INTEGER NOT NULL DEFAULT nextval('source_id_seq'::regclass)," \
                                    "user_id INTEGER NOT NULL," \
                                    "database_type CHARACTER(50)," \
                                    "source_host CHARACTER(100)," \
                                    "source_username CHARACTER(100)," \
                                    "source_password CHARACTER(100)," \
                                    "create_date timestamp without time zone," \
                                    "PRIMARY KEY(source_id))"
        create_user = "create table xcheck.user(" \
                      "user_id INTEGER NOT NULL," \
                      "username CHARACTER(32)," \
                      "password CHARACTER VARYING(32)," \
                      "status INTEGER," \
                      "create_date timestamp without time zone," \
                      "CONSTRAINT user_key PRIMARY KEY(user_id))"
        create_source_target_parameter = "create table xcheck.source_target_parameter(" \
                                         "param_id INTEGER NOT NULL DEFAULT nextval('sou_tar_param_id_seq'::regclass)," \
                                         "user_id INTEGER NOT NULL," \
                                         "source_tablename CHARACTER(100)," \
                                         "target_tablename CHARACTER(100)," \
                                         "source_db CHARACTER(100)," \
                                         "target_db CHARACTER(100)," \
                                         "pi CHARACTER(100)," \
                                         "source_where_condition CHARACTER(100)," \
                                         "target_where_condition CHARACTER(200)," \
                                         "create_date timestamp without time zone," \
                                         "PRIMARY KEY(param_id))"

        self.cursor.execute(create_test_case)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def write_register_sql(self, username, password):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = ''.join(map(str, np.random.randint(0, 9, 6)))
        register_info = """INSERT INTO xcheck.user values('{}','{}','{}','{}','{}')""".format(user_id, username,
                                                                                              password, 0, create_date)
        self.cursor.execute(register_info)
        self.conn.commit()
        self.cursor.close()
        # self.conn.close()

    def write_register_sql_new(self, username, staffid):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # user_id = ''.join(map(str, np.random.randint(0, 9, 6)))
        register_info = """INSERT INTO xcheck.user(username,password,status,create_date,staffid) values('{}','{}','{}','{}','{}')""".format(
            username, "", 0, create_date, staffid)
        self.cursor.execute(register_info)
        self.conn.commit()
        self.cursor.close()
        # self.conn.close()    

    def get_register_username(self, username):
        register_infos = """SELECT username FROM xcheck.user where username = '{}'""".format(username)
        self.cursor.execute(register_infos)
        rows = self.cursor.fetchall()
        return rows

    def get_password(self, username):
        password = """select password from xcheck.user where username = '{}'""".format(username)
        self.cursor.execute(password)
        rows = self.cursor.fetchall()
        return rows

    def login_sql(self, data1):
        pass

    def get_login_userid(self, username):
        user_id_sql = "select user_id from xcheck.user where username='{}'".format(username)
        self.cursor.execute(user_id_sql)
        user_id = self.cursor.fetchall()[0][0]
        # print("user_id......",user_id)
        return user_id

    def write_source_config(self, user_id, database_type, source_host, source_username, source_password):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck.config_source_info(user_id,database_type,source_host,source_username,source_password,create_date) values('{}','{}','{}','{}','{}','{}')""" \
            .format(user_id, database_type, source_host, source_username, source_password, create_date)
        self.cursor.execute(register_info)
        self.conn.commit()
        # self.cursor.close()

    def get_source_config_value(self, user_id, database_type):
        source_ora_config = """select source_host,source_username,source_password from xcheck.config_source_info where user_id = {} and database_type = '{}' order by create_date desc limit 1 """.format(
            user_id, database_type)
        self.cursor.execute(source_ora_config)
        rows = self.cursor.fetchall()
        return rows

    def get_infor_value(self, user_id, case_name):
        infor_value = """select * from xcheck.test_case where user_id = {} and case_name = '{}' """.format(user_id,
                                                                                                           case_name)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def web_get_infor_value(self, user_id, case_name):
        infor_value = """select * from xcheck.web_test_case where user_id = {} and case_name = '{}' """.format(user_id,
                                                                                                               case_name)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def data_get_infor_value(self, case_name):
        infor_value = """select * from xcheck.data_test_case where case_name = '{}' """.format(case_name)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def data_f2t_get_infor_value(self, case_name):
        infor_value = """select * from xcheck.data_test_case_f2t where case_name = '{}' """.format(case_name)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def get_infor_value_id(self, case_id):
        infor_value = """select * from xcheck.test_case where case_id = {}  """.format(case_id)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def web_get_infor_value_id(self, case_id):
        infor_value = """select * from xcheck.web_test_case where case_id = {}  """.format(case_id)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def data_get_infor_value_id(self, case_id):
        infor_value = """select * from xcheck.data_test_case where case_id = {}  """.format(case_id)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def data_f2t_get_infor_value_id(self, case_id):
        infor_value = """select * from xcheck.data_test_case_f2t where case_id = {}  """.format(case_id)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def data_get_case_id(self, case_name):
        infor_value = """select case_id from xcheck.data_test_case where case_name= '{}'  """.format(case_name)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def data_f2t_get_case_id(self, case_name):
        infor_value = """select case_id from xcheck.data_test_case_f2t where case_name= '{}'  """.format(case_name)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def get_infor_value_name(self, case_name):
        infor_value = """select * from xcheck.test_case where case_name = '{}'  """.format(case_name)
        self.cursor.execute(infor_value)
        rows = self.cursor.fetchall()
        return rows

    def write_target_config(self, user_id, target_access_id, target_secret_access_key, target_project, target_endpoint):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        database_type = 'max'
        register_info = """INSERT INTO xcheck.config_target_info(user_id,database_type,target_access_id,target_secret_access_key,target_project,target_endpoint,create_date) values('{}','{}','{}','{}','{}','{}','{}')""" \
            .format(user_id, database_type, target_access_id, target_secret_access_key, target_project, target_endpoint,
                    create_date)
        self.cursor.execute(register_info)
        self.conn.commit()
        # self.cursor.close()

    def write_config_value(self, user_id, case_name, host, username, pwd, access_id, secret_access_key, project,
                           endpoint,
                           database_type, source_tablename, target_tablename, td_columndb, source_db, target_db, pi,
                           source_where_condition, target_where_condition):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck._test_case(user_id,case_name,s_host,s_username,s_pwd,ali_accessid,ali_secret_key,ali_project,ali_endpoint,
                           database_type,s_tablename,t_tablename,td_columndb,source_db,target_db,pi,s_where_condition,t_where_condition,create_date) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""" \
            .format(user_id, case_name, host, username, pwd, access_id, secret_access_key, project, endpoint,
                    database_type, source_tablename, target_tablename, td_columndb, source_db, target_db, pi,
                    source_where_condition, target_where_condition, create_date)
        print(register_info)
        self.cursor.execute(register_info)
        self.conn.commit()
        # self.cursor.close()

    def write_config_value_all(self, user_id, case_name, testinfor):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck.test_case(user_id,case_name,testinfor,create_date) values('{}','{}','{}','{}')""" \
            .format(user_id, case_name, testinfor, create_date)
        print(register_info)
        self.cursor.execute(register_info)
        self.conn.commit()
        # self.cursor.close()

    def web_write_config_value_all(self, user_id, case_name, testinfor):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck.web_test_case(user_id,case_name,testinfor,create_date) values('{}','{}','{}','{}')""" \
            .format(user_id, case_name, testinfor, create_date)
        print(register_info)
        self.cursor.execute(register_info)
        self.conn.commit()

    def data_write_config_value_all(self, user_id, case_name, testinfor, testinfor_db):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck.data_test_case(user_id,case_name,testinfor,testinfor_db,create_date) values('{}','{}','{}','{}','{}')""" \
            .format(user_id, case_name, testinfor, testinfor_db, create_date)
        print(register_info)
        self.cursor.execute(register_info)
        self.conn.commit()

    def data_f2t_write_config_value_all(self, user_id, case_name, testinfor, testinfor_db):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck.data_test_case_f2t(user_id,case_name,testinfor,testinfor_db,create_date) values('{}','{}','{}','{}','{}')""" \
            .format(user_id, case_name, testinfor, testinfor_db, create_date)
        print(register_info)
        self.cursor.execute(register_info)
        self.conn.commit()

    def get_target_config_value(self, user_id, database_type):
        target_ora_config = """select target_access_id,target_secret_access_key,target_project,target_endpoint from xcheck.config_target_info where user_id = {} and database_type = '{}' order by create_date desc limit 1 """.format(
            user_id, database_type)
        self.cursor.execute(target_ora_config)
        rows = self.cursor.fetchall()
        return rows

    def write_source_target_parameter(self, user_id, database_type, source_tablename, target_tablename, source_db,
                                      target_db, pi, source_where_condition, target_where_condition):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # user_id = '675330' #获取当前登录的id
        source_target_info = """INSERT INTO xcheck.source_target_parameter(user_id,database_type,source_tablename,target_tablename,source_db,target_db,pi,source_where_condition,target_where_condition) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""" \
            .format(user_id, database_type, source_tablename, target_tablename, source_db, target_db, pi,
                    source_where_condition, target_where_condition, create_date)
        self.cursor.execute(source_target_info)
        self.conn.commit()
        # self.cursor.close()

    def get_source_target_parameter(self, user_id, database_type):
        source_target_parameter = """select source_tablename,target_tablename,source_db,target_db,pi,source_where_condition,target_where_condition from xcheck.source_target_parameter where user_id = {} and database_type = '{}' order by create_date desc limit 1 """.format(
            user_id, database_type)
        # source_target_parameter = """select source_tablename,target_tablename,source_db,target_db,pi,source_where_condition,target_where_condition from xcheck.source_target_parameter where user_id = {} and database_type = '{}'""".format(user_id, database_type)
        self.cursor.execute(source_target_parameter)
        rows = self.cursor.fetchall()
        return rows

    def update_user_status(self):
        pass

    def get_cookie_userid(self):
        cookies = request.cookies.get('Name')
        user_id = """select user_id from xcheck.user where username = '{}'""".format(cookies)
        self.cursor.execute(user_id)
        rows = self.cursor.fetchall()
        cookies_user_id = rows[0][0]
        return cookies_user_id

    def get_tablename(self, user_id, database_type):
        table_name_sql = """select source_tablename from xcheck.source_target_parameter where user_id = {} and database_type = '{}' order by create_date desc limit 1 """.format(
            user_id, database_type)
        self.cursor.execute(table_name_sql)
        rows = self.cursor.fetchall()
        table_name = rows[0][0]
        return table_name

    def get_cookie(self):
        cookies = request.cookies.get("Name")
        return cookies

    def delete_cookie(self):
        response = make_response("del success")
        response.delete_cookie('Name')

    def get_personal_user_id(self):
        url = UrlManager.buildUrl('/personal')
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        wb_data = response.data.decode('utf-8')  # GB2312
        userid = wb_data.split('="user_id">')[1].split('</div>')[0]
        return userid

    def data_write_connecion_all(self, user_id, case_name, testinfor, testinfor_db):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck.data_test_case(user_id,case_name,testinfor,testinfor_db,create_date) values('{}','{}','{}','{}','{}')""" \
            .format(user_id, case_name, testinfor, testinfor_db, create_date)
        print(register_info)
        self.cursor.execute(register_info)
        self.conn.commit()

    def data_update_connecion_all(self, user_id, case_name, testinfor, testinfor_db):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        register_info = """INSERT INTO xcheck.data_test_case(user_id,case_name,testinfor,testinfor_db,create_date) values('{}','{}','{}','{}','{}')""" \
            .format(user_id, case_name, testinfor, testinfor_db, create_date)
        print(register_info)
        self.cursor.execute(register_info)
        self.conn.commit()

    def get_user_group(self, username):
        group_query = """SELECT xcheck.group.name
                        FROM xcheck.user
                        JOIN xcheck.team ON xcheck.team.team_id = ANY (xcheck.user.team_ids)
                        JOIN xcheck.group ON xcheck.group.group_id = ANY (xcheck.team.group_ids)
                        WHERE xcheck.user.username = '{}' """.format(username)
        self.cursor.execute(group_query)
        rows = self.cursor.fetchall()
        group_names = [row[0].rstrip() for row in rows]
        return group_names

    def get_team(self, username):
        team_query = """SELECT t.name
                        FROM xcheck.team t
                        JOIN xcheck.user u ON u.team_ids @> ARRAY[t.team_id]
                        WHERE u.username = '{}'; """.format(username)
        self.cursor.execute(team_query)
        rows = self.cursor.fetchall()
        team = rows[0][0].rstrip()
        return team

    def get_avatar(self, username):
        avatar_query = """ SELECT avatar_url 
                     from xcheck.user 
                     where username = '{}' """.format(username)
        self.cursor.execute(avatar_query)
        rows = self.cursor.fetchall()
        avatar = rows[0][0].rstrip()
        return avatar


if __name__ == '__main__':
    sql = 'select id,module,name,description from xcheck.test_case where status = 1 order by id desc limit 1000;'
    cases = useDB().search(sql)
    print(cases)
