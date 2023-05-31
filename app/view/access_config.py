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



@web.route('/team/getUserList', methods=['GET'])
def getUserList():
    team_id = request.args.get('teamId')  # 获取团队ID参数
    #根据team_id从数据库中读取user
    userlist= tanos_manage().get_users_from_team(team_id)

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


@web.route('/delete_from_team', methods=['POST'])
def delete_from_team():
    data = request.get_json()
    print(data)
    # id = data['id']
    # teamid= data['team']
    # print(id)
    # print(teamid)

    # 在这里执行删除操作，从关系表中删除指定的关联关系
    # 例如：
    # DELETE FROM xcheck.user_teams WHERE id = <id>

    return jsonify({'message': 'Delete success'})


@web.route('/add_to_team', methods=['POST'])
def add_to_team():
    data = request.get_json()
    print(data)
    # id = data['id']
    # teamid= data['team']
    # print(id)
    # print(teamid)

    # 在这里执行删除操作，从关系表中删除指定的关联关系
    # 例如：
    # DELETE FROM xcheck.user_teams WHERE id = <id>

    return jsonify({'message': 'Add success'})




