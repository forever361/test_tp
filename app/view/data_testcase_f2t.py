import configparser
import subprocess
import traceback
from time import sleep

from flask import Blueprint, render_template, jsonify, request, get_flashed_messages, session
# from app import log
from app.db import test_case_manage
from app.util.Constant_setting import Constant_cmd
from app.util.log import logg
from app.useDB import ConnectSQL
from app.util.crypto_ECB import AEScoder
from app.view import user, viewutil
import os

from app.view.data_batch_new_f2t import get_log_f2t
# from app.data2_check.run_or_mx import method_main

web = Blueprint('data_testcase_f2t', __name__, template_folder='templates/uitest')
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
configP = configparser.ConfigParser()


@web.route('/api_data_test_cases_f2t')
@user.login_required
def test_cases():
    return render_template("uitest/data_test_cases_f2t.html")


@web.route('/data_edit_test_case_f2t', methods=['POST', 'GET'])
@user.login_required
def edit_test_case():
    user_id = session.get('userid', None)
    codelist = []
    codelist1 = []

    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')

        user_path = '{}/userinfo/{}/'.format(configPath, user_id)

        ini_path = user_path + '/' + 'config.ini'
        # 添加section
        configP.clear()
        configP.add_section("default")
        # 添加option并设置值，只能是string
        configP.set("default", "userid", str(user_id))
        configP.set("default", "caseid", str(id))
        configP.set("default", "times", str(2))
        configP.set("default", "returncode", 'NULL')
        # 写入ini文件，注意写入的mode会影响是否覆盖ini文件
        with open(ini_path, "w", encoding="utf8") as f:
            configP.write(f)

        infor_value = ConnectSQL().data_f2t_get_infor_value_id(id)
        for configreader in infor_value:
            testinfor = configreader[3].strip()
            testinfor1 = configreader[4].strip()
            testinfor = AEScoder().decrypt(testinfor)
            testinfor1 = AEScoder().decrypt(testinfor1)
            codelist.append(testinfor)
            codelist1.append(testinfor1)
        return render_template("uitest/data_edit_f2t.html", id=id, code_str=codelist[0], code_str1=codelist1[0])

    # SAVE保存的过程,点save就相当于提交了表单走post
    elif request.method == 'POST':

        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')
        # cmd_td = 'python {}/data2_check/run_or_mx.py'.format(configPath)
        # retcode = subprocess.Popen(cmd_td, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if 'Save' in request.form:
            testinfor = viewutil.getInfoAttribute(info, 'code')
            testinfor1 = viewutil.getInfoAttribute(info, 'code1')
            list = testinfor.split("\r\n")

            newlist = []
            for i in list:
                if i.startswith('Case_name'):
                    print(i)
                    newlist.append(i.strip().split('=')[-1].strip().strip(','))
            case_name = newlist[0]

            testinfor_en = AEScoder().encrypt(testinfor)
            testinfor_en_db = AEScoder().encrypt(testinfor1)
            test_case_manage.test_case_manage().data_f2t_update_test_case(id, ['testinfor', 'testinfor_db', 'case_name'],
                                                                      [testinfor_en, testinfor_en_db, case_name])
            return render_template('uitest/data_edit_f2t.html', code_str=testinfor, code_str1=testinfor1,
                                   message='Save success!')


        elif 'Report' in request.form:
            user_path = '{}/userinfo/{}/'.format(configPath, user_id)
            ini_path = user_path + '/' + 'config.ini'
            config = configparser.ConfigParser()
            config.read(ini_path)  # 读取 ini 文件
            case_id = config.get('default', 'caseid')

            # print("enter report.....")
            # print("retcode.returncode.....",retcode.returncode)
            # print("case_id.....", case_id)

            # print("user_id:", user_id)
            return render_template('data_f2t_test_finish.html', user_id=user_id,
                                   case_id=case_id)

        elif 'Save1' in request.form:

            print("enter save1.....")

            return render_template('uitest/data_edit_f2t.html')


@web.route('/data_f2t_runtest.json', methods=['POST', 'GET'])
@user.login_required
def runtest2():
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

        # print("前端拿到的参数",dict1)

        user_id = session.get('userid', None)
        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        # print(333,user_path)

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

        get_log_f2t(True)

        # info = request.form
        # code = viewutil.getInfoAttribute(info,'code')
        # code1 = viewutil.getInfoAttribute(info,'code1')
        #
        print(111111,"case_f2t subprocess!!!!")

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


@web.route('/data_delete_test_case_f2t', methods=['POST', 'GET'])
@user.login_required
def delete_test_case():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')
        return render_template("uitest/data_test_cases_f2t.html")
    if request.method == 'POST':
        info = request.form
        id = viewutil.getInfoAttribute(info, 'id')
        act = viewutil.getInfoAttribute(info, 'act')
        if act == 'del':
            test_case_manage.test_case_manage().data_f2t_delete_test_case(id)
            code = 200
            message = 'delete success!'
        else:
            code = 500
            message = 'act is not del'
        result = jsonify({'code': code, 'msg': message})
        return result, {'Content-Type': 'application/json'}


@web.route('/data_f2t_search_report', methods=['POST', 'GET'])
@user.login_required
def web_search_report():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        info = request.values
        # print ('info',info)
        id = viewutil.getInfoAttribute(info, 'id')
        # print('idididiidididid', id)
        user_id = session.get('userid', None)

        return render_template("userinfo/{}/{}_data_test.html".format(user_id, id))


# 点击search后查询库中case列表
@web.route('/data_test_case_f2t.json', methods=['POST', 'GET'])
# @user.login_required
def search_test_cases():
    if request.method == 'POST':
        # logger.info("2222222222222222222")
        pass
    if request.method == 'GET':
        # log().logger.info("1111111111111111111")
        # print("tiaoshi", "get 请求")
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit, 它表示一段数据的起点
        type = viewutil.getInfoAttribute(info, 'type')
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info, 'name')
        # database_type = viewutil.getInfoAttribute(info,'database_type')

        valueList = [name]
        conditionList = ['case_name']
        conditionList.append('case_id')
        valueList.append(id)
        fieldlist = []
        rows = 1000
        caseList = test_case_manage.test_case_manage().data_show_test_cases_f2t(conditionList, valueList, fieldlist, rows)
        data = caseList

        # print('1111',type)
        # print (data , "tiaoshi...")

        if type == 'case_one':  # 这种情况就是进入某一个用例，只需要查询一条
            active_id = viewutil.getInfoAttribute(info, 'id')
            print('222', active_id)
            for i in range(len(data)):
                # print (data[i]['id'])
                if data[i]['id'] == active_id:
                    print(data[i]['id'])
                    data1 = jsonify({'total': len(data), 'rows': data[i]})
                    print(data[i])
        else:
            data1 = jsonify({'total': len(data), 'rows': data[int(offset):int(offset) + int(limit)]})
        # log.log().logger.info('data1: %s' %data1)
        return data1, {'Content-Type': 'application/json'}


@web.route('/runtest.json', methods=['POST', 'GET'])
@user.login_required
def runtest():
    print("enter run api...")
    if request.method == 'POST':
        log().logger.info("post")
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        # log.log().logger.info(request.values)
        # log.log().logger.info(request.form)
        info = request.values
        id = viewutil.getInfoAttribute(info, 'id')
        print(id, "tiaoshi")
        # cmd_td = 'python {}/test2.py'.format(configPath)
        result = jsonify({'code': 200, 'msg': 'success!'})
        return result


@web.route('/test_run')
@user.login_required
def test_data():
    return render_template('test_error.html')


@web.route('/data_guide', methods=['GET'])
# @user.login_required
def test_compare():
    return render_template("guide/data_guide.html")


@web.route('/error.json', methods=['GET'])
def error():
    data = get_flashed_messages()
    print(data)
    message = jsonify({'code': 200, 'msg': data[0]})
    return (message)

# @web.route('/data_csv_report', methods=['POST', 'GET'])
# @user.login_required
# def data_csv_report():
#     # log.log().logger.info(request.value)
#     if request.method == 'GET':
#         info = request.values
#         # print ('info',info)
#         id = viewutil.getInfoAttribute(info,'id')
#         print('idididiidididid',id)
#         user_id = session.get('userid', None)
#
#         return render_template("userinfo/{}/{}.csv".format(user_id,id)  )
