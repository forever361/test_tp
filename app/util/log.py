import logging
import os



configPath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOG_PATH_NEW = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

class logg:
    def __init__(self):
        self.logger = self.get_logger("[]")

    def get_logger(self,logger_name):
        from app.data2_check.commom.Constant_t import Constant_id
        userid_ = Constant_id().cookie_id
        LOG_PATH= os.path.join(LOG_PATH_NEW + "/userinfo/{}/log.log".format(userid_))
        print(2222,LOG_PATH)
        logger = logging.getLogger(logger_name)
        logger.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s %(name)s [%(levelname)s] %(lineno)d - %(message)s')
        file_handler = logging.FileHandler(LOG_PATH)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.propagate = False
        return logger


if __name__ == '__main__':
    logg().logger.info("test abc")
    # input("You can not run main!")
