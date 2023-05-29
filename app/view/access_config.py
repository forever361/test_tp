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
    teams_list=  tanos_manage().get_teams()
    teams = []
    for team_data in teams_list:
        team = {"id": team_data[0], "name": team_data[1].strip()}
        teams.append(team)
    return render_template('access_config.html',username=username,team=team,teams=teams)

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
]

all_users = [
    {'id': 4, 'name': 'User 4'},
    {'id': 5, 'name': 'User 5'},
    {'id': 6, 'name': 'User 6'}
]

@web.route('/team/getUserList', methods=['GET'])
def getUserList():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=6, type=int)

    # 在此处可以进行相应的逻辑处理，例如从数据库获取用户列表数据
    # 假设从数据库或其他数据源获取了 team_users 列表数据

    # 获取当前页的用户数据
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    users = team_users[start_index:end_index]

    # 计算总页数
    total_pages = math.ceil(len(team_users) / per_page)

    response = {
        'users': users,
        'totalPages': total_pages
    }

    return jsonify(response)

@web.route('/team/getAllUsers', methods=['GET'])
def getAllUsers():
    # 在此处可以进行相应的逻辑处理，例如从数据库获取所有用户列表数据

    # 假设从数据库或其他数据源获取了 all_users 列表数据
    response = {'users': all_users}

    return jsonify(response)