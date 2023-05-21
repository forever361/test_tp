from datetime import timedelta

from flask import render_template, session, request,redirect
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from app.view import user
from app.application import app

app.send_file_max_age_default = timedelta(seconds=1)

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
        email = user.get('http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress', [''])[0]
        # print(email)
        return render_template("index.html", message='Hello %s,' % email)

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


@app.route('/test_api')
@user.authorize
def test_api():

    return render_template('test_api.html')


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