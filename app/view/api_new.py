import json

import requests
from flask import Blueprint, render_template, request, jsonify, session

import os
import sys

from app.util.permissions import permission_required
from app.view import user

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(configPath)

web = Blueprint('apinew', __name__, template_folder='templates/apitest')


@web.route('/api_intergration', methods=['GET', 'POST'])
# @user.login_required
# @permission_required(session.get('groupname'))
def test_api():
    api_name = request.args.get('apiName', '')
    if 'token' in session:
        return render_template('api/api_intergration_no.html', api_name=api_name)
    else:
        return render_template('api/api_intergration_no.html', api_name=api_name)


@web.route('/api_intergration_normal', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def test_api_normal():
    api_name = request.args.get('apiName', '')
    if 'token' in session:
        return render_template('api/api_intergration_normal.html', api_name=api_name)
    else:
        return render_template('api/api_intergration_normal.html', api_name=api_name)



@web.route('/get_api_detail', methods=['POST'])
def get_api_detail():
    data = request.json
    response_data={
        "issued_token":"43kngdsigh8943nyger9g8e"
    }
    # response_data = {
    #     "apiurl": "https://chinadataplatform.cds.dev.ali.cloud.cn.hsbc/v1/getToken",
    #     "headers": {
    #         "content-type": "application/json",
    #     },
    #     "request_params": {
    #         "username": "45157276",
    #         "password": ""
    #     }
    # }

    return jsonify(response_data)

@web.route('/get_api_detail2', methods=['POST'])
def get_api_detail2():
    data = request.json
    print(111,data)
    url='https://chinadataplatform.cds.dev.ali.cloud.cn.hsbc/v1/hsbc/api/getApiDetail'
    headers={
            "content-type": "application/json",
            "Authorization": "yuxteyJ0eXAiOiJKV1MiLCJraWQiOiJFMkVfVFJVU1RfU0FNTF9DTUJfVUFUIiwiYWxnIjoiUlMyNTYiLCJzY2giOiJ1cm46YWltOnRva2VuOmludGVybmFsIiwic2N2IjoiMS4wIiwidGt2IjoiMS4wIn0.eyJzdWIiOiJXQ1QtSUIyQi1ERVYiLCJncnAiOlsiQ049SW5mb0Rpci1PU1NULUFQSS1TZWNHcnAtTm9uUHJvZCxPVT1PU1NULUFQSSxPVT1BcHBsaWNhdGlvbnMsT1U9R3JvdXBzLERDPUluZm9EaXIsREM9UHJvZCxEQz1IU0JDIiwiQ049aW5mb0Rpci1jbWItZHNwLWliMmItbnByb2QtaGssT1U9SEJISyxPVT1DTUItUExBVEZPUk0tRFNQLE9VPUFwcGxpY2F0aW9ucyxPVT1Hcm91cHMsREM9SW5mb0RpcixEQz1Qcm9kLERDPUhTQkMiLCJDTj1JbmZvZGlyLVdQQi1DQlNWLVVzZXItQ0MsT1U9SEJBUCxPVT1XUEIsT1U9QXBwbGljYXRpb25zLE9VPUdyb3VwcyxEQz1JbmZvRGlyLERDPVByb2QsREM9SFNCQyJdLCJpc3MiOiJjbWJkc3AudWsuaHNiYy5jb20iLCJleHAiOjE2ODE2NzYzNTIsImlhdCI6MTY4MTY3NjMyMiwianRpIjoiZGI1YmUzZTItZDBhMC00ZjgxLTk1MmEtMzBkMjI3NWUyMmEzIiwic2l0IjoiYWQ6c3ZjOnByaW5jaXBhbCJ9.OvPfHwLU9n43eD93zBENc4_4J5jtUmyWC",
        }
    payload ={
             "apiName": data['APIname'],
        }
    try:
        res = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
        data_dict = json.loads((res.text))
        api_detail = json.loads(data_dict['api_detail'])
        apiurl = api_detail['endPoint']

        request_body = json.loads(data_dict['api_detail'])['requestExample']

        if data['APIname'] != 'getToken':

            response_data = {
                "apiurl": apiurl,
                "headers": {
                    "content-type": "application/json",
                    "Authorization": "",
                },
                "request_params": request_body,
                "response_code":res.status_code,
            }

            return jsonify(response_data)
        else:
            response_data = {
                "apiurl": apiurl,
                "headers": {
                    "content-type": "application/json",
                },
                "request_params": request_body,

                "response_code": res.status_code,
            }

            return jsonify(response_data)

    except Exception as e:
        print(e)
        # raise e
        return jsonify("Something wrong!")




@web.route('/run_api_post', methods=['POST'])
def run_api_post():
    data = request.json
    print(data)
    print('POST')
    url = data['send_url']
    headers = data['send_headers']
    payload = data['send_body']
    try:
        res = requests.post(url=url, headers=headers, data=json.dumps(payload),verify=False)
        response = {'response_code': res.status_code, 'response_text': res.text,}
        return jsonify(response)
    except Exception:
        return jsonify({'response_code': 404, 'response_text': "error!!"})


@web.route('/run_api_get', methods=['POST'])
def run_api_get():
    data = request.json
    print(data)
    print('GET')
    url = data['send_url']
    headers = data['send_headers']
    payload = data['send_body']
    try:
        res = requests.get(url=url, headers=headers, data=json.dumps(payload),verify=False)
        response = {'response_code': res.status_code, 'response_text': res.text}
        return jsonify(response)
    except Exception:
        return jsonify({'response_code': 404, 'response_text': "error!!"})


@web.route('/test_api')
@user.login_required
# @permission_required(session.get('groupname'))
def test_api_other():
    return permission_required(session.get('groupname'))(render_template)('util/not-finish.html')

