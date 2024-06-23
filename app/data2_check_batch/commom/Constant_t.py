
from app.util import global_manager


class Constant_id():
    def __init__(self):
        # self.cookie_id  = 580515
        self.cookie_id = global_manager.get_value("user_id")
        self.case_id = global_manager.get_value("case_id")
        # logger_all.info(['执行一次：',self.cookie_id ])

class Testreport():
    def __init__(self):
        self.report_type = 'UAT'
        # self.report_type= 'PROD'



