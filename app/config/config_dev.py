import os
import datetime


from app.application import app

HomePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


DEBUG = True

BIND_IP_PORT = "0.0.0.0:8889"

# AUTH_COOKIE_NAME = "kun"
app.config['SECRET_KEY'] = "nerver guess"
#session life time
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=1200)

app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml_dev')

CERTIFICATE_PATH = '/path/to/uat_certificate.pem'

DOMAIN = '127.0.0.1'

DOMAIN_PORT = 8899


class Config:
    @staticmethod
    def get_cmd_path(user_id,case_id,job_id):
        return '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/data2_check/run_or_mx.py {} {} {}'.format(HomePath, user_id,case_id,job_id)

    @staticmethod
    def get_cmd_path_api(job_id,user_id):
        return '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/api_check/runapi.py {} {}'.format(HomePath, job_id,user_id)

    @staticmethod
    def get_cmd_path_batch(user_id,case_id):
        return '/Users/ventura/miniconda3/envs/myenvn/bin/python3.6 {}/data2_check_batch/run_or_mx.py  {} {}'.format(HomePath, user_id, case_id)



    DATABASE = {
        'database': 'test_frame',
        'user': 'postgres',
        'password': 'postgres',
        'host': '8.134.189.98',
        'port': '3433'
    }

# SSL 配置
# CERT_FILE = "./kund.fun_bundle.pem"
# KEY_FILE = "./kund.fun.key"

