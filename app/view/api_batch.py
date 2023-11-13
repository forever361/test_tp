import json
from datetime import datetime

import openpyxl
import pandas as pd
import requests
from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.utils import secure_filename

import os
import sys

from app.application import app
from app.db.tanos_manage import tanos_manage
from app.util.log_util.all_new_log import logger_all
from app.util.permissions import permission_required
from app.view import user

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
        # 使用pandas读取Excel文件
        df = pd.read_excel(excel_path, engine='openpyxl')
        print(df)
        # 将DataFrame数据插入数据库
        for index, row in df.iterrows():
            url = row['Url']
            method = row['Method']
            request_body = row['Request body']
            header = row['Header']
            expected_result = row['Expected result']

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


