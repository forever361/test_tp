import configparser
import json
import subprocess
import traceback
from time import sleep

from flask import Blueprint, render_template, jsonify, request, get_flashed_messages, session
# from app import log
from app.db import test_case_manage
from app.db.tanos_manage import tanos_manage
from app.util import global_manager
from app.util.log import logg

from app.useDB import ConnectSQL
from app.util.crypto_ECB import AEScoder
from app.util.log_util.all_new_log import logger_all
from app.view import user, viewutil
import os

from app.view.data_batch_new import get_log

from app.util.Constant_setting import Constant_cmd

web = Blueprint('data_testcase_tanos', __name__, template_folder='templates/uitest')
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
configP = configparser.ConfigParser()


@web.route('/api_data_test_cases_tanos')
@user.authorize
def test_cases():
    return render_template("uitest/data_test_cases.html")


@web.route('/data_edit_test_case_tanos', methods=['POST', 'GET'])
@user.authorize
def edit_test_case():
    user_id = session.get('userid', None)
    user_path = '{}/userinfo/{}/'.format(configPath, user_id)

    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')

        ini_path = user_path + '/' + 'config.ini'
        # 添加section
        configP.clear()
        configP.add_section("default")
        # 添加option并设置值，只能是string
        configP.set("default", "userid", str(user_id))
        configP.set("default", "caseid", str(id))
        configP.set("default", "times", str(2))
        configP.set("default", "returncode", 'NULL')
        # 写入ini文件，注意写入的mode会影响是否覆盖ini文件
        with open(ini_path, "w", encoding="utf8") as f:
            configP.write(f)

        infor_value = ConnectSQL().data_get_infor_value_id(id)
        print(infor_value)

        return render_template("uitest/data_edit_tanos_new.html")

    # SAVE保存的过程,点save就相当于提交了表单走post
    elif request.method == 'POST':
        case_id = request.args.get('id')
        print(case_id)

        return render_template('data_test_finish.html', user_id=user_id,
                                   case_id=case_id)


@web.route('/runtest_tanos.json', methods=['POST', 'GET'])
@user.authorize
def runtest_tanos():
    if request.method == 'POST':

        info = request.values
        code = viewutil.getInfoAttribute(info, 'code')
        code1 = viewutil.getInfoAttribute(info, 'code1')

        user_id = session.get('userid', None)
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)

        # # 清空日志
        with open(user_path + "log.log", 'w') as file:
            file.close()

        get_log(True)

        print(111111, "case subprocess!!!!")

        file = open(user_path + 'log.log', 'a')
        file.writelines(
            "|||||||||||||||||||||||||||||||||||||||Start checking|||||||||||||||||||||||||||||||||||||||" + '\n')
        file.writelines("Prepare data..." + '\n')
        file.close()

        retcode = Constant_cmd(user_id).retcode

        stdout, stderr = retcode.communicate()

        if stderr:
            print(str(stderr, "utf-8") + '111111')
        else:
            print(str(stdout, "utf-8") + '222222')

        if retcode.returncode == 0:
            print("Run 按钮执行成功！！")
            sleep(1.6)
            result = jsonify({'code': 200, 'msg': 'run success!', 'returncode': 0})
            print(result)
            return result

        else:
            print("执行失败！！")
            file = open(user_path + 'log.log', 'a')
            file.writelines(str(stderr, "utf-8") + '\n')
            file.close()
            sleep(1.6)
            result = jsonify({'code': 400, 'msg': 'run failed', 'returncode': 1})
            print(result)
            return result, {'Content-Type': 'application/json'}


@web.route('/data_search_report_tanos', methods=['POST', 'GET'])
@user.authorize
def web_search_report():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        info = request.values
        # print ('info',info)
        id = viewutil.getInfoAttribute(info, 'id')
        # print('idididiidididid', id)
        user_id = session.get('userid', None)

        return render_template("userinfo/{}/{}_data_test.html".format(user_id, id))




@web.route('/job_search2.json', methods=['GET'])
def data1():
    data2 = [{
        "job_id": 1,
        "job_name": 'job 1',
        "job": {"source":"a1","target":"b1"},
    }, {
        "job_id": 2,
        "job_name": 'job 2',
         "job": {"source":"a2","target":"b2"},
    },
        {
        "job_id": 3,
        "job_name": 'job 3',
        "job": {"source":"a3","target":"b3"},
    },

        {
            "job_id": 4,
            "job_name": 'job 4',
            "job": {"source": "a3", "target": "b3"},
    },
        {
            "job_id": 4,
            "job_name": 'job 4',
            "job": {"source": "a3", "target": "b3"},
    },
        {
            "job_id": 4,
            "job_name": 'job 4',
            "job": {"source": "a3", "target": "b3"},
    },

    ]

    return jsonify(data2)


@web.route('/job_search.json', methods=['GET'])
def show_data():
    rows = tanos_manage().show_jobs()
    keys=('job_id','job_name','job')
    result_list=[]
    for row in rows:
        values = [value.strip() if isinstance(value,str) else value for value in row]
        result_dict =dict(zip(keys,values))
        result_list.append(result_dict)
    print (result_list)
    return jsonify(result_list)


@web.route('/getMyPoint', methods=['GET'])
def getMyConnect():
    rows = tanos_manage().get_myPoints()
    # TODO: get data from the database
    print(rows)
    result_list = []
    for row in rows:
        values = [value.strip() if isinstance(value, str) else value for value in row]
        result_list.append(values[0])
    print(result_list)
    result = [{'value':item,'text':item} for item in result_list]
    return jsonify(result)

@web.route('/add_job', methods=['POST'])
def addJob():
    data = request.json
    data_str = json.dumps(data['job'])

    # TODO: Update data in the database
    tanos_manage().new_job(data['job_name'],data_str)

    return jsonify(success=True, message='add job successfully')


@web.route('/deleteJob/<int:job_id>', methods=['POST'])
def deleteJob(job_id):
    # TODO: Update data in the database
    tanos_manage().delete_job(job_id)
    return jsonify(success=True, message='delete job successfully')


@web.route('/saveJob', methods=['POST'])
def saveJob():
    # TODO: Update data in the database
    data = request.json
    data_str = json.dumps(data['job'])
    tanos_manage().update_job(data['job_id'],data['job_name'],data_str)
    return jsonify(success=True, message='save job successfully')


@web.route('/runJob2/<int:job_id>', methods=['POST'])
def runJob2(job_id):
    # TODO: Update data in the database
    print(job_id)
    sleep(3)
    return jsonify(success=True, message='run job successfully')



@web.route('/runJob/<int:job_id>', methods=['POST'])
def runJob(job_id):
    # TODO: Update data in the database
    data = request.json
    source_point_name = (data['job']['source_point'])
    target_point_name = (data['job']['target_point'])

    source_connect_id =  tanos_manage().get_connectid_by_point_name(source_point_name)
    target_connect_id = tanos_manage().get_connectid_by_point_name(target_point_name)

    # {'job_name': ' demo ', 'job_id': '515',
    #  'job': {'source_point': 'table_datatest_target_table', 'target_point': 'table_datatest_target_table2',
    #          'source_condition': '', 'target_condition': '', 'select_rules': 'Default', 'custom_rules': '',
    #          'fields': 'user_id'}}

    # 准备数据

    connect_info_s= tanos_manage().search_all_by_connect_id(source_connect_id)
    keys_s=('connect_id','connect_name','dbtype','connect_type','host','dblibrary','username','pwd',"port")
    result_list_s = []
    for row2 in connect_info_s:
        values_s = [value.strip() if isinstance(value, str) else value for value in row2]
        result_dict2 = dict(zip(keys_s, values_s))
        result_list_s.append(result_dict2)
    r_dict_conn_s= dict(result_list_s[0])


    connect_info_t= tanos_manage().search_all_by_connect_id(target_connect_id)
    keys_t=('connect_id','connect_name','dbtype','connect_type','host','dblibrary','username','pwd',"port")
    result_list_t = []
    for row2 in connect_info_t:
        values_t = [value.strip() if isinstance(value, str) else value for value in row2]
        result_dict = dict(zip(keys_t, values_t))
        result_list_t.append(result_dict)
    r_dict_conn_t= dict(result_list_t[0])

    print(r_dict_conn_s)
    print(r_dict_conn_t)


    #连接信息
    # {'connect_id': 10000, 'connect_name': 'pg_server1', 'dbtype': 'PostgreSQL', 'connect_type': 'My connection',
    #  'host': '47.113.185.98', 'dblibrary': 'test_frame', 'username': 'postgres', 'pwd': 'postgres', 'port': 5353}

    # {'Case_name': 'test_mypg_test12_ssh', 'Source TYPE': 'pg', 'Target TYPE': 'pg',
    #  'Source conn': 'pgm-1hl07vmgn0rd297653280.pgsql.rds.ali-ops.cloud.cn.hsbc,3433,test_frame,[remote]',
    #  'Target conn': 'pgm-1hl07vmgn0rd297653280.pgsql.rds.ali-ops.cloud.cn.hsbc,3433,test_frame,cdi,FdiXwYPTdNfc0Hg0leRm6A=='}

    if r_dict_conn_s['dbtype']=='PostgreSQL':
        s_type='pg'
    elif  r_dict_conn_s['dbtype']=='123':
        s_type = '123'
    if r_dict_conn_t['dbtype']=='PostgreSQL':
        t_type='pg'

    connt= {
        'Source TYPE': s_type,
        'Target TYPE': t_type,
        'Source conn': '{},{},{},{},{}'.format(r_dict_conn_s['host'],r_dict_conn_s['port'],r_dict_conn_s['dblibrary'],r_dict_conn_s['username'],r_dict_conn_s['pwd']),
        'Target conn': '{},{},{},{},{}'.format(r_dict_conn_t['host'],r_dict_conn_t['port'],r_dict_conn_t['dblibrary'],r_dict_conn_t['username'],r_dict_conn_t['pwd']),
    }

    # testdata, testdata_dif,, test1, id

    s_tablename= tanos_manage().get_tablename_by_point_name(source_point_name)
    t_tablename = tanos_manage().get_tablename_by_point_name(target_point_name)


    if '.' in s_tablename:
        first_half_s_tablename, second_half_s_tablename = s_tablename.split('.')

    if '.' in t_tablename:
        first_half_t_tablename, second_half_t_tablename = t_tablename.split('.')

    table="{},{},,{},{}".format(second_half_s_tablename,second_half_t_tablename,first_half_s_tablename,data['job']['fields'])


    user_id = session.get('userid', None)
    user_path = '{}/userinfo/{}/'.format(configPath, user_id)

    file = open(user_path + 'data_conn.txt', 'w')
    file.write(str(connt))
    file.close()

    file = open(user_path + 'data_db.csv', 'w')
    file.write(table)
    file.close()

    retcode = Constant_cmd(user_id).retcode
    stdout, stderr = retcode.communicate()

    if stderr:
        print(str(stderr, "utf-8") + '111111')
    else:
        print(str(stdout, "utf-8") + '222222')


    if retcode.returncode == 0:
        print("Run 按钮执行成功！！")
        sleep(1.6)
        result = jsonify({'code': 200, 'msg': 'run success!', 'returncode': 0})
        print(result)
        return result

    else:
        print("执行失败！！")
        file = open(user_path + 'log.log', 'a')
        file.writelines(str(stderr, "utf-8") + '\n')
        file.close()
        sleep(1.6)
        result = jsonify({'code': 400, 'msg': 'run failed', 'returncode': 1})
        print(result)
        return result, {'Content-Type': 'application/json'}
