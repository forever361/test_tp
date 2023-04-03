from datetime import timedelta

from flask import render_template, session

from app.view import user
from app.application import app

app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/')
#@user.authorize
def index():
    list = session.get('username',None)
    # print (list,'1111')
    if list == None:
        return render_template("index.html", message='Hello,')
    else:
        return render_template("index.html", message='Hello %s,' % list)


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
def test_api():
    return render_template('test_api.html')