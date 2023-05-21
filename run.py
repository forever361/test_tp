from app.application import app, socketio
from app.config.config import ProductionConfig,DevelopmentConfig
from app.www import *


if __name__ == '__main__':

    config_domain = app.config['DOMAIN']['WWW']
    ip = config_domain.split('//')[1].split(':')[0]
    port = config_domain.split('//')[1].split(':')[1]

    app.config.from_object(DevelopmentConfig)

    socketio.run(app,host=ip, port=port,allow_unsafe_werkzeug=True)
