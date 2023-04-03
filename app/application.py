from flask import Flask


app = Flask(__name__)
app.config.from_pyfile("config/base_setting.py")

# app.config.from_pyfile("config/base_setting.py")
#ops_confgi=local|production
#linux export ops_confgi=local|production
#win set ops_confgi=local|production

# if "ops_config" in os.environ:
#     application.config.from_pyfile("config/%s_setting.py" % (os.environ['ops_config']))

# db = SQLAlchemy( app  )

# scheduler = APScheduler()
# scheduler.init_app(app)
