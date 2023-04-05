import os
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

    def search_by_connect_id(self, connect_name):
        sql = """select connect_name from xcheck.connection_management where connect_id ={}  """.format(connect_name)
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

    def show_jobs(self):
        user_id = session.get('userid', None)
        sql = """select job_id,job_name,job from xcheck.job_management where user_id= '{}' order by create_date DESC""" \
            .format(user_id)
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

    def new_job(self, job_name, job):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = """INSERT INTO xcheck.job_management (job_name,job,user_id,create_date)\
          VALUES ('{}','{}','{}','{}')""" \
            .format(job_name.strip(), job,user_id, create_date)
        useDB.useDB().executesql(sql)


    def delete_job(self, id):
        sql = "DELETE FROM xcheck.job_management WHERE job_id = {};".format(id)
        useDB.useDB().executesql(sql)


    def update_job(self, job_id, job_name, job):
        sql = "UPDATE xcheck.job_management set job_name='{}',job='{}' WHERE job_id = {};".format(
            job_name.strip(), job, job_id)
        useDB.useDB().executesql(sql)


if __name__ == '__main__':
    testcase = tanos_manage()
    # a= testcase.search_by_connect_id(10002)
    # print (a[0][0].strip())
    # print(type(a))
    # print(testcase.show_test_cases('id','module','name',100))

