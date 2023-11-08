import json

import requests
from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.utils import secure_filename

import os
import sys

from app.application import app
from app.db.tanos_manage import tanos_manage
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
            return jsonify({'success': False, 'message': 'file existed'})

    #入库这里要有异常处理
    tanos_manage().add_api_batch_suite(filename)

    return render_template('api/api_batch_suite.html',)


@web.route('/batch_api_suite_search.json', methods=['GET'])
def show_data():
    rows = tanos_manage().show_api_batch_suite()
    keys=('user_id','suite_id','suite_name','create_date')
    result_list=[]
    for row in rows:
        values = [value.strip() if isinstance(value,str) else value for value in row]
        result_dict =dict(zip(keys,values))
        result_list.append(result_dict)
    print(11,result_list)
    return jsonify(result_list)