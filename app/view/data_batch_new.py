import configparser
import json
import traceback
from datetime import timedelta, datetime
from time import sleep
import time

import pandas as pd
import requests
from flask import Blueprint, render_template, request, redirect, jsonify, session
import subprocess
import os
import sys
from werkzeug.utils import secure_filename

from app.db import test_case_manage
from app.db.tanos_manage import tanos_manage
from app.useDB import ConnectSQL
from app.util.Constant_setting import Constant_cmd, Constant_cmd_data_batch
from app.util.IP_PORT import Constant
from app.util.crypto_ECB import AEScoder
from app.util.permissions import permission_required
from app.view import viewutil, user


from app.application import app

basePath = os.path.join(os.path.join(os.path.dirname(__file__),"../"))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)
# userid = ConnectSQL().get_personal_user_id()
configP2 = configparser.ConfigParser()


web = Blueprint("batch_new", __name__)



@web.route('/data_batch_test_cases')
@user.login_required
# @permission_required(session.get('groupname'))
def test_cases():
    return (render_template)("/data/data_batch_test_cases.html")


# 定义允许的文件扩展名检查函数
def allowed_file_data_batch(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}

# 构建 job_str 字典时将 'nan' 转换为空字符串
def nan_to_empty(value):
    return '' if pd.isna(value) or value == 'nan' else value

@web.route('/data_batch_upload_excel', methods=['POST'])
def data_batch_upload_excel():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    id = session['userid']
    user_folder_path = os.path.join(app.root_path, 'static', 'user_files', str(id))

    filename = file.filename

    excel_path = f'{user_folder_path}/upload/{filename}'

    if file and allowed_file_data_batch(file.filename):
        if not os.path.exists(f'{user_folder_path}/upload/{filename}'):
            if not os.path.exists(f'{user_folder_path}/upload'):
                os.makedirs(os.path.join(user_folder_path, 'upload'))
            file.save(f'{user_folder_path}/upload/{filename}')
        else:
            os.remove(excel_path)
            return jsonify({'success': False, 'message': 'file existed'})


    #这里excel名字作为test_case_name加上时间戳，避免重名
    now = int(round(time.time() * 1000))
    formatted_timestamp =  time.strftime('%Y%m%d%H%M%S',time.localtime(now/1000))
    now_ms = int(round(time.time() * 1000))
    formatted_timestamp_ms = time.strftime('%Y%m%d%H%M%S', time.localtime(now_ms / 1000)) + f"{now_ms % 1000:03d}"
    newfilename = f'{filename}_{formatted_timestamp}'

    try:
        tanos_manage().add_data_batch_test_case(newfilename)


    except Exception as e:
        os.remove(excel_path)
        return jsonify({'success': False, 'message': f'Error insert suite: {str(e)}'})

    print(111111,newfilename)

    case_id = ConnectSQL().data_batch_get_case_id(newfilename.strip())[0][0]
    print(case_id)

    try:
        with pd.ExcelFile(excel_path, engine='openpyxl') as xls:
            sheet_names = xls.sheet_names
            print(sheet_names)

            nan_replacements = {
                'Type': '',
                'Connection Type': '',
                'Host': '',
                'Port': '',
                'Library': '',
                'Username': '',
                'Password': '',
            }

            # 处理第一个 sheet "connection config"
            if 'connection config' in sheet_names:
                df = pd.read_excel(xls, 'connection config', engine='openpyxl').fillna(nan_replacements)

                s_connect_ids = []  # 用于存储第一次循环的 connect_id
                t_connect_ids = []  # 用于存储第二次循环的 connect_id

                for index, row in df.iterrows():

                    Type = str(row['Connection Type'])
                    Connection_Type = str(row['Type'])
                    Host = str(row['Host'])
                    Port = str(row['Port'])
                    Library = str(row['Library'])
                    Username = str(row['Username'])
                    Password = str(row['Password'])

                    if index == 0:
                        # 第一次循环，使用前缀 s_
                        connectname = f's_b_{Host}_{formatted_timestamp}'
                    else:
                        # 第二次循环以及其他迭代，使用前缀 t_
                        connectname = f't_b_{Host}_{formatted_timestamp}'

                    tanos_manage().new_connection(connectname, Type, Connection_Type,
                                                  Host, Library, Username,
                                                  Password,Port)
                    # 获取每次插入表后的 connect_id
                    connect_id = tanos_manage().get_connections_id_by_name(connectname)

                    if index == 0:
                        s_connect_ids.append(connect_id)
                    else:
                        t_connect_ids.append(connect_id)

            print("s_connect_ids:", s_connect_ids)
            print("t_connect_ids:", t_connect_ids)

            # 处理第二个 sheet "job config"
            if 'job config' in sheet_names:
                job_df = pd.read_excel(xls, 'job config', engine='openpyxl').fillna(nan_replacements)

                for index, row in job_df.iterrows():

                    Source_Table = str(row['Source Table'])
                    Source_Condition = str(row['Source Condition'])
                    Target_Table = str(row['Target Table'])
                    Target_Condition = str(row['Target Condition'])
                    By_fields = str(row['By fields'])
                    s_pointname = f'b_{Source_Table}_{formatted_timestamp_ms}'
                    t_pointname = f'b_{Target_Table}_{formatted_timestamp_ms}'

                    jobname = f'b_{Source_Table}_{Target_Table}_{formatted_timestamp}'

                    tanos_manage().new_point2(s_pointname, s_connect_ids[0], Source_Table)
                    tanos_manage().new_point2(t_pointname, t_connect_ids[0], Target_Table)

                    job_str = {
                        "source_point": s_pointname,
                        "target_point": t_pointname,
                        "source_condition": nan_to_empty(Source_Condition),
                        "target_condition": nan_to_empty(Target_Condition),
                        "select_rules": 'Default',
                        "custom_rules": '',
                        "fields": By_fields,
                    }

                    job_str_json = json.dumps(job_str)

                    tanos_manage().new_job(jobname, job_str_json, case_id)

                # 处理 job_config_df 中的数据，可以使用循环遍历每一行

            os.remove(excel_path)

            # 其他处理逻辑...
    except Exception as e:
        os.remove(excel_path)
        print(e)
        return jsonify({'success': False, 'message': f'Error reading Excel file: {str(e)}'})

    return jsonify({'success': True, 'message': 'upload successfully'})


@app.route('/run_data_batch_job',methods=['POST'])
@user.login_required
def run_data_batch_job():
    data = request.json
    case_id= data['caseid']
    user_id = session.get('userid', None)

    print(user_id)
    print(case_id)

    try:
        result = subprocess.run(Constant_cmd_data_batch(user_id,case_id).cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('result:',result.stdout.decode('utf-8'))


    # 检查命令是否成功执行
        if result.returncode == 0:
            # 返回命令执行结果
            return jsonify({'success': True, 'message':'success' }),200
        else:
            # 返回错误信息
            return jsonify({'success': False, 'message':'fail','result':result.stdout.decode('utf-8') }), 200

    except Exception as e:
        return jsonify({'success': False,'message': str(e)}), 500


# 点击search后查询库中case列表
@web.route('/data_batch_test_case.json', methods=['POST', 'GET'])
# @user.login_required
def search_test_cases():
    if request.method == 'POST':
        pass
        # logger.info("2222222222222222222")
    if request.method == 'GET':
        # log().logger.info("1111111111111111111")
        # print("tiaoshi", "get 请求")
        info = request.values
        limit = info.get('limit', 1000)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit, 它表示一段数据的起点
        type = viewutil.getInfoAttribute(info, 'type')
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info, 'name')
        # database_type = viewutil.getInfoAttribute(info,'database_type')

        valueList = [name]
        conditionList = ['case_name']
        conditionList.append('case_id')
        valueList.append(id)
        fieldlist = []
        rows = 1000
        caseList = test_case_manage.test_case_manage().data_batch_show_test_cases(conditionList, valueList, fieldlist, rows)
        data = caseList

        # print('1111',type)
        # print (data , "tiaoshi...")

        if type == 'case_one':  # 这种情况就是进入某一个用例，只需要查询一条
            active_id = viewutil.getInfoAttribute(info, 'id')
            print('222', active_id)
            for i in range(len(data)):
                # print (data[i]['id'])
                if data[i]['id'] == active_id:
                    print(data[i]['id'])
                    data1 = jsonify({'total': len(data), 'rows': data[i]})
                    print(data[i])
        else:
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
        # log.log().logger.info('data1: %s' %data1)
        print(111,data)
        return data1, {'Content-Type': 'application/json'}
