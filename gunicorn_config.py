# gunicorn_config.py

import os


workers = 1 # 或者您可以调整为适合您的应用的进程数
worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
bind = "127.0.0.1:5000"  # 指定您的应用的主机和端口
threads = 4  # 设置每个工作进程的线程数

# 添加 SSL 配置
# certfile = certfile_path
# keyfile = keyfile_path
