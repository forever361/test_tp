from app.util import global_manager


class Constant_api():
    def __init__(self):
        # self.cookie_id  = 580515
        self.job_id = global_manager.get_value("job_id")
        self.user_id = global_manager.get_value("user_id")
        # logger_all.info(['执行一次：',self.cookie_id ])
