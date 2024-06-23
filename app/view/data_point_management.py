import traceback
from traceback import print_exc

import psycopg2
import pymysql
from flask import Blueprint, render_template, request, jsonify, session

from app import useDB
from app.db.tanos_manage import tanos_manage
from app.util.SSH import mySSH
from app.util.crypto_ECB import AEScoder
from app.util.log_util.all_new_log import logger_all
from app.util.permissions import permission_required
from app.view import viewutil, user

web = Blueprint("data_ponint_management", __name__)


@web.route('/data_point_management',methods=['GET'])
@user.login_required
# @permission_required(session.get('groupname'))
def encrypt_page():
        return permission_required(session.get('groupname'))(render_template)('/data/data_point_management.html')


@web.route('/add_point', methods=['POST'])
def add_row():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().new_point(data['point_name'],data['connect_id'],data['table_name'])

    logger_all.info('add connection：{}'.format(data['point_name']))

    return jsonify(success=True, message='add connection successfully')


@web.route('/point_search.json', methods=['GET'])
def show_data():
    rows = tanos_manage().show_points()
    keys=('point_id','point_name','connect_id','_table_name')
    result_list=[]
    for row in rows:
        values = [value.strip() if isinstance(value,str) else value for value in row]
        result_dict =dict(zip(keys,values))
        result_list.append(result_dict)
    return jsonify(result_list)


@web.route('/delete_point', methods=['POST'])
def delete_data():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().delete_point(data["id"])
    return jsonify(success=True, message='Data deleted successfully')


@web.route('/update_point', methods=['POST'])
def update_data():
    data = request.json
    # TODO: Update data in the database
    print(data)
    tanos_manage().update_point(data['point_id'],data['point_name'],data['connect_name'],data['_table_name'])
    return jsonify(success=True, message='Data updated successfully')


@web.route('/getMyConnect', methods=['GET'])
def getMyConnect():
    rows = tanos_manage().get_myConnections()
    # TODO: get data from the database
    print(rows)
    result_list = []
    for row in rows:
        values = [value.strip() if isinstance(value, str) else value for value in row]
        result_list.append(values[0])
    print(result_list)
    result = [{'value':item,'text':item} for item in result_list]
    return jsonify(result)


@web.route('/getMyConnect_key_value', methods=['GET'])
def getMyConnect_key_value():
    rows = tanos_manage().get_myConnections()
    # TODO: get data from the database
    print(rows)
    result_list = []
    for row in rows:
        values = [value.strip() if isinstance(value, str) else value for value in row]
        result_dict =dict(zip(values,values))
        result_list.append(result_dict)
    return jsonify(result_list)



@web.route('/test_connect_point', methods=['POST'])
def test_connect_point():
    data = request.json
    # TODO:

    point_info = tanos_manage().search_point_id(data['id'])
    keys = ('point_name', 'connect_id', 'table_name')
    result_list = []
    for row in point_info:
        values = [value.strip() if isinstance(value, str) else value for value in row]
        result_dict = dict(zip(keys, values))
        result_list.append(result_dict)
    r_dict_point= dict(result_list[0])


    connect_info= tanos_manage().search_all_by_connect_id(r_dict_point['connect_id'])
    keys2=('connect_id','connect_name','dbtype','connect_type','host','dblibrary','username','pwd',"port")
    result_list2 = []
    for row2 in connect_info:
        values2 = [value.strip() if isinstance(value, str) else value for value in row2]
        result_dict2 = dict(zip(keys2, values2))
        result_list2.append(result_dict2)
    r_dict_conn= dict(result_list2[0])

    print(r_dict_conn)

    if r_dict_conn['dbtype'] == 'AliCloud-PostgreSQL':
        try:
            # PostgreSQL connection
            conn = psycopg2.connect(database=r_dict_conn['dblibrary'], user=r_dict_conn['username'],
                                    password=r_dict_conn['pwd'],
                                    host=r_dict_conn['host'], port=r_dict_conn['port'])
            cur = conn.cursor()
            # Extract schema and table name
            schema_name, table_name = r_dict_point['table_name'].split('.')

            # Check if the table exists
            check_table_sql = f"""
                            SELECT EXISTS (
                                SELECT 1
                                FROM information_schema.tables 
                                WHERE table_schema = '{schema_name}'
                                AND table_name = '{table_name}'
                            );
                        """
            cur.execute(check_table_sql)
            table_exists = cur.fetchone()[0]
            cur.close()
            conn.close()

            if table_exists:
                return jsonify(success=True, message=f"Table '{table_name}' exists.")
            else:
                return jsonify(success=False, message=f"Table '{table_name}' does not exist.")

        except Exception:
            logger_all.error('error connection：{}'.format(traceback.format_exc()))
            return jsonify(success=False, message='Connect error')


    elif r_dict_conn['dbtype']== 'Fileserver':
        try:
            test = mySSH(host=r_dict_conn['host'], username=r_dict_conn['username'], password=r_dict_conn['pwd'])
            test.connect()

            return jsonify(success=True, message='connect successfully')

        except Exception:
            print(print_exc())
            logger_all.error('error connection：{}'.format(traceback.format_exc()))
            return jsonify(success=False, message='connect error')


    elif r_dict_conn['dbtype']== 'DB-MySQL':
        try:
            # MySQL connection
            conn = pymysql.connect(database=r_dict_conn['dblibrary'], user=r_dict_conn['username'],
                                   password=r_dict_conn['pwd'],
                                   host=r_dict_conn['host'], port=int(r_dict_conn['port']))
            cur = conn.cursor()
            # Check if the table exists
            table_name = r_dict_point['table_name']
            check_table_sql = f"""
                       SELECT COUNT(*)
                       FROM information_schema.tables 
                       WHERE table_schema = '{r_dict_conn['dblibrary']}'
                       AND table_name = '{table_name}';
                   """
            cur.execute(check_table_sql)
            table_exists = cur.fetchone()[0] == 1
            cur.close()
            conn.close()

            if table_exists:
                return jsonify(success=True, message=f"Table '{table_name}' exists.")
            else:
                return jsonify(success=False, message=f"Table '{table_name}' does not exist.")

        except Exception:
            logger_all.error('error connection：{}'.format(traceback.format_exc()))
            return jsonify(success=False, message='Connect error')

    else:
        return jsonify(success=False, message='connect error')


@web.route('/data1.json', methods=['GET'])
def data1():
    data2 = [{
        "connect_id": 1,
        "connect_name": 'Item 1',
        "dbtype": 'PostgreSQL',
        "connect_type":"My connection",
        "username": 'hsh',
        "pwd": '54uru',
        "host": 'host1',
        "dblibrary":"test1"
    }, {
        "connect_id": 2,
        "connect_name": 'Item 2',
        "dbtype": 'AliCloud',
        "connect_type":"My connection",
        "username": 'hsh',
        "pwd": 'we643w623',
        "host": 'host2',
        "dblibrary": "test2"
    },
        {
        "connect_id": 3,
        "connect_name": 'Item 3',
         "dbtype": 'Oracle',
        "connect_type":"External connection",
        "username": 'hshfaf',
        "pwd": '32623623',
        "host": 'host3',
        "dblibrary": "tes3"
        },
        {
            "connect_id": 4,
            "connect_name": 'Item 3',
            "dbtype": 'Oracle',
            "connect_type": "External connection",
            "username": 'hshfaf',
            "pwd": '32623623',
            "host": 'host3',
            "dblibrary": "tes3"
        },
        {
            "connect_id": 5,
            "connect_name": 'Item 3',
            "dbtype": 'Oracle',
            "connect_type": "External connection",
            "username": 'hshfaf',
            "pwd": '32623623',
            "host": 'host3',
            "dblibrary": "tes3"
        },
        {
            "connect_id": 6,
            "connect_name": 'Item 3',
            "dbtype": 'Oracle',
            "connect_type": "External connection",
            "username": 'hshfaf',
            "pwd": '32623623',
            "host": 'host3',
            "dblibrary": "tes3"
        },
        {
            "connect_id": 7,
            "connect_name": 'Item 3',
            "dbtype": 'Oracle',
            "connect_type": "External connection",
            "username": 'hshfaf',
            "pwd": '32623623',
            "host": 'host3',
            "dblibrary": "tes3"
        },
    ]

    return jsonify(data2)
