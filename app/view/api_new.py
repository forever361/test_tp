
from flask import Blueprint,render_template, request

import os
import sys
basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)

web = Blueprint('apinew', __name__,template_folder='templates/apitest')


@web.route('/api_intergration', methods=['GET','POST'])
# @user.authorize
def test_api():
    api_name = request.args.get('apiName', '')
    return render_template('api/api_intergration.html',api_name= api_name)

