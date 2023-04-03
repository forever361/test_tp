import os
import sys
import time

from flask import session

from app import useDB
from app.util.log import logg

from app.util.crypto_ECB import AEScoder

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__),""))
sys.path.append(configPath)

from app.useDB import ConnectSQL


class test_case_manage():
    def __init__(self):
        self.status = 0
        self.name = ''

    def new_test_case(self,module,name,description):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = "INSERT INTO xcheck.test_case (userid,module,name,description,status) VALUES ('{}','{}','{}','{}','1')".format(user_id,module,name,description)
        useDB.useDB().executesql(sql)

    def web_new_test_case(self,module,name,description):
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_id = session.get('userid', None)
        sql = "INSERT INTO xcheck.web_test_case (userid,module,name,description,status) VALUES ('{}','{}','{}','{}','1')".format(user_id,module,name,description)
        useDB.useDB().executesql(sql)

    def copy_test_case(self,id):
        codelist = []
        newlist = []
        # module, name, steps, description, isPublic
        user_id = session.get('userid', None)
        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = self.show_test_cases2(['case_id'],[id],[],1)


        if len(result):
            result=result[0]
            # casename处理，读出来，解码，修改，编码，保存
            infor_value = ConnectSQL().get_infor_value_name(result['name'])
            for configreader in infor_value:
                testinfor = configreader[3].strip()
                testinfor = AEScoder().decrypt(testinfor)
                codelist.append(testinfor)
            list = codelist[0].split("\r\n")
            for i in list:
                if i.startswith('Case_name'):
                    print(i)
                    newlist.append(i.strip())

            case_name = newlist[0]
            newcode = codelist[0].replace(case_name,case_name+' of copy')
            newcode = AEScoder().encrypt(newcode)

            sql = "INSERT INTO xcheck.test_case (case_name,user_id,testinfor,create_date) " \
                  "VALUES ('{}','{}','{}','{}')".format(
                result['name']+' of copy', user_id, newcode,create_date)
            useDB.useDB().executesql(sql)
            result = 1
        else:
            result = 0
        return result


    def update_test_case(self,id,fieldlist,valueList):
        # update_value = '%s = "%s"' %(fieldlist[0],valueList[0])
        for i in range(0,len(fieldlist)):
            update_value = "{} = '{}'".format(fieldlist[i],valueList[i])
            # print(update_value,'tiaoshi...update_value')
            sql = "update xcheck.test_case set {} where case_id = '{}';".format(update_value,id)
            useDB.useDB().executesql(sql)

    def web_update_test_case(self,id,fieldlist,valueList):
        # update_value = '%s = "%s"' %(fieldlist[0],valueList[0])
        for i in range(0,len(fieldlist)):
            update_value = "{} = '{}'".format(fieldlist[i],valueList[i])
            # print(update_value,'tiaoshi...update_value')
            sql = "update xcheck.web_test_case set {} where case_id = '{}';".format(update_value,id)
            useDB.useDB().executesql(sql)

    def data_update_test_case(self,id,fieldlist,valueList):
        # update_value = '%s = "%s"' %(fieldlist[0],valueList[0])
        for i in range(0,len(fieldlist)):
            update_value = "{} = '{}'".format(fieldlist[i],valueList[i])
            # print(update_value,'tiaoshi...update_value')
            sql = "update xcheck.data_test_case set {} where case_id = '{}';".format(update_value,id)
            useDB.useDB().executesql(sql)




    def data_f2t_update_test_case(self,id,fieldlist,valueList):
        # update_value = '%s = "%s"' %(fieldlist[0],valueList[0])
        for i in range(0,len(fieldlist)):
            update_value = "{} = '{}'".format(fieldlist[i],valueList[i])
            # print(update_value,'tiaoshi...update_value')
            sql = "update xcheck.data_test_case_f2t set {} where case_id = '{}';".format(update_value,id)
            useDB.useDB().executesql(sql)

    def delete_test_case(self,id):
        sql = "DELETE FROM xcheck.test_case WHERE case_id = {};".format(id)
        print(sql)
        useDB.useDB().executesql(sql)

    def web_delete_test_case(self,id):
        sql = "DELETE FROM xcheck.web_test_case WHERE case_id = {};".format(id)
        print(sql)
        useDB.useDB().executesql(sql)

    def data_delete_test_case(self,id):
        sql = "DELETE FROM xcheck.data_test_case WHERE case_id = {};".format(id)
        print(sql)
        useDB.useDB().executesql(sql)

    def data_f2t_delete_test_case(self,id):
        sql = "DELETE FROM xcheck.data_test_case_f2t WHERE case_id = {};".format(id)
        print(sql)
        useDB.useDB().executesql(sql)

    def search_test_case(self,idList,fieldlist):
        id_value = str(idList[0])
        for i in range(1,len(idList)):
            id_value += ','+str(idList[i])
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        sql = 'select ' + search_value + ' from test_case where id in ( ' + str(id_value) + ' ) order by id desc;'
        resultlist = useDB.useDB().search(sql)
        return resultlist

    def show_test_public_cases(self):
        results = []
        sql = 'select name from test_case where status = 1 and isPublicFunction = 1 ;'
        cases = useDB.useDB().search(sql)
        print(cases)
        for i in range(len(cases)):
            results.append(cases[i][0])
        return results

    def show_test_cases(self,conditionList,valueList,fieldlist,rows):
        if len(fieldlist)==0:
            fieldlist = ['id', 'module', 'name', 'description']
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]
        if valueList[1] == 'All':
            condition = "{} like '%{}%'".format(str(conditionList[0]),str(valueList[0]))
        else:
            condition = "{} like '%{}%' and {} = '{}'".format(str(conditionList[0]),str(valueList[0]),conditionList[1],str(valueList[1]))

        results = []

        sql = 'select ' + search_value + ' from xcheck.test_case where ' + str(condition) + ' and status = 1 order by id desc limit '+ str(rows)+';'

        cases = useDB.useDB().search(sql)

        for i in range(len(cases)):
            result = {}
            result['id'] = cases[i][0]
            result['module'] = cases[i][1]
            result['name'] = cases[i][2]
            result['description'] = cases[i][3]
            results.append(result)
        return results

    def show_test_cases2(self,conditionList,valueList,fieldlist,rows):
        user_id = session.get('userid', None)
        codelist = []
        newlist = []
        if len(fieldlist)==0:
            fieldlist = ['case_id', 'case_name',]
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]

        if conditionList[0] == 'case_id':
            condition = "{} = '{}'".format(str(conditionList[0]), str(valueList[0]))
        else:
            condition = "{} like '%{}%'".format(str(conditionList[0]),str(valueList[0]))

        results = []

        # sql = 'select ' + '*' + ' from xcheck.test_case where ' + str(condition) + 'user_id=user_id' + '  order by case_id desc limit '+ str(rows)+';'
        sql = 'select * from xcheck.test_case where {} and user_id={} order by case_id desc limit {};'.format(
            str(condition), user_id, str(rows))

        cases = useDB.useDB().search(sql)
        for i in range(len(cases)):
            result = {}
            result['id'] = str(cases[i][0]).strip()
            result['name'] = cases[i][1].strip()
            result['user_id'] = str(cases[i][2]).strip()
            result['testinfor'] = cases[i][3].strip()


            results.append(result)
        return results

    def web_show_test_cases2(self,conditionList,valueList,fieldlist,rows):
        user_id = session.get('userid', None)
        codelist = []
        newlist = []
        if len(fieldlist)==0:
            fieldlist = ['case_id', 'case_name',]
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]

        if conditionList[0] == 'case_id':
            condition = "{} = '{}'".format(str(conditionList[0]), str(valueList[0]))
        else:
            condition = "{} like '%{}%'".format(str(conditionList[0]),str(valueList[0]))

        results = []

        # sql = 'select ' + '*' + ' from xcheck.test_case where ' + str(condition) + 'user_id=user_id' + '  order by case_id desc limit '+ str(rows)+';'
        sql = 'select * from xcheck.web_test_case where {} and user_id={} order by case_id desc limit {};'.format(
            str(condition), user_id, str(rows))

        cases = useDB.useDB().search(sql)
        for i in range(len(cases)):
            result = {}
            result['id'] = str(cases[i][0]).strip()
            result['name'] = cases[i][1].strip()
            result['user_id'] = str(cases[i][2]).strip()
            result['testinfor'] = cases[i][3].strip()


            results.append(result)
        return results


    def data_show_test_cases(self,conditionList,valueList,fieldlist,rows):
        user_id = session.get('userid', None)
        codelist = []
        newlist = []
        if len(fieldlist)==0:
            fieldlist = ['case_id', 'case_name',]
        search_value = fieldlist[0]
        for i in range(1,len(fieldlist)):
            search_value = search_value + ','+fieldlist[i]

        if conditionList[0] == 'case_id':
            condition = "{} = '{}'".format(str(conditionList[0]), str(valueList[0]))
        else:
            condition = "{} like '%{}%'".format(str(conditionList[0]),str(valueList[0]))

        results = []

        # sql = 'select ' + '*' + ' from xcheck.test_case where ' + str(condition) + 'user_id=user_id' + '  order by case_id desc limit '+ str(rows)+';'
        sql = 'select * from xcheck.data_test_case where {} and user_id={} order by case_id desc limit {};'.format(
            str(condition), user_id, str(rows))

        cases = useDB.useDB().search(sql)
        for i in range(len(cases)):
            result = {}
            result['id'] = str(cases[i][0]).strip()
            result['name'] = cases[i][1].strip()
            result['user_id'] = str(cases[i][2]).strip()
            result['testinfor'] = cases[i][3].strip()


            results.append(result)
        return results

    def data_show_test_cases_f2t(self, conditionList, valueList, fieldlist, rows):
        user_id = session.get('userid', None)
        codelist = []
        newlist = []
        if len(fieldlist) == 0:
            fieldlist = ['case_id', 'case_name', ]
        search_value = fieldlist[0]
        for i in range(1, len(fieldlist)):
            search_value = search_value + ',' + fieldlist[i]

        if conditionList[0] == 'case_id':
            condition = "{} = '{}'".format(str(conditionList[0]), str(valueList[0]))
        else:
            condition = "{} like '%{}%'".format(str(conditionList[0]), str(valueList[0]))

        results = []

        # sql = 'select ' + '*' + ' from xcheck.test_case where ' + str(condition) + 'user_id=user_id' + '  order by case_id desc limit '+ str(rows)+';'
        sql = 'select * from xcheck.data_test_case_f2t where {} and user_id={} order by case_id desc limit {};'.format(
            str(condition), user_id, str(rows))

        cases = useDB.useDB().search(sql)
        for i in range(len(cases)):
            result = {}
            result['id'] = str(cases[i][0]).strip()
            result['name'] = cases[i][1].strip()
            result['user_id'] = str(cases[i][2]).strip()
            result['testinfor'] = cases[i][3].strip()

            results.append(result)
        return results

if __name__ == '__main__':
    testcase = test_case_manage()
    # print(testcase.show_test_cases('id','module','name',100))



