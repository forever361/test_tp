import configparser
import json
import subprocess
import traceback
from time import sleep

from flask import Blueprint, render_template, jsonify, request, get_flashed_messages, send_from_directory, session, redirect, url_for
# from app import log
from flask_socketio import emit

from app.application import socketio
from app.db import test_case_manage
from app.db.tanos_manage import tanos_manage
from app.util import global_manager
from app.util.log import logg

from app.useDB import ConnectSQL
from app.util.crypto_ECB import AEScoder
from app.util.log_util.all_new_log import logger_all
from app.util.permissions import permission_required
from app.view import user, viewutil
import os


from app.util.Constant_setting import Constant_cmd, Constant_cmd_data_batch
from app.application import app

import csv

web = Blueprint('data_testcase_tanos', __name__, template_folder='templates/uitest')
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
configP = configparser.ConfigParser()


@web.route('/api_data_test_cases_tanos')
@user.login_required
# @permission_required(session.get('groupname'))
def test_cases():
    return permission_required(session.get('groupname'))(render_template)("uitest/data_test_cases.html")




@web.route('/data_edit_test_case_tanos', methods=['POST', 'GET'])
@user.login_required
# @permission_required(session.get('groupname'))
def edit_test_case():
    user_id = session.get('userid', None)
    folder_path = os.path.join(app.root_path, 'static', 'user_files', str(user_id))

    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')

        ini_path = folder_path + '/config/' + 'config.ini'
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

    return permission_required(session.get('groupname'))(render_template)("data/data_edit_tanos.html")


    # SAVE保存的过程,点save就相当于提交了表单走post
    # elif request.method == 'POST':
    #     case_id = request.args.get('id')
    #     print(case_id)
    #
    #     # 重定向到目标页面
    #     return redirect(url_for('data_testcase.data_search_report', id=case_id))

        # return render_template('data_test_finish.html', user_id=user_id,
        #                            case_id=case_id)


@web.route('/runtest_tanos.json', methods=['POST', 'GET'])
@user.login_required
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
@user.login_required
def web_search_report():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        info = request.values
        # print ('info',info)
        id = viewutil.getInfoAttribute(info, 'id')
        # print('idididiidididid', id)
        user_id = session.get('userid', None)
        folder_path = os.path.join(app.root_path, 'static', 'user_files', user_id)

        return send_from_directory(folder_path,"/html/{}_data_test.html".format(id))




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


@web.route('/job_search.json', methods=['POST'])
def show_data():
    data = request.json
    print(data)
    case_id = data['case_id']
    rows = tanos_manage().show_jobs(case_id)
    keys=('case_id','job_id','job_name','job')
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
    tanos_manage().new_job(data['job_name'],data_str,data['case_id'])

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
    # print(111,data)
    data_str = json.dumps(data['job'])
    print(222,data_str)
    tanos_manage().update_job(data['job_id'],data['job_name'],data_str)
    return jsonify(success=True, message='save job successfully')


@web.route('/runJob2/<int:job_id>', methods=['POST'])
def runJob2(job_id):
    # TODO: Update data in the database
    print(job_id)
    sleep(3)
    return jsonify(success=True, message='run job successfully')


@socketio.on('run_task')
# @web.route('/runJob/<int:job_id>', methods=['POST'])
def runJob(jsonData):
    # TODO: Update data in the database
    emit('task_start', {'data': "||||||||||||||||||Start checking||||||||||||||||||"})

    data = json.loads(jsonData)

    case_id= data['caseid']
    user_id = data.get('userid')

    if user_id is not None:
        token= request.headers.get('token')
        if token=='7758521':
            user_id = data['userid']
        else:
            return jsonify({'success':False,'message':'token error'}),401
    else:
        user_id = session.get('userid', None)




    try:
        # 创建子进程并异步捕捉其输出
        retcode = Constant_cmd_data_batch(user_id,case_id).retcode

        json_started = False
        json_lines = []

        # 实时读取子进程的输出并发送至前端
        while True:
            output = retcode.stdout.readline().decode()
            if not output:
                break
            if output:
                if "JSON_RESULT_START" in output:
                    json_started = True
                    continue
                elif "JSON_RESULT_END" in output:
                    json_started = False
                    try:
                        json_output = json.loads(''.join(json_lines))
                        json_lines = []  # 清空 json_lines 以处理未来可能的 JSON 输出
                    except json.JSONDecodeError:
                        print('Failed to decode JSON output from subprocess')
                        json_output = None
                    continue

                if json_started:
                    json_lines.append(output)
                else:
                    emit('task_log', {'data': output.strip()})

        # 等待子进程执行完毕，并根据其状态发送事件
        retcode.wait()


        if json_output:
            source_count = json_output['source_count']
            target_count = json_output['target_count']
            rule = json_output['rule']

            print(source_count)
            print(target_count)
            print(rule)


            if retcode.returncode == 0:
                emit('task_complete', {'data': '||||||||||||||||||Job completed successfully!!||||||||||||||||||', 'rule':rule,'source_count': source_count, 'target_count': target_count,})
                return 'run success!'
            else:
                emit('task_error', {'data': '||||||||||||||||||Job execution failed!!||||||||||||||||||'})
                return 'run failed'

    except subprocess.CalledProcessError as e:
        emit('task_error', {'data': f'||||||||||||||||||{e}||||||||||||||||||'})




@app.route('/run_data_job',methods=['POST'])
def run_data_job():
    data = request.json
    # case_id= data['caseid']
    # user_id = session.get('userid', None)

    data = request.json
    case_id= data['caseid']
    user_id = data.get('userid')
    job_id = data.get('jobid')


    if user_id is not None:
        token= request.headers.get('token')
        if token=='7758521':
            user_id = data['userid']
        else:
            return jsonify({'success':False,'message':'token error'}),401
    else:
        user_id = session.get('userid', None)
        print(user_id)

    try:
        result = subprocess.run(Constant_cmd(user_id,case_id,job_id).cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('result:',result.stdout.decode('utf-8'))
        output = result.stdout.decode('utf-8')


        # 提取 JSON_RESULT_START 和 JSON_RESULT_END 之间的 JSON 数据
        start_index = output.find("JSON_RESULT_START")
        end_index = output.find("JSON_RESULT_END")

        if start_index != -1 and end_index != -1:
            json_result = output[start_index + len("JSON_RESULT_START"):end_index].strip()
            result_data = json.loads(json_result)
            return jsonify({'status': 'true', 'message':"run job success",'data':result_data }),200
        else:
            # 返回错误信息
            return jsonify({'status': 'false', 'message':'run job fail','result':result.stdout.decode('utf-8') }), 200

    except Exception as e:
        return jsonify({'status': 'false','message':'run job fail','result': str(e)}), 200