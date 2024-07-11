
import paramiko
import pandas as pd
import traceback
from itertools import (takewhile, repeat)

pd.set_option('display.max_columns', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)



class mySSH:
    def __init__(self, host='', username='', port=22, password='',remote_path='',id=''):
        self.ip = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.remote_path = remote_path
        self.id = id

    def connect(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.password != '':
                self.connection.connect(self.ip, self.port, self.username, (str(self.password)), timeout=5.0)
            else:
                try:
                    self.connection.connect(self.ip, self.port, self.username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                except paramiko.ssh_exception.SSHException:
                    self.connection.get_transport().auth_none(self.username)
                    self.connection.exec_command('uname -a')
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
        except Exception as e:
            raise e

    def connect_ftp(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.password != '':
                self.connection.connect(self.ip, self.port, self.username, (str(self.password)), timeout=5.0)

                sftp_client = self.connection.open_sftp()
                remote_file = sftp_client.open(self.remote_path)
                try:
                    df = pd.read_csv(remote_file, sep="", nrows=10000, encoding="utf-8", dtype="str",na_filter=False)
                    # self.id
                    # @@@

                    df.insert(0, 'id_no', "")
                    # print(22222,df[list(self.id.split(","))])

                    for i in self.id.split(","):
                        # print(22222,df["id"].map(str)+'|'+ df[i].map(str))
                        df["id_no"]= df["id_no"] + "|" + df[i]
                    # print(1111,df["id"])
                    df["id_no"] = df["id_no"].map(lambda x: x.strip("|"))

                    # print(33333, df["id"].sort_values()	)
                    # print(4444, type(df["id"]))

                    df.insert(1, 'pi_split', '@@@')
                    # print(f"count is {df.shape[0]}, col is {df.shape[1]}")  # {df.columns.values.tolist()}
                    colname = df.columns.values.tolist()
                    # print(colname)
                    dff = df.sort_values(by=["id_no"], inplace=False)
                    dff = dff.fillna(value='null')
                    remote_file.close()
                    sftp_client.close()

                    return colname,dff,df.shape[0]
                except Exception as e:
                    print("An error occurred.")
                    traceback.print_exc()
                    sftp_client.close()
                    remote_file.close()

            else:
                try:
                    self.connection.connect(self.ip, self.port, self.username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                except paramiko.ssh_exception.SSHException:
                    self.connection.get_transport().auth_none(self.username)


                    self.connection.exec_command('uname -a')
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
        except Exception as e:
            try:
                print(str(e.args))
                traceback.print_exc()
                self.connection = None
            finally:
                e = None
                del e

    def connect_get_col_name(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.password != '':
                self.connection.connect(self.ip, self.port, self.username, (str(self.password)), timeout=5.0)
                sftp_client = self.connection.open_sftp()
                # remote_file = sftp_client.open(self.remote_path)
                try:
                    with sftp_client.open(self.remote_path) as f:
                        line = f.readline().strip('\n').split("")
                        # print(type(f.readline()))
                        return line
                except Exception as e:
                    print("An error occurred.")
                    traceback.print_exc()
                    sftp_client.close()
                    raise e
                    # remote_file.close()
            else:
                try:
                    self.connection.connect(self.ip, self.port, self.username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                except paramiko.ssh_exception.SSHException:
                    self.connection.get_transport().auth_none(self.username)

                    self.connection.exec_command('uname -a')
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
        except Exception as e:
            try:
                print(str(e.args))
                self.connection = None
            finally:
                e = None
                del e

    def connect_ftp_batch(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.password != '':
                self.connection.connect(self.ip, self.port, self.username, (str(self.password)), timeout=5.0)
                try:
                    sftp_client = self.connection.open_sftp()
                    remote_file = sftp_client.open(self.remote_path)
                    try:
                        df = pd.read_csv(remote_file, sep="", chunksize=40, encoding="utf-8", dtype="str",na_filter=False)
                        for l, chunk in enumerate(df):
                            print(f"l is {l}")
                            chunk.insert(0, 'id_no', "")
                            for i in self.id.split(","):
                                chunk["id_no"] = chunk["id_no"] + "|" + chunk[i]
                            chunk["id_no"] = chunk["id_no"].map(lambda x: x.strip("|"))
                            chunk.insert(1, 'pi_split', '@@@')
                            col_name = chunk.columns.values.tolist()
                            dff = chunk.sort_values(by=["id_no"], inplace=False).fillna(value='null')
                            ddd = pd.concat([dff], ignore_index=True)
                            yield ddd
                    except Exception:
                        print("An error occurred.")
                        traceback.print_exc()
                        sftp_client.close()
                        remote_file.close()
                except Exception:
                    traceback.print_exc()
                    sftp_client.close()
                    remote_file.close()
                finally:
                    remote_file.close()
                    sftp_client.close()
            else:
                try:
                    self.connection.connect(self.ip, self.port, self.username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                except paramiko.ssh_exception.SSHException:
                    self.connection.get_transport().auth_none(self.username)
                    self.connection.exec_command('uname -a')
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
        except Exception:
            traceback.print_exc()
            self.connection = None



    def connect_get_count(self):
        buffer = 1024 * 1024
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.password != '':
                self.connection.connect(self.ip, self.port, self.username, (str(self.password)), timeout=5.0)
                sftp_client = self.connection.open_sftp()
                # remote_file = sftp_client.open(self.remote_path)
                try:
                    with sftp_client.open(self.remote_path) as f:
                        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                        # print(111,[buf.decode("utf8") for buf in buf_gen])
                        for buf in buf_gen:
                            return (buf.decode("utf8").count('\n'))-1

                except Exception:
                    print("An error occurred.")
                    traceback.print_exc()
                    sftp_client.close()
                    # remote_file.close()
            else:
                try:
                    self.connection.connect(self.ip, self.port, self.username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                except paramiko.ssh_exception.SSHException:
                    self.connection.get_transport().auth_none(self.username)

                    self.connection.exec_command('uname -a')
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
        except Exception as e:
            try:
                print(str(e.args))
                self.connection = None
            finally:
                e = None
                del e

    def connect_get_count_no_col(self):
        buffer = 1024 * 1024
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.password != '':
                self.connection.connect(self.ip, self.port, self.username, (str(self.password)), timeout=5.0)
                sftp_client = self.connection.open_sftp()
                # remote_file = sftp_client.open(self.remote_path)
                try:
                    with sftp_client.open(self.remote_path) as f:
                        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                        # print(111,[buf.decode("utf8") for buf in buf_gen])
                        for buf in buf_gen:
                            return (buf.decode("utf8").count('\n'))

                except Exception:
                    print("An error occurred.")
                    traceback.print_exc()
                    sftp_client.close()
                    # remote_file.close()
            else:
                try:
                    self.connection.connect(self.ip, self.port, self.username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                except paramiko.ssh_exception.SSHException:
                    self.connection.get_transport().auth_none(self.username)

                    self.connection.exec_command('uname -a')
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
        except Exception as e:
            try:
                print(str(e.args))
                self.connection = None
            finally:
                e = None
                del e

    def connect_ftp_no_col(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.password != '':
                self.connection.connect(self.ip, self.port, self.username, (str(self.password)), timeout=5.0)

                sftp_client = self.connection.open_sftp()
                remote_file = sftp_client.open(self.remote_path)
                try:
                    # 读取没有表头的CSV文件
                    df = pd.read_csv(remote_file, sep=",", header=None, nrows=10000, encoding="utf-8", dtype="str",
                                     na_filter=False)

                    # 自动生成列名
                    # df.columns = [f'col{i + 1}' for i in range(df.shape[1])]


                    return df, df.shape[0]
                except Exception as e:
                    print("An error occurred.")
                    traceback.print_exc()
                    sftp_client.close()
                    remote_file.close()

            else:
                try:
                    self.connection.connect(self.ip, self.port, self.username, look_for_keys=False,
                                            allow_agent=False, timeout=5.0)
                except paramiko.ssh_exception.SSHException:
                    self.connection.get_transport().auth_none(self.username)

                    self.connection.exec_command('uname -a')
                self.connection.sftp = paramiko.SFTPClient.from_transport(self.connection.get_transport())
        except Exception as e:
            try:
                print(str(e.args))
                traceback.print_exc()
                self.connection = None
            finally:
                e = None
                del e


def get_batch_data():
    pass

if __name__ == '__main__':
    # test = mySSH(host='8.134.189.98', username='realtime', password='wesoftar1')
    # test.connect()
    # stdin1, stdout1, stderr1 = test.connection.exec_command(
    #     'pwd')
    # stdin2, stdout2, stderr2 = test.connection.exec_command(
    #     'pwd')
    # uid_result = str(stdout1.read(), 'UTF-8')
    # psw_result = str(stdout2.read(), 'UTF-8')
    # print(uid_result.strip(), psw_result.strip())
    test = mySSH(host='8.134.189.98', username='realtime', password='wesoftar1',remote_path='/home/realtime/1.csv')
    a,b=test.connect_ftp_no_col()
    print(a)
    print(b)

