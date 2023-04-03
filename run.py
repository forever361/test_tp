from app.application import app
from app.www import *


if __name__ == '__main__':

    config_domain = app.config['DOMAIN']['WWW']
    ip = config_domain.split('//')[1].split(':')[0]
    port = config_domain.split('//')[1].split(':')[1]

    app.run(host=ip, port=port)
