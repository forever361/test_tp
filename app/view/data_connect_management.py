from traceback import print_exc

from flask import Blueprint, render_template, request, jsonify
import json
from app.db.tanos_manage import tanos_manage
from app.util.crypto_ECB import AEScoder
from app.view import viewutil
import psycopg2

web = Blueprint("data_connect_management", __name__)


@web.route('/data_connect_management', methods=['GET'])
def data_connect_page():
    return render_template('/data_connect_management.html')

@web.route('/connect_search.json', methods=['GET'])
def show_data():
    rows = tanos_manage().show_connections()
    keys=('connect_id','connect_name','dbtype','connect_type','host','dblibrary','username','pwd',"port")
    result_list=[]
    for row in rows:
        values = [value.strip() if isinstance(value,str) else value for value in row]
        result_dict =dict(zip(keys,values))
        result_list.append(result_dict)
    return jsonify(result_list)

@web.route('/update_connect', methods=['POST'])
def update_data():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().update_connection(data['connect_id'],data['connect_name'],data['dbtype'],data['connect_type'],
                                  data['host'],data['db_library'],data['username'],data['pwd'],data['port'])
    return jsonify(success=True, message='Data updated successfully')


@web.route('/delete_connect', methods=['POST'])
def delete_data():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().delete_connection(data["id"])
    return jsonify(success=True, message='Data deleted successfully')

@web.route('/add_connetion', methods=['POST'])
def add_row():
    data = request.json
    # TODO: Update data in the database
    tanos_manage().new_connection(data['connect_name'],data['dbtype'],data['connect_type'],
                                  data['host'],data['db_library'],data['username'],data['pwd'],data['port'])

    return jsonify(success=True, message='add connection successfully')


@web.route('/test_connect', methods=['POST'])
def test_connect():
    data = request.json
    # TODO:
    rows = tanos_manage().search_connections_id(data['id'])
    keys = ('dbtype', 'connect_type', 'host', 'dblibrary', 'username', 'pwd','port')
    result_list = []
    for row in rows:
        values = [value.strip() if isinstance(value, str) else value for value in row]
        result_dict = dict(zip(keys, values))
        result_list.append(result_dict)
    r_dict= dict(result_list[0])
    try:
        # TODO: connect function
        conn = psycopg2.connect(database=r_dict['dblibrary'], user=r_dict['username'], password=r_dict['pwd'],
                                 host=r_dict['host'], port=r_dict['port'])
        cur = conn.cursor()
        print(cur)
        conn.close()
        return jsonify(success=True, message='connect successfully')

    except Exception:
        print(print_exc())
        return jsonify(success=False, message='connect error')




@web.route('/data3.json', methods=['GET'])
def data2():
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

