from functools import wraps

from datetime import timedelta
from shutil import copy
from flask import Blueprint,render_template,request,redirect,make_response,session
import os
import sys

from app.common.libs.Helper import ops_render, ops_rederErrJSON, ops_rederJSON
from app.util.IP_PORT import Constant
from app.util.log_util.all_new_log import logger_all

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(configPath)

from app.util.crypto_ECB import AEScoder
from app.useDB import ConnectSQL
from app.personal_center import Template_user


web = Blueprint("user", __name__)

web.send_file_max_age_default = timedelta(seconds=1)


#设置登录认证
def authorize(fn):
    @wraps(fn)
    def wrapper():
        user = session.get('username',None)
        if user:
            # 判断文件是否存在，copyexcel到个人目录
            # user_id = session.get('userid', None)
            user_id = session.get('userid', None)
            # print ("我已经登录~~~~~~",user_id)
            user_path = '{}/static/userinfo/{}/'.format(configPath, user_id)
            # if os.path.exists(user_path+'info.ini')==False:
            #     os.makedirs(user_path+'info.ini')
            # s_file_excel = '{}/static/verification_result.xlsx'.format(configPath)
            # t_file_excel = user_path + '/verification_result.xlsx'
            # userinfo_fold = os.path.exists(user_path)
            # t_file_excel_fold = os.path.exists(t_file_excel)
            # if userinfo_fold and not t_file_excel_fold:
            #     copy(s_file_excel, user_path)
            # log.log().logger.info("已登录")
            return fn()
        else:
            # log.log().logger.info("未登录")
            return render_template("auth/login.html"  )
    return wrapper
    # def wrapper():
    #     user = session.get('username',None)
    #     if user:
    #         return fn()
    #     else:
    #         return render_template("auth/login.html"  )
    # return wrapper


@web.route('/login',methods=['GET','POST'])
def login():
    if "Login" in request.form:
        username_login = request.form.get("login_name")
        password_login = request.form.get("login_pwd")
        if username_login and password_login:
            rows = ConnectSQL().get_register_username(username_login)
            if rows == [] or rows == None:
                return render_template('auth/login.html'  , message='Please enter the correct username and password!')
            elif rows != [] or rows != None:
                rows_username = rows[0][0].strip()
                if rows_username != '' and rows_username != None and rows_username == username_login:
                    password_old = ConnectSQL().get_password(username_login)
                    password_key_login = AEScoder().decrypt('{}'.format(password_old))
                    if password_login == password_key_login:
                        user_id = ConnectSQL().get_login_userid(username_login)
                        Template_user().Data_html(username_login,user_id)
                        if user_id:
                            response = make_response(redirect('/'))
                            response.set_cookie('Name', '{}'.format(rows_username),60*60*24*1000)
                            response.set_cookie('ID', '{}'.format(user_id), 60 * 60 * 24 * 1000)
                            session['username'] = rows_username
                            session['userid'] = user_id
                            session.permanent = True
                            return response
                        # return render_template('index.html')
                    else:
                        return render_template('auth/login.html'  ,message='Please enter the correct username and password!')
            else:
                return render_template('auth/login.html'  ,message='Please enter the correct username and password!')
        else:
            return render_template('auth/login.html'  )
    else:
        return render_template('auth/login.html'  )
    return render_template('auth/login.html'  )



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


@web.route('/logout')
def logout():
    logger_all.info("log out~~")
    cookies = ConnectSQL().get_cookie()
    is_delete = 'del'
    session.clear()
    # session['username'] = None
    if cookies:
        if is_delete == 'del':
            response = make_response(redirect('/'))
            response.set_cookie('Name', '', expires=0)
            response.set_cookie('ID', '', expires=0)
            return response
        # return render_template('index.html')
    else:
        return render_template('index.html'  )


@web.route('/personal')
def personal():
    return render_template('personal/personal_center.html'  )


