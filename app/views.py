import os
from datetime import timedelta

from flask import render_template, session, request, redirect, send_file
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from app.util import global_manager
from app.view import user
from app.application import app

app.send_file_max_age_default = timedelta(seconds=1)
from app.useDB import ConnectSQL

# @app.route('/')
# #@user.authorize
# def index():
#     list = session.get('username',None)
#     # print (list,'1111')
#     if list == None:
#         return render_template("index.html", message='Hello,')
#     else:
#         return render_template("index.html", message='Hello %s,' % list)

@app.route('/')
#@user.authorize
def index():
    list = session.get('user',None)

    # print (list,'1111')

    if list == None:
        return render_template("index.html", message='Hello,')
    else:
        user = session['user']
        email = user.get('http://schemas.microsoft.com/identity/claims/displayname', [''])[0]
        # groupname = ConnectSQL().get_user_group(email)
        # print("user group:",groupname)
        # session['groupname'] = groupname[0]

        return render_template("index.html", message='Hi, %s' % email)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if 'token' in session:
#         print('已经有token')
#         username = session.get('username', None)
#         token = session['token']
#         print('old',username)
#         return render_template("index.html", message='Hello %s,' % username)
#     else:
#         print('获取新token')
#         req = prepare_flask_request(request)
#         auth = init_saml_auth(req)
#         return redirect(auth.login())  # Redirect to SSO login page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('util/404.html',message='Sorry, page not found!'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('util/500.html',message='Something is wrong, please retry !'), 500


def getInfoAttribute(info,field):
    try:
        value = info.get(field)
    except:
        value = ''
    if value == None:
        value = ''
    return value


@app.route('/test_webui')
def test_webui():
    return render_template('test_webui.html')


def is_authenticated(token):
    return token == '7758521'
#http://127.0.0.1:8889/logfile?s=7758521 只有知道token才能访问
@app.route('/logfile')
def logfile():
    s = request.args.get('s')
    if not s or not is_authenticated(s):
        return "Authentication failed. Access denied.", 403
    LOG_PATH_NEW = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    log_file_path = LOG_PATH_NEW+'/Log/tanos.log'
    return send_file(log_file_path, as_attachment=True)