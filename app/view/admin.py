from datetime import datetime

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

@web.route('/admin/user_status', methods=['GET'])
def user_status():
    return render_template('/access/user_status.html')


@web.route('/admin/getAllUsers.json', methods=['GET'])
def getAllUsers():
    userlist = tanos_manage().get_all_user()
    all_users = []
    for row in userlist:
        staffid = row[1]
        name = row[0].strip()

        # 解析原始的 GMT 时间字符串
        latest_login_date = row[2]
        if latest_login_date != None:
            # 转换为你想要的格式
            latest_login_date = latest_login_date.strftime("%Y-%m-%d %H:%M:%S")

        user_id=row[3]
        user = {'staffid': staffid, 'username': name,'latest_login_date':latest_login_date,'user_id':user_id}
        all_users.append(user)

    return jsonify(all_users)


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
