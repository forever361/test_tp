from functools import wraps

from flask import jsonify, request, render_template, redirect

from app.application import app
from app.db.tanos_manage import tanos_manage


class Scope():
    allow_api = []
    allow_module = []
    forbidden_api = []

    def __add__(self, other):
        self.allow_api = list(set(self.allow_api + other.allow_api))
        self.allow_module = list(set(self.allow_module + other.allow_module))
        self.forbidden_api = list(set(self.forbidden_api + other.forbidden_api))
        return self

class UserScope(Scope):
    pass
    # allow_module = ['data_connect_management']
    allow_api = ['data_connect_management.data_connect_page']

class AdminGroup(Scope):
    allow_module = ['access_config','data_testcase_tanos']
    def __init__(self):
        # 只有在实例化AdminGroup类时才会执行这部分代码
        self.p = tanos_manage().get_role_value('Admin')
        print(1111, self.p)
        allapi = ['data_connect_management.data_connect_page', 'data_ponint_management.encrypt_page', 'data_testcase.test_cases', 'web_compare.test_compare', 'apinew.test_api_normal', 'apinew.test_api_other', 'apinew.test_api_other1', 'apinew.test_api_other2', 'apinew.test_api_other3', 'access_config.access_page', 'othertools.encrypt_page']
        # allow_module = ['data_connect_management','data_ponint_management','data_testcase','data_testcase_tanos','web_testcase','web_compare','apinew','access_config','othertools']
        params = self.p.split('|')
        self.allow_api = [api for api, param in zip(allapi, params) if param == '11' or param == '10']
        print(2222, self.allow_api)

class Guest(Scope):
    # allow_module = ['data_connect_management','data_ponint_management','data_testcase']
    # allow_module = ['apinew','data_connect_management','data_ponint_management',]
    def __init__(self):
        # 只有在实例化AdminGroup类时才会执行这部分代码
        self.p = tanos_manage().get_role_value('Guest')
        print(1111, self.p)
        allapi = ['data_connect_management.data_connect_page', 'data_ponint_management.encrypt_page', 'data_testcase.test_cases', 'web_compare.test_compare', 'apinew.test_api_normal', 'apinew.test_api_other', 'apinew.test_api_other1', 'apinew.test_api_other2', 'apinew.test_api_other3', 'access_config.access_page', 'othertools.encrypt_page']
        # allow_module = ['data_connect_management','data_ponint_management','data_testcase','data_testcase_tanos','web_testcase','web_compare','apinew','access_config','othertools']
        params = self.p.split('|')
        self.allow_api = [api for api, param in zip(allapi, params) if param == '11' or param == '10']
        print(2222, self.allow_api)


class SuperScope(Scope):
    allow_module = ['v1.user']

class DelosTestGroup(Scope):
    pass
    #绑定一个API就是一个role
    # allow_module = ['data_ponint_management',]
    def __init__(self):
        # 只有在实例化AdminGroup类时才会执行这部分代码
        self.p = tanos_manage().get_role_value('DelosUsers')
        print(1111, self.p)
        allapi = ['data_connect_management.data_connect_page', 'data_ponint_management.encrypt_page', 'data_testcase.test_cases', 'web_compare.test_compare', 'apinew.test_api_normal', 'apinew.test_api_other', 'apinew.test_api_other1', 'apinew.test_api_other2', 'apinew.test_api_other3', 'access_config.access_page', 'othertools.encrypt_page']
        # allow_module = ['data_connect_management','data_ponint_management','data_testcase','data_testcase_tanos','web_testcase','web_compare','apinew','access_config','othertools']
        params = self.p.split('|')
        self.allow_api = [api for api, param in zip(allapi, params) if param == '11' or param == '10']
        print(2222, self.allow_api)


class DataTestGroup(Scope):
    allow_module = ['access_config','data_testcase_tanos']
    #绑定一个API就是一个role
    # allow_module = ['data_connect_management',]
    def __init__(self):
        # 只有在实例化AdminGroup类时才会执行这部分代码
        self.p = tanos_manage().get_role_value('ChinaDataSolution ')
        print(1111, self.p)
        allapi = ['data_connect_management.data_connect_page', 'data_ponint_management.encrypt_page', 'data_testcase.test_cases', 'web_compare.test_compare', 'apinew.test_api_normal', 'apinew.test_api_other', 'apinew.test_api_other1', 'apinew.test_api_other2', 'apinew.test_api_other3', 'access_config.access_page', 'othertools.encrypt_page']
        # allow_module = ['data_connect_management','data_ponint_management','data_testcase','data_testcase_tanos','web_testcase','web_compare','apinew','access_config','othertools']
        params = self.p.split('|')
        self.allow_api = [api for api, param in zip(allapi, params) if param == '11' or param == '10']
        print(2222, self.allow_api)



def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    splits = endpoint.split('.')
    module = splits[0]
    print(1111,endpoint)
    print(222,module)

    if endpoint in scope.forbidden_api:
        return False
    elif module in scope.allow_module:
        return True
    elif endpoint in scope.allow_api:
        return True
    else:
        return False


# def permission_required(scope):
#     def decorator(fn):
#         @wraps(fn)
#         def decorated_function(*args, **kwargs):
#             endpoint = request.endpoint
#             if is_in_scope(scope, endpoint):
#                 return fn(*args, **kwargs)
#             else:
#                 return redirect("/permission")
#         return decorated_function
#     return decorator

def permission_required(scope):
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            endpoint = request.endpoint
            print("my scope:",scope)
            if is_in_scope(scope, endpoint):
                return fn(*args, **kwargs)
            else:
                return redirect("/permission")
        return decorated_function
    return decorator


# def get_user_scope(user):
#     print(333,user)
#     if user.is_admin:
#         return AdminScope
#     elif user.is_super:
#         return SuperScope
#     else:
#         return UserScope