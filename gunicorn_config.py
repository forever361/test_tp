
# gunicorn_config.py

import os

# 设置日志文件路径
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Log")
os.makedirs(log_dir, exist_ok=True)
startup_log_file = os.path.join(log_dir, "tanos.log")

workers = 1 # 或者您可以调整为适合您的应用的进程数
worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
bind = "0.0.0.0:8889"  # 指定您的应用的主机和端口
threads = 4  # 设置每个工作进程的线程数
timeout= 300

loglevel = "info"  # 指定日志级别
errorlog = startup_log_file  # 指定启动日志输出文件
accesslog = "-"  # 指定访问日志输出，这里设置为 "-" 表示输出到标准输出

# 添加 SSL 配置
# certfile = "./kund.fun_bundle.pem"
# keyfile = "./kund.fun.key"
