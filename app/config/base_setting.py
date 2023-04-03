import os
import datetime

from app.application import app

HomePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
DEBUG = True

# AUTH_COOKIE_NAME = "kun"
app.config['SECRET_KEY'] = "nerver guess"
#session life time
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=1200)

DOMAIN = {
    "WWW":"http://127.0.0.1:8888",
    "WWW2":"http://10.189.164.6:8899",
}

#RELEASE_PATH =  (HomePath)+'/release_version'
