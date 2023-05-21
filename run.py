from app.application import app, socketio
from app.www import *
from  flask_cors  import *
from app.config.config import DevelopmentConfig, ProductionConfig


if __name__ == '__main__':

    config_domain = app.config['DOMAIN']['WWW']
    ip = config_domain.split('//')[1].split(':')[0]
    port = config_domain.split('//')[1].split(':')[1]

    app.config.from_object(DevelopmentConfig)

    # CORS(app, supports_credentials=True)

    # socketio.run(app,host='chinadataplatform.cds.dev.ali.cloud.cn.hsbc', port=8889,allow_unsafe_werkzeug=True,ssl_context=("chinadataplatform_cds_dev_ali_cloud_cn_hsbc.pem","chinadataplatform_cds_dev_ali_cloud_cn_hsbc.key"))
    # socketio.run(app,host='0.0.0.0', port=port,allow_unsafe_werkzeug=True)
    socketio.run(app,host='127.0.0.1', port=8889,allow_unsafe_werkzeug=True,ssl_context=('./aixint.cn_bundle.pem', './aixint.cn.key'))
