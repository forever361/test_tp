import os


def get_path():
    # 取得项目根目录
    base_dir = str(os.path.dirname(os.path.dirname(__file__)))
    # print(base_dir)
    base_dir = base_dir.replace("\\", "/")
    return base_dir


if __name__ == '__main__':
    print('\n取得的项目路径为：\n', get_path())
