import json
import subprocess
from datetime import datetime

import openpyxl
import pandas as pd
import requests
from flask import Blueprint, render_template, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename

import os
import sys

from app.application import app
from app.db.tanos_manage import tanos_manage
from app.util.log_util.all_new_log import logger_all
from app.util.permissions import permission_required
from app.view import user, viewutil

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(configPath)

web = Blueprint('api_batch', __name__, template_folder='templates/api')

@web.route('/api_batch', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch():
    return render_template('api/api_batch.html',)

@web.route('/api_batch_suite', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_suite():
    return render_template('api/api_batch_suite.html',)


@web.route('/api_batch_case', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_case():
    return render_template('api/api_batch_case.html',)


@web.route('/api_batch_job', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_job():
    return render_template('api/api_batch_job.html',)


@web.route('/api_batch_result', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_result():
    return render_template('api/api_batch_result.html',)


# 定义允许的文件扩展名检查函数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}

@web.route('/upload_excel', methods=['POST'])
# @permission_required(session.get('groupname'))
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    id = session['userid']
    user_folder_path = os.path.join(app.root_path, 'static', 'user_files', str(id))

    filename = file.filename
    if file and allowed_file(file.filename):
        #secure_filename(file.filename) 是为了确保上传的文件的文件名是安全的
        # filename = secure_filename(file.filename)
        if not os.path.exists(f'{user_folder_path}/upload/{filename}'):
            if not os.path.exists(f'{user_folder_path}/upload'):
                os.makedirs(os.path.join(user_folder_path, 'upload'))
            file.save(f'{user_folder_path}/upload/{filename}')
        else:
            # os.remove(f'{user_folder_path}/upload/{filename}')
            return jsonify({'success': False, 'message': 'file existed'})

    # 读取Excel文件并插入数据
    excel_path = f'{user_folder_path}/upload/{filename}'


    try:
        #入库这里要有异常处理
        tanos_manage().add_api_batch_suite(filename)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error insert suite: {str(e)}'})

    suite_id = tanos_manage().get_suite_id(filename)

    try:

        nan_replacements = {
            'Url': '',  # 适当替换为数据库中的空值
            'Method': '',  # 适当替换为数据库中的空值
            'Request body': '',  # 适当替换为数据库中的空值
            'Header': '',  # 适当替换为数据库中的空值
            'Expected result': ''  # 适当替换为数据库中的空值
        }

        # 使用pandas读取Excel文件
        df = pd.read_excel(excel_path, engine='openpyxl').fillna(nan_replacements)
        print(df)
        # 将DataFrame数据插入数据库
        for index, row in df.iterrows():
            url = str(row['Url'])
            method = str(row['Method'])
            request_body = str(row['Request body'])
            header = str(row['Header'])
            expected_result = str(row['Expected result'])

            # 在这里使用 tanos_manager.add_api_batch_suite 方法插入数据库，具体根据您的模型和需求调整
            tanos_manage().add_api_batch_case(suite_id=suite_id, url=url, methods=method, request_body=request_body, headers=header,
                                              expected_result=expected_result)

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error reading Excel file: {str(e)}'})

    return render_template('api/api_batch_suite.html',)


@web.route('/batch_api_suite_search.json', methods=['GET'])
def show_batch():
    rows = tanos_manage().show_api_batch_suite()
    keys=('user_id','suite_id','suite_name','create_date')
    result_list=[]
    for row in rows:
        # Assuming create_date is the fourth element in the row
        create_date_str = row[3].strftime("%a, %d %b %Y %H:%M:%S GMT")
        # Convert create_date string to datetime object
        create_date_datetime = datetime.strptime(create_date_str, "%a, %d %b %Y %H:%M:%S GMT")
        # Format datetime object as needed
        formatted_create_date = create_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Update the row with the formatted create_date
        row_with_formatted_date = (*row[:3], formatted_create_date)
        # Create a dictionary from keys and updated row
        result_dict = dict(zip(keys, row_with_formatted_date))
        # Append the result dictionary to the list
        result_list.append(result_dict)
    return jsonify(result_list)


@web.route('/delete_api_batch_suite', methods=['POST'])
def delete_data():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().delete_api_batch_suite(data["id"])
    #这里文件最好也能删掉
    logger_all.info('delete connection：{}'.format(data["id"]))
    return jsonify(success=True, message='Data deleted successfully')




@web.route('/batch_api_case_search.json', methods=['GET'])
def show_case():
    rows = tanos_manage().show_api_batch_case()
    keys=('user_id','case_id','suite_id','url','methods','request_body','headers','expected_result','create_date')
    result_list=[]
    for row in rows:
        # Assuming create_date is the fourth element in the row
        create_date_str = row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")
        # Convert create_date string to datetime object
        create_date_datetime = datetime.strptime(create_date_str, "%a, %d %b %Y %H:%M:%S GMT")
        # Format datetime object as needed
        formatted_create_date = create_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Update the row with the formatted create_date
        row_with_formatted_date = (*row[:8], formatted_create_date)
        # Create a dictionary from keys and updated row
        result_dict = dict(zip(keys, row_with_formatted_date))
        # Append the result dictionary to the list
        result_list.append(result_dict)
    return jsonify(result_list)


@app.route('/batch_search_case',methods=['GET'])
def batch_search_case():
    # 获取请求参数中的id
    suite_id = request.args.get('id')
    return render_template('api/api_batch_case.html', suite_id=suite_id)

@app.route('/batch_search_case_json', methods=['GET'])
def batch_search_case_json():
    # 获取请求参数中的id
    suite_id = request.args.get('id')

    rows = tanos_manage().show_api_batch_case_in_suite_id(suite_id)
    keys = (
        'user_id', 'case_id', 'suite_id', 'url', 'methods', 'request_body', 'headers', 'expected_result', 'create_date')
    result_list = []
    for row in rows:
        # Assuming create_date is the fourth element in the row
        create_date_str = row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")
        # Convert create_date string to datetime object
        create_date_datetime = datetime.strptime(create_date_str, "%a, %d %b %Y %H:%M:%S GMT")
        # Format datetime object as needed
        formatted_create_date = create_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Update the row with the formatted create_date
        row_with_formatted_date = (*row[:8], formatted_create_date)
        # Create a dictionary from keys and updated row
        result_dict = dict(zip(keys, row_with_formatted_date))
        # Append the result dictionary to the list
        result_list.append(result_dict)

    return jsonify(result_list)


@app.route('/batch_search_job',methods=['GET'])
def batch_search_job():
    # 获取请求参数中的id
    suite_id = request.args.get('id')
    return render_template('api/api_batch_case.html', suite_id=suite_id)

@app.route('/batch_search_job_json', methods=['GET'])
def batch_search_job_json():
    # 获取请求参数中的id
    suite_id = request.args.get('id')

    rows = tanos_manage().show_api_batch_case_in_suite_id(suite_id)
    keys = (
        'user_id', 'case_id', 'suite_id', 'url', 'methods', 'request_body', 'headers', 'expected_result', 'create_date')
    result_list = []
    for row in rows:
        # Assuming create_date is the fourth element in the row
        create_date_str = row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")
        # Convert create_date string to datetime object
        create_date_datetime = datetime.strptime(create_date_str, "%a, %d %b %Y %H:%M:%S GMT")
        # Format datetime object as needed
        formatted_create_date = create_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Update the row with the formatted create_date
        row_with_formatted_date = (*row[:8], formatted_create_date)
        # Create a dictionary from keys and updated row
        result_dict = dict(zip(keys, row_with_formatted_date))
        # Append the result dictionary to the list
        result_list.append(result_dict)

    return jsonify(result_list)



@app.route('/gen_api_batch_job',methods=['POST'])
def gen_api_batch_job():
    data = request.json
    print(data)
    print(data['caseIds'])

    current_time = datetime.now()

    # 格式化时间戳
    formatted_time = current_time.strftime("%Y_%m_%d_%H%M_%S%f")[:-3]  # 去掉最后的微秒部分
    case_ids_count = len(data['caseIds'])
    job_name = f"{formatted_time}_[{case_ids_count}]"

    try:
        #入库这里要有异常处理
        tanos_manage().add_api_batch_job(job_name)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error insert job: {str(e)}'})

    job_id = tanos_manage().get_job_id(job_name)

    for case_id in data['caseIds']:
        # 查询相关信息，替换下面的示例数据
        case_info = tanos_manage().search_api_batch_case_from_case_id(case_id)
        print(11111,case_info)

        url = case_info[0][3]
        methods = case_info[0][4]
        request_body = case_info[0][5]
        headers = case_info[0][6]
        expected_result = case_info[0][7]

        try:
            tanos_manage().add_api_batch_result(case_id=case_id, job_id=job_id, url=url, methods=methods,
                                              request_body=request_body, headers=headers,
                                              expected_result=expected_result,test_result='')
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error insert result: {str(e)}'})

    return jsonify({'job_id':job_id})

@web.route('/batch_api_job_search.json', methods=['GET'])
def show_batch_job():
    rows = tanos_manage().show_api_batch_job()
    keys=('user_id','job_id','job_name','create_date')
    result_list=[]
    for row in rows:
        # Assuming create_date is the fourth element in the row
        create_date_str = row[3].strftime("%a, %d %b %Y %H:%M:%S GMT")
        # Convert create_date string to datetime object
        create_date_datetime = datetime.strptime(create_date_str, "%a, %d %b %Y %H:%M:%S GMT")
        # Format datetime object as needed
        formatted_create_date = create_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Update the row with the formatted create_date
        row_with_formatted_date = (*row[:3], formatted_create_date)
        # Create a dictionary from keys and updated row
        result_dict = dict(zip(keys, row_with_formatted_date))
        # Append the result dictionary to the list
        result_list.append(result_dict)
    return jsonify(result_list)


@app.route('/batch_search_result',methods=['GET'])
def batch_search_result():
    # 获取请求参数中的id
    job_id = request.args.get('id')
    # print(2222,job_id)
    return render_template('api/api_batch_result.html', job_id=job_id)

@app.route('/batch_search_result_json', methods=['GET'])
def batch_search_result_json():
    # 获取请求参数中的id
    job_id = request.args.get('id')

    rows = tanos_manage().show_api_batch_result_in_job_id(job_id)
    keys = (
        'user_id', 'case_id', 'job_id', 'url', 'methods', 'request_body', 'headers', 'expected_result', 'test_result','create_date')
    result_list = []
    for row in rows:
        # Assuming create_date is the fourth element in the row
        create_date_str = row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")
        # Convert create_date string to datetime object
        create_date_datetime = datetime.strptime(create_date_str, "%a, %d %b %Y %H:%M:%S GMT")
        # Format datetime object as needed
        formatted_create_date = create_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Update the row with the formatted create_date
        row_with_formatted_date = (*row[:8], formatted_create_date)
        # Create a dictionary from keys and updated row
        result_dict = dict(zip(keys, row_with_formatted_date))
        # Append the result dictionary to the list
        result_list.append(result_dict)

    return jsonify(result_list)



@app.route('/run_api_batch_job',methods=['POST'])
@user.login_required
def run_api_batch_job():
    data = request.json
    job_id= data['jobid']
    user_id = session.get('userid', None)
    # print(111111111111,user_id)
    configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    command = 'D:/software/miniconda3/envs/tanos/python {}/api_check/runapi.py {} {}'.format(configPath, job_id,user_id)

    # print(command)
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # print(111,result)
        print('result:',result.stdout.decode('gbk'))



    # 检查命令是否成功执行
        if result.returncode == 0:
            # 返回命令执行结果
            return jsonify({'success': True, 'message':'success' }),200
        else:
            # 返回错误信息
            return jsonify({'success': False, 'message':'fail' }), 500

    except Exception as e:
        return jsonify({'success': False,'message': str(e)}), 500




@web.route('/search_api_batch_result', methods=['POST', 'GET'])
@user.login_required
def search_api_batch_result():
    if request.method == 'GET':
        job_id = request.args.get('jobid')
        print(1111234,job_id)
        user_id = session.get('userid', None)

        folder_path = os.path.join(app.root_path, 'static', 'user_files', str(user_id))
        print(folder_path+'/html',"{}_apibatch_report".format(job_id))

        return send_from_directory(folder_path+'/html',"{}_apibatch_report.html".format(job_id))


@app.route('/apitest111',methods=['GET'])
def apitest111():
    data = [
            {
                "connect_id": 1,
                "connect_name": 'Item 1',
                "dbtype": 'PostgreSQL',
                "connect_type": "My connection",
                "username": 'hsh',
                "pwd": '54uru',
                "host": 'host1',
                "dblibrary": "test1"
            },
            {
                "connect_id": 2,
                "connect_name": 'Item 2',
                "dbtype": 'AliCloud',
                "connect_type": "My connection",
                "username": 'hsh',
                "pwd": 'we643w623',
                "host": 'host2',
                "dblibrary": "test2"
            },
    ]
    return jsonify(data)


@app.route('/apitest222',methods=['GET'])
def apitest222():
    data = [
            {
                "connect_id": 100,
                "connect_name": 'Item 1',
                "dbtype": 'PostgreSQL',
                "connect_type": "My connection",
                "username": 'hsh',
                "pwd": '54uru',
                "host": 'host1',
                "dblibrary": "test1"
            },
            {
                "connect_id": 200,
                "connect_name": 'Item 2',
                "dbtype": 'AliCloud',
                "connect_type": "My connection",
                "username": 'hsh',
                "pwd": 'we643w623',
                "host": 'host2',
                "dblibrary": "test2"
            },
    ]
    return jsonify(data)


@app.route('/apitest333', methods=['POST'])
def apitest333():
    data1 = request.json
    print(111,data1)
    if data1:
        data = {
            "connect_id": 100,
            "connect_name": 'Item 1',
            "dbtype": 'PostgreSQL',
            "connect_type": "My connection",
            "username": 'hsh',
            "pwd": '54uru',
            "host": 'host1',
            "dblibrary": "test1"
        }
        return jsonify(data)
    else:
        return jsonify({'success': False,'error': 'data is empty'})