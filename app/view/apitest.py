import subprocess
import time

from flask import Blueprint,render_template, request
# from app import log
from werkzeug.utils import secure_filename

from app.api_check.run_case import get_report_name
import os
import sys

from app.view import user

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)

web = Blueprint('apitest', __name__,template_folder='templates/apitest')


@web.route('/test_api123', methods=['GET','POST'])
@user.login_required
def test_api():
    print(111111111111111)
    if 'Run' in request.form:
        cmd_td = 'python {}/api_check/run_case.py'.format(configPath)
        print(cmd_td)

        retcode = subprocess.call(cmd_td)
        if retcode == 0:
            report_path = os.path.join(configPath, "templates/report")  # 测试报告路径
            report_file = get_report_name(report_path)  # 测试报告文件名
            time.sleep(2)
            # if os.path.exists(report_file):
            return render_template('report/{}'.format(report_file)  )
        return render_template('test_error.html'  )

    elif request.method == 'POST':
        f = request.files['file']
        print(f)
        fname = secure_filename(f.filename)
        print("源文件>>>>>>>>>>", fname)
        ext = fname.split('.')[1]
        new_filename = "config_api" + '.' + ext  #修改上传文件名

        print("上传api文件重命名>>>>>>>>>>>>>", new_filename)

        filepath = configPath  #当前文件所在路径
        print(filepath)

        upload_path = os.path.join(filepath, 'api_check/Case/', new_filename)  #注意：没有文件夹一定要先创建，不然会提示没有该路径
        print(upload_path)
        f.save(upload_path)
        return render_template('apitest/test_api2.html'  )

    return render_template('apitest/test_api2.html'  )

