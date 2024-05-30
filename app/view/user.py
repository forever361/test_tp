import re
from functools import wraps

from datetime import timedelta
from shutil import copy
from flask import Blueprint, render_template, request, redirect, make_response, session, url_for, jsonify
import os
import sys

from app.db.tanos_manage import tanos_manage
from app.util.log_util.all_new_log import logger_all

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)


web = Blueprint("user", __name__)

web.send_file_max_age_default = timedelta(seconds=1)


#设置登录认证
def login_required(fn):
    @wraps(fn)
    def wrapper():
        user = session.get('userid', None)
        # print(11111,user)
        if user:
            return fn()
        else:
            redirect_url = tanos_manage().get_login_para()
            return render_template('auth/login_sso.html', redirect_url=redirect_url)
    return wrapper

#捕捉异常
#用法：@handle_exceptions
def handle_exceptions(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger_all.info(f"An error occurred: {str(e)}",exc_info=True)
            return jsonify({"error": "An error occurred"}), 500
    return wrapper

