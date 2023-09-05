import logging
import os
from app.application import app
from app.util.log_util.yaml_handler import yaml_data

LOG_PATH_NEW = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

# 自定义日志格式化器
class CommaToDotFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        time_str = super().formatTime(record, datefmt)
        return time_str.replace(',', '.')

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
        fmt = CommaToDotFormatter(format)  # 使用自定义的格式化器
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
ALL_LOG_PATH= os.path.join(LOG_PATH_NEW + "/Log/tanos.log")

custom_format = '%(asctime)s-%(levelname)s: %(message)s'.replace(',', '.')

logger_all = LoggerHandler(name=yaml_data['logger']['name'],
                       level=yaml_data['logger']['level'],
                       file=ALL_LOG_PATH,
                       format=yaml_data['logger']['format2'])

# logger_all.info([222,ALL_LOG_PATH])

if __name__ == '__main__':
    logger_all.info('*'*88)
    logger_all.info('ha' * 88)