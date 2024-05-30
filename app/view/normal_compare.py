import subprocess
from datetime import datetime
from app.util.crypto_ECB import AEScoder

from flask import Blueprint, render_template, request, redirect, session
# from app import log
import os
from app.useDB import ConnectSQL

web = Blueprint('test_normal_compare', __name__)
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))


@web.route('/test_normal_compare')
# @user.login_required
def test_normal_compare():
    return render_template("code_mode/test_normal_compare.html"  )

@web.route('/test_normal_compare',methods=['POST'])
def test_normal_compare1():
    user_id = session.get('userid', None)
    now_time = datetime.now()
    str_time = now_time.strftime("%Y%m%d%H%M%S")
    case_name = 'testcase_'+str_time

    if 'Save' in request.form:
        code = request.form['code']
        list= code.split("\r\n")
        newlist = [None]*20
        for i in list:
            if i.startswith('host'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[0]= i.strip().split('=')[-1].strip()
            elif i.startswith('username'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[1] = i.strip().split('=')[-1].strip()
            elif i.startswith('pwd'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[2] = i.strip().split('=')[-1].strip()
            elif i.startswith('access_id'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[3] = i.strip().split('=')[-1].strip()
            elif i.startswith('secret_access_key'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[4] = i.strip().split('=')[-1].strip()
            elif i.startswith('project'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[5] = i.strip().split('=')[-1].strip()
            elif i.startswith('endpoint'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[6] = i.strip().split('=')[-1].strip()
            elif i.startswith('database_type'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[7] = i.strip().split('=')[-1].strip()
            elif i.startswith('source_tablename'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[8] = i.strip().split('=')[-1].strip()
            elif i.startswith('target_tablename'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[9] = i.strip().split('=')[-1].strip()
            elif i.startswith('td_columndb'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[10] = i.strip().split('=')[-1].strip()
            elif i.startswith('source_db'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[11] = i.strip().split('=')[-1].strip()
            elif i.startswith('target_db'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[12] = i.strip().split('=')[-1].strip()
            elif i.startswith('pi'):
                # newlist.append(i.strip().split('=')[-1].strip())
                newlist[13] = i.strip().split('=')[-1].strip()
            elif i.startswith('source_where_condition'):
                # newlist.append(AEScoder().encrypt(i.strip().split(':')[-1].strip()).replace(" ' ", " '' "))
                newlist[14] = AEScoder().encrypt(i.strip().split(':')[-1].strip())
            elif i.startswith('target_where_condition'):
                # print (i.strip().split(':')[-1].strip())
                # newlist.append(AEScoder().encrypt(i.strip().split(':')[-1].strip()).replace(" ' ", " '' "))
                newlist[15] = AEScoder().encrypt(i.strip().split(':')[-1].strip())
        print (newlist)
        print (newlist[14],newlist[15])
        ConnectSQL().write_config_value(user_id, case_name, newlist[0], newlist[1], newlist[2], newlist[3], newlist[4], newlist[5],
                                        newlist[6],newlist[7], newlist[8], newlist[9], newlist[10], newlist[11],
                                        newlist[12], newlist[13],AEScoder().decrypt(newlist[14]).replace("'","\""),AEScoder().decrypt(newlist[15]).replace("'","\""))

        return render_template('code_mode/test_normal_compare.html'  )

    elif 'Run' in request.form:

        # cmd_td = '/opt/app/anaconda3/bin/python {}/data_check/td_mx.py'.format(basePath)
        cmd_td = 'python {}/data_check/td_mx.py'.format(configPath)

        # cmd_ora = '/opt/app/anaconda3/bin/python {}/data_check/or_mx.py'.format(basePath)
        cmd_ora = 'python {}/data_check/or_mx.py'.format(configPath)


        retcode = subprocess.call(cmd_td)
        # retcode = subprocess.call(cmd_td,shell=True)
        # print(retcode)
        if retcode == 0:
            return redirect('/test_finish')
        return render_template('test_error.html'  )



