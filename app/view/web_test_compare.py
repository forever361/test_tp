import subprocess
from datetime import datetime
from app.util.crypto_ECB import AEScoder
from app.util.permissions import permission_required
from app.view import viewutil, user

from flask import Blueprint, render_template, jsonify, request, redirect, flash, session

from app.util.IP_PORT import Constant
import os
from app.useDB import ConnectSQL

web = Blueprint('web_compare', __name__)
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))


@web.route('/web_test_compare',methods=['GET'])
@user.login_required
# @permission_required(session.get('groupname'))
def test_compare():
    return permission_required(session.get('groupname'))(render_template)("code_mode/web_test_compare.html"  )


@web.route('/web_test_compare',methods=['POST'])
def test_compare1():
    user_id = session.get('userid', None)
    now_time = datetime.now()
    str_time = now_time.strftime("%Y%m%d%H%M%S")
    # case_name = 'testcase_'+str_time

    if 'Save' in request.form:
        info = request.values
        code_str = viewutil.getInfoAttribute(info, 'code')


        code = request.form['code']

        print(code)

        list = code.split("\r\n")

        newlist = []
        for i in list:
            if i.startswith('#Case_name'):
                print (i)
                newlist.append(i.strip().split('=')[-1].strip())
        case_name = newlist[0]
        # print (case_name)

        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        file = open(user_path + 'config.ini', 'w')
        file.writelines(case_name)
        file.close()

        #加判断库里面case_name是否存在，如果存在就提示
        rows= ConnectSQL().web_get_infor_value(user_id, case_name)
        # print (rows,"rows")

        if  rows == [] or rows == None:
            # 保存到py文件
            file = open(user_path + 'webui_testcase.py', 'w')
            file.write(code)
            file.close()

            code = AEScoder().encrypt(code)
            ConnectSQL().web_write_config_value_all(user_id, case_name, code)

            return render_template('code_mode/web_test_compare_save.html'  ,
                                   message='Save success!',code_str=code_str)
        else:
            return render_template('code_mode/web_test_compare_save.html'  ,
                                   message='Casename already exists!',code_str=code_str)




    elif 'Run' in request.form:

        code = request.form['code']
        list = code.split("\r\n")

        newlist = []
        for i in list:
            if i.startswith('#Case_name'):
                newlist.append(i.strip().split('=')[-1].strip())
        case_name = newlist[0]

        user_path = '{}/userinfo/{}/'.format(configPath, user_id)
        file = open(user_path + 'config.ini', 'w')
        file.writelines(case_name)
        file.close()

        #加判断库里面case_name是否存在，如果存在就run，如果不存在弹框提示先save
        rows= ConnectSQL().web_get_infor_value(user_id, case_name)

        if  rows == [] or rows == None:
            return render_template('code_mode/web_test_compare.html'  ,
                                   message='Please save first!')

        else:
            case_id = rows[0][0]
            user_path = '{}/userinfo/{}/'.format(configPath, user_id)
            template_user_path = '{}/templates/userinfo/{}'.format(configPath, user_id)
            webui_dir =  '{}/webui_check'.format(configPath)

            # cmd_td = '/opt/app/anaconda3/bin/python {}/data_check/td_mx.py'.format(basePath)
            cmd_td = 'pytest {}/webui_testcase.py  --html={}/{}.html --self-contained-html --demo_mode --settings={}/custom_settings.py'.format(user_path,template_user_path,case_id,webui_dir)

            retcode = subprocess.call(cmd_td)
            # retcode = subprocess.call(cmd_td,shell=True)
            # print(retcode)
            if retcode == 0:
                return render_template('web_test_finish.html',case_name=case_name, user_id=user_id, case_id = case_id )
            return render_template('web_test_finish.html',case_name=case_name, user_id=user_id, case_id = case_id )








