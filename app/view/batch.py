from datetime import timedelta
from flask import Blueprint,render_template,request,redirect
import subprocess
import os
import sys
from werkzeug.utils import secure_filename

from app.util.IP_PORT import Constant
from app.view.user import authorize

basePath = os.path.join(os.path.join(os.path.dirname(__file__),"../"))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)

from app.util.crypto_ECB import AEScoder
from app.useDB import ConnectSQL


web = Blueprint("batch", __name__)

@web.route('/batch_test_data',methods=['GET','POST'])
def AD2_test_data():
    ip = Constant().ip
    port = Constant().port
    if 'Run' in request.form:
        database_type1 = request.form[('db1')]
        database_type2 = request.form[('db2')]
        cmd_td = 'python {}/data_check/td_mx.py'.format(basePath)
        cmd_ora = 'python {}/data_check/or_mx.py'.format(basePath)

        if database_type1 == "td" and database_type2 == "max":
            retcode = subprocess.call(cmd_td)
            if retcode == 0:
                return render_template('/test_finish.html',ip=Constant().ip, port=Constant().port)
            return render_template('test_error.html'  )
        elif database_type1 == "ora" and database_type2 == "max":
            retcode = subprocess.call(cmd_ora)
            if retcode == 0:
                return render_template('/test_finish2.html',ip=Constant().ip, port=Constant().port)
            return render_template('test_error.html'  )
    elif request.method == 'POST':
        database_type1 = request.form[('db1')]
        database_type2 = request.form[('db2')]
        if database_type1 == "td" and database_type2 == "max":
            f = request.files['file']
            print(f)
            fname = secure_filename(f.filename)
            print("源文件>>>>>>>>>>", fname)
            ext = fname.rsplit('.',1)[1]  #获取文件后缀
            new_filename = "config_td" + '.' + ext  #修改上传文件名
            # new_filename = "config_td.csv"  # 修改上传文件名

            print("上传td文件重命名>>>>>>>>>>>>>", new_filename)

            filepath = configPath  #当前文件所在路径
            print(filepath)

            upload_path = os.path.join(filepath, 'data_check\config', new_filename)  #注意：没有文件夹一定要先创建，不然会提示没有该路径
            print(upload_path)
            f.save(upload_path)
            return render_template('batch_test_data.html',ip=Constant().ip, port=Constant().port)

        elif database_type1 == "ora" and database_type2 == "max":
            f = request.files['file']
            print(f)
            fname = secure_filename(f.filename)
            print("源文件>>>>>>>>>>", fname)
            ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
            new_filename = "config_ora" + '.' + ext  # 修改上传文件名
            # new_filename = "config_or.csv"  # 修改上传文件名

            print("上传or文件重命名>>>>>>>>>>>>>", new_filename)

            filepath = configPath  # 当前文件所在路径
            print(filepath)

            upload_path = os.path.join(filepath, 'data_check\config', new_filename)  # 注意：没有文件夹一定要先创建，不然会提示没有该路径
            print(upload_path)
            f.save(upload_path)
            return render_template('batch_test_data.html'  )
    else:
        pass
        return render_template('batch_test_data.html',ip=Constant().ip, port=Constant().port)
    return render_template('batch_test_data.html'  )
