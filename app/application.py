import os

from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)


env = os.environ.get('APP_ENV', 'dev')

if env == 'uat':
    app.config.from_pyfile('config/config_uat.py')
elif env == 'dev':
    app.config.from_pyfile('config/config_dev.py')
elif env == 'prod':
    app.config.from_pyfile('config/config_prod.py')


# app.config.from_pyfile("config/config_dev.py")
app.debug = app.config['DEBUG']
# socketio = SocketIO(app, async_mode='gevent')
socketio = SocketIO(app, async_mode='threading')


# app.config.from_pyfile("config/base_setting.py")
#ops_confgi=local|production
#linux export ops_confgi=local|production
#win set ops_confgi=local|production

# if "ops_config" in os.environ:
#     application.config.from_pyfile("config/%s_setting.py" % (os.environ['ops_config']))

# db = SQLAlchemy( app  )

# scheduler = APScheduler()
# scheduler.init_app(app)
