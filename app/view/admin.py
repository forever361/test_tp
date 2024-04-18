from flask import Blueprint, render_template, request, jsonify, session

import os
import sys

from app.application import app
from app.db.tanos_manage import tanos_manage
from app.util.permissions import permission_required
from app.view import user

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(configPath)

web = Blueprint('admin', __name__)

@web.route('/admin/7758521', methods=['GET'])
def admin_page():
    return render_template('admin.html')

@web.route('/admin/update_login_type', methods=['POST'])
def update_login_type():
    data = request.json
    new_login_type = data.get('login_type')
    # 在这里执行更新数据库中 login_type 的逻辑
    tanos_manage().update_login_type(new_login_type)
    return jsonify({'status': 'success'})


@web.route('/admin/get_login_type', methods=['GET'])
def get_login_type():
    login_type = tanos_manage().get_login_para()
    return jsonify({'login_type': login_type})
