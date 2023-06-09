import os
import re
import sys
import time

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
        sql = """INSERT INTO xcheck.connection_management (user_id,connect_name,dbtype,connect_type,host,dblibrary,username,pwd,port,create_date)\
        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""" \
            .format(user_id, connect_name.strip(), dbtype.strip(), connect_type.strip(), host.strip(),
                    dblibrary.strip(), username.strip(), pwd.strip(), port.strip(), create_date)
        useDB.useDB().executesql(sql)

    def update_connection(self, connect_id, connect_name, dbtype, connect_type, host, dblibrary, username, pwd, port):
        sql = "UPDATE xcheck.connection_management set connect_name='{}',dbtype='{}',connect_type='{}',host='{}',dblibrary='{}',username='{}',pwd='{}', port={} WHERE connect_id = {};".format(
            connect_name, dbtype, connect_type, host, dblibrary, username, pwd, port, connect_id)
        useDB.useDB().executesql(sql)

    def delete_connection(self, id):
        sql = "DELETE FROM xcheck.connection_management WHERE connect_id = {};".format(id)
        useDB.useDB().executesql(sql)

    def show_connections(self):
        user_id = session.get('userid', None)
        sql = """select connect_id,connect_name,dbtype,connect_type,host,dblibrary,username,pwd,port from xcheck.connection_management where user_id= '{}'  """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def search_connections_id(self, connect_id):
        user_id = session.get('userid', None)
        sql = """select dbtype,connect_type,host,dblibrary,username,pwd,port from xcheck.connection_management where user_id= '{}' and connect_id='{}'  """ \
            .format(user_id, connect_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result


    def search_point_id(self, connect_id):
        user_id = session.get('userid', None)
        sql = """select point_name,connect_id,_table_name from xcheck.point_management where user_id= '{}' and point_id='{}'  """ \
            .format(user_id, connect_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def new_point(self, point_name, connect_name, table_name):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        connect_id = self.search_by_connect_name(connect_name)
        sql = """INSERT INTO xcheck.point_management (user_id,point_name,connect_id,_table_name,create_date)\
        VALUES ('{}','{}','{}','{}','{}')""" \
            .format(user_id, point_name.strip(), connect_id, table_name.strip(), create_date)
        useDB.useDB().executesql(sql)

    def search_by_connect_name(self, connect_name):
        sql = """select connect_id from xcheck.connection_management where connect_name ='{}'  """.format(connect_name)
        result = useDB.useDB().executesql_fetch(sql)
        id = int(str(result[0][0]).strip())
        return id

    def search_by_connect_id(self, connect_id):
        sql = """select connect_name from xcheck.connection_management where connect_id ={}  """.format(connect_id)
        result = useDB.useDB().executesql_fetch(sql)
        name = result[0][0].strip()
        return name

    def search_all_by_connect_id(self, connect_id):
        sql = """select connect_id,connect_name,dbtype,connect_type,host,dblibrary,username,pwd,"port" from xcheck.connection_management where connect_id ={}""".format(connect_id)
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def show_points(self):
        user_id = session.get('userid', None)
        # sql = """select point_id,point_name,connect_id,_table_name from xcheck.point_management where user_id= '{}'  """ \
        #     .format(user_id)

        sql = """select A.point_id,A.point_name,B.connect_name,A._table_name from xcheck.point_management  A
                    left join xcheck.connection_management B
                    on A.connect_id = B.connect_id
                    where A.user_id= {}
                    """.format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def delete_point(self, id):
        sql = "DELETE FROM xcheck.point_management WHERE point_id = {};".format(id)
        useDB.useDB().executesql(sql)

    def update_point(self, point_id, point_name, connect_name, _table_name):
        connect_id = self.search_by_connect_name(connect_name)
        sql = "UPDATE xcheck.point_management set point_name='{}',connect_id='{}',_table_name='{}' WHERE point_id = {};".format(
            point_name, connect_id, _table_name, point_id)
        useDB.useDB().executesql(sql)

    def get_myConnections(self):
        user_id = session.get('userid', None)
        sql = """select connect_name from xcheck.connection_management where user_id ={}   """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def show_jobs(self,case_id):
        user_id = session.get('userid', None)
        sql = """select case_id,job_id,job_name,job from xcheck.job_management where user_id= '{}' and case_id={} order by create_date DESC""" \
            .format(user_id,case_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result


    def get_myPoints(self):
        user_id = session.get('userid', None)
        sql = """select point_name from xcheck.point_management where user_id ={}   """ \
            .format(user_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def new_job(self, job_name, job, case_id):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO xcheck.job_management (job_name,job,user_id,create_date,case_id)\
          VALUES ('{}','{}','{}','{}',{})""" \
            .format(job_name.strip(), job,user_id, create_date,case_id)
        useDB.useDB().executesql(sql)


    def delete_job(self, id):
        sql = "DELETE FROM xcheck.job_management WHERE job_id = {};".format(id)
        useDB.useDB().executesql(sql)


    def update_job(self, job_id, job_name, job):
        sql = "UPDATE xcheck.job_management set job_name='{}',job='{}' WHERE job_id = {};".format(
            job_name.strip(), job, job_id)
        useDB.useDB().executesql(sql)


    def get_connectid_by_point_name(self, point_name):
        sql = """select connect_id from xcheck.point_management where point_name ='{}'  """.format(point_name)
        result = useDB.useDB().executesql_fetch(sql)
        connect_id = int(str(result[0][0]).strip())
        return connect_id

    def get_tablename_by_point_name(self, point_name):
        sql = """select _table_name from xcheck.point_management where point_name ='{}'  """.format(point_name)
        result = useDB.useDB().executesql_fetch(sql)
        table_name = str(result[0][0]).strip()
        return table_name

    # def update_team(self, username, team):
    #     sql = """UPDATE xcheck.user
    #             set team_ids='{}'
    #             WHERE username = '{}' """.format(
    #          team,username.strip())
    #     useDB.useDB().executesql(sql)

    def update_team(self, username, team):
        sql = """
            UPDATE xcheck.user_teams
            SET teamid = %s
            WHERE userid IN (
                SELECT user_id
                FROM xcheck.user
                WHERE username = %s
            )
        """
        useDB.useDB().executesql(sql, (team, username.strip()))

    def get_teams(self):
        sql = """select * from xcheck.team  """
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    # def get_teams_owner(self, teams):
    #     placeholders = ', '.join(["'{}'".format(team) for team in teams])
    #     sql = "SELECT * FROM xcheck.team WHERE name IN ({})".format(placeholders)
    #     result = useDB.useDB().executesql_fetch(sql)
    #     return result

    def get_teams_owner(self,team):
        sql = """select * from xcheck.team where name='{}' """.format(team)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        return result

    # def get_user_from_team(self, team):
    #     if team is None:
    #         return []  # 返回空结果集或采取其他处理方式
    #     sql = "SELECT username, staffid FROM xcheck.user WHERE '{}' = ANY (team_ids)".format(team)
    #     result = useDB.useDB().executesql_fetch(sql)
    #     return result

    def get_users_from_team(self, team_id):
        sql = """
            SELECT u.username, u.staffid,t.is_owner
            FROM xcheck.user u
            JOIN xcheck.user_teams t ON u.user_id = t.userid
            WHERE t.teamid = {}
        """.format(team_id)
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def get_all_user(self):
        sql = "SELECT username, staffid FROM xcheck.user "
        result = useDB.useDB().executesql_fetch(sql)
        return result

    def delete_user_from_team(self,team_id, staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM xcheck.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            # 在数据库中删除用户与团队的关联关系
            delete_sql = "DELETE FROM xcheck.user_teams WHERE teamid = {} AND userid = {}".format(team_id, user_id)
            useDB.useDB().executesql(delete_sql)
            return True  # 返回删除成功的标识，可以根据需要返回其他信息
        else:
            return False  # 如果找不到对应的用户，返回删除失败的标识

    def add_user_to_team(self,team_id, staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM xcheck.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            # 在数据库中插入用户与团队的关联关系
            add_sql = "INSERT INTO xcheck.user_teams (teamid, userid) VALUES ({}, {})".format(team_id, user_id)
            useDB.useDB().executesql(add_sql)
            return True  # 返回添加成功的标识，可以根据需要返回其他信息
        else:
            return False  # 如果找不到对应的用户，返回添加失败的标识


    def get_username_from_staffid(self,staffid):
        team_query = """
            SELECT u.username
            FROM xcheck.user u
            WHERE u.staffid = '{}'
        """.format(staffid)
        rows = useDB.useDB().executesql_fetch(team_query)
        user = rows[0][0].rstrip() if rows else None
        return user


    def if_owner(self,name,team):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM xcheck.user WHERE username = '{}'".format(name)
        result = useDB.useDB().executesql_fetch(sql)

        sql = "SELECT team_id FROM xcheck.team WHERE name = '{}'".format(team)
        team_id = useDB.useDB().executesql_fetch(sql)

        if result:
            user_id = result[0][0]
            team_id= team_id[0][0]
            team_sql = "SELECT is_owner from xcheck.user_teams where userid= '{}' and teamid='{}'".format(user_id,team_id)
            rows = useDB.useDB().executesql_fetch(team_sql)
            is_owner = rows[0][0] if rows else None
            return is_owner  # 返回添加成功的标识，可以根据需要返回其他信息
    # def if_owner(self, name, teams):
    #     # 根据用户名查询对应的用户ID
    #     sql = "SELECT user_id FROM xcheck.user WHERE username = '{}'".format(name)
    #     result = useDB.useDB().executesql_fetch(sql)
    #
    #     owners = {}  # 存储每个团队的所有者信息
    #
    #     if result:
    #         user_id = result[0][0]
    #
    #         for team in teams:
    #             # 查询团队ID
    #             sql = "SELECT team_id FROM xcheck.team WHERE name = '{}'".format(team)
    #             team_id = useDB.useDB().executesql_fetch(sql)
    #
    #             if team_id:
    #                 team_id = team_id[0][0]
    #                 team_sql = "SELECT is_owner FROM xcheck.user_teams WHERE userid = '{}' AND teamid = '{}'".format(
    #                     user_id, team_id)
    #                 rows = useDB.useDB().executesql_fetch(team_sql)
    #                 is_owner = rows[0][0] if rows else None
    #                 owners[team] = is_owner
    #
    #     return owners

    # def get_team_from_user(self, username):
    #     sql = "SELECT user_id FROM xcheck.user WHERE username = '{}'".format(username)
    #     result = useDB.useDB().executesql_fetch(sql)
    #
    #     if result:
    #         user_id = result[0][0]
    #         sql = """
    #             SELECT t.teamid
    #             FROM xcheck.user_teams t
    #             WHERE t.userid = {}
    #         """.format(user_id)
    #         result = useDB.useDB().executesql_fetch(sql)
    #         if result:
    #             teamid = result[0][0]
    #             sql = "SELECT name FROM xcheck.team WHERE team_id = '{}'".format(teamid)
    #             rows = useDB.useDB().executesql_fetch(sql)
    #             team = rows[0][0].strip() if rows else None
    #             return team  # 返回添加成功的标识，可以根据需要返回其他信息

    def get_teams_from_user(self, username):
        sql = "SELECT user_id FROM xcheck.user WHERE username = '{}'".format(username)
        result = useDB.useDB().executesql_fetch(sql)

        if result:
            user_id = result[0][0]
            sql = """
                SELECT t.teamid
                FROM xcheck.user_teams t
                WHERE t.userid = {}
            """.format(user_id)
            result = useDB.useDB().executesql_fetch(sql)
            teams = []
            for row in result:
                team_id = row[0]
                sql = "SELECT name FROM xcheck.team WHERE team_id = '{}'".format(team_id)
                print(sql)
                rows = useDB.useDB().executesql_fetch(sql)
                team = rows[0][0].strip() if rows else None
                teams.append(team)
            return teams
        return []

    def search_user_in_team(self,staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM xcheck.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            s_sql = "SELECT * from xcheck.user_teams WHERE userid = {}".format(user_id)
            rows= useDB.useDB().executesql_fetch(s_sql)
            if rows:
                return True  # 返回删除成功的标识，可以根据需要返回其他信息
            else:
                return False  # 如果找不到对应的用户，返回删除失败的标识

    def search_user_in_guest(self, staff_id):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM xcheck.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            s_sql = "SELECT * FROM xcheck.user_teams WHERE userid = {} AND teamid = 3001".format(user_id)
            rows = useDB.useDB().executesql_fetch(s_sql)
            if rows:
                return True
            else:
                return False  # 如果找不到对应的用户，返回删除失败的标识

    def update_owner_info(self,staff_id, teamId, isChecked):
        # 根据 staff_id 查询对应的 userid
        sql = "SELECT user_id FROM xcheck.user WHERE staffid = '{}'".format(staff_id)
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            user_id = result[0][0]
            update_sql = """UPDATE xcheck.user_teams SET is_owner = {} WHERE userid = {} AND teamid = {}""".format(isChecked,user_id,teamId)
            rows= useDB.useDB().executesql(update_sql)
            if rows:
                return True  # 返回删除成功的标识，可以根据需要返回其他信息
            else:
                return False  # 如果找不到对应的用户，返回删除失败的标识

    def get_group_from_team(self,team):
        sql = """select group_ids from xcheck.team where name='{}' """.format(team)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            group_id = result[0][0][0]
            group_sql = """select name from xcheck.group where group_id='{}' """.format(group_id)
            result = useDB.useDB().executesql_fetch(group_sql)
            groupname = result[0][0].strip()
            return groupname


    def get_teamname_fromid(self,id):
        sql = """select name from xcheck.team where name='{}' """.format(id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            team_name = result[0][0]
            return team_name


    def get_role_value(self,team_id):
        sql = """SELECT role_value FROM xcheck.role2 WHERE role_id = '{}' """.format(team_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            role_value = result[0][0]
            return role_value

    def get_role_read_write(self,team_id):
        sql = """SELECT read,write FROM xcheck.role2 WHERE role_id = '{}' """.format(team_id)
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            role_value = result[0]
            return role_value

    def get_all_role_calue(self):
        sql = """SELECT name,role_value FROM xcheck.role2  """
        # sql = """select connect_name,dbtype,connect_type,host,dblibrary,username,pwd from xcheck.connection_management """
        result = useDB.useDB().executesql_fetch(sql)
        if result:
            return result

    def save_role_value(self, data):
        for name, role_value in data:
            sql = """UPDATE xcheck.role2 SET role_value = '{}' WHERE name = '{}'""".format(role_value, name)
            useDB.useDB().executesql(sql)

if __name__ == '__main__':
    testcase = tanos_manage()
    # a= testcase.search_by_connect_id(10002)
    # print (a[0][0].strip())
    # print(type(a))
    # print(testcase.show_test_cases('id','module','name',100))

