import subprocess

from flask import Blueprint, render_template, jsonify, request, redirect, session
# from app import log
from app.db import test_case_manage
from app.util.log import logg
from app.useDB import ConnectSQL
from app.util.crypto_ECB import AEScoder
from app.view import viewutil
import os

web = Blueprint('testcase', __name__,template_folder='templates/uitest')
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))

@web.route('/test_suites')
# @authorize
def test_suite():
    return render_template("uitest/test_suite.html"  )


@web.route('/test_cases')
# @user.authorize
def test_cases():

    return render_template("uitest/test_cases.html"  )


@web.route('/add_test_case', methods=['POST', 'GET'])
# @user.authorize
def save_new_test_case():
    if request.method == 'GET':
        return render_template("uitest/new_test_cases.html"  )
    if request.method == 'POST':
        info = request.form
        name = viewutil.getInfoAttribute(info,'name')
        module = viewutil.getInfoAttribute(info,'module')
        description = viewutil.getInfoAttribute(info,'description')
        type = viewutil.getInfoAttribute(info,'type')
        if module == '' or name == '' or module == 'All':
            return 'Required fields cannot be empty!'
        else:
            test_case_manage.test_case_manage().new_test_case(module,name,description)
        return redirect('test_cases')


@web.route('/edit_test_case', methods=['POST', 'GET'])
# @user.authorize
def edit_test_case():
    user_id = session.get('userid', None)
    codelist=[]
    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info,'id')
        infor_value= ConnectSQL().get_infor_value_id(id)
        for configreader in infor_value:
            testinfor = configreader[3].strip()
            testinfor = AEScoder().decrypt(testinfor)
            codelist.append(testinfor)
        return render_template("uitest/edit.html", id=id  ,code_str=codelist[0])
    #SAVE保存的过程,点save就相当于提交了表单走post
    elif request.method == 'POST':
        if 'Save' in request.form:
            info = request.values
            id = viewutil.getInfoAttribute(info,'id')
            testinfor = viewutil.getInfoAttribute(info, 'code')

            list = testinfor.split("\r\n")

            newlist = []
            for i in list:
                if i.startswith('Case_name'):
                    print(i)
                    newlist.append(i.strip().split('=')[-1].strip())
            case_name = newlist[0]

            user_path = '{}/userinfo/{}/'.format(configPath, user_id)
            file = open(user_path + 'config.ini', 'w')
            file.writelines(case_name)
            file.close()

            testinfor_en = AEScoder().encrypt(testinfor)
            test_case_manage.test_case_manage().update_test_case(id,['testinfor','case_name'],
                                                                     [testinfor_en,case_name])
            return render_template('uitest/edit.html'  ,code_str=testinfor,message='Save success!')


        elif 'Run' in request.form:
            code = request.form['code']
            list = code.split("\r\n")
            newlist = []
            for i in list:
                if i.startswith('Case_name'):
                    newlist.append(i.strip().split('=')[-1].strip())
            case_name = newlist[0]
            user_path = '{}/userinfo/{}/'.format(configPath, user_id)
            file = open(user_path + 'config.ini', 'w')
            file.writelines(case_name)
            file.close()
            # 加判断库里面case_name是否存在，如果存在就run，如果不存在弹框提示先save
            rows = ConnectSQL().get_infor_value(user_id, case_name)
            if rows == [] or rows == None:
                return render_template('uitest/edit.html'  ,
                                       message='Please save first!',code_str=code)

            else:

                # cmd_td = '/opt/app/anaconda3/bin/python {}/data_check/td_mx.py'.format(basePath)
                cmd_td = 'python {}/data_check/viola.py'.format(configPath)
                retcode = subprocess.call(cmd_td)
                # retcode = subprocess.call(cmd_td,shell=True)
                # print(retcode)
                if retcode == 0:
                    return render_template('test_error.html'  ,case_name=case_name)
                return render_template('test_error.html'  ,case_name=case_name)


@web.route('/copy_test_case', methods=['POST', 'GET'])
# @user.authorize
def copy_test_case():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        result = jsonify({'code': 500, 'msg':'should be get!'})
        return result
    if request.method == 'POST':
        info = request.form
        id = viewutil.getInfoAttribute(info,'id')
        if id == '':
            result = jsonify({'code': 500, 'msg':'test case is not found!'})
        else:
            result0 = test_case_manage.test_case_manage().copy_test_case(id)
            if result0:
                result = jsonify({'code': 200, 'msg':'copy success!'})
            else:
                result = jsonify({'code': 500, 'msg': 'test case is not found!'})
        return result




@web.route('/delete_test_case', methods=['POST', 'GET'])
# @user.authorize
def delete_test_case():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info,'id')
        return render_template("uitest/test_cases.html"  )
    if request.method == 'POST':
        info = request.form
        id = viewutil.getInfoAttribute(info,'id')
        act = viewutil.getInfoAttribute(info,'act')
        if act == 'del':
            test_case_manage.test_case_manage().delete_test_case(id)
            code = 200
            message = 'delete success!'
        else:
            code = 500
            message = 'act is not del'
        result = jsonify({'code': code, 'msg': message})
        return result,{'Content-Type': 'application/json'}


#点击search后查询库中case列表
@web.route('/test_case.json', methods=['POST', 'GET'])
# @user.authorize
def search_test_cases():

    if request.method == 'POST':
        log().logger.info("2222222222222222222")
    if request.method == 'GET':
        log().logger.info("1111111111111111111")
        # print("tiaoshi", "get 请求")
        info = request.values
        limit = info.get('limit', 10)  #每页显示的条数
        offset = info.get('offset',0)  #分片数，(页码-1)*limit, 它表示一段数据的起点
        type = viewutil.getInfoAttribute(info,'type')
        id = viewutil.getInfoAttribute(info, 'id')
        name = viewutil.getInfoAttribute(info,'name')
        # database_type = viewutil.getInfoAttribute(info,'database_type')

        valueList = [name]
        conditionList = ['case_name']
        conditionList.append('case_id')
        valueList.append(id)
        fieldlist = []
        rows = 1000
        caseList = test_case_manage.test_case_manage().show_test_cases2(conditionList,valueList,fieldlist,rows)
        data = caseList

        # print('1111',type)
        # print (data , "tiaoshi...")

        if type == 'case_one': #这种情况就是进入某一个用例，只需要查询一条
            active_id = viewutil.getInfoAttribute(info, 'id')
            print('222',active_id)
            for i in range(len(data)):
                # print (data[i]['id'])
                if data[i]['id'] == active_id:
                    print(data[i]['id'])
                    data1 = jsonify({'total':len(data),'rows':data[i]})
                    print (data[i])
        else:
            data1 = jsonify({'total':len(data),'rows':data[int(offset):int(offset)+int(limit)]})
        # log.log().logger.info('data1: %s' %data1)
        return data1,{'Content-Type': 'application/json'}


@web.route('/runtest.json', methods=['POST', 'GET'])
# @user.authorize
def runtest():
    # log.log().logger.info(request)
    if request.method == 'POST':
        log().logger.info("post")
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        # log.log().logger.info(request.values)
        # log.log().logger.info(request.form)
        info = request.values
        id = viewutil.getInfoAttribute(info,'id')
        print (id , "tiaoshi")
        # cmd_td = 'python {}/test2.py'.format(configPath)
        result = jsonify({'code': 200, 'msg': 'success!'})
        return result

@web.route('/test_run')
# @user.authorize
def test_data():
    return render_template('test_error.html'  )