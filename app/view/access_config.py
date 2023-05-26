from flask import Blueprint, render_template, session, request

from app.db.tanos_manage import tanos_manage
from app.useDB import ConnectSQL
from app.view import user

web = Blueprint("access_config", __name__)

@web.route('/access', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def access_page():
    username = session.get('username', None)
    team = session.get('team', None)
    return render_template('access_config.html',username=username,team=team)

@web.route('/save_permissions', methods=[ 'POST'])
def save_permission():
    data = request.json
    print(1111, data)
    if data['permissions']== ['DELOS_User']:
        teamid = '{3002}'
    elif data['permissions']== ['Admin']:
        teamid = '{3000}'
    elif data['permissions']== ['China_Data_Solution']:
        teamid = '{3003}'
    else:
        teamid = '{3001}'
    print(teamid)
    tanos_manage().update_team(data['username'],teamid)
    team = ConnectSQL().get_team(data['username'])
    session['team'] = team

    groupname = ConnectSQL().get_user_group(data['username'])
    session['groupname'] = groupname[0]

    return "OK"