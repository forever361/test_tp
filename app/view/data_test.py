from datetime import timedelta
from flask import Blueprint, render_template, request, redirect, session
import subprocess
import os
import sys

from app.util.IP_PORT import Constant
from app.view.user import authorize

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append(basePath)

from app.util.crypto_ECB import AEScoder
from app.useDB import ConnectSQL


web = Blueprint("data_test", __name__)

web.send_file_max_age_default = timedelta(seconds=1)


@web.route('/test_data')
@authorize
def test_data():
    return render_template('/test_data/test_data2.html'  )


@web.route('/test_data',methods=['POST'])
def test_data1():
    database_type1 = request.form[('db1')]
    database_type2 = request.form[('db2')]

    if 'Save' in request.form:
        host = request.form['config1_1']
        username = request.form['config1_2']
        pwd = AEScoder().encrypt(request.form['config1_3'])
        # 源头连接信息
        list_conn_source = [host,username,pwd]
        access_id = request.form['config2_1']
        secret_access_key = AEScoder().encrypt(request.form['config2_2'])
        project = request.form['config2_3']
        endpoint = request.form['config2_5']
        # 目标连接信息
        list_conn_target = [access_id,secret_access_key,project,endpoint]
        list_conn = [host,username,pwd,access_id,secret_access_key,project,endpoint]

        if database_type1=="td" and database_type2=="max":
            source_tablename = request.form['config3_3']
            # CST_FHC_ARR
            target_tablename = request.form['config4_3']
            # CDS_FHC_FIN_HCK_ARR
            user_id = session.get('userid', None)

            if source_tablename != '' and target_tablename != '':
                database_type = 'TD2MC'
                pi = request.form['config3_1']
                source_db = request.form['config4_2']
                td_columndb = request.form['config3_2']
                source_where_condition = request.form['config3_4']
                target_where_condition = request.form['config4_4']

                td_list = [source_tablename,target_tablename,td_columndb,source_db,pi,source_where_condition,target_where_condition]

                # if td_list !=[]:
                #     ConnectSQL().write_source_target_parameter(user_id,database_type_source1,td_list[0],td_list[1],td_list[2],td_list[3],td_list[4],td_list[5],td_list[6])
                #
                # if list_conn_source != []:
                #     ConnectSQL().write_source_config(user_id,database_type_source1,list_conn_source[0],list_conn_source[1],list_conn_source[2])
                #
                # if list_conn_target != []:
                #     ConnectSQL().write_target_config(user_id,list_conn_target[0],list_conn_target[1],list_conn_target[2],list_conn_target[3])

                if  list_conn != []:
                    target_db=''
                    case_name = 'testcase1'
                    ConnectSQL().write_config_value(user_id,case_name,host,username,pwd,access_id,secret_access_key,project,endpoint,
                                                    database_type,source_tablename,target_tablename,td_columndb,source_db,target_db,pi,source_where_condition,target_where_condition)

                # with open("./app/data_check/config/config_info_td_p.csv","w",newline='',encoding='utf-8') as f:
                #     csv_writer = csv.writer(f)
                #     csv_writer.writerow(td_list)
                #     f.close()
                #
                # with open("./app/data_check/config/config_info_td_conn.csv","w",newline='',encoding='utf-8') as f:
                #     csv_writer = csv.writer(f)
                #     csv_writer.writerow(list_conn_source)
                #     csv_writer.writerow(list_conn_target)
                #     f.close()

            return render_template('/test_data/test_data2.html'  )

        elif database_type1=="ora" and database_type2=="max":
            source_tablename = request.form['config3_3']
            # CST_FHC_ARR
            target_tablename = request.form['config4_3']
            # CDS_FHC_FIN_HCK_ARR
            # user_id = ConnectSQL().get_cookie()
            user_id = session.get('userid', None)

            if source_tablename != '' and target_tablename != '':
                database_type_target1 = 'ora'
                database_type_target2 = 'max'
                pi = request.form['config3_1']
                # source_db = request.form['config3_2']
                source_db = request.form['config4_2']
                # target_db = request.form['config4_2']
                td_columndb = ""
                source_where_condition = AEScoder().encrypt(request.form['config3_4']).replace(" ' ", " '' ")
                target_where_condition = AEScoder().encrypt(request.form['config4_4']).replace(" ' ", " '' ")

                ora_list = [source_tablename, target_tablename, td_columndb, source_db, pi, source_where_condition,target_where_condition]

                if ora_list != []:
                    ConnectSQL().write_source_target_parameter(user_id, database_type_target1, ora_list[0], ora_list[1],ora_list[2], ora_list[3], ora_list[4], ora_list[5],ora_list[6])

                if list_conn_source != []:
                    ConnectSQL().write_source_config(user_id, database_type_target1, list_conn_source[0],list_conn_source[1], list_conn_source[2])

                if list_conn_target != []:
                    ConnectSQL().write_target_config(user_id, list_conn_target[0], list_conn_target[1],list_conn_target[2], list_conn_target[3])

                # with open("./app/data_check/config/config_info_or_p.csv","w",newline='',encoding='utf-8') as f:
                #     csv_writer = csv.writer(f)
                #     csv_writer.writerow(ora_list)
                #     f.close()
                #
                # with open("./app/data_check/config/config_info_ora_conn.csv","w",newline='',encoding='utf-8') as f:
                #     csv_writer = csv.writer(f)
                #     csv_writer.writerow(list_conn_source)
                #     csv_writer.writerow(list_conn_target)
                #     f.close()
            return render_template('/test_data/test_data2.html'  )

    elif 'Run' in request.form:

        # cmd_td = '/opt/app/anaconda3/bin/python {}/data_check/td_mx.py'.format(basePath)
        cmd_td = 'python {}/data_check/td_mx.py'.format(configPath)

        # cmd_ora = '/opt/app/anaconda3/bin/python {}/data_check/or_mx.py'.format(basePath)
        cmd_ora = 'python {}/data_check/or_mx.py'.format(configPath)

        if database_type1 == "td" and database_type2 == "max":
            retcode = subprocess.call(cmd_td)
            # retcode = subprocess.call(cmd_td,shell=True)
            # print(retcode)
            if retcode == 0:
                return redirect('/test_finish')
            return render_template('test_error.html'  )

        elif database_type1 == "ora" and database_type2 == "max":
            # retcode = subprocess.call(cmd_ora,shell=True)
            # print(retcode)
            retcode = subprocess.call(cmd_ora)
            if retcode == 0:
                return redirect('/test_finish2')
            return render_template('test_error.html'  )

    else:
        pass
        return render_template('/test_data/test_data2.html'  )


@web.route('/test_finish')
# @authorize
def test_finish():
    user_id = session.get('userid', None)
    table_name = ConnectSQL().get_tablename(user_id, 'td').strip()
    return render_template('test_finish.html',user_id=user_id  , table_name=table_name)

@web.route('/test_finish2')
# @authorize
def test_finish2():
    user_id = session.get('userid', None)
    table_name = ConnectSQL().get_tablename(user_id, 'ora').strip()
    return render_template('test_finish2.html',user_id=user_id  , table_name=table_name)


@web.route('/data_test_report')
def data_test_report():
    user_id = session.get('userid', None)
    table_name = ConnectSQL().get_tablename(user_id, 'ora').strip()
    return render_template('/templates/userinfo/{}/10217_data_test.html'.format(user_id), user_id=user_id, table_name=table_name)