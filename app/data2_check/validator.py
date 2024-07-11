# import teradata
import pandas as pd
from sys import flags
import configparser



import paramiko
import psycopg2
# import teradatasql
import pymysql
from odps import ODPS
from hashlib import md5
import argparse
import re
from enum import Enum
from decimal import Decimal
import time
from itertools import zip_longest
import traceback
import os
import logging
from datetime import datetime, timedelta
from typing import List
import cx_Oracle

from app.data2_check.commom.Constant_t import Constant_id
from app.data2_check.parameter import Parameter_common
from app.useDB import ConnectSQL
from app.util.SSH import mySSH
import app.util.global_manager as glob

import queue
q = queue.Queue(-1)


basePath = os.path.join(os.path.join(os.path.dirname(__file__)))

os.environ['TZ'] = 'Asia/Shanghai'
# time.tzset()
argparser = argparse.ArgumentParser(description='Usage for Verify.py')
# os.environ["ODBCINI"]="/opt/teradata/client/16.20/odbc_64/odbc.ini"
# os.environ["ODBCINIST"]="/opt/teradata/client/16.20/odbc_64/odbcinst.ini"

os.environ["ODBCINI"] = basePath + "./file/odbc.ini"
os.environ["ODBCINIST"] = basePath + "./file/odbcinst.ini"
# udaExec = teradata.UdaExec (appName="HelloWorld", version="1.0", configureLogging=False ,logConsole=False,logLevel='ERROR')

config = configparser.ConfigParser()

LOG_PATH_NEW = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
userid = Constant_id().cookie_id
iniPath = os.path.join(LOG_PATH_NEW + "/userinfo/{}/config_ssh.ini".format(userid))


class Validator(object):
    class FileNature(Enum):
        MASTER = "MASTER"
        TRANSACTION = "TRANSACTION"

    class Delta(Enum):
        DELTA = "DELTA"
        FULL = "FULL"
        ONE_BATCH = "ONE_BATCH"

    def __init__(self, batch_dt=None, file_nature:str=None, delta:str=None, sys_cde:str=None, sub_sys_cde:str=None,
                 tablename:str=None, logger=None, remove_col_list:dict=None, batch_check_column=None, table=None,
                 verifydb=None, pi_str=None, pi=None,col_str=None, where_condition:str=None, **kwargs):
        self.str_container = []
        self.md5_container = []
        self.ori_data = []
        self.count = {}
        self.sums = []
        # if batch_dt !='':
        #     self.batch_dt = datetime.strptime(batch_dt, '%Y-%m-%d').date()
        # else:
        #     self.batch_dt =''
        # self.file_nature = Validator.FileNature(file_nature.upper())
        # self.delta = Validator.Delta(delta.upper())
        # self.sys_cde = sys_cde.upper()
        # self.sub_sys_cde = sub_sys_cde.upper()
        self.table = table.upper()

        self.tablename = tablename.upper()
        self.error_str_list = []
        self.pi_split = "@@@"
        self.logger = logger
        # self.remove_col_list = remove_col_list.get(self.sys_cde, [])
        self.remove_col_list = remove_col_list
        # self.batch_check_column = batch_check_column
        # self.table_preflix = table
        self.verify_tablename = self.table
        self.verifydb = verifydb
        self.pi = pi
        self.pi_str = pi_str
        self.col_str = col_str
        self.where_condition = where_condition


    def gen_md5(self, records, str_container:List, md5_container:List, ori_data:List ):
        for record in records:
            # print(record)
            join_str = "".join([self.convert_to_str(i) for i in record])
            join_str2 = ",".join([self.convert_to_str(i) for i in record])
            # ori_str = join_str2.split("@@@,")[1]
            ori_str = join_str2
            md5_str = md5(join_str.encode('utf-8')).hexdigest()
            # print(join_str)
            str_container.append(join_str)
            md5_container.append(md5_str)
            ori_data.append(ori_str)

    def convert_to_str(self, s):
        """
        convert values into string
        :param s:
        :return:
        """
        if isinstance(s, Decimal):
            if str(s.to_integral() if s == s.to_integral() else s.normalize()).endswith('.0'):
                return str(s.to_integral() if s == s.to_integral() else s.normalize()).split('.0')[0]
            else:
                return str(s.to_integral() if s == s.to_integral() else s.normalize())
        elif s is None:
            return ''
        else:
            # add 换行符和空格处理
            s_str = str(s).replace('\n', '').replace('\r', '').replace(' ', '')
            if s_str.endswith('.0'):
                return s_str.split('.0')[0]
            else:
                return s_str

    def convert2str(self, s):
        if isinstance(s, Decimal):
            return str(s.to_integral() if s == s.to_integral() else s.normalize())
        elif s is None:
            return ''
        else:
            return str(s)

    def get_batch_value_check_sql(self, pi_str, col_str, pi, verifydb, verify_tablename):
        # print(11111,pi)
        if verifydb == '':
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verify_tablename} {self.where_condition} order by {pi}  \n"
        else:
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename}  {self.where_condition} order by {pi}   \n"

    def get_batch_count_check_sql(self, verify_tablename, verifydb):
        if verifydb == '':
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from {verify_tablename} {self.where_condition}\n"
        else:
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from {verifydb}.{verify_tablename} {self.where_condition}\n"
        return sql

    def execute(self, sql):
        pass

    def shipping_count_container(self):
        sql = self.get_batch_count_check_sql(self.verify_tablename, self.verifydb)
        # self.logger.info(sql)
        counts = self.execute(sql)
        self.count = {count_type: count for tablename, count_type, count in counts}

    def shipping_value_container(self):
        runsql = self.get_batch_value_check_sql(self.pi_str, self.col_str, self.pi, self.verifydb,
                                                self.verify_tablename)

        print("**sql_value:", runsql)

        # self.logger.info(runsql)

        records = self.execute(runsql)

        self.gen_md5(records, self.str_container, self.md5_container, self.ori_data)


class AliValidator(Validator):
    def __init__(self,ods_prj=None, ads_prj="", access_id="", secret_access_key="", endpoint="", pi=None, where_condition:str=None, remove_col_list=None,**kwargs):
        super().__init__(**kwargs) 
        # self.ods_prj = ods_prj
        self.ads_prj = ads_prj
        self.pre_tblname_oss = "OSS"
        self.pre_tblname_CDS_T1 = "CDS_T1"
        self.pre_tblname_CDS_T2 = "CDS_T2"
        self.pre_tblname_CDS = "CDS"

        self.odps = ODPS(access_id = access_id,
                         secret_access_key = secret_access_key,
                         project = self.ads_prj,
                         endpoint = endpoint )

        # print(access_id,secret_access_key,self.ads_prj,endpoint)
        # self.odps = ODPS(access_id='FYBlngS1UDOUAqNO', #登陆账号
        # secret_access_key='YOsAjo6f0pgyKGrnUoDaQG7gCllToQ', #登陆密码
        # project='CN_CDS_DEV', #odps上的项目名称
        # endpoint='https://service.cn-hk-hsbc-d01.odps.ali-ops.cloud.cn.hsbc:443/api') #官方提供的接口
        sql_spilt = "||\"|\"||"
        self.pi = pi

        self.remove_col_list = remove_col_list
        a=[]
        for i in self.remove_col_list.split(","):
            a.append(i.upper().strip())
        self.remove_col_list = a
        # print(11111,self.remove_col_list)

        self.pi_list = self.pi.split(",")
        self.pi_str= f'{self.pi.replace(",",sql_spilt)} as id_no'
        # print(111111,self.pi_str)
        # self.pi_str = ",',',".join([f"{i} as id" for i in self.pi_list if i not in self.remove_col_list])
        self.col_str = self.get_table_columns(self.verify_tablename, self.ads_prj, self.remove_col_list)


        if where_condition == ''or where_condition =='\n':
            self.where_condition = where_condition
        else:
            self.where_condition = 'where {}'.format(where_condition)

    def execute(self, sql):
        instance = self.odps.execute_sql(sql)
        with instance.open_reader() as reader: 
            records = [record[:] for record in reader] 
            return records

    def get_table_columns(self, table_name, prj, remove_col_list):
        """
        Ali get column names of the table
        """
        t = self.odps.get_table(table_name, project=prj)
        odps_columns = t.schema.columns
        columns = []
        for i in odps_columns:
            columns.append(i.name.upper())
        columns.sort()
        res = ','.join([c.upper() for c in columns if c not in remove_col_list])
        # self.logger.info('get_table_columns: ' + str(res))
        return res
    
    def get_batch_error_sql(self):
        if self.error_str_list:
            return f"select {self.col_str} from {self.ads_prj}.{self.verify_tablename} where {self.batch_check_column} = '{self.batch_dt}' and {self.pi_str} in ({','.join(self.error_str_list)})"

    def convert_to_str(self, s):
        """
        convert values into string
        :param s:
        :return:
        """
        if isinstance(s, Decimal):
            if str(s.to_integral() if s == s.to_integral() else s.normalize()).endswith('.0'):
                return str(s.to_integral() if s == s.to_integral() else s.normalize()).split('.0')[0]
            else:
                return str(s.to_integral() if s == s.to_integral() else s.normalize())
        elif s is None:
            return ''
        else:
            # add 换行符和空格处理
            s_str = str(s).replace('\n', '').replace('\r', '').replace(' ', '')
            # 不管小数点后面多少0，用正则表达式去掉后面小数点
            simplified_str = re.sub(r'\.0+$', '', s_str)
            return simplified_str

    def convert2str(self, s):
        if isinstance(s, Decimal):
            return str(s.to_integral() if s == s.to_integral() else s.normalize())
        elif s is None:
            return ''
        else:
            return str(s)

    def get_batch_value_check_sql(self, pi_str, col_str, pi, verifydb, verify_tablename):
        # print(11111,pi)
        if verifydb == '':
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verify_tablename} {self.where_condition} order by {pi}  \n"
        else:
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename}  {self.where_condition} order by {pi}   \n"

    def get_batch_value_check_sql_int(self, pi_str, col_str, pi, verifydb, verify_tablename):
        # print(11111,pi)
        if verifydb == '':
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verify_tablename} {self.where_condition} order by to_char({pi})  \n"
        else:
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename}  {self.where_condition} order by to_char({pi})   \n"

    def get_batch_count_check_sql(self, verify_tablename, verifydb):
        if verifydb == '':
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from {verify_tablename} {self.where_condition}\n"
        else:
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from {verifydb}.{verify_tablename} {self.where_condition}\n"
        return sql


    def shipping_count_container(self):
        sql = self.get_batch_count_check_sql(self.verify_tablename, self.verifydb)
        # self.logger.info(sql)
        counts = self.execute(sql)
        self.count = {count_type: count for tablename, count_type, count in counts}

    def shipping_value_container(self):
        runsql = self.get_batch_value_check_sql(self.pi_str, self.col_str, self.pi, self.verifydb,
                                                self.verify_tablename)
        runsql_int = self.get_batch_value_check_sql_int(self.pi_str, self.col_str, self.pi, self.verifydb,
                                                        self.verify_tablename)
        print("**sql_value:", runsql)

        # self.logger.info(runsql)
        try:
            records = self.execute(runsql_int)
        except:
            records = self.execute(runsql)

        self.gen_md5(records, self.str_container, self.md5_container, self.ori_data)
    
# class TdValidator(Validator):
#     def __init__(self, host=None, user=None, password=None,columndb=None, exportdb=None, mi_code=None, pi=None,where_condition:str=None,**kwargs):
#         super().__init__(**kwargs)
#         # self.con = udaExec.connect(method="odbc", system=kwargs["host"], username=kwargs["user"], password=kwargs["password"],charset='utf8')
#         self.columns_dict = {}
#         self.con = teradatasql.connect(host=host, user=user, password=password)
#         self.columndb = columndb
#         self.exportdb = exportdb
#         # self.pre_mi_code = mi_code
#         self.pi = pi or self._getpi()
#         self.column_list = self._get_table_columns(self.verify_tablename, self.columndb)
#         self.column_list.sort()
#         self.columnType_dict = {columnName: columnType for columnName, columnType in self.column_list}
#         self.pi_str = self._get_pi_str("trim(", ")")
#         # self.col_str = self.get_table_columns_str('trim(', ")", self.remove_col_list)
#         self.col_str = self.get_table_columns_str2(self.remove_col_list,)

#         if where_condition == ''or where_condition =='\n':
#             self.where_condition = where_condition
#         else:
#             self.where_condition = 'where {}'.format(where_condition)


#     def execute(self, sql):
#         # self.logger.info(sql)
#         cur = self.con.cursor()
#         cur.execute(sql)
#         return cur.fetchall()

#     def get_table_columns_str(self, sql_preflix, sql_suffix, remove_col_list):
#         columns = []
#         for columName, columnType in self.column_list:
#             if columName not in remove_col_list:
#                 if columnType in ('CV','CF'):
#                     columns.append(f"{sql_preflix}{columName}{sql_suffix}")
#                 else:
#                     # columns.append(f"{sql_preflix}{columName}{sql_suffix}")
#                     columns.append(columName)

#         res = ','.join(columns)
#         # self.logger.info('get_table_columns_str: ' + res)
#         return res

#     def get_table_columns_str2(self, remove_col_list):
#         columns = []
#         for columName, columnType in self.column_list:
#             if columName not in remove_col_list:
#                 if columnType in ('CV', 'CF'):
#                     columns.append(f"{columName}")
#                 else:
#                     # columns.append(f"{sql_preflix}{columName}{sql_suffix}")
#                     columns.append(columName)

#         res = ','.join(columns)
#         # self.logger.info('get_table_columns_str: ' + res)
#         return res

#     def _getpi(self):
#         runsql = f"select columnName from dbc.indicesv where tablename = '{self.verify_tablename}' and databaseName = '{self.columndb}' and indextype in ('P','Q');"
#         pis = self.execute(runsql)
#         return ",".join([i[0]for i in pis])

#     def _get_pi_str(self, sql_preflix, sql_suffix):
#         pi_list = self.pi.split(",")
#         columns = []
#         for columName in pi_list:
#             if columName not in self.remove_col_list:
#                 if self.columnType_dict[columName] in ('CV','CF'):
#                     columns.append("{}{}{}".format(sql_preflix, columName, sql_suffix))
#                 else:
#                     # columns.append(f"{sql_preflix}{columName}{sql_suffix}")
#                     columns.append(columName)
#         # return ",',',".join(columns)
#         res = ','.join(columns)
#         # self.logger.error('_get_pi_str res: ' + res)
#         return res

#     def _get_table_columns(self, table_name, db):
#         """
#         TD get column names of the table
#         """
#         sql = "select trim(ColumnName), trim(ColumnType) from DBC.ColumnsV " \
#               "where DATABASENAME = '{}' and tablename = '{}' order by ColumnId;" \
#             .format(db, table_name)
#         # self.logger.info('_get_table_columns sql: ' + sql)
#         return self.execute(sql)

#     def get_batch_error_sql(self):
#         pi_str = "||".join(self.pi.split(","))
#         if self.error_str_list:
#             return f"select {self.col_str} from {self.exportdb}.{self.verify_tablename} where {self.batch_check_column} = '{self.batch_dt}' and {pi_str} in ({','.join(self.error_str_list)})"


class OraValidator(Validator):
    def __init__(self, host=None, user=None, password=None, columndb=None, exportdb=None, mi_code=None, pi=None,where_condition:str=None,
                 **kwargs):
        super().__init__(**kwargs)
        # self.con = udaExec.connect(method="odbc", system=kwargs["host"], username=kwargs["user"], password=kwargs["password"],charset='utf8')
        self.columns_dict = {}
        self.con = cx_Oracle.connect(user, password, host)
        self.columndb = columndb
        self.exportdb = exportdb
        # self.pre_mi_code = mi_code
        self.pi = pi or self._getpi()
        self.column_list = self._get_table_columns(self.verify_tablename)
        self.column_list.sort()
        # print (self.column_list)
        # self.columnType_dict = {columnName: columnType for columnName, columnType in self.column_list}
        # print(self.columnType_dict)
        self.pi_str = self._get_pi_str("trim(", ")")
        # self.col_str = self.get_table_columns_str('trim(', ")", self.remove_col_list)
        self.col_str = self.get_table_columns_str2(self.remove_col_list,self.pi)


        if where_condition == '':
            self.where_condition = where_condition
        else:
            self.where_condition = 'where {}'.format(where_condition)


    def execute(self, sql):
        # print(sql)
        cur = self.con.cursor()
        cur.execute(sql)
        # cur.close()
        # self.con.close()
        return cur.fetchall()

    def get_table_columns_str(self, sql_preflix, sql_suffix, remove_col_list):
        columns = []
        for columName, columnType in self.column_list:
            if columName not in remove_col_list:
                if columnType in ('CV', 'CF'):
                    columns.append(f"{sql_preflix}{columName}{sql_suffix}")
                else:
                    # columns.append(f"{sql_preflix}{columName}{sql_suffix}")
                    columns.append(columName)

        res = ','.join(columns)
        # self.logger.info('get_table_columns_str: ' + res)
        return res

    def get_table_columns_str2(self, remove_col_list,pi):
        columns = []
        for columName in self.column_list:
            if columName[0] not in remove_col_list and columName[0]!= pi:
                    columns.append(columName[0].upper())
        res = ','.join(columns)
        # self.logger.info('get_table_columns_str: ' + res)
        return res

    def _getpi(self):
        runsql = f"select columnName from dbc.indicesv where tablename = '{self.verify_tablename}' and databaseName = '{self.columndb}' and indextype in ('P','Q');"
        pis = self.execute(runsql)
        return ",".join([i[0] for i in pis])

    def _get_pi_str(self, sql_preflix, sql_suffix):
        pi_list = self.pi.split(",")
        columns = []
        for columName in pi_list:
            if columName not in self.remove_col_list:
                    # columns.append(f"{sql_preflix}{columName}{sql_suffix}")
                    columns.append(columName)
        # return ",',',".join(columns)
        res = ','.join(columns)
        # self.logger.error('_get_pi_str res: ' + res)
        return res

    def _get_table_columns(self, table_name):
        sql = "select trim(column_name) from all_tab_columns where Table_Name = '{}'".format(table_name)
        # print ('get_table_colums:',sql)
        # self.logger.info('_get_table_columns sql: ' + sql)
        return self.execute(sql)

    def get_batch_error_sql(self):
        pi_str = "||".join(self.pi.split(","))
        if self.error_str_list:
            return f"select {self.col_str} from {self.exportdb}.{self.verify_tablename} where {self.batch_check_column} = '{self.batch_dt}' and {pi_str} in ({','.join(self.error_str_list)})"

class PgValidator(Validator):
    def __init__(self, host=None, user=None, password=None, database=None, port=None, columndb=None, sourcedb=None, mi_code=None, pi=None,
                 where_condition: str = None,**kwargs):
        super().__init__(**kwargs)
        # self.con = udaExec.connect(method="odbc", system=kwargs["host"], username=kwargs["user"], password=kwargs["password"],charset='utf8')
        self.columns_dict = {}
        self.con = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        self.columndb = columndb
        self.sourcedb = sourcedb
        # self.pre_mi_code = mi_code
        self.pi = pi or self._getpi()
        self.column_list = self._get_table_columns(self.verify_tablename)
        self.column_list.sort()
        # self.columnType_dict = {columnName: columnType for columnName, columnType in self.column_list}
        # print(self.columnType_dict)
        self.pi_str = self._get_pi_str("trim(", ")")
        # self.col_str = self.get_table_columns_str('trim(', ")", self.remove_col_list)
        self.col_str = self.get_table_columns_str2(self.remove_col_list, self.pi)

        if where_condition == ''or where_condition =='\n':
            self.where_condition = where_condition
        else:
            self.where_condition = 'where {}'.format(where_condition)

    def execute(self, sql):
        print(sql)
        cur = self.con.cursor()
        cur.execute(sql)
        # cur.close()
        # self.con.close()
        return cur.fetchall()

    def get_table_columns_str(self, sql_preflix, sql_suffix, remove_col_list):
        columns = []
        for columName, columnType in self.column_list:
            if columName not in remove_col_list:
                if columnType in ('CV', 'CF'):
                    columns.append(f"{sql_preflix}{columName}{sql_suffix}")
                else:
                    # columns.append(f"{sql_preflix}{columName}{sql_suffix}")
                    columns.append(columName)

        res = ','.join(columns)
        # self.logger.info('get_table_columns_str: ' + res)
        return res

    def get_table_columns_str2(self, remove_col_list, pi):
        columns = []
        for columName in self.column_list:
            if columName[0] not in remove_col_list and columName[0] != pi:
                columns.append(columName[0].upper())
        res = ','.join(columns)
        # self.logger.info('get_table_columns_str: ' + res)
        return res

    def _getpi(self):
        runsql = f"select columnName from dbc.indicesv where tablename = '{self.verify_tablename}' and databaseName = '{self.columndb}' and indextype in ('P','Q');"
        pis = self.execute(runsql)
        return ",".join([i[0] for i in pis])

    def _get_pi_str(self, sql_preflix, sql_suffix):
        pi_list = self.pi.split(",")
        columns = []
        for columName in pi_list:
            if columName not in self.remove_col_list:
                # columns.append(f"{sql_preflix}{columName}{sql_suffix}")
                columns.append(columName)
        # return ",',',".join(columns)
        res = ','.join(columns)
        # self.logger.error('_get_pi_str res: ' + res)
        return res

    def _get_table_columns(self, table_name):
        # sql = "select trim(column_name) from user_tab_columns where Table_Name = '{}'".format(table_name)

        sql = "SELECT attname FROM pg_class as c,pg_attribute as a where c.relname = '{}' and a.attrelid = c.oid and a.attnum>0".format(table_name.lower())
        # self.logger.info('_get_table_columns sql: ' + sql)
        return self.execute(sql)

    def get_batch_error_sql(self):
        pi_str = "||".join(self.pi.split(","))
        if self.error_str_list:
            return f"select {self.col_str} from {self.sourcedb}.{self.verify_tablename} where {self.batch_check_column} = '{self.batch_dt}' and {pi_str} in ({','.join(self.error_str_list)})"


    def get_batch_value_check_sql(self, pi_str, col_str, pi, verifydb, verify_tablename):
        # P_common = Parameter_common()
        rule = 'Default'
        # print(11111,pi)
        if verifydb == '':
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verify_tablename} {self.where_condition} order by {pi}  \n"
        elif rule=="Check-the-first-200-rows":
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename}  order by {pi}  limit 200  \n"
        elif rule=="Check-the-first-500-rows":
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename}  order by {pi}  limit 500 \n"
        elif rule=="Check-the-first-1000-rows":
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename} order by {pi}   limit 1000  \n"
        else:
            return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename}  {self.where_condition} order by {pi}   \n"

    def get_batch_count_check_sql(self, verify_tablename, verifydb):
        # P_common = Parameter_common()
        rule = 'Default'
        if verifydb == '':
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from {verify_tablename} {self.where_condition}\n"
        elif rule == "Check-the-first-200-rows":
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from (select * from {verifydb}.{verify_tablename}  limit 200) as t\n"
        elif rule == "Check-the-first-500-rows":
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from (select * from {verifydb}.{verify_tablename}  limit 500) as t\n"
        elif rule == "Check-the-first-1000-rows":
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from (select * from {verifydb}.{verify_tablename}  limit 1000) as t\n"
        else:
            sql = f"select cast('{verify_tablename}' as varchar(100)) tablename, cast('total_count' as varchar(20)) as count_type, count(1) as c from {verifydb}.{verify_tablename} {self.where_condition}\n"
        return sql

class MysqlValidator(Validator):
    def __init__(self, host=None, user=None, password=None, database=None, port=None, columndb=None, sourcedb=None, mi_code=None, pi=None, where_condition: str = None, **kwargs):
        super().__init__(**kwargs)
        self.columns_dict = {}
        self.con = pymysql.connect(database=database, user=user, password=password, host=host, port=port)
        self.columndb = columndb
        self.sourcedb = sourcedb
        self.database = database
        self.pi = pi or self._getpi()
        self.column_list = self._get_table_columns(self.verify_tablename.lower())
        print(111,self.column_list)
        self.column_list.sort()
        self.pi_str = self._get_pi_str("TRIM(", ")")
        self.col_str = self.get_table_columns_str2(self.remove_col_list, self.pi)

        if where_condition == '' or where_condition == '\n':
            self.where_condition = where_condition
        else:
            self.where_condition = f'WHERE {where_condition}'

    def execute(self, sql):
        print(sql)
        cur = self.con.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def get_table_columns_str(self, sql_prefix, sql_suffix, remove_col_list):
        columns = []
        for columnName, columnType in self.column_list:
            if columnName not in remove_col_list:
                if columnType in ('CV', 'CF'):
                    columns.append(f"{sql_prefix}{columnName}{sql_suffix}")
                else:
                    columns.append(columnName)
        return ','.join(columns)

    def get_table_columns_str2(self, remove_col_list, pi):
        columns = []
        for columnName in self.column_list:
            if columnName not in remove_col_list and columnName != pi:
                columns.append(columnName.upper())
        return ','.join(columns)

    def _getpi(self):
        runsql = f"SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = '{self.verify_tablename}' AND TABLE_SCHEMA = '{self.columndb}' "
        pis = self.execute(runsql)
        return ",".join([i[0] for i in pis])

    def _get_pi_str(self, sql_prefix, sql_suffix):
        pi_list = self.pi.split(",")
        columns = []
        for columnName in pi_list:
            if columnName not in self.remove_col_list:
                columns.append(columnName)
        return ','.join(columns)


    def _get_table_columns(self, table_name):
        sql = f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{self.database}';"
        result = self.execute(sql)
        columns = [row[0] for row in result]
        return columns

    def get_batch_error_sql(self):
        pi_str = "||".join(self.pi.split(","))
        if self.error_str_list:
            return f"SELECT {self.col_str} FROM {self.sourcedb}.{self.verify_tablename} WHERE {self.batch_check_column} = '{self.batch_dt}' AND {pi_str} IN ({','.join(self.error_str_list)})"

    def get_batch_value_check_sql(self, pi_str, col_str, pi, verifydb, verify_tablename):
        P_common = Parameter_common()
        rule = P_common.select_rules
        if verifydb == '':
            return f"SELECT {pi_str},'{self.pi_split}',{col_str} FROM {verify_tablename} {self.where_condition} ORDER BY {pi}\n"
        elif rule == "Check-the-first-200-rows":
            return f"SELECT {pi_str},'{self.pi_split}',{col_str} FROM {verifydb}.{verify_tablename} ORDER BY {pi} LIMIT 200\n"
        elif rule == "Check-the-first-500-rows":
            return f"SELECT {pi_str},'{self.pi_split}',{col_str} FROM {verifydb}.{verify_tablename} ORDER BY {pi} LIMIT 500\n"
        elif rule == "Check-the-first-1000-rows":
            return f"SELECT {pi_str},'{self.pi_split}',{col_str} FROM {verifydb}.{verify_tablename} ORDER BY {pi} LIMIT 1000\n"
        else:
            return f"SELECT {pi_str},'{self.pi_split}',{col_str} FROM {self.verify_tablename.lower()} {self.where_condition} ORDER BY {pi}\n"

    def get_batch_count_check_sql(self, verify_tablename, verifydb):
        P_common = Parameter_common()
        rule = P_common.select_rules
        if verifydb == '':
            sql = f"SELECT CAST('{verify_tablename}' AS CHAR(100)) tablename, CAST('total_count' AS CHAR(20)) AS count_type, COUNT(1) AS c FROM {self.verify_tablename.lower()}\n"
        elif rule == "Check-the-first-200-rows":
            sql = f"SELECT CAST('{verify_tablename}' AS CHAR(100)) tablename, CAST('total_count' AS CHAR(20)) AS count_type, COUNT(1) AS c FROM (SELECT * FROM {self.verify_tablename.lower()} LIMIT 200) AS t\n"
        elif rule == "Check-the-first-500-rows":
            sql = f"SELECT CAST('{verify_tablename}' AS CHAR(100)) tablename, CAST('total_count' AS CHAR(20)) AS count_type, COUNT(1) AS c FROM (SELECT * FROM {self.verify_tablename.lower()} LIMIT 500) AS t\n"
        elif rule == "Check-the-first-1000-rows":
            sql = f"SELECT CAST('{verify_tablename}' AS CHAR(100)) tablename, CAST('total_count' AS CHAR(20)) AS count_type, COUNT(1) AS c FROM (SELECT * FROM {self.verify_tablename.lower()} LIMIT 1000) AS t\n"
        else:
            sql = f"SELECT CAST('{verify_tablename}' AS CHAR(100)) tablename, CAST('total_count' AS CHAR(20)) AS count_type, COUNT(1) AS c FROM {self.verify_tablename.lower()} {self.where_condition}\n"
        return sql


class FileValidator(Validator):
    def __init__(self, where_condition='',verifydb='',verify_tablename='',tablename='', table='',host=None, user=None, password=None, port=22, pi=None,**kwargs):
        # super().__init__(**kwargs)

        self.str_container = []
        self.md5_container = []
        self.ori_data = []
        self.count = {}
        self.sums = []
        self.error_str_list = []
        self.pi_split = "@@@"

        self.host = host
        self.port = port
        self.username = user
        self.password = password
        self.pi=pi
        self.table=table
        self.col_str = self.getcol()
        self.tablename = tablename
        self.verify_tablename=verify_tablename
        self.verifydb=verifydb
        self.where_condition=where_condition



    def getcol(self):
        test = mySSH(host=self.host, username=self.username, password=self.password,
                      remote_path=self.table, id=self.pi)
        col= test.connect_get_col_name()
        # print(22222,col)

        # col = col.sort()
        col=','.join(col)
        return col.upper()

    def ssh_value(self):
        test2 = mySSH(host=self.host, username=self.username, password=self.password,
                      remote_path=self.table, id=self.pi)
        col, records, count = test2.connect_ftp()
        return [col,records,count]

    def shipping_count_container(self):
        test = mySSH(host=self.host, username=self.username, password=self.password,
                     remote_path=self.table, id=self.pi)
        count = test.connect_get_count()
        self.count = {'total_count': int(count)}

    def shipping_value_container(self):

        col,records,count = self.ssh_value()
        # config.read(iniPath_ssh)  # 读取 ini 文件
        new_col=self.col_str
        # new_col = config.get('ssh', 'colname')
        records.rename(columns=str.upper, inplace=True)
        sort_col_name = [i for i in new_col.split(',')]
        sort_col_name.sort()


        sort_col_name.insert(0, 'ID_NO')
        sort_col_name.insert(1, 'PI_SPLIT')

        self.gen_md5(records[sort_col_name].values.tolist(), self.str_container, self.md5_container, self.ori_data)


    def gen_md5(self, records, str_container:List, md5_container:List, ori_data:List ):
        for record in records:
            # print(record)
            join_str = "".join([self.convert_to_str(i) for i in record])
            join_str2 = ",".join([self.convert_to_str(i) for i in record])
            # ori_str = join_str2.split("@@@,")[1]
            ori_str = join_str2
            md5_str = md5(join_str.encode('utf-8')).hexdigest()
            # print(join_str)
            str_container.append(join_str)
            md5_container.append(md5_str)
            ori_data.append(ori_str)

    def convert_to_str(self, s):
        """
        convert values into string
        :param s:
        :return:
        """
        if isinstance(s, Decimal):
            if str(s.to_integral() if s == s.to_integral() else s.normalize()).endswith('.0'):
                return str(s.to_integral() if s == s.to_integral() else s.normalize()).split('.0')[0]
            else:
                return str(s.to_integral() if s == s.to_integral() else s.normalize())
        elif s is None:
            return ''
        else:
            # add 换行符和空格处理
            s_str = str(s).replace('\n', '').replace('\r', '').replace(' ', '')
            if s_str.endswith('.0'):
                return s_str.split('.0')[0]
            elif s_str.endswith('.00'):
                return s_str.split('.00')[0]
            elif s_str.endswith('.000'):
                return s_str.split('.000')[0]
            elif s_str.endswith('.0000'):
                return s_str.split('.0000')[0]
            elif s_str.endswith('.00000'):
                return s_str.split('.00000')[0]
            elif s_str.endswith('.000000'):
                return s_str.split('.000000')[0]
            elif s_str.endswith('.0000000'):
                return s_str.split('.0000000')[0]
            elif s_str.endswith('.00000000'):
                return s_str.split('.00000000')[0]
            elif s_str.endswith('.000000000'):
                return s_str.split('.000000000')[0]
            elif s_str.endswith('.0000000000'):
                return s_str.split('.0000000000')[0]
            else:
                return s_str

class FileValidator_no_col(Validator):
    def __init__(self, where_condition='',verifydb='',verify_tablename='',tablename='', table='',host=None, user=None, password=None, port=22, pi=None,**kwargs):
        # super().__init__(**kwargs)

        self.str_container = []
        self.md5_container = []
        self.ori_data = []
        self.count = {}
        self.sums = []
        self.error_str_list = []
        self.pi_split = "@@@"

        self.host = host
        self.port = port
        self.username = user
        self.password = password
        self.pi=pi
        self.table=table
        self.col_str = self.getcol()
        self.tablename = tablename
        self.verify_tablename=verify_tablename
        self.verifydb=verifydb
        self.where_condition=where_condition



    def getcol(self):
        pass

    def ssh_value(self):
        test2 = mySSH(host=self.host, username=self.username, password=self.password,
                      remote_path=self.table)
        records, count = test2.connect_ftp_no_col()
        return [records,count]

    def shipping_count_container(self):
        test = mySSH(host=self.host, username=self.username, password=self.password,
                     remote_path=self.table)
        count = test.connect_get_count_no_col()
        self.count = {'total_count': int(count)}

    def shipping_value_container(self):
        records, count = self.ssh_value()

        # 自动生成列名
        records.columns = [f'col{i + 1}' for i in range(records.shape[1])]

        sort_col_name = list(records.columns)
        # print(sort_col_name)
        # # 假设你需要的列名中包含ID_NO和PI_SPLIT
        # sort_col_name.insert(0, 'ID_NO')
        # sort_col_name.insert(1, 'PI_SPLIT')
        #
        # print(sort_col_name)
        # sort_col_name = list(records.columns)
        # print(sort_col_name)

        self.gen_md5(records[sort_col_name].values.tolist(), self.str_container, self.md5_container, self.ori_data)

    def gen_md5(self, records, str_container:List, md5_container:List, ori_data:List ):
        for record in records:
            # print(record)
            join_str = "".join([self.convert_to_str(i) for i in record])
            join_str2 = ",".join([self.convert_to_str(i) for i in record])
            # ori_str = join_str2.split("@@@,")[1]
            ori_str = join_str2
            md5_str = md5(join_str.encode('utf-8')).hexdigest()
            # print(join_str)
            str_container.append(join_str)
            md5_container.append(md5_str)
            ori_data.append(ori_str)

    def convert_to_str(self, s):
        """
        convert values into string
        :param s:
        :return:
        """
        if isinstance(s, Decimal):
            if str(s.to_integral() if s == s.to_integral() else s.normalize()).endswith('.0'):
                return str(s.to_integral() if s == s.to_integral() else s.normalize()).split('.0')[0]
            else:
                return str(s.to_integral() if s == s.to_integral() else s.normalize())
        elif s is None:
            return ''
        else:
            # add 换行符和空格处理
            s_str = str(s).replace('\n', '').replace('\r', '').replace(' ', '')
            if s_str.endswith('.0'):
                return s_str.split('.0')[0]
            elif s_str.endswith('.00'):
                return s_str.split('.00')[0]
            elif s_str.endswith('.000'):
                return s_str.split('.000')[0]
            elif s_str.endswith('.0000'):
                return s_str.split('.0000')[0]
            elif s_str.endswith('.00000'):
                return s_str.split('.00000')[0]
            elif s_str.endswith('.000000'):
                return s_str.split('.000000')[0]
            elif s_str.endswith('.0000000'):
                return s_str.split('.0000000')[0]
            elif s_str.endswith('.00000000'):
                return s_str.split('.00000000')[0]
            elif s_str.endswith('.000000000'):
                return s_str.split('.000000000')[0]
            elif s_str.endswith('.0000000000'):
                return s_str.split('.0000000000')[0]
            else:
                return s_str


class AliValidator_batch(Validator):
    def __init__(self, ods_prj=None, ads_prj="", access_id="", secret_access_key="", endpoint="", pi=None,
                 where_condition: str = None, id_per_batch=None, remove_col_list=None,**kwargs):
        super().__init__(**kwargs)
        # self.ods_prj = ods_prj
        if id_per_batch is None:
            id_per_batch = []
        self.id_per_batch =id_per_batch

        self.ads_prj = ads_prj
        self.pre_tblname_oss = "OSS"
        self.pre_tblname_CDS_T1 = "CDS_T1"
        self.pre_tblname_CDS_T2 = "CDS_T2"
        self.pre_tblname_CDS = "CDS"

        self.odps = ODPS(access_id=access_id,
                         secret_access_key=secret_access_key,
                         project=self.ads_prj,
                         endpoint=endpoint)

        # print(access_id,secret_access_key,self.ads_prj,endpoint)
        # self.odps = ODPS(access_id='FYBlngS1UDOUAqNO', #登陆账号
        # secret_access_key='YOsAjo6f0pgyKGrnUoDaQG7gCllToQ', #登陆密码
        # project='CN_CDS_DEV', #odps上的项目名称
        # endpoint='https://service.cn-hk-hsbc-d01.odps.ali-ops.cloud.cn.hsbc:443/api') #官方提供的接口
        sql_spilt = "||\"|\"||"
        self.pi = pi
        self.pi_list = self.pi.split(",")
        self.pi_str = f'{self.pi.replace(",", sql_spilt)} as id_no'
        # print(111111, self.pi_str)

        self.remove_col_list = remove_col_list
        a=[]
        for i in self.remove_col_list.split(","):
            a.append(i.upper().strip())
        self.remove_col_list = a
        # print(11111,self.remove_col_list)

        # self.pi_str = ",',',".join([f"{i} as id" for i in self.pi_list if i not in self.remove_col_list])
        self.col_str = self.get_table_columns(self.verify_tablename, self.ads_prj, self.remove_col_list)

        if where_condition == '' or where_condition == '\n':
            self.where_condition = where_condition
        else:
            self.where_condition = 'where {}'.format(where_condition)

    def execute(self, sql):
        instance = self.odps.execute_sql(sql)
        with instance.open_reader() as reader:
            records = [record[:] for record in reader]
            return records

    def get_table_columns(self, table_name, prj, remove_col_list):
        """
        Ali get column names of the table
        """
        t = self.odps.get_table(table_name, project=prj)
        odps_columns = t.schema.columns
        columns = []
        for i in odps_columns:
            columns.append(i.name.upper())
        columns.sort()
        res = ','.join([c.upper() for c in columns if c not in remove_col_list])
        # self.logger.info('get_table_columns: ' + str(res))
        return res

    def get_batch_error_sql(self):
        if self.error_str_list:
            return f"select {self.col_str} from {self.ads_prj}.{self.verify_tablename} where {self.batch_check_column} = '{self.batch_dt}' and {self.pi_str} in ({','.join(self.error_str_list)})"



    def shipping_value_container2(self):
        runsql = self.get_batch_value_check_sql(self.pi_str, self.col_str, self.pi, self.verifydb, self.verify_tablename)
        print("**sql_value:", runsql)

        # self.logger.info(runsql)
        records = self.execute(runsql)
        self.gen_md5(records, self.str_container, self.md5_container,self.ori_data)

    def shipping_value_container(self):

        # sessionid_list = glob.get_value('sessionid')
        while not q.empty():
            sessionid_list = q.get()
            sessionid_list.sort()
            # self.logger.info(f"sessionid is {type(sessionid_list)}")
            self.logger.info(f"################ sessionid is {sessionid_list}  ")
            sessionid = str(tuple(sessionid_list))
            # self.logger.info(f"sessionid is {sessionid}")
            runsql = self.get_batch_value_check_sql(self.pi_str, self.col_str, self.pi, self.verifydb,
                                                    self.verify_tablename, sessionid)
            print("**sql_value:", runsql)

            # self.logger.info(runsql)
            records = self.execute(runsql)

            self.gen_md5(records, self.str_container, self.md5_container, self.ori_data)


    def get_batch_value_check_sql(self, pi_str, col_str, pi, verifydb, verify_tablename, sessionid):
        if verifydb == '':
            if len(sessionid):
                # self.logger.info("one")
                return f"select {pi_str},'{self.pi_split}',{col_str} from {verify_tablename} {self.where_condition} where and {pi} in {sessionid} order by {pi} \n"
            else:
                # self.logger.info("two")
                return f"select {pi_str},'{self.pi_split}',{col_str} from {verify_tablename} {self.where_condition} order by {pi} \n"
        else:
            if len(sessionid):
                # self.logger.info("three")
                return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename} {self.where_condition} and {pi} in {sessionid} order by {pi} \n"
            else:
                # self.logger.info("four")
                return f"select {pi_str},'{self.pi_split}',{col_str} from {verifydb}.{verify_tablename} {self.where_condition} and order by {pi} \n"

class FileValidator_batch(Validator):
    def __init__(self, where_condition='',verifydb='',verify_tablename='',tablename='', table='',host=None, user=None, password=None, port=22, pi=None,**kwargs):
        # super().__init__(**kwargs)

        self.str_container = []
        self.md5_container = []
        self.ori_data = []
        self.count = {}
        self.sums = []
        self.error_str_list = []
        self.pi_split = "@@@"

        self.host = host
        self.port = port
        self.username = user
        self.password = password
        self.pi=pi
        self.table=table
        self.col_str = self.getcol()
        self.tablename = tablename
        self.verify_tablename=verify_tablename
        self.verifydb=verifydb
        self.where_condition=where_condition



    def getcol(self):

        test = mySSH(host=self.host, username=self.username, password=self.password,
                      remote_path=self.table, id=self.pi)
        col = test.connect_get_col_name()
        # col.remove("id")
        # col.remove("pi_split")
        # col = col.sort()
        col=','.join(col)
        return col.upper()

    def ssh_value(self):
        test2 = mySSH(host=self.host, username=self.username, password=self.password,
                      remote_path=self.table, id=self.pi)
        col, records, count = test2.connect_ftp()
        return [col,records,count]

    def ssh_value_batch(self):
        test3 = mySSH(host=self.host, username=self.username, password=self.password,
                      remote_path=self.table, id=self.pi)
        records = test3.connect_ftp_batch()
        return records

    def shipping_count_container(self):
        test2 = mySSH(host=self.host, username=self.username, password=self.password,
                     remote_path=self.table, id=self.pi)
        count = test2.connect_get_count()
        self.count = {'total_count': int(count)}

    def shipping_value_container(self):

        self.batch_process()


    def batch_process(self):
        new_col = self.col_str
        sort_col_name = [i.strip().upper() for i in new_col.split(',')]
        sort_col_name.sort()
        # print(222,sort_col_name)
        sort_col_name.insert(0, 'ID_NO')
        sort_col_name.insert(1, 'PI_SPLIT')
        # print(111, sort_col_name)
        records = self.ssh_value_batch()

        for rec in records:
            rec.rename(columns=str.upper, inplace=True)
            self.id_per_batch = rec[self.pi.upper()].values.tolist()
            # glob.set_value('sessionid', self.id_per_batch)
            q.put(self.id_per_batch)
            self.gen_md5(rec[sort_col_name].values.tolist(), self.str_container, self.md5_container, self.ori_data)


    def gen_md5(self, records, str_container:List, md5_container:List, ori_data:List ):
        for record in records:
            # print(record)
            join_str = "".join([self.convert_to_str(i) for i in record])
            join_str2 = ",".join([self.convert_to_str(i) for i in record])
            # ori_str = join_str2.split("@@@,")[1]
            ori_str = join_str2
            md5_str = md5(join_str.encode('utf-8')).hexdigest()
            # print(join_str)
            str_container.append(join_str)
            md5_container.append(md5_str)
            ori_data.append(ori_str)

