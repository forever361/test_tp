import json
import math

from flask import Blueprint, render_template, session, request, jsonify

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
    teams_list = tanos_manage().get_teams()
    teams = []
    for team_data in teams_list:
        team = {"id": team_data[0], "name": team_data[1].strip()}
        teams.append(team)
    return render_template('access_config.html', username=username, team=team, teams=teams)


@web.route('/save_permissions', methods=['POST'])
def save_permission():
    data = request.json
    print(1111, data)
    if data['permissions'] == ['DELOS_User']:
        teamid = '{3002}'
    elif data['permissions'] == ['Admin']:
        teamid = '{3000}'
    elif data['permissions'] == ['China_Data_Solution']:
        teamid = '{3003}'
    else:
        teamid = '{3001}'
    print(teamid)
    tanos_manage().update_team(data['username'], teamid)
    team = ConnectSQL().get_team(data['username'])
    session['team'] = team

    groupname = ConnectSQL().get_user_group(data['username'])
    session['groupname'] = groupname[0]

    return "OK"


# 示例用户数据
team_users = [
    {'id': 1, 'name': 'User 1'},
    {'id': 2, 'name': 'User 2'},
    {'id': 3, 'name': 'User 3'},
    {'id': 3, 'name': 'User 3'},
    {'id': 3, 'name': 'User 3'},
    {'id': 3, 'name': 'User 3'},
    {'id': 9, 'name': 'User 3'},
    {'id': 10, 'name': 'User 3'},
    {'id': 3, 'name': 'User 3'},
    {'id': 9, 'name': 'User 3'},
    {'id': 10, 'name': 'User 3'},
    {'id': 3, 'name': 'User 3'},
    {'id': 9, 'name': 'User 3'},
    {'id': 10, 'name': 'User 3'},
    {'id': 3, 'name': 'User 3'},
    {'id': 9, 'name': 'User 3'},
    {'id': 10, 'name': 'User 3'},
    {'id': 3, 'name': 'User 3'},
    {'id': 9, 'name': 'User 3'},
    {'id': 10, 'name': 'User 3'},
]

all_users = [
    {'id': 100, 'name': 'User 4'},
    {'id': 200, 'name': 'User 5'},
    {'id': 300, 'name': 'User 6'}
]


@web.route('/team/getUserList', methods=['GET'])
def getUserList():
    team_id = request.args.get('teamId')  # 获取团队ID参数
    #根据team_id从数据库中读取user
    userlist= tanos_manage().get_user_from_team(team_id)

    team_users = []
    for row in userlist:
        staffid = row[1]
        name = row[0].strip()
        user = {'staffid': staffid, 'name': name}
        team_users.append(user)

    return jsonify(team_users)


@web.route('/team/getAllUsers.json', methods=['GET'])
def getAllUsers():
    userlist= tanos_manage().get_all_user()
    all_users = []
    for row in userlist:
        staffid = row[1]
        name = row[0].strip()
        user = {'staffid': staffid, 'name': name}
        all_users.append(user)

    return jsonify(all_users)


