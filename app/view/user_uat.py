import re
from functools import wraps

from datetime import timedelta, datetime
from shutil import copy
from flask import Blueprint, render_template, request, redirect, make_response, session, url_for, jsonify
import os
import sys

from onelogin.saml2.auth import OneLogin_Saml2_Auth

from app.application import app
from app.common.libs.Helper import ops_render, ops_rederErrJSON, ops_rederJSON
from app.db.tanos_manage import tanos_manage
from app.util.IP_PORT import Constant
from app.util.log_util.all_new_log import logger_all

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)

from app.util.crypto_ECB import AEScoder
from app.util.oss import AliyunOSSClient
from app.useDB import ConnectSQL
from app.personal_center import Template_user


web = Blueprint("user_uat", __name__)

web.send_file_max_age_default = timedelta(seconds=1)


#设置登录认证
# def authorize(fn):
#     @wraps(fn)
#     def wrapper():
#         user = session.get('user',None)
#         if user:
#             # 判断文件是否存在，copyexcel到个人目录
#             user_id = session.get('userid', None)
#             # user_id = session.get('userid', None)
#             print ("我已经登录~~~~~~",user_id)
#             # user_path = '{}/static/userinfo/{}/'.format(configPath, user_id)
#             return fn()
#         else:
#             return render_template("auth/login_sso.html")
#     return wrapper

#设置登录认证
# def login_required(fn):
#     @wraps(fn)
#     def wrapper():
#         user = session.get('userid', None)
#         # print(11111,user)
#         if user:
#             return fn()
#         else:
#             redirect_url = tanos_manage().get_login_para()
#             return render_template('auth/login_sso.html', redirect_url=redirect_url)
#     return wrapper

#捕捉异常
#用法：@handle_exceptions
# def handle_exceptions(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         try:
#             return fn(*args, **kwargs)
#         except Exception as e:
#             logger_all.info(f"An error occurred: {str(e)}",exc_info=True)
#             return jsonify({"error": "An error occurred"}), 500
#     return wrapper

# @web.route('/login',methods=['GET','POST'])
# def login():
#     if "Login" in request.form:
#         username_login = request.form.get("login_name")
#         password_login = request.form.get("login_pwd")
#         if username_login and password_login:
#             rows = ConnectSQL().get_register_username(username_login)
#             if rows == [] or rows == None:
#                 return render_template('auth/login.html'  , message='Please enter the correct username and password!')
#             elif rows != [] or rows != None:
#                 rows_username = rows[0][0].strip()
#                 if rows_username != '' and rows_username != None and rows_username == username_login:
#                     password_old = ConnectSQL().get_password(username_login)
#                     password_key_login = AEScoder().decrypt('{}'.format(password_old))
#                     if password_login == password_key_login:
#                         user_id = ConnectSQL().get_login_userid(username_login)
#                         Template_user().Data_html(username_login,user_id)
#                         if user_id:
#                             response = make_response(redirect('/'))
#                             response.set_cookie('Name', '{}'.format(rows_username),60*60*24*1000)
#                             response.set_cookie('ID', '{}'.format(user_id), 60 * 60 * 24 * 1000)
#                             session['username'] = rows_username
#                             session['userid'] = user_id
#                             session.permanent = True
#                             return response
#                         # return render_template('index.html')
#                     else:
#                         return render_template('auth/login.html'  ,message='Please enter the correct username and password!')
#             else:
#                 return render_template('auth/login.html'  ,message='Please enter the correct username and password!')
#         else:
#             return render_template('auth/login.html'  )
#     else:
#         return render_template('auth/login.html'  )
#     return render_template('auth/login.html'  )



@web.route('/register',methods=['GET','POST'])
def register():
    try:
        if request.method == 'POST' and "register" in request.form:
            username_reg = request.form['username']
            password = request.form['password']
            PassTwo = request.form['PassTwo']
            if username_reg != '' and username_reg.__len__()>=6 and password != '' and password.__len__()>=6 and password == PassTwo:
                rows = ConnectSQL().get_register_username(username_reg)
                if rows == [] or rows == None:
                    pwd_key = AEScoder().encrypt(password)
                    ConnectSQL().write_register_sql(username_reg,pwd_key)
                    user_id = ConnectSQL().get_login_userid(username_reg)
                    Template_user().Data_html(username_reg,user_id)
                    if user_id:
                        response = make_response(redirect('/'))
                        response.set_cookie('Name', '{}'.format(username_reg), 60 * 60 * 24 * 1000)
                        response.set_cookie('ID', '{}'.format(user_id), 60 * 60 * 24 * 1000)
                        session['username'] = username_reg
                        session['userid'] = user_id
                        session.permanent = True
                        #创建用户个人文件夹
                        user_path = '{}/userinfo/{}/'.format(configPath,user_id)
                        userinfo_fold = os.path.exists(user_path)

                        if not userinfo_fold:
                            os.makedirs(user_path)
                        file = open(user_path + 'config.ini', 'w')
                        file.close()

                        template_user_path = '{}/templates/userinfo/{}'.format(configPath,user_id)
                        userinfo_fold2 = os.path.exists(template_user_path)
                        if not userinfo_fold2:
                            os.makedirs(template_user_path)

                        static_user_path = '{}/static/userinfo/{}'.format(configPath, user_id)
                        userinfo_fold3 = os.path.exists(static_user_path)
                        if not userinfo_fold3:
                            os.makedirs(static_user_path)

                        return response
                    # return render_template('index.html')
                elif rows != [] or rows != None:
                    rows_username = rows[0][0].strip()
                    return render_template('auth/register.html'  ,message = "Account already exists!")
            elif username_reg.__len__()<6 or password.__len__()<6:
                return render_template('auth/register.html'  ,message="Please make sure that the account and password are loger than 6 digits!")
            elif password != PassTwo:
                return render_template('auth/register.html'  ,message="The two passwords are inconsistent!")
            else:
                return render_template('auth/register.html'  ,message = "please enter the correct username and password!")
        else:
            return render_template('auth/register.html'  )
    except Exception as e:
        print("no value")
        raise e


# @web.route('/logout')
# def logout():
#     logger_all.info("log out~~")
#     cookies = ConnectSQL().get_cookie()
#     is_delete = 'del'
#     session.clear()
#     # session['username'] = None
#     if cookies:
#         if is_delete == 'del':
#             response = make_response(redirect('/'))
#             # response.set_cookie('Name', '', expires=0)
#             # response.set_cookie('ID', '', expires=0)
#             response.set_cookie('username', '', expires=0)
#             response.set_cookie('userid', '', expires=0)
#             response.set_cookie('token', '', expires=0)
#             print(11111)
#             return response
#     else:
#         return render_template('index.html'  )
    
@web.route('/logout')
def logout():
    logger_all.info(22222222222222222222222222222)
    cookies = request.cookies.get("session")
    is_delete = 'del'
    session.clear()
    # session['username'] = None
    if cookies:
        if is_delete == 'del':
            response = make_response(redirect('/'))
            # response.set_cookie('Name', '', expires=0)
            # response.set_cookie('ID', '', expires=0)
            response.set_cookie('username', '', expires=0)
            response.set_cookie('userid', '', expires=0)
            response.set_cookie('token', '', expires=0)
            response.set_cookie('session', '', expires=0)
            return response
    else:
        return render_template('index.html'  )    


@web.route('/personal')
def personal():
    return render_template('personal/personal_center.html'  )

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth

def prepare_flask_request(request):
    # If server is behind proxies or balancers, use the HTTP_X_FORWARDED fields
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'get_data': request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.form.copy()
    }

# @web.route('/login/callback', methods=['GET', 'POST'])
# def login_callback():
#     session_current_url = session.get('current_url', None)
#     print(555555,session_current_url)
#     req = prepare_flask_request(request)
#     auth = init_saml_auth(req)
#     auth.process_response()
#     auth.get_last_response_xml()
#     # print('Response:',auth.get_last_response_xml())
#     errors = auth.get_errors()
#     # print(111,auth.get_attributes())
#     # print(222,auth.get_session_index())
#     StaffID = auth.get_attributes()['psid'][0]
#     StaffName = auth.get_attributes()['displayname'][0]

#     if len(errors) == 0 and auth.is_authenticated():
#         session['username'] = StaffName  # Save user information in session
#         session['userid'] = StaffID
#         session['token'] = auth.get_session_index()  # Save token in session
#         session.permanent = True

#         if session_current_url:
#             response = make_response(redirect('/' + session_current_url))
#         else:
#             response = make_response(redirect('/'))

#         return response
#     else:
#         return 'Login failed'

@web.route('/login/callback', methods=['GET', 'POST'])
# @handle_exceptions
def login_callback():
    session_current_url = session.get('current_url', None)
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    auth.get_last_response_xml()
    # print('Response:',auth.get_last_response_xml())
    errors = auth.get_errors()

    match2 = re.search(
        r'<Attribute Name="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"><AttributeValue>(.*?)</AttributeValue>',
        auth.get_last_response_xml())

    logger_all.info(match2.group(1))

    if len(errors) == 0 and auth.is_authenticated():



        session['user'] = auth.get_attributes()  # Save user information in session
        session['token'] = auth.get_session_index()  # Save token in session
        session['staffid'] = 580515000
        session['username'] = session['user']['http://schemas.microsoft.com/identity/claims/displayname'][0]
        session.permanent = True
        logger_all.info(111,auth.get_attributes())

        # print('user:',auth.get_attributes())
        username = session['username']
        logger_all.info(222,username)
        token = session['token']
        staffid = session['staffid']

        logger_all.info('User {} {} logging'.format(username,staffid))

        avatarUrl = 'https://img1.baidu.com/it/u=1215581741,978897026&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=468'
        session['avatar']=avatarUrl

        # print(333,avatar)

        #查数据库是否有该用户
        rows = ConnectSQL().get_register_username(username)
        if rows == [] or rows == None:
            #将此用户录入数据库
            ConnectSQL().write_register_sql_new(username,staffid)
            id = ConnectSQL().get_login_userid(username)
            session['userid']= id
            #在/static/user_files下面创建id命名的文件夹，里面包含三个子文件夹：config,html,csv
            user_folder_path = os.path.join(app.root_path, 'static', 'user_files', str(id))

            # 检查文件夹是否存在
            if not os.path.exists(user_folder_path):
                # 创建用户文件夹及子文件夹
                os.makedirs(os.path.join(user_folder_path, 'config'))
                os.makedirs(os.path.join(user_folder_path, 'html'))
                os.makedirs(os.path.join(user_folder_path, 'csv'))

                # AliyunOSSClient().upload_file(app.root_path+'/util/oss_a','TANOS/user_files/{}/config/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/html/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/csv/oss_a'.format(str(id)))



        else:
            id = ConnectSQL().get_login_userid(username)
            session['userid'] = id

            # print(1111111,app.root_path+'/util/oss_a')
            # print(2222222, 'TANOS/user_files/{}/csv/oss_a'.format(str(id)))

            #在/static/user_files下面创建id命名的文件夹，里面包含三个子文件夹：config,html,csv
            user_folder_path = os.path.join(app.root_path, 'static', 'user_files', str(id))

            # 检查文件夹是否存在
            if not os.path.exists(user_folder_path):
                # 创建用户文件夹及子文件夹
                os.makedirs(os.path.join(user_folder_path, 'config'))
                os.makedirs(os.path.join(user_folder_path, 'html'))
                os.makedirs(os.path.join(user_folder_path, 'csv'))

                # AliyunOSSClient().upload_file(app.root_path+'/util/oss_a','TANOS/user_files/{}/config/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/html/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/csv/oss_a'.format(str(id)))




        groupname = ConnectSQL().get_user_group(username)
        print("user group:",groupname)
        session['groupname'] = groupname[0]

        current_team_list = tanos_manage().get_teams_from_user(username)
        # current_team_list = ['Admin', 'ChinaDataSolution']
        session['teams'] = current_team_list

        session['team'] = current_team_list[0]

        # 将最后登录时间写入数据库
        tanos_manage().update_login_date(id)

        # avatar = ConnectSQL().get_avatar(username)
        # session['avatar'] = avatar

        if session_current_url:
            response = make_response(redirect('/' + session_current_url))
        else:
            response = make_response(redirect('/'))
        return response
    else:
        return 'Login failed'



@web.route('/login2', methods=['GET', 'POST'])
# @handle_exceptions
def login2():
    # session_current_url = session.get('current_url', None)
    # req = prepare_flask_request(request)
    # auth = init_saml_auth(req)
    # auth.process_response()
    # auth.get_last_response_xml()
    # # print('Response:',auth.get_last_response_xml())
    # errors = auth.get_errors()
    #
    # match2 = re.search(
    #     r'<Attribute Name="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"><AttributeValue>(.*?)</AttributeValue>',
    #     auth.get_last_response_xml())
    #
    # logger_all.info(match2.group(1))

    if True:

        auth= {'http://schemas.microsoft.com/identity/claims/tenantid': ['984e1357-e1c3-4b1d-ad0c-f74666a67c87'], 'http://schemas.microsoft.com/identity/claims/objectidentifier': ['8a6d2bcf-4380-4021-8580-d162ca884fc7'], 'http://schemas.microsoft.com/identity/claims/displayname': ['wang Arrow'], 'http://schemas.microsoft.com/identity/claims/identityprovider': ['live.com'], 'http://schemas.microsoft.com/claims/authnmethodsreferences': ['urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport', 'http://schemas.microsoft.com/claims/multipleauthn', 'http://schemas.microsoft.com/ws/2008/06/identity/authenticationmethod/unspecified'], 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname': ['Arrow'], 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname': ['wang'], 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': ['Arrow.wk@hotmail.com'], 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': ['Arrow.wk_hotmail.com#EXT#@Arrowwkhotmail.onmicrosoft.com']}
        session['user'] = auth  # Save user information in session
        session['token'] = '.eJydVH9r2zAQ_SpDhfwVx5J_KgazlrUUxgaFZjAopciSHGu1JSPJ9Urpd-_ZaUY61q0dGGQ96d69ezrpAd300nZMS-1R4e0gl4jdMc8sKlDjfe-KMFTdlqwqpsSw4qYLlQ-HkkQkTSnJE7Jc55Sucxxli7orozSGwZds8GbB-r4kMV3U5eeLs_OPY5livGjKJKNoibbWDL1mnYRMp7I1biOdP59AWHSe1bUSqEgpTgmE4SXyknX7vd-ctA7tMIeKq5fop0ZpdgpVXJp28MpowE5EpzS6hhBzKzXw3FRVRqqUR0FcCR4k6zwOKkHqADNCophHcYQxBA5AioqH2Q0ww_FGdsytOsWtcab2sye8ZapzIVTd6E76xghnZS2t1FzO-garC8OccsVUsis8Ly5Pvn4pohUuGC8g3jmAL2AYjRUX1njJvRQby7TrjfWg5C0KuqH1qm_lrORfMaMLoUYa4ixUAjpA-fu5hOmXs8m4XS3hABokV7WSYrLwr6S_mJ4VCeX6lt3vTvoKjUxvP5xYa8Z3M-3nvTV38G8nulbdyWnzu8lM9QMM3qFQ10xGWSaiitdBElMcJDgiAYUGDATJIs4oTWqevzuRl5oBIKYEa5pIEqd5IAmPg6QiImAC86DOkyzLWJZz-qcEP7vWGdavjN0-n1kawvd7JtirWiaElW7uudnl1Xh73Bg_Lb3i0xvZt-C03p_iawf4Rq4XNKDw5kDh0dn3zdHxvDLe7nHoxEOT_z-zg4t40Ino-nF3w-e3Zo0xIbv588N00K2PT3w7xnk.ZbdrgA.MRHj5N1XI6NDBxF_gJq3TgY7mQU'  # Save token in session
        session['staffid'] = 580515000
        session['username'] = session['user']['http://schemas.microsoft.com/identity/claims/displayname'][0]
        session.permanent = True
        # logger_all.info(auth.get_attributes())

        # print('user:',auth.get_attributes())
        username = session['username']
        logger_all.info(username)
        token = session['token']
        staffid = session['staffid']

        logger_all.info('User {} {} logging'.format(username,staffid))

        avatarUrl = 'https://img1.baidu.com/it/u=1215581741,978897026&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=468'
        session['avatar']=avatarUrl

        # print(333,avatar)

        #查数据库是否有该用户
        rows = ConnectSQL().get_register_username(username)
        if rows == [] or rows == None:
            #将此用户录入数据库
            ConnectSQL().write_register_sql_new(username,staffid)
            id = ConnectSQL().get_login_userid(username)
            session['userid']= id
            #在/static/user_files下面创建id命名的文件夹，里面包含三个子文件夹：config,html,csv
            user_folder_path = os.path.join(app.root_path, 'static', 'user_files', str(id))

            # 检查文件夹是否存在
            if not os.path.exists(user_folder_path):
                # 创建用户文件夹及子文件夹
                os.makedirs(os.path.join(user_folder_path, 'config'))
                os.makedirs(os.path.join(user_folder_path, 'html'))
                os.makedirs(os.path.join(user_folder_path, 'csv'))

                # AliyunOSSClient().upload_file(app.root_path+'/util/oss_a','TANOS/user_files/{}/config/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/html/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/csv/oss_a'.format(str(id)))



        else:
            id = ConnectSQL().get_login_userid(username)
            session['userid'] = id

            # print(1111111,app.root_path+'/util/oss_a')
            # print(2222222, 'TANOS/user_files/{}/csv/oss_a'.format(str(id)))

            #在/static/user_files下面创建id命名的文件夹，里面包含三个子文件夹：config,html,csv
            user_folder_path = os.path.join(app.root_path, 'static', 'user_files', str(id))

            # 检查文件夹是否存在
            if not os.path.exists(user_folder_path):
                # 创建用户文件夹及子文件夹
                os.makedirs(os.path.join(user_folder_path, 'config'))
                os.makedirs(os.path.join(user_folder_path, 'html'))
                os.makedirs(os.path.join(user_folder_path, 'csv'))

                # AliyunOSSClient().upload_file(app.root_path+'/util/oss_a','TANOS/user_files/{}/config/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/html/oss_a'.format(str(id)))
                # AliyunOSSClient().upload_file(app.root_path + '/util/oss_a', 'TANOS/user_files/{}/csv/oss_a'.format(str(id)))




        groupname = ConnectSQL().get_user_group(username)
        print("user group:",groupname)
        session['groupname'] = groupname[0]

        current_team_list = tanos_manage().get_teams_from_user(username)
        # current_team_list = ['Admin', 'ChinaDataSolution']
        session['teams'] = current_team_list

        session['team'] = current_team_list[0]

        response = make_response(redirect('/'))
        return response

        # avatar = ConnectSQL().get_avatar(username)
        # session['avatar'] = avatar

        # if session_current_url:
        #     response = make_response(redirect('/' + session_current_url))
        # else:
        #     response = make_response(redirect('/'))
        # return response
    else:
        return 'Login failed'


@web.route('/login_page',methods=['GET','POST'])
def login_page():
    if request.method == 'GET':
        redirect_url = tanos_manage().get_login_para()
        return render_template('auth/login_sso.html',redirect_url=redirect_url  )

@web.route('/login',methods=['GET','POST'])
def login():
    current_url = request.args.get('currentUrl')
    if current_url:
        current_path = current_url[current_url.find('/', 8) + 1:]
        print(44444444,current_path)
        session['current_url'] = current_path
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    print(auth)
    return redirect(auth.login())  # Redirect to SSO login page
    # return render_template('index.html')

@web.route('/permission',methods=['GET','POST'])
def permission():
    return render_template("auth/permission.html")


@web.route('/update_session_team',methods=['GET','POST'])
def update_session_team():
    selected_team = request.form.get('team').strip()  # 获取前端发送的选项值
    session['team'] = selected_team
    group = tanos_manage().get_group_from_team(selected_team)
    session['groupname'] = group
    return 'Success'
