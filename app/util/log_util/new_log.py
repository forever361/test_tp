import logging
import os
from app.application import app
from app.util.log_util.yaml_handler import yaml_data

configPath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOG_PATH_NEW = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class LoggerHandler(logging.Logger):
    # 继承Logger类
    def __init__(self,
                 name='root',
                 level='DEBUG',
                 file=None,
                 format=None
                 ):
        # 设置收集器
        super().__init__(name)
        # 设置收集器级别
        self.setLevel(level)
        # 设置日志格式
        fmt = logging.Formatter(format)
        # 如果存在文件，就设置文件处理器，日志输出到文件
        if file:
            file_handler = logging.FileHandler(file,encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(fmt)
            self.addHandler(file_handler)
        # 设置StreamHandler,输出日志到控制台
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(fmt)
        self.addHandler(stream_handler)
# 从yaml配置文件中读取logging相关配置


from app.data2_check.commom.Constant_t import Constant_id
user_id = Constant_id().cookie_id
folder_path = os.path.join(app.root_path, 'static', 'user_files', str(user_id))
user_path = folder_path + '/config/' 
LOG_PATH= os.path.join(user_path + "/log.log")
# LOG_PATH= os.path.join(LOG_PATH_NEW + "/data2_check/Log/test.log")

# print(222,LOG_PATH)
logger = LoggerHandler(name=yaml_data['logger']['name'],
                       level=yaml_data['logger']['level'],
                       file=LOG_PATH,
                       format=yaml_data['logger']['format2'])

# logger.info([111,LOG_PATH])

if __name__ == '__main__':
    logger.info('*'*88)
    logger.info('ha' * 88)