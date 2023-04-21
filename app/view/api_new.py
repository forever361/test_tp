from flask import Blueprint, render_template, request, jsonify

import os
import sys



basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(configPath)

web = Blueprint('apinew', __name__, template_folder='templates/apitest')


@web.route('/api_intergration', methods=['GET', 'POST'])
# @user.authorize
def test_api():
    api_name = request.args.get('apiName', '')
    return render_template('api/api_intergration.html', api_name=api_name)


@web.route('/get_api_detail', methods=['POST'])
def get_api_detail():
    data = request.json
    print(data)
    if data["apiname"]=='taobao.appstore.subscribe.get':
        response_data = [{
            "apiurl":"http://gw.api.taobao.com/router/rest?app_key=12129701&method=taobao.appstore.subscribe.get&v=2.0",
            "headers": {
                "content-type": "application/json",
                "token": "testtoken",
            },
            "request_params": {
                "id": "null",
                "name": "null",
                "name2": "null",
                "name3": "null",
                "name4": "null",
                "name5": "null",

            }
        }]
    else:
        response_data = {
            "apiurl": "http://gw.api.taobao.com/router/rest?app_key=12129701&method=taobao.appstore.subscribe.get&v=2.0",
            "headers": {
                "content-type": "application/json",
                "token": "null",
            },
            "request_params": {
                "id": "null",
                "name": "null",
                "name2": "null",
                "name3": "null",
                "name4": "null",
                "name5": "null",

            }
        }

    return jsonify(response_data)
