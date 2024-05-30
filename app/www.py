from app.application import app, env







from app.view import  data_test, batch, testcase, compare, normal_compare, web_testcase, web_test_compare, \
    data_batch_new, data_testcase_management, othertools,data_batch_new_f2t,data_testcase_f2t,data_point_management,\
    data_connect_management,data_job_management,api_new,access_config,docs,api_batch,api_batch_opp,admin

# 定义蓝图变量
user_dev = None
user_uat = None
user_prod = None

if env == 'dev':
    from app.view import user_dev
    user_dev = user_dev.web
elif env == 'uat':
    from app.view import user_uat
    user_uat = user_uat.web
elif env == 'prod':
    from app.view import user_prod
    user_prod = user_prod.web


# 注册蓝图
if user_dev:
    app.register_blueprint(user_dev)
if user_uat:
    app.register_blueprint(user_uat)
if user_prod:
    app.register_blueprint(user_prod)

# app.register_blueprint(user.web)
app.register_blueprint(data_test.web)
app.register_blueprint(batch.web)
app.register_blueprint(data_batch_new.web)
app.register_blueprint(testcase.web)
app.register_blueprint(compare.web)
app.register_blueprint(normal_compare.web)
app.register_blueprint(web_testcase.web)
app.register_blueprint(web_test_compare.web)
app.register_blueprint(data_testcase_management.web)
app.register_blueprint(othertools.web)
app.register_blueprint(data_batch_new_f2t.web)
app.register_blueprint(data_testcase_f2t.web)
app.register_blueprint(data_point_management.web)
app.register_blueprint(data_connect_management.web)
app.register_blueprint(data_job_management.web)
app.register_blueprint(api_new.web)
app.register_blueprint(access_config.web)
app.register_blueprint(docs.web)
app.register_blueprint(api_batch.web)
app.register_blueprint(api_batch_opp.web)
app.register_blueprint(admin.web)

from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildStaticUrl_no_v, 'buildStaticUrl_no_v')

from app import views