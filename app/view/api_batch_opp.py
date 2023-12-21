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
from app.util.Constant_setting import Constant_cmd_api
from app.util.log_util.all_new_log import logger_all
from app.util.permissions import permission_required
from app.view import user, viewutil

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(configPath)

web = Blueprint('api_batch_opp', __name__, template_folder='templates/api')

@web.route('/api_batch_opp', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_opp():
    return render_template('api/api_batch_opp/api_batch_opp.html',)

@web.route('/api_batch_suite_opp', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_suite_opp():
    return render_template('api/api_batch_opp/api_batch_suite_opp.html',)


@web.route('/api_batch_case_opp', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_case_opp():
    return render_template('api/api_batch_opp/api_batch_case_opp.html',)


@web.route('/api_batch_job_opp', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_job_opp():
    return render_template('api/api_batch_opp/api_batch_job_opp.html',)


@web.route('/api_batch_result_opp', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_result_opp():
    return render_template('api/api_batch_opp/api_batch_result_opp.html',)


# 定义允许的文件扩展名检查函数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}

@web.route('/upload_excel_opp', methods=['POST'])
# @permission_required(session.get('groupname'))
def upload_file_opp():
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
        with pd.ExcelFile(excel_path, engine='openpyxl') as xls:
            sheet_names = xls.sheet_names

            for sheet_name in sheet_names:

                if tanos_manage().sheet_exists(sheet_name):
                    xls.close()
                    os.remove(f'{user_folder_path}/upload/{filename}')
                    return jsonify(
                        {'success': False, 'message': f'Sheet "{sheet_name}" already exists in the database'})

                try:
                    tanos_manage().add_api_batch_suite(sheet_name)
                except Exception as e:
                    xls.close()
                    os.remove(f'{user_folder_path}/upload/{filename}')
                    return jsonify({'success': False, 'message': f'Error insert suite: {str(e)}'})

                suite_id = tanos_manage().get_suite_id(sheet_name)

                nan_replacements = {
                    'Url': '',
                    'Method': '',
                    'Request body': '',
                    'Header': '',
                    'Expected result': ''
                }

                df = pd.read_excel(xls, sheet_name, engine='openpyxl').fillna(nan_replacements)

                for index, row in df.iterrows():
                    url = str(row['Url'])
                    method = str(row['Method'])
                    request_body = str(row['Request body'])
                    header = str(row['Header'])
                    expected_result = str(row['Expected result'])

                    tanos_manage().add_api_batch_case(suite_id=suite_id, url=url, methods=method,
                                                      request_body=request_body, headers=header,
                                                      expected_result=expected_result)
        try:
            xls.close()
            os.remove(f'{user_folder_path}/upload/{filename}')
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message': f'Error Delete Excel file: {str(e)}'})

    except Exception as e:
        xls.close()
        os.remove(f'{user_folder_path}/upload/{filename}')
        return jsonify({'success': False, 'message': f'Error reading Excel file: {str(e)}'})

    return jsonify({'success': True, 'message': 'upload successfully'})


@web.route('/batch_api_suite_search_opp.json', methods=['GET'])
def show_batch_opp():
    rows = tanos_manage().show_api_batch_suite()
    print(rows)
    keys=('user_id','suite_id','suite_name','create_date','suite_label')
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

        result_dict['suite_label'] = row[4] if row[4] else ""
        result_list.append(result_dict)

    print(result_list)
    return jsonify(result_list)


@web.route('/delete_api_batch_suite_opp', methods=['POST'])
def delete_data_opp():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().delete_api_batch_suite(data["id"])
    #这里文件最好也能删掉
    logger_all.info('delete connection：{}'.format(data["id"]))
    return jsonify(success=True, message='Data deleted successfully')




@web.route('/batch_api_case_search_opp.json', methods=['GET'])
def show_case_opp():
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


@app.route('/batch_search_case_opp',methods=['GET'])
def batch_search_case_opp():
    # 获取请求参数中的id
    suite_id = request.args.get('id')
    return render_template('api/api_batch_opp/api_batch_case_opp.html', suite_id=suite_id)

@app.route('/batch_search_case_json_opp', methods=['GET'])
def batch_search_case_json_opp():
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


@app.route('/batch_search_job_opp',methods=['GET'])
def batch_search_job_opp():
    # 获取请求参数中的id
    suite_id = request.args.get('id')
    return render_template('api/api_batch_opp/api_batch_case_opp.html', suite_id=suite_id)

@app.route('/batch_search_job_json_opp', methods=['GET'])
def batch_search_job_json_opp():
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



@app.route('/gen_api_batch_job_opp',methods=['POST'])
def gen_api_batch_job_opp():
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

@web.route('/batch_api_job_search_opp.json', methods=['GET'])
def show_batch_job_opp():
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


@app.route('/batch_search_result_opp',methods=['GET'])
def batch_search_result_opp():
    # 获取请求参数中的id
    job_id = request.args.get('id')
    # print(2222,job_id)
    return render_template('api/api_batch_opp/api_batch_result_opp.html', job_id=job_id)

@app.route('/batch_search_result_json_opp', methods=['GET'])
def batch_search_result_json_opp():
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



@app.route('/run_api_batch_job_opp',methods=['POST'])
@user.login_required
def run_api_batch_job_opp():
    data = request.json
    job_id= data['jobid']
    user_id = session.get('userid', None)
    # print(111111111111,user_id)
    # configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    # command = '/Users/kun/miniconda3/envs/myenv/bin/python3.6 {}/api_check/runapi.py {} {}'.format(configPath, job_id,user_id)

    try:
        result = subprocess.run(Constant_cmd_api(user_id,job_id).cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # print('result:',result.stdout.decode('gbk'))



    # 检查命令是否成功执行
        if result.returncode == 0:
            # 返回命令执行结果
            return jsonify({'success': True, 'message':'success' }),200
        else:
            # 返回错误信息
            return jsonify({'success': False, 'message':'fail' }), 500

    except Exception as e:
        return jsonify({'success': False,'message': str(e)}), 500




@web.route('/search_api_batch_result_opp', methods=['POST', 'GET'])
@user.login_required
def search_api_batch_result_opp():
    if request.method == 'GET':
        job_id = request.args.get('jobid')
        print(1111234,job_id)
        user_id = session.get('userid', None)

        folder_path = os.path.join(app.root_path, 'static', 'user_files', str(user_id))
        print(folder_path+'/html',"{}_apibatch_report".format(job_id))

        return send_from_directory(folder_path+'/html',"{}_apibatch_report.html".format(job_id))



@app.route('/apitestgettoken_opp', methods=['POST'])
def apitestgettoken_opp():
    data1 = request.json
    print(333333, data1)

    if data1 is None:
        return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400

    print(data1)
    job_id = data1.get('jobid')
    print(111, data1)

    if job_id == '10031':
        data = {
            "token": "2eJydVH9r2zAQ_SpDg_wVx5LjH4rArGUthbFBoR0MSimyJMdabclIcr1S-t13dpqRjnVrBwZZT7p3755OekA3vXIdN8oExIIb1BLxOx64Qww1IfSexbHutmRVcS2HlbBdrEM8lCQhWUZJkZLlpqB0U-AkX9RdmWRrGELJh2AXvO9LsqaLuvx0fnr2YSwzjBdNmeYULdHW2aE3vFOQ6US11l8qH84mEBZ94HWtJWIZxRmBMLxEQfFuv_erV86jHeYRu3qOfmy04SdQxYVth6CtAexYdtqgawixt8oAz01a1TivJY5IxnGU4pxGlUyyqMrTFBcbkiqMIXAAUsQeZjfADC8a1XG_6rRw1ts6zJ6IluvOx1B1YzoVGiu9U7Vyygg16xucYZZ77dlUsmdBsIvjL59ZssKMCwbx3gN8DsNonTx3NigRlLx03PjeugBKXqOgG9qg-1bNSv4VM_o4wZjGOI-1hA7Q4X4uYfoVfDJuV0s8gAYldK2VnCz8K-kvpidFUvu-5fe7k75CIzfbd8fO2fHNTPt57-wd_LuJrtV3atr8ZjJbfQeDdyjUNZNRnsukEnWUrunUEQmJKDRgJEmeCE5pWovizYmCMhwAOSXY0FSRdVZEioh1lFZERlxiEdVFmuc5zwtB_5TgR9d6y_uVddunM8ti-H7PBHt1y6V0ys89N7u8Gm-PGhumpRd8eiX7Fpw2-1N86QBfyfWMBhTeHCh8f_rt8v3RvDLe7nHoxEOT_z-zh4t40Ino-nF3w-e3ZoMxIbv508N00K2PPwF1z8X8.ZW6bow.QJ1druwWcAj77H5sma4O_u2oKCI",
        }
        return jsonify(data)
    else:
        return jsonify({'success': False, 'error': 'data is empty'})


@web.route('/get_api_token_detail_opp', methods=['POST'])
def get_api_token_detail_opp():
    data = request.json

    url = data.get('url')
    body = data.get('body')

    print('URL:', url)
    print('Body:', body)
    print(type(body))

    try:
        res = requests.post(url=url, json=body, verify=False)
        data_dict = json.loads(res.text)
        print('Response:', data_dict)
        return jsonify(data_dict)

    except Exception as e:
        print('Error:', e)
        return jsonify({"error": "Something went wrong"}), 500


@web.route('/save_api_token_opp', methods=['POST'])
def save_api_token_opp():
    data = request.json

    job_id = data.get('job_id')
    url = data.get('url')
    body = data.get('body')
    test_rule= data.get('test_rule')

    try:
        tanos_manage().add_api_batch_token(job_id, url, body,test_rule)
        return jsonify({'success': True, 'info': 'save successfully '})


    except Exception as e:
        print('Error:', e)
        return jsonify({"error": "Something went wrong"}), 500


@app.route('/get_data_by_job_id_opp', methods=['GET'])
def get_data_by_job_id_opp():
    job_id = request.args.get('id')
    if job_id:
        try:
            token_data= tanos_manage().get_api_batch_token(job_id)
            return jsonify(token_data)

        except Exception as e:
            print('Error:', e)
            return jsonify({"error": "Something went wrong"}), 500


@web.route('/update_batch_suite_info_opp', methods=['POST'])
def update_batch_suite_info_opp():
    data = request.json
    print(1111,data)
    # TODO: Update data in the database  suite_id,suite_name,suite_label
    tanos_manage().update_batch_suite_info(data['suite_id'],data['suite_name'],data['suite_label'])
    return jsonify(success=True, message='Data updated successfully')


@web.route('/delete_api_batch_job_opp', methods=['POST'])
def delete_data_job_opp():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().delete_api_batch_job(data["id"])
    #这里文件最好也能删掉
    logger_all.info('delete connection：{}'.format(data["id"]))
    return jsonify(success=True, message='Job deleted successfully')
