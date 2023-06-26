import json
import math

from flask import Blueprint, render_template, session, request, jsonify, redirect

from app.db.tanos_manage import tanos_manage
from app.useDB import ConnectSQL
from app.view import user

web = Blueprint("access_config", __name__)


@web.route('/access', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def access_page():
    username = session.get('username', None)

    current_team_list = tanos_manage().get_teams_from_user(username)
    # current_team_list = ['Admin', 'ChinaDataSolution']
    session['teams'] = current_team_list

    if len(current_team_list) == 1:
        team = current_team_list[0]
        session['team'] = team
    else:
        team = session.get('team', {})

    group = tanos_manage().get_group_from_team(team)
    session['groupname'] = group
    teams = []

    # 通过用户名获取是否为owner
    is_owner = tanos_manage().if_owner(username, team)
    # is_owner = {'DelosUsers': 0, 'ChinaDataSolution': 0}

    if "Admin" == team:
        teams_list = tanos_manage().get_teams()

        for team_data in teams_list:
            team = {"id": team_data[0], "name": team_data[1].strip()}
            teams.append(team)
        return render_template('access/access_config.html', teams=teams)
    else:
        if is_owner:
            teams_list = tanos_manage().get_teams_owner(team)

            for team_data in teams_list:
                team = {"id": team_data[0], "name": team_data[1].strip()}
                teams.append(team)
            return render_template('access/access_config.html', teams=teams)
        else:
            return render_template('access/access_config_normal.html', teams=teams)


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
    current_team_list = tanos_manage().get_teams_from_user(data['username'])
    # current_team_list = ['Admin', 'ChinaDataSolution']
    session['teams'] = current_team_list

    groupname = ConnectSQL().get_user_group(data['username'])
    session['groupname'] = groupname[0]

    return "OK"


@web.route('/team/getUserList', methods=['GET'])
def getUserList():
    team_id = request.args.get('teamId')  # 获取团队ID参数
    # 根据team_id从数据库中读取user
    userlist = tanos_manage().get_users_from_team(team_id)

    team_users = []
    for row in userlist:
        staffid = row[1]
        name = row[0].strip()
        owner = row[2]
        is_owner = 'yes' if owner == 1 else 'no'  # 根据条件设置 is_owner 的值
        user = {'staffid': staffid, 'name': name, "is_owner": is_owner}
        team_users.append(user)

    return jsonify(team_users)


@web.route('/team/getAllUsers.json', methods=['GET'])
def getAllUsers():
    userlist = tanos_manage().get_all_user()
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
    teamid = data['team']
    print(staffid)
    print(teamid)

    # 在这里执行删除操作，从关系表中删除指定的关联关系
    tanos_manage().delete_user_from_team(teamid, staffid)

    # 查找是否在至少一个team,如果在,不做任何事，如果不在，默认加入guest team
    t = tanos_manage().search_user_in_team(staffid)
    if t is False:
        tanos_manage().add_user_to_team(3001, staffid)

    return jsonify({'message': 'Delete success'})


@web.route('/add_to_team', methods=['POST'])
def add_to_team():
    data = request.get_json()
    print(data)
    staffid = data['id']
    teamid = data['team']

    tanos_manage().add_user_to_team(teamid, staffid)

    # 查找是否在guest team,如果在，删除

    t = tanos_manage().search_user_in_guest(staffid)
    if t:
        tanos_manage().delete_user_from_team(3001, staffid)

    return jsonify({'message': 'Add success'})


@web.route('/team/updateOwnerInfo', methods=['POST'])
def update_owner_info():
    data = request.get_json()
    # 根据具体的业务逻辑，更新 teams 字典中对应 teamId 的 owner 状态
    staffId = data['staffId']
    teamId = data['team']
    isChecked = 1 if data['isChecked'] else 0

    tanos_manage().update_owner_info(staffId, teamId, isChecked)

    # 假设更新成功后，返回一个成功的响应
    response = {'message': 'Owner information updated successfully'}
    return jsonify(response), 200


@web.route('/role_config', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def role_config():
    username = session.get('username', None)

    current_team_list = tanos_manage().get_teams_from_user(username)
    # current_team_list = ['Admin', 'ChinaDataSolution']
    session['teams'] = current_team_list

    if len(current_team_list) == 1:
        team = current_team_list[0]
        session['team'] = team
    else:
        team = session.get('team', {})

    group = tanos_manage().get_group_from_team(team)
    session['groupname'] = group
    teams = []

    # 通过用户名获取是否为owner
    # is_owner = tanos_manage().if_owner(username,team)
    # is_owner = {'DelosUsers': 0, 'ChinaDataSolution': 0}

    if "Admin" == team:
        teams_list = tanos_manage().get_teams()

        for team_data in teams_list:
            team = {"id": team_data[0], "name": team_data[1].strip()}
            teams.append(team)
        return render_template('/access/role_config.html', teams=teams)
    else:
        return redirect("/permission")


@web.route('/team/getAllRole.json', methods=['GET'])
def getAllRole():

    result = tanos_manage().get_all_role_calue()
    print(result)
    data2 = []
    for team, values in result:
        value_list = values.strip().split("|")
        data_dict = {
            "team": team.strip(),
            "data_connection": value_list[0],
            "data_point": value_list[1],
            "data_validation": value_list[2],
            "web_test": value_list[3],
            "api_test_system": value_list[4],
            "api_test_smoke": value_list[5],
            "api_test_sanity": value_list[6],
            "api_test_health": value_list[7],
            "api_test_null": value_list[8],
            "tools": value_list[9],
            "config": value_list[10],
        }
        data2.append(data_dict)

    # print(data2)


    data = [{
        "team": 'Admin',
        "data_connection": '11',
        "data_point": '11',
        "data_validation": "11",
        "api_test_system": "11",
        "api_test_smoke": "11",
        "api_test_sanity": "11",
        "api_test_health": "11",
        "api_test_null": "11",
        "web_test": "11",
        "tools": '11',
        "config": '11',
    }, {
        "team": 'Guest',
        "data_connection": '10',
        "data_point": '10',
        "data_validation": "10",
        "api_test_system": "10",
        "api_test_smoke": "10",
        "api_test_sanity": "10",
        "api_test_health": "10",
        "api_test_null": "10",
        "web_test": "10",
        "tools": '00',
        "config": '00',
    },
        {
            "team": 'DelosUsers',
            "data_connection": '11',
            "data_point": '11',
            "data_validation": "00",
            "api_test_system": "11",
            "api_test_smoke": "00",
            "api_test_sanity": "00",
            "api_test_health": "00",
            "api_test_null": "00",
            "web_test": "00",
            "tools": '00',
            "config": '00',
        },
        {
            "team": 'ChinaDataSolution',
            "data_connection": '01',
            "data_point": '00',
            "data_validation": "00",
            "api_test_system": "00",
            "api_test_smoke": "00",
            "api_test_sanity": "00",
            "api_test_health": "00",
            "api_test_null": "00",
            "web_test": "11",
            "tools": '00',
            "config": '00',
        },

    ]

    return jsonify(data2)


@web.route('/team/saveRole.json', methods=['POST'])
def saveRole():
    data = request.get_json()
    data_str = []

    for item in data:
        first_column = item['firstColumnValue']
        group_str = ''
        for index in range(1, 12):  # 11个复选框，索引从1到11
            checkbox_r = item[f'checkbox{index}_r']
            checkbox_w = item[f'checkbox{index}_w']
            if checkbox_r and checkbox_w:
                group_str += '11'  # 保存为11
            elif checkbox_r and not checkbox_w:
                group_str += '10'  # 保存为10
            elif not checkbox_r and checkbox_w:
                group_str += '01'  # 保存为01
            else:
                group_str += '00'  # 保存为00
        data_str.append((first_column, group_str))


    converted_data = convert_data_format(data_str)

    tanos_manage().save_role_value(converted_data)
    return jsonify('save data')





def convert_data_format(data):
    converted_data = []
    for item in data:
        name = item[0]
        role_value = item[1]

        # 将字符串的每两个字符分组并用竖线连接
        role_value_formatted = '|'.join([role_value[i:i+2] for i in range(0, len(role_value), 2)])

        converted_data.append((name, role_value_formatted))

    return converted_data

