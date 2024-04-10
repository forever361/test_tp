
from app.application import app

class Constant():
    def __init__(self):
        self.ip = app.config['DOMAIN']
        self.port = app.config['DOMAIN_PORT']


# class Constant():
#     def __init__(self):
#         self.ip = "hkl20091115.hc.cloud.hk.hsbc"
#         self.port = "8100"


