# -*- coding: utf-8 -*-
__author__= "Sen"
__version__= "1.0"


import os
import sys
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
personalcenter_Path = os.path.join(basepath + "/templates/personal/")
# print(personalcenter_Path)
sys.path.append(basepath)
import time
from flask import request
from useDB import ConnectSQL


class Template_user(object):

    def __init__(self):
        pass
        # self.username = request.form.get('username')
        # self.user_id = ConnectSQL.get_login_userid(self.username)
        # self.username = 'senquan'
        # self.user_id = '123456'
        self.login_date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    html_tmp = """<!DOCTYPE html>
    <html LANG="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                content="width=divice-width,user-scalable=no,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0">
            <meta http-equiv="X-UA-Compatible", content="ie=edge"/>
            <title>User login</title>
            <link type="text/css" rel="stylesheet" href="../static/personal_center.css">
        </head>
        <body>
        <div class="row">
            %(timesheet)s
        </div>
        </body>
    </html>"""

    timesheet = """<div style="margin-top:150px;" class="col-md-6 col-md-offset-3">
                <div class="row">
                    <div class="col-md-2">
                        <a onclick="window.history.go(-1)" href="#">Back</a>
                    </div>
                </div>
                <div class="bg-container">
                    <div class="row">
                        <div class="col-md-4 col-md-offset-4 text-center">
                            <span class="big-title">%(username)s</span>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8 col-md-offset-2 flex-vertical text-center">
                        <div id="username" class="username">%(username)s</div>
                        <div id="user_id" class="user_id">%(user_id)s</div>
                        <div id="login_date" class="login_date">%(login_date)s</div>
                    </div>
                </div>
            </div>"""

    def timesheet_page(self,username,user_id):
        report = Template_user.timesheet % dict(
            username=username,
            user_id=user_id,
            login_date=self.login_date
        )
        return report

    def Data_html(self,username,user_id):
        timesheet = Template_user.timesheet_page(self, username, user_id)
        with open(personalcenter_Path+'personal_center.html','w',encoding="utf-8") as f:
            f.write(Template_user.html_tmp % {'username':username, 'user_id':user_id, 'login_date':self.login_date,'timesheet':timesheet})
            f.close()


if __name__ == '__main__':
    write = Template_user()
    # write.Data_html('senquan','123456')