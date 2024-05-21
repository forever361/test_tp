import configparser
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import psycopg2

sys.path.append('..')

from app.util import global_manager
from app.util.log_util.all_new_log import logger_all

user_id = sys.argv[1]
# user_id = '580515'
global_manager._init()
global_manager.set_value('user_id', user_id)

from app.data2_check.commom.Constant_t import Constant_id



# from mapping import ValidateStatue
from openpyxl import Workbook

from app.data2_check.parameter import Parameter_pg_pg, Parameter_file_ali, Parameter_tmp
# from app.useDB import ConnectSQL




import app.data2_check.checker as checker
# import argparse
from odps import ODPS
from collections import defaultdict

import math
import cx_Oracle
import csv
from app.data2_check.parameter import Parameter_or_ali, Parameter_or_or,Parameter_ali_ali,Parameter_common,Parameter_db,Parameter_pg_ali
from app.data2_check.commom.main_Gen import Parser as GenReport
from app.data2_check.commom.write_excel_data import ExcelUtilAll
from app.util.log_util.new_log import logger
from app.application import app



basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))

# argparser = argparse.ArgumentParser(description='Usage for Verify.py')
# argparser.add_argument('-pw', "--password", help='example: -p xxxxxx this parameter is optional', default=False)
# argparser.add_argument('-u', "--user", help='example: -u xxxxxx this parameter is optional ', default=False)
# argparser.add_argument('-p', "--parameter", help='parameter（参数）：在./parameters/batch_check/路径下存放你需要的参数文件', required=False)
# argparser.add_argument('-m', "--mi_code", help='mi code is used for get password', required=False)
# argparser.add_argument('-e', '--env', help='env: input UAT or PROD', default='UAT')
# argparser.add_argument('-c', "--count", help='count check', action='store_true')
# argparser.add_argument('-v', "--value", help='value check', action='store_true')
# _args = argparser.parse_args()
# LOG_PATH = basePath + './LOG/'

#db type

Excel_write = ExcelUtilAll()
userid = Constant_id().cookie_id


P_common = Parameter_common()
# print(P_common)
S_TYPE = P_common.source_type.strip().split('=')[-1].strip()  # orl,ali,pg
print("source: " + S_TYPE)
T_TYPE = P_common.target_type.strip().split('=')[-1].strip()  # orl,ali,pg
print("target: " + T_TYPE)


rule = P_common.select_rules
logger.info(" check rule is : {}".format(rule))


# db config
P_db = Parameter_db()


if S_TYPE == 'orl' and T_TYPE == 'ali':

    P_OR = Parameter_or_ali()

    HOST_S = P_OR.host
    USER_S = P_OR.user
    PASSWORD_S = P_OR.pwd

    ACCESS_ID = P_OR.access_id
    SECRET_ACCESS_KEY = P_OR.secret_access_key
    ENDPOINT = P_OR.endpoint
    PROJECT = P_OR.project

    # logger.info([ACCESS_ID, SECRET_ACCESS_KEY, ENDPOINT, PROJECT])
    logger.info([ACCESS_ID, SECRET_ACCESS_KEY, ENDPOINT, PROJECT])

    con_s = cx_Oracle.connect(USER_S, PASSWORD_S, HOST_S)
    odps_t = ODPS(access_id=ACCESS_ID, secret_access_key=SECRET_ACCESS_KEY, project=PROJECT, endpoint=ENDPOINT)

elif S_TYPE == 'orl' and T_TYPE == 'orl':

    P = Parameter_or_or()
    HOST_S = P.host_s
    USER_S = P.user_s
    PASSWORD_S = P.pwd_s

    HOST_T = P.host_t
    USER_T = P.user_t
    PASSWORD_T = P.pwd_t

    con_s = cx_Oracle.connect(USER_S, PASSWORD_S, HOST_S)
    con_t = cx_Oracle.connect(USER_T, PASSWORD_T, HOST_T)

elif S_TYPE == 'ali' and T_TYPE == 'ali':
    P = Parameter_ali_ali()

    ACCESS_ID_S = P.access_id_s
    SECRET_ACCESS_KEY_S = P.secret_access_key_s
    ENDPOINT_S = P.endpoint_s
    PROJECT_S = P.project_s

    ACCESS_ID_T = P.access_id_t
    SECRET_ACCESS_KEY_T = P.secret_access_key_t
    ENDPOINT_T = P.endpoint_t
    PROJECT_T = P.project_t

    odps_s = ODPS(access_id=ACCESS_ID_S, secret_access_key=SECRET_ACCESS_KEY_S, project=PROJECT_S,
                  endpoint=ENDPOINT_S)
    odps_t = ODPS(access_id=ACCESS_ID_T, secret_access_key=SECRET_ACCESS_KEY_T, project=PROJECT_T,
                  endpoint=ENDPOINT_T)


elif S_TYPE == 'pg' and T_TYPE == 'ali':
    P = Parameter_pg_ali()

    DB_S = P.db
    USER_S = P.user
    PASSWORD_S = P.pwd
    HOST_S = P.host
    PORT_S = P.port

    ACCESS_ID_T = P.access_id_t
    SECRET_ACCESS_KEY_T = P.secret_access_key_t
    ENDPOINT_T = P.endpoint_t
    PROJECT_T = P.project_t

    con_s = psycopg2.connect(database=DB_S, user=USER_S, password=PASSWORD_S, host=HOST_S, port=PORT_S)
    odps_t = ODPS(access_id=ACCESS_ID_T, secret_access_key=SECRET_ACCESS_KEY_T, project=PROJECT_T,
                  endpoint=ENDPOINT_T)


elif S_TYPE == 'pg' and T_TYPE == 'pg':
    P = Parameter_pg_pg()

    DB_S = P.db_s
    USER_S = P.user_s
    PASSWORD_S = P.pwd_s
    HOST_S = P.host_s
    PORT_S = P.port_s

    DB_T = P.db_t
    USER_T = P.user_t
    PASSWORD_T = P.pwd_t
    HOST_T = P.host_t
    PORT_T = P.port_t

    # logger.info(["HOST_S:", HOST_S])
    # logger.info(["username:",USER_S])
    # logger.info(["pwd:", PASSWORD_S])
    # logger.info(["port:", PORT_S])
    # logger.info(["DB_S:", DB_S])

    con_s = psycopg2.connect(database=DB_S, user=USER_S, password=PASSWORD_S, host=HOST_S, port=PORT_S)
    con_t = psycopg2.connect(database=DB_T, user=USER_T, password=PASSWORD_T, host=HOST_T, port=PORT_T)


elif S_TYPE == 'landingserver_file' and T_TYPE == 'ali':
    P = Parameter_file_ali()

    HOST_S = P.host_s
    USER_S = P.user_s
    PASSWORD_S = P.pwd_s

    ACCESS_ID_T = P.access_id_t
    SECRET_ACCESS_KEY_T = P.secret_access_key_t
    ENDPOINT_T = P.endpoint_t
    PROJECT_T = P.project_t

    odps_t = ODPS(access_id=ACCESS_ID_T, secret_access_key=SECRET_ACCESS_KEY_T, project=PROJECT_T,
                  endpoint=ENDPOINT_T)


elif S_TYPE == 'landingserver_file_batch' and T_TYPE == 'ali_batch':
    P = Parameter_file_ali()

    HOST_S = P.host_s
    USER_S = P.user_s
    PASSWORD_S = P.pwd_s

    ACCESS_ID_T = P.access_id_t
    SECRET_ACCESS_KEY_T = P.secret_access_key_t
    ENDPOINT_T = P.endpoint_t
    PROJECT_T = P.project_t

    odps_t = ODPS(access_id=ACCESS_ID_T, secret_access_key=SECRET_ACCESS_KEY_T, project=PROJECT_T,
                  endpoint=ENDPOINT_T)

# cx_Oracle.init_oracle_client(lib_dir="C:\swdtools\instantclient_19_12")

PARAMETER_FILE_PATH = basePath + '/config/config_info_or_p.csv'
# PARAMETER_FILE_PATH = ConnectSQL().get_source_target_parameter(user_id,'ora')
REM_LIST_PATH = basePath + '/config/remove_list.csv'

def parse_parameter_files(parameter_value):
    for f in parameter_value:
        parameters_from_file = [i.strip().split(',')[0] for i in f]
        return [parameters_from_file]

def parse_parameter_file(parameter_file_path):
    with open(parameter_file_path, "r") as f:
        return [i.split(',') for i in f.readlines() if i[0] not in ('#', '\n')]

def parse_parameter_file2(parameter_file_path):
    with open(parameter_file_path, "r") as f:
        return [i.split(',') for i in f.readlines() if i[0] not in ('#', '\n')]

def parse_parameter_file3(parameter_file_path):
    with open(parameter_file_path, 'r', encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        result = []
        for i in csv_reader:
            result.append(i)
    return result

def parse_parameter_file_re(parameter_file_path):
    with open(parameter_file_path, "r") as f:
        for i in f.readlines():
            if i[0] not in ('#', '\n'):
                return i

def sql_execute_s(sql):
    cur = con_s.cursor()
    cur.execute(sql)
    return cur.fetchall()

def sql_execute_t(sql):
    cur = con_t.cursor()
    cur.execute(sql)
    return cur.fetchall()

def ali_execute_s(sql):
    instance = odps_s.execute_sql(sql)
    with instance.open_reader() as reader:
        records = [record[:] for record in reader]
        return records

def ali_execute_t(sql):
    instance = odps_t.execute_sql(sql)
    with instance.open_reader() as reader:
        records = [record[:] for record in reader]
        return records

def optimize_count_check(s_count_sql_list, t_count_sql_list):  # 这个函数很重要，查询出对比双方count，并输出最后对比结果,目前可以先不调用这个函数
    s_sql = "select * from (" + " union all ".join(s_count_sql_list) + ") t order by t.tablename desc"
    t_sql = "select * from (" + " union all ".join(t_count_sql_list) + ") t order by t.tablename desc"
    error_table_list = []

    if S_TYPE == 'orl' and T_TYPE == 'ali':
        s_counts = sql_execute_s(s_sql)
        t_counts = ali_execute_t(t_sql)

    elif S_TYPE == 'orl' and T_TYPE == 'orl':
        s_counts = sql_execute_s(s_sql)
        t_counts = sql_execute_t(t_sql)

    elif S_TYPE == 'ali' and T_TYPE == 'ali':
        s_counts = ali_execute_s(s_sql)
        t_counts = ali_execute_t(t_sql)

    elif S_TYPE == 'pg' and T_TYPE == 'ali':
        s_counts = sql_execute_s(s_sql)
        t_counts = ali_execute_t(t_sql)

    elif S_TYPE == 'pg' and T_TYPE == 'pg':
        s_counts = sql_execute_s(s_sql)
        t_counts = sql_execute_t(t_sql)

    s_count_dict = convert_count_result(s_counts)
    t_count_dict = convert_count_result(t_counts)
    count_check_flag = True
    for s_tablename, t_tablename in zip(s_count_dict.keys(), t_count_dict.keys()):
        # logger.info(f"table:{s_tablename}")
        table_count_check_flag = True
        for key in s_count_dict[s_tablename]:
            s = s_count_dict[s_tablename][key]
            t = t_count_dict[t_tablename][key]
            # s和t就是最终的count数
            # logger.info(f"|{key:<13} check|source:{s} target:{t}")
            # Excel_write.get_source_count(s)
            # Excel_write.get_target_count(t)

            if s != t:
                count_check_flag = False
                table_count_check_flag = False
                error_table_list.append(s_tablename)

        # Excel_write.get_source_table_name(s_tablename)
        # Excel_write.get_target_table_name(t_tablename)

        if table_count_check_flag:
            logger.info(f"{'=' * 20}{s_tablename:}:count check successfully{'=' * 20}")
            Excel_write.get_count_result_pass2(table_count_check_flag)

        else:
            logger.info(f"{'#' * 20}{s_tablename:^25}:count check failed{'#' * 20}")
            Excel_write.get_count_result_pass2(table_count_check_flag)
    return count_check_flag, list(set(error_table_list))

def convert_count_result(counts: list) -> dict:
    d = defaultdict(dict)
    for tablename, type, count in counts:
        d[tablename][type] = count
    return d

def configure_validator(
        source_table: str = '',
        target_table: str = '',
        columndb='',
        exportdb='',
        pi: str = '',
        s_where_condition='',
        t_where_condition='',
        remove_col_list=''
):
    # pi = pi.replace("|",",") or get_pi(f"{source_table}", columndb)
    pi = pi.replace("|", ",")
    # remove_col_list = parse_parameter_file_re(REM_LIST_PATH)
    remove_col_list = remove_col_list.replace("|", ",")

    if S_TYPE == 'orl' and T_TYPE == 'ali':
        logger.info("S:orl,T:ali")
        job_configure = {
            "source_validator": {
                "name": "OraValidator",
                "host": HOST_S,
                "user": USER_S,
                "password": PASSWORD_S,
                "tablename": source_table.split('_')[-1],
                "columndb": columndb,
                "remove_col_list": remove_col_list,
                "pi": pi,
                "verifydb": exportdb,
                "table": source_table.upper().strip(),
                "where_condition": s_where_condition
            },
            "target_validator": {
                "name": "AliValidator",
                "access_id": ACCESS_ID,
                "secret_access_key": SECRET_ACCESS_KEY,
                "endpoint": ENDPOINT,
                "ads_prj": PROJECT,
                "tablename": target_table.split('_')[-1],
                "pi": pi,
                "remove_col_list": remove_col_list,
                "table": target_table.upper().strip(),
                "verifydb": PROJECT,
                "where_condition": t_where_condition
            }
        }

    elif S_TYPE == 'orl' and T_TYPE == 'orl':
        logger.info("S:orl,T:orl")
        job_configure = {
            "source_validator": {
                "name": "OraValidator",
                "host": HOST_S,
                "user": USER_S,
                "password": PASSWORD_S,
                "tablename": source_table.split('_')[-1],
                "columndb": columndb,
                "remove_col_list": remove_col_list,
                "pi": pi,
                "verifydb": exportdb,
                "table": source_table.upper().strip(),
                "where_condition": s_where_condition
            },
            "target_validator": {
                "name": "OraValidator",
                "host": HOST_T,
                "user": USER_T,
                "password": PASSWORD_T,
                "tablename": target_table.split('_')[-1],
                "columndb": columndb,
                "remove_col_list": remove_col_list,
                "pi": pi,
                "verifydb": exportdb,
                "table": target_table.upper().strip(),
                "where_condition": t_where_condition
            }
        }

    elif S_TYPE == 'ali' and T_TYPE == 'ali':
        logger.info("S:ali,T:ali")
        job_configure = {
            "source_validator": {
                "name": "AliValidator",
                "access_id": ACCESS_ID_S,
                "secret_access_key": SECRET_ACCESS_KEY_S,
                "endpoint": ENDPOINT_S,
                "ads_prj": PROJECT_S,
                "tablename": source_table.split('_')[-1],
                "pi": pi,
                "remove_col_list": remove_col_list,
                "table": source_table.upper().strip(),
                "verifydb": PROJECT_S,
                "where_condition": s_where_condition
            },
            "target_validator": {
                "name": "AliValidator",
                "access_id": ACCESS_ID_T,
                "secret_access_key": SECRET_ACCESS_KEY_T,
                "endpoint": ENDPOINT_T,
                "ads_prj": PROJECT_T,
                "tablename": target_table.split('_')[-1],
                "pi": pi,
                "remove_col_list": remove_col_list,
                "table": target_table.upper().strip(),
                "verifydb": PROJECT_T,
                "where_condition": t_where_condition
            }
        }


    elif S_TYPE == 'pg' and T_TYPE == 'ali':
        logger.info("S:pg,T:ali")
        job_configure = {
            "source_validator": {
                "name": "PgValidator",
                "host": HOST_S,
                "user": USER_S,
                "password": PASSWORD_S,
                "port": PORT_S,
                "database": DB_S,
                "tablename": source_table.split('_')[-1],
                "pi": pi,
                "verifydb": exportdb,
                "remove_col_list": remove_col_list,
                "table": source_table.upper().strip(),
                "where_condition": s_where_condition
            },
            "target_validator": {
                "name": "AliValidator",
                "access_id": ACCESS_ID_T,
                "secret_access_key": SECRET_ACCESS_KEY_T,
                "endpoint": ENDPOINT_T,
                "ads_prj": PROJECT_T,
                "tablename": target_table.split('_')[-1],
                "pi": pi,
                "remove_col_list": remove_col_list,
                "table": target_table.upper().strip(),
                "verifydb": PROJECT_T,
                "where_condition": t_where_condition
            }
        }


    elif S_TYPE == 'pg' and T_TYPE == 'pg':
        logger.info("S:pg,T:pg")
        job_configure = {
            "source_validator": {
                "name": "PgValidator",
                "host": HOST_S,
                "user": USER_S,
                "password": PASSWORD_S,
                "port": PORT_S,
                "database": DB_S,
                "tablename": source_table.split('_')[-1],
                "pi": pi,
                "verifydb": exportdb,
                "remove_col_list": remove_col_list,
                "table": source_table.upper().strip(),
                "where_condition": s_where_condition
            },
            "target_validator": {
                "name": "PgValidator",
                "host": HOST_T,
                "user": USER_T,
                "password": PASSWORD_T,
                "port": PORT_T,
                "database": DB_T,
                "tablename": target_table.split('_')[-1],
                "pi": pi,
                "verifydb": exportdb,
                "remove_col_list": remove_col_list,
                "table": target_table.upper().strip(),
                "where_condition": t_where_condition
            }
        }

    elif S_TYPE == 'landingserver_file' and T_TYPE == 'ali':
        logger.info("S:file,T:ali")
        job_configure = {
            "source_validator": {
                "name": "FileValidator",
                "table": source_table,
                "host": HOST_S,
                "user": USER_S,
                "password": PASSWORD_S,
                "port": 22,
                "pi": pi,
                "tablename": '',
                "remove_col_list": remove_col_list,
                "where_condition": s_where_condition
            },
            "target_validator": {
                "name": "AliValidator",
                "access_id": ACCESS_ID_T,
                "secret_access_key": SECRET_ACCESS_KEY_T,
                "endpoint": ENDPOINT_T,
                "ads_prj": PROJECT_T,
                "tablename": target_table.split('_')[-1],
                "pi": pi,
                "remove_col_list": remove_col_list,
                "table": target_table.upper().strip(),
                "verifydb": PROJECT_T,
                "where_condition": t_where_condition
            }
        }


    elif S_TYPE == 'landingserver_file_batch' and T_TYPE == 'ali_batch':
        logger.info("S:file,T:ali_batch")
        job_configure = {
            "source_validator": {
                "name": "FileValidator_batch",
                "table": source_table,
                "host": HOST_S,
                "user": USER_S,
                "password": PASSWORD_S,
                "port": 22,
                "pi": pi,
                "tablename": '',
                "remove_col_list": remove_col_list,
                "where_condition": s_where_condition,
                "id_per_batch": []
            },
            "target_validator": {
                "name": "AliValidator_batch",
                "access_id": ACCESS_ID_T,
                "secret_access_key": SECRET_ACCESS_KEY_T,
                "endpoint": ENDPOINT_T,
                "ads_prj": PROJECT_T,
                "tablename": target_table.split('_')[-1],
                "pi": pi,
                "remove_col_list": remove_col_list,
                "table": target_table.upper().strip(),
                "verifydb": PROJECT_T,
                "where_condition": t_where_condition,
                "id_per_batch": []
            }
        }

    # _args.count = True
    # _args.value = True
    if S_TYPE == 'landingserver_file':
        c = checker.BatchChecker2(job_configure, True, True)
    elif rule=='Check-count':
        c = checker.BatchChecker_count(job_configure, True, True)
    else:
        c = checker.BatchChecker1(job_configure, True, True)

    s_count_sql, t_count_sql, v_satuts, c_status = c.check()
    return s_count_sql, t_count_sql, v_satuts, c_status, source_table



def method_main():

    # global parameter
    v_flag = True
    c_flag = True
    # p_list = parse_parameter_file(PARAMETER_FILE_PATH)
    p_list = P_db.parse_parameter_file()
    # logger.info(p_list)
    # p_lists = p_list
    # print(p_list)
    j = 0
    n_jobs = 20
    page_count = math.ceil(len(p_list) / n_jobs)
    value_check_error_list = []
    count_check_error_list = []
    config = configparser.ConfigParser()
    folder_path = os.path.join(app.root_path, 'static', 'user_files', user_id)

    user_path = '{}/userinfo/{}/'.format(configPath, userid)
    ini_path = folder_path + '/config/config.ini'
    config.read(ini_path)
    # clear excel
    excel_path = folder_path + '/config/verification_result.xlsx'
    if os.path.exists(excel_path):
        os.remove(excel_path)
        wb = Workbook()
        wb.save(excel_path)
    else:
        wb = Workbook()
        wb.save(excel_path)
    for i in range(1, page_count + 1):
        n = n_jobs * i
        p_list = p_list[j:n]
        j += n_jobs
        s_count_sql_list = []
        t_count_sql_list = []
        times = 1
        for parameter in p_list:  # 多批次处理list
            times = times + 1
            config.set("default", "times", str(times))
            with open(ini_path, "w+", encoding="utf8") as f:
                config.write(f)
            # print("times:", times)
            # 进入核心算法
            s_count_sql, t_count_sql, v_status, c_status, tablename = configure_validator(*parameter)

            s_count_sql_list.append(s_count_sql)  # 这两句也是为optimize_count_check服务，可以不要
            t_count_sql_list.append(t_count_sql)

            if v_status == "FAIL":
                v_flag = False
                value_check_error_list.append(tablename)

            if c_status == "FAIL":
                c_flag = False
                count_check_error_list.append(tablename)

            # if c_status == "FAIL":
            #     flag, error_list = optimize_count_check(s_count_sql_list,t_count_sql_list)  # s_count_sql_list和t_count_sql_list就是查count的两句sql
            #     if not flag:
            #         count_check_error_list.extend(error_list)
            #         c_flag = False

        # if _args.count:
        #     flag, error_list = optimize_count_check(s_count_sql_list, t_count_sql_list) #s_count_sql_list和t_count_sql_list就是查count的两句sql
        #     if not flag:
        #         count_check_error_list.extend(error_list)
        #         c_flag = False
    # print('v_flag',v_flag,'c_flag',c_flag)
    # print(count_check_error_list)
    # if v_flag:
    #     pass
    # else:
    #     logger.info(f"{'*'*30}value check fail, please check table:{str(value_check_error_list)}")
    if c_flag:
        pass
    else:
        logger.info(f"count check fail please check table:{str(count_check_error_list)}")
    GenReport().gen_html()
    # print('生成报告。。。。。。。。。。。。。。。。。。。。。。')


if __name__ == "__main__":

    method_main()
#

