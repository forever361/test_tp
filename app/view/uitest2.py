from flask import Blueprint,render_template,jsonify,request,redirect
# from app import log
from app.db import test_case_manage
from app.util.log import log
from app.view import viewutil

web = Blueprint('uitest_x', __name__,template_folder='templates/uitest_x')


@web.route('/test_suites')
# @authorize
def test_suite():
    return render_template("uitest_x/test_suite.html"  )


@web.route('/test_cases')
#@authorize
def test_cases():
    return render_template("uitest_x/test_cases.html"  )


@web.route('/add_test_case', methods=['POST', 'GET'])
#@authorize
def save_new_test_case():
    if request.method == 'GET':
        return render_template("uitest_x/new_test_cases.html"  )
    if request.method == 'POST':
        info = request.form
        name = viewutil.getInfoAttribute(info,'name')
        module = viewutil.getInfoAttribute(info,'module')
        description = viewutil.getInfoAttribute(info,'description')
        type = viewutil.getInfoAttribute(info,'type')
        if module == '' or name == '' or module == 'All':
            return 'Required fields cannot be empty!'
        else:
            test_case_manage.test_case_manage().new_test_case(module,name,description)
        return redirect('test_cases')


@web.route('/edit_test_case', methods=['POST', 'GET'])
#@authorize
def edit_test_case():
    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info,'id')
        return render_template("uitest_x/edit_test_cases2.html", id=id  )
    if request.method == 'POST':
        info = request.form
        id = viewutil.getInfoAttribute(info,'id')
        name = viewutil.getInfoAttribute(info,'name')
        module = viewutil.getInfoAttribute(info,'module')
        description = viewutil.getInfoAttribute(info,'description')
        steps = viewutil.getInfoAttribute(info,'steps')
        steps = steps.replace('"',"'")
        type = viewutil.getInfoAttribute(info,'type')
        if module == '' or name == '' or module == '--Option--':
            return '必填字段不得为空!'
        else:
            test_case_manage.test_case_manage().update_test_case(id,['module','name','description'],[module,name,description])
        return render_template('uitest_x/test_cases.html'  )


@web.route('/copy_test_case', methods=['POST', 'GET'])
#@authorize
def copy_test_case():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        result = jsonify({'code': 500, 'msg':'should be get!'})
        return result
    if request.method == 'POST':
        info = request.form
        id = viewutil.getInfoAttribute(info,'id')
        if id == '':
            result = jsonify({'code': 500, 'msg':'test case is not found!'})
        else:
            result0 = test_case_manage.test_case_manage().copy_test_case(id)
            if result0:
                result = jsonify({'code': 200, 'msg':'copy success!'})
            else:
                result = jsonify({'code': 500, 'msg': 'test case is not found!'})
        return result


@web.route('/copy_test_suite', methods=['POST', 'GET'])
#@authorize
def copy_test_suite():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        result = jsonify({'code': 500, 'msg':'should be get!'})
        return result
    if request.method == 'POST':
        info = request.form
        id = viewutil.getInfoAttribute(info,'id')
        if id == '':
            result = jsonify({'code': 500, 'msg':'test case is not found!'})
        else:
            import random,time
            batchId = str(random.randint(10000,99999)) + str(time.time())
            test_suite_manage.test_suite_manage().copy_test_suite(id,batchId)
            newId = test_suite_manage.test_suite_manage().show_test_suites(["batchId"],[batchId],['id'],1)
            if len(newId):
                ext = newId[0]['id']
                if ext != '0':
                    test_batch_manage.test_batch_manage().copy_test_batch(ext,id)
                message = 'success!'
                code = 200
                result = jsonify({'code': 200, 'msg':'copy success!'})
            else:
                result = jsonify({'code': 500, 'msg': 'test case is not found!'})
        return result


@web.route('/delete_test_case', methods=['POST', 'GET'])
#@authorize
def delete_test_case():
    # log.log().logger.info(request.value)
    if request.method == 'GET':
        info = request.values
        id = viewutil.getInfoAttribute(info,'id')
        return render_template("uitest_x/test_cases.html"  )
    if request.method == 'POST':
        info = request.form
        id = viewutil.getInfoAttribute(info,'id')
        act = viewutil.getInfoAttribute(info,'act')
        if act == 'del':
            test_case_manage.test_case_manage().delete_test_case(id)
            code = 200
            message = 'delete success!'
        else:
            code = 500
            message = 'act is not del'
        result = jsonify({'code': code, 'msg': message})
        return result,{'Content-Type': 'application/json'}


#点击search后查询库中case列表
@web.route('/test_case.json', methods=['POST', 'GET'])
#@authorize
def search_test_cases():
    if request.method == 'POST':
        log().logger.info("2222222222222222222")
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  #每页显示的条数
        offset = info.get('offset',0)  #分片数，(页码-1)*limit, 它表示一段数据的起点
        id = viewutil.getInfoAttribute(info,'id')
        module = viewutil.getInfoAttribute(info,'module')
        type = viewutil.getInfoAttribute(info,'type')
        name = viewutil.getInfoAttribute(info,'name')

        valueList = [name]
        conditionList = ['name']
        if type != 'test_case':
            if len(module) != 0 and module[0] != 'All' and module[0] != '':
                conditionList.append('module')
                valueList.append(module)
            # print('info content: id- %s, module -%s, name - %s' %(id,module,name,type), "111")
        else:
            conditionList.append('id')
            valueList.append(id)
            # print('info content: id- %s, module -%s, name - %s' % (id, module, name, type), "222")
        fieldlist = []
        rows = 1000
        print(conditionList,valueList,fieldlist,rows)
        caseList = test_case_manage.test_case_manage().show_test_cases(conditionList,valueList,fieldlist,rows)
        data = caseList
        print (type,"tiaoshi")
        if type == 'test_case':
            data1 = jsonify({'total':len(data),'rows':data[0]})
        else:
            data1 = jsonify({'total':len(data),'rows':data[int(offset):int(offset)+int(limit)]})
        # log.log().logger.info('data1: %s' %data1)
        return data1,{'Content-Type': 'application/json'}


@web.route('/runtest.json', methods=['POST', 'GET'])
#@authorize
def runtest():
    # log.log().logger.info(request)
    if request.method == 'POST':
        log().logger.info("post")
        result = jsonify({'code': 500, 'msg': 'should be get!'})
        return result
    else:
        # log.log().logger.info(request.values)
        # log.log().logger.info(request.form)
        info = request.values
        id = viewutil.getInfoAttribute(info,'id')
        test_case_id = viewutil.getInfoAttribute(info,'test_case_id')
        ipVal = viewutil.getInfoAttribute(info,'ipVal')
        type = viewutil.getInfoAttribute(info,'type')
        if type == 'test_suite':
            test_suite_manage.test_suite_manage().new_test_run_list(id)
            result = jsonify({'code': 200, 'msg': 'success!'})
        elif type == 'test_suite_rerun_all':
            ipList = ipVal.split(',')
            for i in range(len(ipList)):
                test_suite_manage.test_suite_manage().new_test_run_list(id)
                if ipList[i] == '':
                    test_batch_manage.test_batch_manage().rerun_test_batch(id,'all')
                else:
                    test_batch_manage.test_batch_manage().rerun_test_batch_Ip(id, 'all',ipList[i])
            result = jsonify({'code': 200, 'msg': 'success!'})

        elif type == 'test_suite_rerun_part':
            test_suite_manage.test_suite_manage().new_test_run_list(id)
            test_batch_manage.test_batch_manage().rerun_test_batch(id, 'part')
            result = jsonify({'code': 200, 'msg': 'success!'})
        elif type == 'test_batch':
            # test_suite_manage.test_suite_manage().new_test_run_list(id)
            test_batch_manage.test_batch_manage().rerun_test_batch_record(id, test_case_id)
            result = jsonify({'code': 200, 'msg': 'success!'})
        elif type == 'test_case':
            ipList = ipVal.split(',')
            for i in range(len(ipList)):
                test_suite_manage.test_suite_manage().new_test_run_list(id)
                if ipList[i] == '':
                    test_batch_manage.test_batch_manage().rerun_test_batch('0', [id])
                else:
                    test_batch_manage.test_batch_manage().rerun_test_batch_Ip('0', [id], str(ipList[i]))
            result = jsonify({'code': 200, 'msg': 'success!'})
        else:
            result = jsonify({'code': 200, 'msg': 'type is not defined!'})
        return result
