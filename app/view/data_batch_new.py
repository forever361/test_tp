import configparser
import json
import traceback
from datetime import timedelta
from time import sleep

import requests
from flask import Blueprint, render_template, request, redirect, jsonify, session
import subprocess
import os
import sys
from werkzeug.utils import secure_filename

from app.db.tanos_manage import tanos_manage
from app.useDB import ConnectSQL
from app.util.Constant_setting import Constant_cmd
from app.util.IP_PORT import Constant
from app.util.crypto_ECB import AEScoder
from app.view import viewutil, user


from app.application import app

basePath = os.path.join(os.path.join(os.path.dirname(__file__),"../"))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)
# userid = ConnectSQL().get_personal_user_id()
configP2 = configparser.ConfigParser()


web = Blueprint("batch_new", __name__)

@web.route('/api_batch_test_data',methods=['GET'])
@user.login_required
def batch_test_compare():
    return render_template("/code_mode/batch_tanos_data_new.html",domain=app.config['URL'] )


@web.route('/api_batch_test_data',methods=['POST'])
def batch_test_compare1():
    user_id = session.get('userid', None)

    user_path = '{}/userinfo/{}/'.format(configPath, user_id)
    ini_path = user_path + '/' + 'config.ini'
    # now_time = datetime.now()
    # str_time = now_time.strftime("%Y%m%d%H%M%S")
    # case_name = 'testcase_'+str_time

    if 'Save' in request.form:

        info = request.values
        code_str = viewutil.getInfoAttribute(info, 'code')

        code_str1 = viewutil.getInfoAttribute(info, 'code1')

        code = request.form['code']
        code1 =  request.form['code1']

        list = code.split("\r\n")

        newlist = []
        for i in list:
            if i.startswith('Case_name'):
                print (i)
                newlist.append(i.strip().split('=')[-1].strip())
        case_name = newlist[0]

        # user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        # file = open(user_path + 'config.ini', 'w')
        # file.writelines(case_name)
        # file.close()

        #加判断库里面case_name是否存在，如果存在就提示
        rows= ConnectSQL().data_get_infor_value( case_name)
        print ('rows:',rows)

        if  rows == [] or rows == None:

            code = AEScoder().encrypt(code)
            code1 = AEScoder().encrypt(code1)
            ConnectSQL().data_write_config_value_all(user_id, case_name, code, code1)

            case_id = ConnectSQL().data_get_case_id(case_name)[0][0]
            configP2.clear()
            configP2.add_section("default")
            # 添加option并设置值，只能是string
            configP2.set("default", "userid", str(user_id))
            configP2.set("default", "caseid", str(case_id))
            configP2.set("default", "times", str(2))
            configP2.set("default", "returncode", 'NULL')
            # 写入ini文件，注意写入的mode会影响是否覆盖ini文件
            with open(ini_path, "w", encoding="utf8") as f:
                configP2.write(f)

            return render_template('code_mode/data_test_compare_save.html'  ,
                                   message='Save success!',code_str=code_str, code_str1=code_str1)
        else:
            return render_template('code_mode/data_test_compare_save.html'  ,
                                   message='Case name already exists!',code_str=code_str,code_str1=code_str1)


    elif 'Report' in request.form:

        config = configparser.ConfigParser()
        config.read(ini_path)  # 读取 ini 文件
        case_id = config.get('default', 'caseid')

        # print("enter report.....")
        # print("retcode.returncode.....",retcode.returncode)
        # print("case_id.....", case_id)

        # print("user_id:", user_id)
        return render_template('data_test_finish.html', user_id=user_id,
                               case_id=case_id)


@web.route('/runtest3.json', methods=['POST', 'GET'])
@user.login_required
def runtest3():
    if request.method == 'POST':

        info = request.values
        code = viewutil.getInfoAttribute(info, 'code')
        code1 = viewutil.getInfoAttribute(info, 'code1')
        # 将连接参数保存为字典的键值对，就不怕顺序乱了
        list = code.split("\n")
        list1 = []
        list2 = []
        for i in list:
            if (i.startswith('#')): #不要注释行
                pass
            else:
                m = i.strip().find('=')
                list1.append(i.strip().split('=')[0].strip())
                list2.append(i[m + 1:].strip())  # 取第一个出现的=后面的
        d = zip(list1, list2)
        dict1 = dict(d)



        user_id = session.get('userid', None)
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)

        file = open(user_path + 'data_conn.txt', 'w')
        file.write(str(dict1))
        file.close()

        file = open(user_path + 'data_db.csv', 'w')
        file.write(code1)
        file.close()

        ini_path = user_path + '/' + 'config.ini'
        # # 清空日志
        with open(user_path + "log.log", 'w') as file:
            # file.writelines("11111")
            file.close()

        get_log(True)
        # info = request.form
        # code = viewutil.getInfoAttribute(info,'code')
        # code1 = viewutil.getInfoAttribute(info,'code1')
        #
        # print(111,code)

        file = open(user_path + 'log.log', 'a')
        file.writelines(
            "|||||||||||||||||||||||||||||||||||||||Start checking|||||||||||||||||||||||||||||||||||||||" + '\n')
        file.writelines("Prepare data..." + '\n')
        file.close()

        # cmd_td = 'python {}/data2_check/run_or_mx.py {}'.format(configPath, user_id)
        # retcode = subprocess.Popen(cmd_td, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        retcode = Constant_cmd(user_id).retcode

        # cmd_td = '/hsbc/tac/app/anaconda3/bin/python3.6 {}/data2_check/run_or_mx.py {}'.format(configPath,user_id)
        # retcode = subprocess.Popen(cmd_td, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = retcode.communicate()

        if stderr:
            print(str(stderr, "utf-8") + '111111')
            # file = open(user_path + 'log.log', 'a')
            # file.writelines(str(stderr, "utf-8") + '\n')
            # file.close()
        else:
            print(str(stdout, "utf-8") + '222222')
        #
        # # 添加section
        # configP.set("default", "returncode", str(retcode.returncode))
        # # 写入ini文件，注意写入的mode会影响是否覆盖ini文件
        # with open(ini_path, "w+", encoding="utf8") as f:
        #     configP.write(f)

        # from app.data2_check.run_or_mx import method_main
        # from app.util.log_util.new_log import logger
        # # from app.data2_check.test import testrun
        #
        # try:
        #     method_main()
        #     # testrun()
        #     print("Run 按钮执行成功！！")
        #     result = jsonify({'code': 200, 'msg': 'run success!', 'returncode': 0})
        #     print(result)
        #     sleep(1.5)
        #     return result
        # except:
        #     s= traceback.format_exc()
        #     # checker.logger.info(s)
        #     logger.info(s)
        #     print("执行失败！！")
        #     result = jsonify({'code': 400, 'msg': 'run failed', 'returncode': 1})
        #     print(result)
        #     sleep(1.5)
        #     return result, {'Content-Type': 'application/json'}

        if retcode.returncode == 0:
            print("Run 按钮执行成功！！")
            sleep(1.6)
            result = jsonify({'code': 200, 'msg': 'run success!', 'returncode': 0})
            print(result)
            return result

        else:
            print("执行失败！！")
            file = open(user_path + 'log.log', 'a')
            file.writelines(str(stderr, "utf-8") + '\n')
            file.close()
            sleep(1.6)
            result = jsonify({'code': 400, 'msg': 'run failed', 'returncode': 1})
            print(result)
            return result, {'Content-Type': 'application/json'}


line_number = [0] #存放当前日志行数
log_data = []
# 定义接口把处理日志并返回到前端
@web.route('/get_log',methods=['GET','POST'])
# @user.login_required
def get_log(flag=False):
    if flag==False:
        log_data = red_logs() # 获取日志
        # print(len(log_data),11111)
        # print(line_number[0],222222)
        # 判断如果此次获取日志行数减去上一次获取日志行数大于0，代表获取到新的日志
        if len(log_data) - line_number[0] > 0:
            log_type = 2 # 当前获取到日志
            log_difference = len(log_data) - line_number[0] # 计算获取到少行新日志
            log_list = [] # 存放获取到的新日志
            # 遍历获取到的新日志存放到log_list中
            for i in range(log_difference):
                log_i = log_data[-(i+1)].decode('utf-8') # 遍历每一条日志并解码
                log_list.insert(0,log_i) # 将获取的日志存放log_list中
        else:
            log_type = 3
            log_list = ''
        # 已字典形式返回前端
        _log = {
            'log_type' : log_type,
            'log_list' : log_list
        }
        # print(_log, 7777777777777777777)
        line_number.pop() # 删除上一次获取行数
        line_number.append(len(log_data)) # 添加此次获取行数
        # print(line_number)
        return _log
    else:
        log_data = red_logs() # 获取日志
        # print(len(log_data),11111)
        # print(line_number[0],222222)
        # 判断如果此次获取日志行数减去上一次获取日志行数大于0，代表获取到新的日志
        if len(log_data) - line_number[0] > 0:
            log_type = 2 # 当前获取到日志
            log_difference = len(log_data) - line_number[0] # 计算获取到少行新日志
            log_list = [] # 存放获取到的新日志
            # 遍历获取到的新日志存放到log_list中
            for i in range(log_difference):
                log_i = log_data[-(i+1)].decode('utf-8') # 遍历每一条日志并解码
                log_list.insert(0,log_i) # 将获取的日志存放log_list中
        else:
            log_type = 3
            log_list = ''
        # 已字典形式返回前端
        _log = {
            'log_type' : log_type,
            'log_list' : log_list
        }
        line_number.clear() # 删除上一次获取行数
        line_number.append(0) # 添加此次获取行数
        # print(line_number)
        return _log


def red_logs():
    user_id = session.get('userid', None)
    _path = '{}/userinfo/{}/'.format(configPath, user_id)
    log_path = f'{_path}log.log'  # 获取日志文件路径
    with open(log_path, 'rb') as f:
        log_size = os.path.getsize(log_path)  # 获取日志大小
        offset = -100
        # 如果文件大小为0时返回空
        if log_size == 0:
            return ''
        while True:
            # 判断offset是否大于文件字节数,是则读取所有行,并返回
            if (abs(offset) >= log_size):
                f.seek(-log_size, 2)
                data = f.readlines()
                return data
            # 游标移动倒数的字节数位置
            data = f.readlines()
            # 判断读取到的行数，如果大于1则返回最后一行，否则扩大offset
            if (len(data) > 1):
                return data
            else:
                offset *= 2


@web.route('/clear_log',methods=['GET','POST'])
def clear_log():
    get_log(flag=True)
    return ''


@web.route('/saveCase', methods=['POST'])
def saveCase():
    # TODO: Update data in the database
    data = request.json
    print(data)
    # 新建case
    user_id = session.get('userid', None)
    case_name = data['case_name']
    code=""
    code1=""
    ConnectSQL().data_write_config_value_all(user_id, case_name, code, code1)

    case_id = ConnectSQL().data_get_case_id(case_name)[0][0]

    # 新建job
    data_str = json.dumps(data['job'])
    print(data_str)
    # TODO: Update data in the database
    tanos_manage().new_job(data['job_name'],data_str,case_id)
    #查询case#查询job，跳转到http://127.0.0.1:8889/data_edit_test_case_tanos?id=10074，前端实现

    return jsonify(success=True, message='run job successfully',case_id=case_id)