from app.application import app, socketio
from app.www import *


if __name__ == '__main__':

    config_domain = app.config['DOMAIN']['WWW']
    ip = config_domain.split('//')[1].split(':')[0]
    port = config_domain.split('//')[1].split(':')[1]

    socketio.run(app,host=ip, port=port,allow_unsafe_werkzeug=True)
