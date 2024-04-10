import os
import datetime

from app.application import app

HomePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
DEBUG = True

# AUTH_COOKIE_NAME = "kun"
app.config['SECRET_KEY'] = "nerver guess"
#session life time
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=1200)

app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml_test')

# DOMAIN = {
#     "WWW":"https://chinadataplatform.cds.dev.ali.cloud.cn.hsbc:8889",
#     "WWW2":"http://10.189.164.60:8899",
# }

DOMAIN = {
    "WWW":"http://127.0.0.1:8889",
    "WWW2":"http://10.189.164.60:8899",
}

DOMAIN1 = '127.0.0.1'

DOMAIN_PORT = 8889


#RELEASE_PATH =  (HomePath)+'/release_version'
