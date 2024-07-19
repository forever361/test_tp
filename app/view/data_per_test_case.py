import configparser

import json
import subprocess
import traceback
from datetime import datetime
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

web = Blueprint('data_per_test_case', __name__, template_folder='templates/performace')
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
configP = configparser.ConfigParser()


@web.route('/data_performance_testing')
@user.login_required
def data_per_test_case_management():
    return render_template ('performace/data_per_job_management.html')


@web.route('/data_per_job_search.json', methods=['GET'])
def show_batch_job():
    rows = tanos_manage().show_data_per_job()
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

@web.route('/add_per_job', methods=['get'])
def add_per_job():
    tanos_manage().add_data_per_job('test123')
    return 'OK'


@app.route('/data_per_search_case',methods=['GET'])
def data_per_search_case():
    # 获取请求参数中的id
    job_id = request.args.get('id')
    return render_template('performace/data_per_job_detail.html', job_id=job_id)


@app.route('/data_per_config',methods=['GET','POST'])
def data_per_config():
    # 获取请求参数中的id
    job_id = request.args.get('id')
    return render_template('performace/data_per_config.html', job_id=job_id)



@app.route('/saveDataPerConfiguration',methods=['POST'])
def saveDataPerConfiguration():
    data = request.json
    job_id = data['jobId']

    return render_template('performace/data_per_config.html', job_id=job_id)