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
    # session['team'] = "Admin"
    team = session.get('team', None)
    teams = []
    #通过用户名获取是否为owner

    is_owner = tanos_manage().if_owner(username,team)
    if team=="Admin":
        teams_list = tanos_manage().get_teams()

        for team_data in teams_list:
            team = {"id": team_data[0], "name": team_data[1].strip()}
            teams.append(team)
        return render_template('access_config.html', username=username, team=team, teams=teams)
    elif is_owner==1:
        teams_list = tanos_manage().get_teams_owner(team)

        for team_data in teams_list:
            team = {"id": team_data[0], "name": team_data[1].strip()}
            teams.append(team)
        return render_template('access_config.html', username=username, team=team, teams=teams)
    else:
        return render_template('access_config_normal.html', username=username, team=team, teams=teams)


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
        owner = row[2]
        is_owner = 'yes' if owner == 1 else 'no'  # 根据条件设置 is_owner 的值
        user = {'staffid': staffid, 'name': name,"is_owner":is_owner}
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
    staffid = data['id']
    teamid= data['team']
    print(staffid)
    print(teamid)

    # 在这里执行删除操作，从关系表中删除指定的关联关系
    tanos_manage().delete_user_from_team(teamid, staffid)

    return jsonify({'message': 'Delete success'})


@web.route('/add_to_team', methods=['POST'])
def add_to_team():
    data = request.get_json()
    print(data)
    staffid = data['id']
    teamid= data['team']

    tanos_manage().add_user_to_team(teamid, staffid)

    current_user = tanos_manage().get_username_from_staffid(staffid)
    username = session.get('username', None)
    if  username == current_user:
        team = ConnectSQL().get_team_from_teamid(teamid)
        print(1111,team)
        session['team'] = team

        groupname = ConnectSQL().get_user_group(current_user)
        session['groupname'] = groupname[0]

    return jsonify({'message': 'Add success'})




