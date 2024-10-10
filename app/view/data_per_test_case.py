import configparser

import json
import re
import subprocess
import traceback
from datetime import datetime
from time import sleep

import paramiko
import psycopg2
from flask import Blueprint, render_template, jsonify, request, get_flashed_messages, send_from_directory, session, redirect, url_for
# from app import log
from flask_socketio import emit
from psycopg2 import sql

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

@web.route('/add_per_job', methods=['post'])
def add_per_job():
    data = request.json
    job_name = data['job_name']
    try:
        tanos_manage().add_data_per_job(job_name)
        return jsonify(success=True,message="add successfully")
    except:
        return jsonify(success=False,message="Fail to add")


@web.route('/delete_per_job', methods=['post'])
def delete_per_job():
    data = request.json
    tanos_manage().delete_data_per_job(data["id"])
    #这里文件最好也能删掉
    logger_all.info('delete connection：{}'.format(data["id"]))
    return jsonify(success=True, message='Job deleted successfully')



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
    job_config = json.dumps(data)
    print(job_config)
    tanos_manage().update_data_per_job_config(job_id,job_config)


    return render_template('performace/data_per_config.html', job_id=job_id)


@app.route('/loadDataPerConfiguration', methods=['POST'])
def load_data_per_configuration():
    data = request.json
    job_id = data['jobId']
    print(1111,job_id)

    result = tanos_manage().show_data_per_job_config(job_id)

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'No configuration found for this job ID'}), 404


@app.route('/fetchPhaseData', methods=['POST'])
def fetch_phase_data():
    # 示例数据，可以从数据库或其他数据源获取实际数据


    data = request.json
    job_id = data['jobId']

    expectedTime = data['expectedTime']
    print('expectedTime',expectedTime)

    result = tanos_manage().show_data_per_job_config(job_id)


    # 从 result 中提取各个 datapoint
    fileServerDatapoint1 = result['fileServerDatapoint1']
    fileServerDatapoint2 = result['fileServerDatapoint2']
    odsDatapoint = result['odsDatapoint']
    cdsDatapoint = result['cdsDatapoint']

    # 函数用于获取连接信息
    def get_connection_info(datapoint):
        connect_id = tanos_manage().get_connectid_by_point_name(datapoint)
        connect_info = tanos_manage().search_all_by_connect_id(connect_id)
        keys = ('connect_id', 'connect_name', 'dbtype', 'connect_type', 'host', 'dblibrary', 'username', 'pwd', "port")
        result_list = []
        for row in connect_info:
            values = [value.strip() if isinstance(value, str) else value for value in row]
            result_dict = dict(zip(keys, values))
            result_list.append(result_dict)
        return dict(result_list[0])

    # 获取连接信息
    conn_fileServerDatapoint1 = get_connection_info(fileServerDatapoint1)
    conn_fileServerDatapoint2 = get_connection_info(fileServerDatapoint2)
    conn_odsDatapoint = get_connection_info(odsDatapoint)
    conn_cdsDatapoint = get_connection_info(cdsDatapoint)

    # 获取表名
    fileServerDatapoint1_tablename = tanos_manage().get_tablename_by_point_name(fileServerDatapoint1)
    fileServerDatapoint2_tablename = tanos_manage().get_tablename_by_point_name(fileServerDatapoint2)
    odsDatapoint_tablename = tanos_manage().get_tablename_by_point_name(odsDatapoint)
    cdsDatapoint_tablename = tanos_manage().get_tablename_by_point_name(cdsDatapoint)

    # 整合所有连接信息到 connt 字典中
    conn_info  = {
        'fileServer_conn1': '{},{},{},{},{},{}'.format(
            conn_fileServerDatapoint1['host'], conn_fileServerDatapoint1['port'],
            conn_fileServerDatapoint1['dblibrary'], conn_fileServerDatapoint1['username'],
            conn_fileServerDatapoint1['pwd'], fileServerDatapoint1_tablename),
        'fileServer_conn2': '{},{},{},{},{},{}'.format(
            conn_fileServerDatapoint2['host'], conn_fileServerDatapoint2['port'],
            conn_fileServerDatapoint2['dblibrary'], conn_fileServerDatapoint2['username'],
            conn_fileServerDatapoint2['pwd'], fileServerDatapoint2_tablename),
        'ODS_conn': '{},{},{},{},{},{}'.format(
            conn_odsDatapoint['host'], conn_odsDatapoint['port'],
            conn_odsDatapoint['dblibrary'], conn_odsDatapoint['username'],
            conn_odsDatapoint['pwd'], odsDatapoint_tablename),
        'CDS_conn': '{},{},{},{},{},{}'.format(
            conn_cdsDatapoint['host'], conn_cdsDatapoint['port'],
            conn_cdsDatapoint['dblibrary'], conn_cdsDatapoint['username'],
            conn_cdsDatapoint['pwd'], cdsDatapoint_tablename)
    }

    def get_log_times(server, port, username, password, file_path):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port=port, username=username, password=password)

        sftp = ssh.open_sftp()
        file = sftp.file(file_path)
        lines = file.readlines()
        file.close()
        sftp.close()
        ssh.close()

        start_time_pattern = re.compile(r"TANOS_start_time:(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")
        end_time_pattern = re.compile(r"TANOS_end_time:(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")

        start_time = None
        end_time = None

        for line in lines:
            start_time_match = start_time_pattern.search(line)
            if start_time_match:
                start_time = datetime.strptime(start_time_match.group(1), '%Y-%m-%d %H:%M:%S')

            end_time_match = end_time_pattern.search(line)
            if end_time_match:
                end_time = datetime.strptime(end_time_match.group(1), '%Y-%m-%d %H:%M:%S')

        return start_time, end_time

    print(conn_info )

    start_times = []
    end_times = []

    for key in ['fileServer_conn1', 'fileServer_conn2']:
        server, _, _, username, password, file_path = conn_info[key].split(',')
        start_time, end_time = get_log_times(server, 22, username, password, file_path)

        if start_time and end_time:
            start_times.append(start_time)
            end_times.append(end_time)

        earliest_start_time = min(start_times)
        latest_end_time = max(end_times)
        print(f"Earliest start time: {earliest_start_time}")
        print(f"Latest end time: {latest_end_time}")

    # 连接pg数据库
    ods_conn_info = conn_info['ODS_conn'].split(',')
    cds_conn_info = conn_info['CDS_conn'].split(',')

    # 创建连接字符串
    ods_conn_str = "host={} port={} dbname={} user={} password={}".format(
        ods_conn_info[0], ods_conn_info[1], ods_conn_info[2], ods_conn_info[3], ods_conn_info[4]
    )

    cds_conn_str = "host={} port={} dbname={} user={} password={}".format(
        cds_conn_info[0], cds_conn_info[1], cds_conn_info[2], cds_conn_info[3], cds_conn_info[4]
    )

    print(result['odsSystemCode'],result['odsSubSystemCode'],result['odsBatchData'])

    def fetch_data(conn_str,tablename,aa,bb,cc):
        try:
            # 连接到 PostgreSQL 数据库
            conn = psycopg2.connect(conn_str)
            cur = conn.cursor()

            print(111,tablename)

            # 查询 datatest.datatest 表中的数据
            # 分离模式名和表名
            schema_name, table_name = tablename.split('.')

            # 使用 sql.Identifier 格式化模式名和表名
            query = sql.SQL("SELECT ods_start_time, ods_end_time FROM {}.{}").format(
                sql.Identifier(schema_name),
                sql.Identifier(table_name)
            )
            cur.execute(query)

            # 获取查询结果
            rows = cur.fetchall()
            print(rows)
            # 将 datetime 对象格式化为字符串
            formatted_rows = [(row[0].strftime('%Y-%m-%d %H:%M:%S'), row[1].strftime('%Y-%m-%d %H:%M:%S')) for row in
                              rows]
            print("Formatted rows:", formatted_rows)

            # 关闭游标和连接
            cur.close()
            conn.close()
            return formatted_rows

        except Exception as error:
            print(f"Error: {error}")
            return []

    # 查询 ODS 数据库
    ods_data = fetch_data(ods_conn_str,ods_conn_info[5],result['odsSystemCode'],result['odsSubSystemCode'],result['odsBatchData'])

    # 查询 CDS 数据库
    cds_data = fetch_data(cds_conn_str, cds_conn_info[5],result['cdsSystemCode'],result['cdsSubSystemCode'],result['cdsBatchData'])

    # 如果查询到的行数不为0, 取第一行的时间数据
    ods_start_time, ods_end_time = ods_data[0] if ods_data else (None, None)
    cds_start_time, cds_end_time = cds_data[0] if cds_data else (None, None)

    if isinstance(cds_end_time, str):
        cds_end_time = datetime.strptime(cds_end_time, '%Y-%m-%d %H:%M:%S')
    if isinstance(earliest_start_time, str):
        earliest_start_time = datetime.strptime(earliest_start_time, '%Y-%m-%d %H:%M:%S')

    # Calculate duration as a timedelta object
    duration = cds_end_time - earliest_start_time
    print(cds_end_time)
    print(earliest_start_time)
    duration_seconds = duration.total_seconds()


    data = {
        "serverData": {
            "startTime": earliest_start_time,
            "endTime": latest_end_time
        },
        "juniperData": {
            "startTime": latest_end_time,
            "endTime": ods_start_time
        },
        "odsData": {
            "startTime": ods_start_time,
            "endTime": ods_end_time
        },
        "cdsData": {
            "startTime": cds_start_time,
            "endTime": cds_end_time
        },
        "during":duration_seconds,
        "expectedTime":expectedTime,
        "test_result":""
    }

    # 确保 during 和 expectedTime 都是有效数值
    if isinstance(data['during'], (int, float)) and isinstance(data['expectedTime'], (int, float)):
        # 判断 during 是否大于 expectedTime
        if data['during'] > data['expectedTime']:
            data['test_result'] = "fail"
        else:
            data['test_result'] = "pass"
    else:
        # 在这里处理无效值的情况
        print("Error: during or expectedTime is not a valid number.")
        data['test_result'] = "invalid"

    print(data)

    # 格式化时间的函数
    def format_datetime(value):
        """
        Format a datetime object or a string to 'YYYY-MM-DD HH:MM:SS'.
        """
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, str):
            # 这里假设字符串已经是正确的格式
            # 如果不确定，可以使用 datetime.strptime 来解析和重组格式
            try:
                return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                print(f"Error parsing date: {e}")
                return value
        return value

    # 更新数据字典中所有时间字段为格式化字符串
    for key in ['serverData', 'juniperData', 'odsData', 'cdsData']:
        for time_key in ['startTime', 'endTime']:
            data[key][time_key] = format_datetime(data[key][time_key])

    print(data)

    return jsonify(data)

# Remote server configuration
REMOTE_SERVER = {
    'hostname': '8.134.189.98',  # Replace with the remote server IP or domain
    'port': 22,
    'username': 'realtime',  # Replace with your SSH username
    'password': 'wesoftar1',  # Replace with your SSH password (or use private key auth)
    'directory': '/home/realtime'  # Remote directory where files are stored
}

def extract_timestamp(filename):
    """
    Extract the timestamp part from the filename.
    Example: s1_testa_testa_2024091706008.log -> 2024091706008
    """
    match = re.search(r'(\d{13})', filename)  # This will match the 13-digit timestamp
    if match:
        return match.group(1)
    return None

def ssh_list_files(code, sub_code, script_name):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh.connect(
            hostname=REMOTE_SERVER['hostname'],
            port=REMOTE_SERVER['port'],
            username=REMOTE_SERVER['username'],
            password=REMOTE_SERVER['password']  # Consider using a key file for better security
        )

        # Define the search pattern for the files
        search_pattern = f"{script_name}_{code}_{sub_code}"

        print(f"Search pattern: {search_pattern}")

        # Construct the command to list files in the remote directory
        command = f"ls {REMOTE_SERVER['directory']} | grep '{search_pattern}'"
        print(f"Executing command: {command}")

        # Execute the command on the remote server
        stdin, stdout, stderr = ssh.exec_command(command)

        # Capture the output (list of files)
        files = stdout.read().decode().splitlines()
        errors = stderr.read().decode()

        # Close the SSH connection
        ssh.close()

        # Check for errors returned by stderr
        if errors:
            print(f"Error from SSH command: {errors}")
            return [], errors

        sorted_files = sorted(files, key=lambda f: extract_timestamp(f), reverse=True)

        # Return the list of files and no error
        return sorted_files, None

    except Exception as e:
        # If an error occurs, return an empty list and the error message
        return [], str(e)



@app.route('/search_log_files', methods=['POST'])
def search_log_files():
    data = request.get_json()
    code = data.get('code')
    sub_code = data.get('sub_code')
    script_name = data.get('script_name')

    print(data)

    # Get the list of files from the remote server
    files, error = ssh_list_files(code, sub_code, script_name)

    if error:
        return jsonify({"error": error}), 500

    if files:
        return jsonify({"files": files})
    else:
        return jsonify({"files": []}), 200