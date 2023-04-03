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

        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')

        if 'Save' in request.form:
            print('save my testid:{}'.format(id))

            select1 = request.form['select1']
            select2 = request.form['select2']
            select_rule = request.form['select_rule']
            field = request.form['field']

            dict1 = {
                'select1': select1,
                'select2': select2,
                'select_rule': select_rule,
                'field': field,
            }

            file = open(user_path + 'temp.txt', 'w')
            file.write(str(dict1))
            file.close()

            data_conn = {'Case_name': 'test_mypg_test12_ssh', 'Source TYPE': 'pg', 'Target TYPE': 'pg',
                         'Source conn': 'pgm-1hl07vmgn0rd297653280.pgsql.rds.ali-ops.cloud.cn.hsbc,3433,test_frame,[remote]',
                         'Target conn': 'pgm-1hl07vmgn0rd297653280.pgsql.rds.ali-ops.cloud.cn.hsbc,3433,test_frame,cdi,FdiXwYPTdNfc0Hg0leRm6A=='}

            file = open(user_path + 'data_conn.txt', 'w')
            file.write(str(data_conn))
            file.close()

            data_db= 'testdata,testdata_dif,,test1,id'

            file = open(user_path + 'data_db.csv', 'w')
            file.write(data_db)
            file.close()

            # return jsonify(data_conn)

            return render_template('uitest/data_edit_tanos_new.html', select_rule=select_rule,field=field,
                                   message='Save success!')


        elif 'Report' in request.form or 'Report1' in request.form:
            user_path = '{}/userinfo/{}/'.format(configPath, user_id)
            ini_path = user_path + '/' + 'config.ini'
            config = configparser.ConfigParser()
            config.read(ini_path)  # 读取 ini 文件
            case_id = config.get('default', 'caseid')

            # print("enter report.....")
            # print("retcode.returncode.....",retcode.returncode)
            # print("case_id.....", case_id)

            # print("user_id:", user_id)
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