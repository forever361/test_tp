import json
import os
import re
import sys
import time
from datetime import datetime

from flask import session

from app import useDB
from app.util.log import logg

from app.util.crypto_ECB import AEScoder

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
sys.path.append(configPath)

from app.useDB import ConnectSQL


class tanos_manage():
    def __init__(self):
        self.status = 0
        self.name = ''

    def new_connection(self, connect_name, dbtype, connect_type, host, dblibrary, username, pwd, port):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.connection_management (user_id,connect_name,dbtype,connect_type,host,dblibrary,username,pwd,port,create_date)\
        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""" \
            .format(user_id, connect_name.strip(), dbtype.strip(), connect_type.strip(), host.strip(),
                    dblibrary.strip(), username.strip(), pwd.strip(), port.strip(), create_date)
        useDB.useDB().executesql(sql)

    def update_connection(self, connect_id, connect_name, dbtype, connect_type, host, dblibrary, username, pwd, port):
        sql = "UPDATE tanos.connection_management set connect_name='{}',dbtype='{}',connect_type='{}',host='{}',dblibrary='{}',username='{}',pwd='{}', port='{}' WHERE connect_id = {};".format(
            connect_name, dbtype, connect_type, host, dblibrary, username, pwd, port, connect_id)
        useDB.useDB().executesql(sql)

    def delete_connection(self, id):
        sql = "DELETE FROM tanos.connection_management WHERE connect_id = {};".format(id)
        useDB.useDB().executesql(sql)

    def show_connections(self):
        user_id = session.get('userid', None)
        sql = """select connect_id,connect_name,dbtype,connect_type,host,dblibrary,username,pwd,port from tanos.connection_management where user_id= '{}'  """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def search_connections_id(self, connect_id):
        user_id = session.get('userid', None)
        sql = """select dbtype,connect_type,host,dblibrary,username,pwd,port from tanos.connection_management where user_id= '{}' and connect_id='{}'  """ \
            .format(user_id, connect_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def get_connections_id_by_name(self,connect_name):
        sql = """select connect_id from tanos.connection_management where connect_name ='{}'  """.format(connect_name)
        result = useDB.useDB().executesql_fetch(sql)
        connect_id = str(result[0][0]).strip()
        return connect_id



    def search_point_id(self, connect_id):
        user_id = session.get('userid', None)
        sql = """select point_name,connect_id,_table_name from tanos.point_management where user_id= '{}' and point_id='{}'  """ \
            .format(user_id, connect_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def new_point(self, point_name, connect_name, table_name):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        connect_id = self.search_by_connect_name(connect_name)
        sql = """INSERT INTO tanos.point_management (user_id,point_name,connect_id,_table_name,create_date)\
        VALUES ('{}','{}','{}','{}','{}')""" \
            .format(user_id, point_name.strip(), connect_id, table_name.strip(), create_date)
        useDB.useDB().executesql(sql)

    def new_point2(self, point_name, connect_id, table_name):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.point_management (user_id,point_name,connect_id,_table_name,create_date)\
        VALUES ('{}','{}','{}','{}','{}')""" \
            .format(user_id, point_name.strip(), connect_id, table_name.strip(), create_date)
        useDB.useDB().executesql(sql)

    def search_by_connect_name(self, connect_name):
        sql = """select connect_id from tanos.connection_management where connect_name ='{}'  """.format(connect_name)
        result = useDB.useDB().executesql_fetch(sql)
        id = int(str(result[0][0]).strip())
        return id

    def search_by_connect_id(self, connect_id):
        sql = """select connect_name from tanos.connection_management where connect_id ={}  """.format(connect_id)
        result = useDB.useDB().executesql_fetch(sql)
        name = result[0][0].strip()
        return name

    def search_all_by_connect_id(self, connect_id):
        sql = """select connect_id,connect_name,dbtype,connect_type,host,dblibrary,username,pwd,"port" from tanos.connection_management where connect_id ={}""".format(connect_id)
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def show_points(self):
        user_id = session.get('userid', None)
        # sql = """select point_id,point_name,connect_id,_table_name from tanos.point_management where user_id= '{}'  """ \
        #     .format(user_id)

        sql = """select A.point_id,A.point_name,B.connect_name,A._table_name from tanos.point_management  A
                    left join tanos.connection_management B
                    on A.connect_id = B.connect_id
                    where A.user_id= {}
                    """.format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def delete_point(self, id):
        sql = "DELETE FROM tanos.point_management WHERE point_id = {};".format(id)
        useDB.useDB().executesql(sql)

    def update_point(self, point_id, point_name, connect_name, _table_name):
        connect_id = self.search_by_connect_name(connect_name)
        sql = "UPDATE tanos.point_management set point_name='{}',connect_id='{}',_table_name='{}' WHERE point_id = {};".format(
            point_name, connect_id, _table_name, point_id)
        useDB.useDB().executesql(sql)

    def get_myConnections(self):
        user_id = session.get('userid', None)
        sql = """select connect_name from tanos.connection_management where user_id ={}   """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def show_jobs(self,case_id):
        user_id = session.get('userid', None)
        sql = """select case_id,job_id,job_name,job from tanos.job_management where user_id= '{}' and case_id={} order by create_date DESC""" \
            .format(user_id,case_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result


    def get_myPoints(self):
        user_id = session.get('userid', None)
        sql = """select point_name from tanos.point_management where user_id ={}   """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def new_job(self, job_name, job, case_id):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.job_management (job_name,job,user_id,create_date,case_id)\
          VALUES ('{}','{}','{}','{}',{})""" \
            .format(job_name.strip(), job,user_id, create_date,case_id)
        useDB.useDB().executesql(sql)


    def delete_job(self, id):
        sql = "DELETE FROM tanos.job_management WHERE job_id = {};".format(id)
        useDB.useDB().executesql(sql)


    # def update_job(self, job_id, job_name, job):
    #     sql = "UPDATE tanos.job_management set job_name='{}',job='{}' WHERE job_id = {};".format(
    #         job_name.strip(), job, job_id)
    #     useDB.useDB().executesql(sql)

    def update_job(self, job_id, job_name, job):
        sql = "UPDATE tanos.job_management SET job_name = %s, job = %s WHERE job_id = %s;"
        params = (job_name.strip(), job, job_id)
        useDB.useDB().executesqlP(sql, params)


    def get_connectid_by_point_name(self, point_name):
        sql = """select connect_id from tanos.point_management where point_name ='{}'  """.format(point_name)
        result = useDB.useDB().executesql_fetch(sql)
        connect_id = int(str(result[0][0]).strip())
        return connect_id

    def get_tablename_by_point_name(self, point_name):
        sql = """select _table_name from tanos.point_management where point_name ='{}'  """.format(point_name)
        result = useDB.useDB().executesql_fetch(sql)
        table_name = str(result[0][0]).strip()
        return table_name

    # def update_team(self, username, team):
    #     sql = """UPDATE tanos.user
    #             set team_ids='{}'
    #             WHERE username = '{}' """.format(
    #          team,username.strip())
    #     useDB.useDB().executesql(sql)

    def update_team(self, username, team):
        sql = """
            UPDATE tanos.user_teams
            SET teamid = %s
            WHERE userid IN (
                SELECT user_id
                FROM tanos.user
                WHERE username = %s
            )
        """
        useDB.useDB().executesql(sql, (team, username.strip()))

    def get_teams(self):
        sql = """select * from tanos.team  """
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    # def get_teams_owner(self, teams):
    #     placeholders = ', '.join(["'{}'".format(team) for team in teams])
    #     sql = "SELECT * FROM tanos.team WHERE name IN ({})".format(placeholders)
    #     result = useDB.useDB().executesql_fetch(sql)
    #     return result

    def get_teams_owner(self,team):
        sql = """select * from tanos.team where name='{}' """.format(team)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    # def get_user_from_team(self, team):
    #     if team is None:
    #         return []  # 返回空结果集或采取其他处理方式
    #     sql = "SELECT username, staffid FROM tanos.user WHERE '{}' = ANY (team_ids)".format(team)
    #     result = useDB.useDB().executesql_fetch(sql)
    #     return result

    def get_users_from_team(self, team_id):
        sql = """
            SELECT u.username, u.staffid,t.is_owner
            FROM tanos.user u
            JOIN tanos.user_teams t ON u.user_id = t.userid
            WHERE t.teamid = {}
        """.format(team_id)
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def get_all_user(self):
        sql = "SELECT username, staffid, latest_login_date,user_id FROM tanos.user "
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def delete_user_from_team(self,team_id, staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM tanos.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            # 在数据库中删除用户与团队的关联关系
            delete_sql = "DELETE FROM tanos.user_teams WHERE teamid = {} AND userid = {}".format(team_id, user_id)
            useDB.useDB().executesql(delete_sql)
            return True  # 返回删除成功的标识，可以根据需要返回其他信息
        else:
            return False  # 如果找不到对应的用户，返回删除失败的标识

    def add_user_to_team(self,team_id, staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM tanos.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            # 在数据库中插入用户与团队的关联关系
            add_sql = "INSERT INTO tanos.user_teams (teamid, userid) VALUES ({}, {})".format(team_id, user_id)
            useDB.useDB().executesql(add_sql)
            return True  # 返回添加成功的标识，可以根据需要返回其他信息
        else:
            return False  # 如果找不到对应的用户，返回添加失败的标识


    def get_username_from_staffid(self,staffid):
        team_query = """
            SELECT u.username
            FROM tanos.user u
            WHERE u.staffid = '{}'
        """.format(staffid)
        rows = useDB.useDB().executesql_fetch(team_query)
        user = rows[0][0].rstrip() if rows else None
        return user


    def if_owner(self,name,team):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM tanos.user WHERE username = '{}'".format(name)
        result = useDB.useDB().executesql_fetch(sql)

        sql = "SELECT team_id FROM tanos.team WHERE name = '{}'".format(team)
        team_id = useDB.useDB().executesql_fetch(sql)

        if result:
            user_id = result[0][0]
            team_id= team_id[0][0]
            team_sql = "SELECT is_owner from tanos.user_teams where userid= '{}' and teamid='{}'".format(user_id,team_id)
            rows = useDB.useDB().executesql_fetch(team_sql)
            is_owner = rows[0][0] if rows else None
            return is_owner  # 返回添加成功的标识，可以根据需要返回其他信息
    # def if_owner(self, name, teams):
    #     # 根据用户名查询对应的用户ID
    #     sql = "SELECT user_id FROM tanos.user WHERE username = '{}'".format(name)
    #     result = useDB.useDB().executesql_fetch(sql)
    #
    #     owners = {}  # 存储每个团队的所有者信息
    #
    #     if result:
    #         user_id = result[0][0]
    #
    #         for team in teams:
    #             # 查询团队ID
    #             sql = "SELECT team_id FROM tanos.team WHERE name = '{}'".format(team)
    #             team_id = useDB.useDB().executesql_fetch(sql)
    #
    #             if team_id:
    #                 team_id = team_id[0][0]
    #                 team_sql = "SELECT is_owner FROM tanos.user_teams WHERE userid = '{}' AND teamid = '{}'".format(
    #                     user_id, team_id)
    #                 rows = useDB.useDB().executesql_fetch(team_sql)
    #                 is_owner = rows[0][0] if rows else None
    #                 owners[team] = is_owner
    #
    #     return owners

    # def get_team_from_user(self, username):
    #     sql = "SELECT user_id FROM tanos.user WHERE username = '{}'".format(username)
    #     result = useDB.useDB().executesql_fetch(sql)
    #
    #     if result:
    #         user_id = result[0][0]
    #         sql = """
    #             SELECT t.teamid
    #             FROM tanos.user_teams t
    #             WHERE t.userid = {}
    #         """.format(user_id)
    #         result = useDB.useDB().executesql_fetch(sql)
    #         if result:
    #             teamid = result[0][0]
    #             sql = "SELECT name FROM tanos.team WHERE team_id = '{}'".format(teamid)
    #             rows = useDB.useDB().executesql_fetch(sql)
    #             team = rows[0][0].strip() if rows else None
    #             return team  # 返回添加成功的标识，可以根据需要返回其他信息

    def get_teams_from_user(self, username):
        sql = "SELECT user_id FROM tanos.user WHERE username = '{}'".format(username)
        result = useDB.useDB().executesql_fetch(sql)

        if result:
            user_id = result[0][0]
            sql = """
                SELECT t.teamid
                FROM tanos.user_teams t
                WHERE t.userid = {}
            """.format(user_id)
            result = useDB.useDB().executesql_fetch(sql)
            teams = []
            for row in result:
                team_id = row[0]
                sql = "SELECT name FROM tanos.team WHERE team_id = '{}'".format(team_id)
                print(sql)
                rows = useDB.useDB().executesql_fetch(sql)
                team = rows[0][0].strip() if rows else None
                teams.append(team)
            return teams
        return []

    def search_user_in_team(self,staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM tanos.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            s_sql = "SELECT * from tanos.user_teams WHERE userid = {}".format(user_id)
            rows= useDB.useDB().executesql_fetch(s_sql)
            if rows:
                return True  # 返回删除成功的标识，可以根据需要返回其他信息
            else:
                return False  # 如果找不到对应的用户，返回删除失败的标识

    def search_user_in_guest(self, staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM tanos.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            s_sql = "SELECT * FROM tanos.user_teams WHERE userid = {} AND teamid = 3001".format(user_id)
            rows = useDB.useDB().executesql_fetch(s_sql)
            if rows:
                return True
            else:
                return False  # 如果找不到对应的用户，返回删除失败的标识

    def update_owner_info(self,staff_id, teamId, isChecked):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM tanos.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            update_sql = """UPDATE tanos.user_teams SET is_owner = {} WHERE userid = {} AND teamid = {}""".format(isChecked,user_id,teamId)
            rows= useDB.useDB().executesql(update_sql)
            if rows:
                return True  # 返回删除成功的标识，可以根据需要返回其他信息
            else:
                return False  # 如果找不到对应的用户，返回删除失败的标识

    def get_group_from_team(self,team):
        sql = """select group_ids from tanos.team where name='{}' """.format(team)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            group_id = result[0][0][0]
            group_sql = """select name from tanos.group where group_id='{}' """.format(group_id)
            result = useDB.useDB().executesql_fetch(group_sql)
            groupname = result[0][0].strip()
            return groupname


    def get_teamname_fromid(self,id):
        sql = """select name from tanos.team where name='{}' """.format(id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            team_name = result[0][0]
            return team_name


    def get_role_value(self,team_name):
        sql = """SELECT role_value FROM tanos.role2 WHERE name = '{}' """.format(team_name)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            role_value = result[0][0]
            return role_value

    def get_role_read_write(self,team_id):
        sql = """SELECT read,write FROM tanos.role2 WHERE role_id = '{}' """.format(team_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            role_value = result[0]
            return role_value

    def get_all_role_calue(self):
        sql = """SELECT name,role_value FROM tanos.role2  """
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            return result

    def save_role_value(self, data):
        for name, role_value in data:
            sql = """UPDATE tanos.role2 SET role_value = '{}' WHERE name = '{}'""".format(role_value, name)
            useDB.useDB().executesql(sql)

    def show_api_batch_suite(self):
        user_id = session.get('userid', None)
        sql = """
                SELECT u.username, s.suite_id, s.suite_name, s.create_date, s.suite_label
                FROM tanos.api_batch_suite s
                INNER JOIN tanos."user" u ON s.user_id = CAST(u.user_id AS VARCHAR)
                WHERE s.user_id = '{}'
            """.format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def add_api_batch_suite(self, suite_name):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.api_batch_suite (user_id,suite_name,create_date)\
          VALUES ('{}','{}','{}')""" \
            .format(user_id, suite_name.strip(),create_date)
        useDB.useDB().executesql(sql)

    def add_api_batch_case(self, suite_id, url, methods, request_body, headers,expected_result):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.api_batch_case (user_id,suite_id,url,methods,request_body,headers,expected_result,create_date)\
          VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')""" \
            .format(user_id,suite_id, url.strip(),methods.strip(),request_body.strip(),headers.strip(),expected_result.strip(),create_date)
        useDB.useDB().executesql(sql)

    def delete_api_batch_suite(self, id):
        sql = "DELETE FROM tanos.api_batch_suite WHERE suite_id = '{}';".format(id)
        useDB.useDB().executesql(sql)

    def get_suite_id(self,filename):
        sql = """SELECT suite_id FROM tanos.api_batch_suite where suite_name='{}'  """.format(filename)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            result = result[0][0]
            return result


    def show_api_batch_case(self):
        user_id = session.get('userid', None)
        sql = """select user_id,case_id,suite_id,url,methods,request_body,headers,expected_result,create_date from tanos.api_batch_case where user_id= '{}'  """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def show_api_batch_case_in_suite_id(self,suite_id):
        user_id = session.get('userid', None)
        sql = """select user_id,case_id,suite_id,url,methods,request_body,headers,expected_result,create_date from tanos.api_batch_case where suite_id= '{}'  """ \
            .format(suite_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def search_api_batch_case_from_case_id(self,case_id):
        # user_id = session.get('userid', None)
        sql = """select * from tanos.api_batch_case where case_id= '{}'  """ \
            .format(case_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def add_api_batch_job(self,job_name):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.api_batch_job (user_id,job_name,create_date)\
          VALUES ('{}','{}','{}')""" \
            .format(user_id, job_name.strip(),create_date)
        useDB.useDB().executesql(sql)

    def get_job_id(self,job_name):
        sql = """SELECT job_id FROM tanos.api_batch_job where job_name='{}'  """.format(job_name)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            result = result[0][0]
            return result


    def show_api_batch_job(self):
        user_id = session.get('userid', None)
        sql = """select user_id,job_id,job_name,create_date from tanos.api_batch_job where user_id= '{}'  """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def add_api_batch_result(self, case_id, job_id, url, methods, request_body, headers,expected_result,test_result):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.api_batch_result (user_id,case_id, job_id,url,methods,request_body,headers,expected_result,test_result,create_date)\
          VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""" \
            .format(user_id, case_id,job_id, url.strip(),methods.strip(),request_body.strip(),headers.strip(),expected_result.strip(),test_result.strip(),create_date)
        useDB.useDB().executesql(sql)


    def show_api_batch_result_in_job_id(self,job_id):
        # user_id = session.get('userid', None)
        sql = """select user_id,case_id,job_id,url,methods,request_body,headers,expected_result,create_date from tanos.api_batch_result where job_id= '{}'  """ \
            .format(job_id)
        print(sql)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result


    def add_api_batch_token(self, job_id, url, body,test_rule):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Check if the job_id already exists in the database
        check_sql = "SELECT * FROM tanos.api_batch_token WHERE job_id = '{}'".format(job_id)
        result = useDB.useDB().executesql_fetch(check_sql)

        if result and len(result) > 0:
            # Job_id exists, update the existing record
            update_sql = """UPDATE tanos.api_batch_token 
                            SET url = '{}', body = '{}',test_rule='{}', create_date = '{}' 
                            WHERE job_id = '{}'""" \
                .format(url.strip(), json.dumps(body), test_rule.strip(),create_date, job_id)
            useDB.useDB().executesql(update_sql)
        else:
            # Job_id doesn't exist, insert a new record
            insert_sql = """INSERT INTO tanos.api_batch_token (job_id, url, body,test_rule,create_date) 
                            VALUES ('{}', '{}', '{}','{}', '{}')""" \
                .format(job_id, url.strip(), json.dumps(body),test_rule.strip(), create_date)
            useDB.useDB().executesql(insert_sql)

    def get_api_batch_token(self, job_id):
        # user_id = session.get('userid', None)
        sql = """select url, body,test_rule from tanos.api_batch_token where job_id= '{}'  """ \
            .format(job_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            return result[0]
        else:
            return None


    def sheet_exists(self, sheet_name):
        try:
            # Assuming your table is named 'api_batch_suite'

            sql = """SELECT COUNT(*) FROM tanos.api_batch_suite WHERE suite_name = '{}'""".format(sheet_name)
            result = useDB.useDB().executesql_fetch(sql)
            if result[0][0] > 0:
                return True  # If count is greater than 0, sheet exists
            else:
                return False
        except Exception as e:
            print(f"Error checking if sheet exists: {str(e)}")
            return False

    def update_batch_suite_info(self, suite_id,suite_name,suite_label):
        sql = "UPDATE tanos.api_batch_suite set suite_name='{}',suite_label='{}' WHERE suite_id = '{}';".format(
            suite_name,suite_label,suite_id)
        useDB.useDB().executesql(sql)

    def delete_api_batch_job(self, id):
        sql = "DELETE FROM tanos.api_batch_job WHERE job_id = '{}';".format(id)
        useDB.useDB().executesql(sql)

    def add_data_batch_test_case(self, case_name):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.data_batch_test_case (case_name,user_id,create_date)\
          VALUES ('{}','{}','{}')""" \
            .format(case_name.strip(),user_id,create_date)
        useDB.useDB().executesql(sql)


    def get_data_batch(self, case_id):
        # user_id = session.get('userid', None)
        sql = """select job_id,job_name,job from tanos.job_management where case_id= '{}'  """ \
            .format(case_id)
        # print(sql)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def get_data_batch_job(self, job_id):
        # user_id = session.get('userid', None)
        sql = """select job_id,job_name,job from tanos.job_management where job_id= '{}'  """ \
            .format(job_id)
        # print(sql)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def add_team(self,team_name,team_role):
        sql = """INSERT INTO tanos.team (name,group_ids)\
          VALUES ('{}','{}')""" \
            .format(team_name, team_role)
        useDB.useDB().executesql(sql)

    def delete_team(self, team_id):

        sql = "DELETE FROM tanos.team WHERE team_id = '{}';".format(team_id)
        result = useDB.useDB().executesql(sql)
        return result

    def get_login_para(self):
        sql = "SELECT login_type FROM tanos.admin_config;"
        result = useDB.useDB().executesql_fetch(sql)
        return result[0][0]

    def update_login_type(self,new_login_type):
        sql = "UPDATE tanos.admin_config set login_type='{}';".format(new_login_type)
        useDB.useDB().executesql(sql)


    def show_data_per_job(self):
        user_id = session.get('userid', None)
        sql = """select user_id,job_id,job_name,create_date from tanos.data_per_job where user_id= '{}'  """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from tanos.connection_management """
        result = useDB.useDB().executesql_fetch(sql)

        return result

    def add_data_per_job(self,job_name):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO tanos.data_per_job (user_id,job_name,create_date)\
          VALUES ('{}','{}','{}')""" \
            .format(user_id, job_name.strip(),create_date)
        useDB.useDB().executesql(sql)

    def delete_data_per_job(self, id):
        sql = "DELETE FROM tanos.data_per_job WHERE job_id = '{}';".format(id)
        useDB.useDB().executesql(sql)

    def update_data_per_job_config(self,job_id,job_config):
        sql = "UPDATE tanos.data_per_job SET job_config = %s WHERE job_id = %s;"
        params = ( job_config,job_id)
        useDB.useDB().executesqlP(sql, params)

    def show_data_per_job_config(self,job_id):

        sql = """SELECT job_config FROM tanos.data_per_job WHERE job_id='{}'  """ \
            .format(job_id)
        print(sql)
        result = useDB.useDB().executesql_fetch(sql)
        print(result[0][0])
        print(type(result[0][0]))
        if result:
            job_config = result[0][0]
            return json.loads(job_config)

    def update_login_date(self,user_id):
        login_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "UPDATE tanos.user set latest_login_date='{}' where user_id={};".format(login_date,user_id)
        useDB.useDB().executesql(sql)





if __name__ == '__main__':
    testcase = tanos_manage()
    # a= testcase.search_by_connect_id(10002)
    # print (a[0][0].strip())
    # print(type(a))
    # print(testcase.show_test_cases('id','module','name',100))

