#!/bin/bash

# 设置目标目录路径
target_directory="/app/tanos/application"

# 检查目录是否存在
if [ ! -d "$target_directory" ]; then
    # 如果目录不存在，创建目录
    mkdir -p "$target_directory"
    echo "目录已创建: $target_directory"
else
    echo "目录已存在: $target_directory"
fi


# 检查是否安装了 bzip2
if command -v bzip2 >/dev/null 2>&1; then
    echo "bzip2 is already installed."
else
    # 如果没有安装，尝试使用 yum 安装
    echo "Installing bzip2..."
    
    sudo yum install -y bzip2

    # 验证安装
    if command -v bzip2 >/dev/null 2>&1; then
        echo "bzip2 installed successfully."
    else
        echo "Failed to install bzip2. Please install it manually."
        exit 1
    fi
fi


# 定义安装路径
INSTALL_PATH="/app/tanos/application/anaconda3"

# 下载 Anaconda 安装脚本


# 检查环境是否存在
if [ -d "$INSTALL_PATH" ]; then
    echo "Anaconda3 already exists."
else
    # 如果环境不存在，创建环境
    echo "install Anaconda3..."
    
    # 运行安装脚本
	bash Anaconda3-5.2.0-Linux-x86_64.sh -b -p "$INSTALL_PATH"

    # 验证环境是否成功创建
    if [ $? -eq 0 ]; then
        echo "install Anaconda3 successfully."
    else
        echo "Failed to install Anaconda3 ."
        exit 1
    fi
fi




CONDARC_PATH="home/realtime/.condarc"

# 检查是否已存在 ~/.condarc 文件，如果存在则备份
if [ -f "$CONDARC_PATH" ]; then
    echo "Backing up existing ~/.condarc to ~/.condarc.bak"
    mv "$CONDARC_PATH" "$CONDARC_PATH.bak"
fi

# 创建 ~/.condarc 文件并写入配置信息
echo "Creating ~/.condarc with custom configurations..."
cat <<EOL > "$CONDARC_PATH"
channels:
  - defaults
show_channel_urls: true
channel_alias: http://mirrors.tuna.tsinghua.edu.cn/anaconda
default_channels:
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
EOL

echo "Configuration completed. ~/.condarc has been created with custom configurations."



CONDA_ENV_PATH="/app/tanos/application/anaconda3/env/env1"

# 检查环境是否存在
if [ -d "$CONDA_ENV_PATH" ]; then
    echo "Conda environment 'env1' already exists."
else
    # 如果环境不存在，创建环境
    echo "Creating Conda environment 'env1'..."
    
    /app/tanos/application/anaconda3/bin/conda create -y -n env1 python=3.6.7

    # 验证环境是否成功创建
    if [ $? -eq 0 ]; then
        echo "Conda environment 'env1' created successfully."
    else
        echo "Failed to create Conda environment 'env1'."
        exit 1
    fi
fi


PIP_CONF_DIR="/home/realtime/.pip"
PIP_CONF_FILE="$PIP_CONF_DIR/pip.conf"

# 检查是否存在 ~/.pip 目录，如果不存在则创建
if [ ! -d "$PIP_CONF_DIR" ]; then
    echo "Creating ~/.pip directory..."
    mkdir -p "$PIP_CONF_DIR"
fi

# 检查是否存在 ~/.pip/pip.conf 文件，如果不存在则创建并写入配置信息
if [ ! -f "$PIP_CONF_FILE" ]; then
    echo "Creating ~/.pip/pip.conf with custom configurations..."
    cat <<EOL > "$PIP_CONF_FILE"
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host = mirrors.aliyun.com
EOL

    echo "Configuration completed. ~/.pip/pip.conf has been created with custom configurations."
else
    echo "File ~/.pip/pip.conf already exists. Skipping creation."
fi


ANACONDA_BIN="/app/tanos/application/anaconda3/envs/env1/bin"
PYTHON="$ANACONDA_BIN/python"
PIP="$ANACONDA_BIN/pip"

# 安装依赖项
sudo yum install -y libxml2-devel libtool-ltdl-devel gcc

# 安装 xmlsec1-devel 和 xmlsec1-openssl-devel
sudo yum install -y xmlsec1-devel-1.2.20-7.el7_4.x86_64.rpm
sudo yum install -y xmlsec1-openssl-devel-1.2.20-7.el7_4.x86_64.rpm

# 升级 pip
$PYTHON -m pip install -U --force-reinstall pip

# 安装 gunicorn
$PIP install pip install -upgrade pip
$PIP install gunicorn
$PIP install gevent-websocket==0.10.1
$PIP install Flask==2.0.3
$PIP install Flask-SocketIO==5.3.3
$PIP install PyYAML
$PIP install pycryptodome==3.10.4
$PIP install psycopg2-binary==2.9.5
$PIP install numpy==1.19.5
$PIP install Flask-Cors==4.0.0
$PIP install cx-Oracle==8.3.0
$PIP install pyodps==0.10.7
$PIP install cryptography==3.3.2
$PIP install pyOpenSSL==20.0.1
$PIP install oss2==2.18.3
$PIP install openpyxl==3.0.9
$PIP install paramiko==2.12.0
$PIP install pandas==1.1.5
$PIP install xlrd==2.0.1
$PIP install xlutils==2.0.0
$PIP install xlwt==1.3.0
$PIP install ParamUnittest==0.2


# 安装 python3_saml
$PIP install python3_saml

echo "All finish!!!"
