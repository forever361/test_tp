from app.data2_check.commom.Constant_t import Constant_id, Testreport
from app.data2_check.commom.write_excel_data import ExcelUtilAll
from datetime import datetime
import configparser

import app.data2_check.validator as v
from itertools import zip_longest
import app.data2_check.mapping as m
import os
import sys
from traceback import print_exc


from app.util.IP_PORT import Constant
from app.util.log_util.all_new_log import logger_all
from app.util.log_util.new_log import logger
from app.application import app

basePath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(basePath)

Excel_write = ExcelUtilAll()

LOG_PATH = os.path.join(os.path.join(os.path.dirname(__file__)))
LOG_PATH_NEW = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))



user_id = Constant_id().cookie_id
folder_path = os.path.join(app.root_path, 'static', 'user_files', str(user_id))
user_path = folder_path + '/config/' 
iniPath = os.path.join(user_path + "/config.ini")
logPath = os.path.join(user_path + "/log.log")


config = configparser.ConfigParser()
config.read(iniPath)  # 读取 ini 文件
caseid = config.get('default', 'caseid')


# def get_logger(logger_name):
#     LOG_PATH_NEW = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
#     userid_ = Constant_id().cookie_id
#     # logPath = os.path.join(LOG_PATH_NEW + "/userinfo/{}/log.log".format(userid_))
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(level=logging.DEBUG)
#     formatter = logging.Formatter(
#         fmt='%(asctime)s %(name)s [%(levelname)s] %(lineno)d - %(message)s')
#     # file_handler = logging.FileHandler(logPath)
#     file_handler2 = logging.FileHandler(LOG_PATH+"/Log/test.log")
#     stream_handler = logging.StreamHandler()
#     stream_handler.setFormatter(formatter)
#     logger.addHandler(stream_handler)
#     # logger.addHandler(file_handler)
#     logger.addHandler(file_handler2)
#     logger.propagate = False
#     return logger
# 
# 
# logger = get_logger("[]")


class Checker(object):
    def __init__(self, job_configure: dict, logger=1) -> None:
        # types.new_class(v, job_configure['source_validator'])


        self.s_validator = self.load_validator(
            job_configure["source_validator"])
        self.t_validator = self.load_validator(
            job_configure["target_validator"])
        self.logger = logger


    def check(self):
        pass

    def load_validator(self, configure) -> v.Validator:
        return getattr(v, configure["name"], None)(**configure)


class BatchChecker(Checker):
    def __init__(self, job_configure: dict, c_check_flag=False, v_check_flag=False) -> None:
        super().__init__(job_configure)
        self.c_check_flag = c_check_flag
        self.v_check_flag = v_check_flag
        self.row = 0



    def check(self):  # 两个check
        if self.v_check_flag:
            v_status = self.value_check()
        if self.c_check_flag:
            c_status = self.count_check()

        return v_status,c_status

    def count_check(self):  # count核心校验
        self.s_validator.shipping_count_container()
        self.t_validator.shipping_count_container()
        count_check_flag = True

        config = configparser.ConfigParser()
        config.read(iniPath)  # 读取 ini 文件
        times = config.get('default', 'times')
        # print("111111111111111111111", times)

        Excel_write.head_row()

        for key in self.s_validator.count:
            # logger.info(
            #     f"|{key:<13} check|source:{self.s_validator.count[key]} target:{self.t_validator.count[key]}")
            logger.info(
                f"|{key:<13} check|source:{self.s_validator.count[key]} target:{self.t_validator.count[key]}")
            # print('self.s_validator.count[key]', self.s_validator.count[key])

            Excel_write.get_source_count(
                self.s_validator.count[key], int(times))
            Excel_write.get_target_count(
                self.t_validator.count[key], int(times))
            Excel_write.get_source_table_name(
                self.s_validator.table, int(times))
            Excel_write.get_target_table_name(
                self.t_validator.table, int(times))
            Excel_write.get_value_detail('http://{}:{}/static/user_files/{}/csv/{}_{}.csv'.format(
                Constant().ip, Constant().port, user_id, self.t_validator.table, caseid), int(times))

            if self.s_validator.count[key] != self.t_validator.count[key]:
                count_check_flag = False

        # Excel_write.get_check_count(count_check_flag)

        if count_check_flag:
            # logger.info("count check successfully")
            logger.info("count check successfully")
            Excel_write.get_count_result_pass2(count_check_flag, int(times))
            return m.ValidateStatue.SUCCESS
        else:
            # logger.error("count check failed")
            logger.info("count check failed")
            Excel_write.get_count_result_pass2(count_check_flag, int(times))
            return m.ValidateStatue.FAIL

    def value_check(self):
        self.s_validator.shipping_value_container()
        self.t_validator.shipping_value_container()

        config = configparser.ConfigParser()
        config.read(iniPath)  # 读取 ini 文件
        times = config.get('default', 'times')
        # print("2222222222222222222222", times)

        s_count = len(self.s_validator.md5_container)
        t_count = len(self.t_validator.md5_container)
        value_check_flag = True
        # verify_result_log_file_path = f"{LOG_PATH}/{self.s_validator.table}"
        # userid = ConnectSQL().get_personal_user_id()
        userPath = folder_path + '/csv/' 
        verify_result_log_file_path = LOG_PATH+'/Log'
        date_str = datetime.strftime(datetime.now(), '%Y%m%d%H%M')

        if os.path.exists(verify_result_log_file_path):
            pass
        else:
            os.makedirs(verify_result_log_file_path)

        batch_valueflag = True
        # userPath = os.path.join(csv_path + "/static/userinfo/{}".format(userid))

        # user_id = ConnectSQL().get_personal_user_id()
        # ExcelLog().create_excel(user_id, self.s_validator.verify_tablename)

        # with open(f"{userPath}/{self.s_validator.verify_tablename}_{caseid}.csv", "w",encoding='utf-8-sig') as writer:
        #     writer.write(f"TITLE,{self.s_validator.pi},{self.s_validator.pi_split},{self.s_validator.col_str}\n")
        #     batch_valueflag = True
        #     # ns = 1
        #     # ms = 0
        #     for source_str_old,target_str_old,source_str, target_str, source_md5, target_md5 in zip_longest(self.s_validator.ori_data,self.t_validator.ori_data,self.s_validator.str_container, self.t_validator.str_container, self.s_validator.md5_container, self.t_validator.md5_container):
        #         if source_md5 == target_md5:
        #             value_check_flag = True
        #             # writer.write(f"|SOURCE STR|{str(source_str):<32}|\n")
        #             # writer.write(f"|TARGET STR|{str(target_str):<32}|\n")
        #             writer.write(f"SOURCE DATA,{source_str_old}\n")
        #             writer.write(f"TARGET DATA,{target_str_old}\n")
        #             # writer.write(f"|SOURCE MD5 |{str(source_md5):<32}|\n")
        #             # writer.write(f"|TARGET MD5 |{str(target_md5):<32}|\n")
        #             writer.write(f"|VALIDATE  SUCCESS|\n")
        #             if source_str is not None and target_str is not None:
        #                 self.s_validator.error_str_list.append(
        #                     "'%s'" % source_str.split(self.s_validator.pi_split)[0])
        #                 self.t_validator.error_str_list.append(
        #                     "'%s'" % target_str.split(self.t_validator.pi_split)[0])
        #         else:
        #             # 这里把写日志和校验值写一起了, 默认flag为true，一旦有对不上,flag 为false，输出日志
        #             value_check_flag = False
        #             # writer.write(f"|SOURCE STR|{str(source_str):<32}|\n")
        #             # writer.write(f"|TARGET STR|{str(target_str):<32}|\n")
        #             writer.write(f"SOURCE DATA,{source_str_old}\n")
        #             writer.write(f"TARGET DATA,{target_str_old}\n")
        #             # writer.write(f"|SOURCE MD5 |{str(source_md5):<32}|\n")
        #             # writer.write(f"|TARGET MD5 |{str(target_md5):<32}|\n")
        #             writer.write(f"|VALIDATE  FAIL|\n")
        #             batch_valueflag = False
        #             if source_str is not None and target_str is not None:
        #                 self.s_validator.error_str_list.append("'%s'"%source_str.split(self.s_validator.pi_split)[0])
        #                 self.t_validator.error_str_list.append("'%s'"%target_str.split(self.t_validator.pi_split)[0])

        #NEW
        if Testreport().report_type=='PROD':
            try:
                with open(f"{userPath}/{self.t_validator.verify_tablename}_{caseid}.csv", "w", encoding='utf-8-sig') as writer:
                    # writer.write(f"TITLE,{self.t_validator.pi},{self.t_validator.pi_split},{self.t_validator.col_str}\n")

                    # self.logger.info(f"self.s_validator {self.s_validator}")
                    writer.write(
                        f"Title,ID,Result,DiffCol\n")

                    # self.logger.info(f"{self.s_validator}")
                    # writer.write(
                    #     f"{self.s_validator.pi},result,{self.s_validator.col_str}\n")

                    # ns = 1
                    # ms = 0

                    self.s_validator.col_str = self.s_validator.pi + ',' + self.s_validator.pi_split + ',' + self.s_validator.col_str
                    self.t_validator.col_str = self.t_validator.pi + ',' + self.t_validator.pi_split + ',' + self.t_validator.col_str

                    total_num = 0
                    error_num = 0

                    if error_num < 500:
                        for source_str_old, target_str_old, source_str, target_str, source_md5, target_md5 in zip_longest(self.s_validator.ori_data, self.t_validator.ori_data, self.s_validator.str_container, self.t_validator.str_container, self.s_validator.md5_container, self.t_validator.md5_container):
                            if source_md5 != target_md5:
                                error_num += 1
                                total_num += 1

                                # 这里把写日志和校验值写一起了, 默认flag为true，一旦有对不上,flag 为false，输出日志
                                value_check_flag = False

                                try:
                                    source_dict = dict(
                                        zip(self.s_validator.col_str.split(","),
                                            source_str_old.split(",")))
                                    target_dict = dict(
                                        zip(self.t_validator.col_str.split(","),
                                            target_str_old.split(","))
                                    )
                                    # self.logger.info(
                                    #     f"col_str {self.s_validator.col_str}")
                                    # self.logger.info(
                                    #     f"source_dict {source_str},type is {type(source_str)}")
                                    # self.logger.info(
                                    #     f"target_dict {target_str},type is {type(target_str)}")
                                    # self.logger.info(
                                    #     f"source_dict {source_dict},type is {type(source_dict)}")
                                    # self.logger.info(
                                    #     f"target_dict {target_dict},type is {type(target_dict)}")
                                    differ = list(set(source_dict.items()) ^ set(
                                        target_dict.items()))
                                    diff_key = list(set(i[0] for i in differ))
                                    diff_value = [[]]*len(diff_key)
                                    diff = dict(zip(diff_key, diff_value))
                                    for i in differ:
                                        if len(i) == 2:
                                            diff[i[0]].append(i[1])

                                        elif len(i) == 1:
                                            diff[i[0]].append(None)
                                        else:
                                            pass
                                    # diff = str(diff).replace(",", "|")
                                    diff = str(list(diff.keys())).replace(",", "|")
                                    # self.logger.info(
                                    #     f"differ is {diff}, type is {type(diff)}")
                                    if len(differ) > 0:
                                        # writer.write(
                                        #     f"source_data,{source_str_old.split(',')[0]},{value_check_flag},{source_dict}\n")
                                        # writer.write(
                                        #     f"target_data,{target_str_old.split(',')[0]},{value_check_flag},{target_dict}\n")
                                        writer.write(
                                            f"dif:,{source_str_old.split(',')[0]},{value_check_flag},{diff}\n")
                                        batch_valueflag = False
                                        if source_str is not None and target_str is not None:
                                            self.s_validator.error_str_list.append(
                                                "'%s'" % source_str.split(self.s_validator.pi_split)[0])
                                            self.t_validator.error_str_list.append(
                                                "'%s'" % target_str.split(self.t_validator.pi_split)[0])
                                except Exception:
                                    print(print_exc())
                            else:
                                total_num += 1
                    else:
                        logger_all.info(
                            "If the number of unmatched entries exceeds 500, please check the source table and target table")
                    writer.write(f"total num:{total_num}\n")
                    writer.write(f"error num:{int(error_num)}\n")
            except Exception:
                print(print_exc())
                logger_all.info(print_exc())
            finally:
                pass

        elif Testreport().report_type=='UAT':
            #之前结果样式
            with open(f"{userPath}/{self.t_validator.verify_tablename}_{caseid}.csv", "w", encoding='utf-8-sig') as writers:
                writers.write(f"TITLE,{self.t_validator.pi_str},{self.t_validator.pi_split},{self.t_validator.col_str}\n")
                batch_valueflag = True
                for source_str_old, target_str_old, source_str, target_str, source_md5, target_md5 in zip_longest(
                        self.s_validator.ori_data, self.t_validator.ori_data, self.s_validator.str_container,
                        self.t_validator.str_container, self.s_validator.md5_container, self.t_validator.md5_container):
                    if source_md5 != target_md5:
                        # 这里把写日志和校验值写一起了, 默认flag为true，一旦有对不上,flag 为false，输出日志
                        value_check_flag = False
                        # writers.write(f"|SOURCE STR|{str(source_str):<32}|\n")
                        # writers.write(f"|TARGET STR|{str(target_str):<32}|\n")
                        writers.write(f"SOURCE DATA,{source_str_old}\n")
                        writers.write(f"TARGET DATA,{target_str_old}\n")
                        # writers.write(f"|SOURCE MD5 |{str(source_md5):<32}|\n")
                        # writers.write(f"|TARGET MD5 |{str(target_md5):<32}|\n")
                        writers.write(f"|VALIDATE  FAIL|\n")
                        batch_valueflag = False
                        if source_str is not None and target_str is not None:
                            self.s_validator.error_str_list.append("'%s'" % source_str.split(self.s_validator.pi_split)[0])
                            self.t_validator.error_str_list.append("'%s'" % target_str.split(self.t_validator.pi_split)[0])
                    else :
                        writers.write(f"SOURCE DATA,{source_str_old}\n")
                        writers.write(f"TARGET DATA,{target_str_old}\n")
                        # writers.write(f"|SOURCE MD5 |{str(source_md5):<32}|\n")
                        # writers.write(f"|TARGET MD5 |{str(target_md5):<32}|\n")
                        writers.write(f"|VALIDATE  SUCCESS|\n")
                        # batch_valueflag = True
                        if source_str is not None and target_str is not None:
                            self.s_validator.error_str_list.append("'%s'" % source_str.split(self.s_validator.pi_split)[0])
                            self.t_validator.error_str_list.append("'%s'" % target_str.split(self.t_validator.pi_split)[0])

        if batch_valueflag:
            logger.info("value check sucessfully")
            Excel_write.get_value_result_pass2(batch_valueflag, int(times))
            return m.ValidateStatue.SUCCESS
        else:
            logger.error("value check failed")
            Excel_write.get_value_result_pass2(batch_valueflag, int(times))
            return m.ValidateStatue.FAIL


class BatchChecker1(BatchChecker):
    def __init__(self, job_configure: dict, c_check_flag=False, v_check_flag=False) -> None:
        super().__init__(job_configure)
        self.c_check_flag = c_check_flag
        self.v_check_flag = v_check_flag
        self.columns_dict = {}


    def check(self):
        s_count_sql = None
        t_count_sql = None
        statuts = None

        # logger.info(
        #     f"{'=' * 20}{self.s_validator.tablename:}:start check{'=' * 20}")
        # logger.info(
        #     f"{'=' * 20}{self.s_validator.tablename:}:start check{'=' * 20}")
        if self.c_check_flag:
            s_count_sql = self.s_validator.get_batch_count_check_sql(
                self.s_validator.verify_tablename, self.s_validator.verifydb)
            t_count_sql = self.t_validator.get_batch_count_check_sql(
                self.t_validator.verify_tablename, self.t_validator.verifydb)
            print("**sql_s_count:", s_count_sql)
            print("**sql_t_count:", t_count_sql)
            # self.count_check()
        if self.v_check_flag:
            # 核心校验
            td_col_set = set(self.s_validator.col_str.split(','))
            # print('SOURCE COL:', td_col_set)
            ali_col_set = set(self.t_validator.col_str.split(','))
            # print('TARGET COL:', ali_col_set)
            final_col_set = td_col_set.intersection(ali_col_set)
            diff = td_col_set.symmetric_difference(ali_col_set)
            # logger.info(
            #     'different columns between Source and Target are: ' + (str(diff) if len(diff) != 0 else 'None'))
            logger.info(
                'different columns between Source and Target are: ' + (str(diff) if len(diff) != 0 else 'None'))
            final_col_list = list(final_col_set)
            final_col_list.sort()
            self.s_validator.col_str = ','.join(final_col_list)
            self.t_validator.col_str = self.s_validator.col_str

            print('SOURCE COL:', self.s_validator.col_str)
            print('TARGET COL:', self.t_validator.col_str)


            # self.s_validator.col_str = self.decorate_col_str(self.s_validator.col_str, 'trim(', ")")
            c_status = self.count_check()

            v_statuts = self.value_check()


        return s_count_sql, t_count_sql, v_statuts, c_status

    def decorate_col_str(self, col_str, sql_prefix, sql_suffix):
        columns = col_str.split(',')
        for index in range(len(columns)):
            columns[index] = sql_prefix + columns[index] + sql_suffix
        col_str = ','.join(columns)
        return col_str



class BatchChecker2(BatchChecker):
    def __init__(self, job_configure: dict, c_check_flag=False, v_check_flag=False) -> None:
        super().__init__(job_configure)
        self.c_check_flag = c_check_flag
        self.v_check_flag = v_check_flag
        self.columns_dict = {}


    def check(self):
        s_count_sql = None
        t_count_sql = None
        statuts = None

        # logger.info(
        #     f"{'=' * 20}{self.s_validator.tablename:}:start check{'=' * 20}")
        # logger.info(
        #     f"{'=' * 20}{self.s_validator.tablename:}:start check{'=' * 20}")
        if self.c_check_flag:
            s_count_sql = self.s_validator.get_batch_count_check_sql(
                self.s_validator.verify_tablename, self.s_validator.verifydb)
            t_count_sql = self.t_validator.get_batch_count_check_sql(
                self.t_validator.verify_tablename, self.t_validator.verifydb)
            print("**sql_s_count:", s_count_sql)
            print("**sql_t_count:", t_count_sql)
            # self.count_check()
        if self.v_check_flag:
            # 核心校验
            self.get_newcol_name()
            # self.s_validator.col_str = self.decorate_col_str(self.s_validator.col_str, 'trim(', ")")

            v_statuts = self.value_check()
            c_status = self.count_check()

        return s_count_sql, t_count_sql, v_statuts, c_status

    def get_newcol_name(self):
        source_col_set = set(self.s_validator.col_str.split(','))
        target_col_set = set(self.t_validator.col_str.split(','))
        final_col_set = source_col_set.intersection(target_col_set)
        diff = source_col_set.symmetric_difference(target_col_set)
        # logger.info(
        #     'different columns between Source and Target are: ' + (str(diff) if len(diff) != 0 else 'None'))
        logger.info(
            'different columns between Source and Target are: ' + (str(diff) if len(diff) != 0 else 'None'))
        final_col_list = list(final_col_set)
        final_col_list.sort()
        self.s_validator.col_str = ','.join(final_col_list)
        self.t_validator.col_str = ','.join(final_col_list)
        config.clear()
        config.add_section("ssh")
        config.set("ssh", "colname", self.s_validator.col_str)
        # 写入ini文件，注意写入的mode会影响是否覆盖ini文件
        userid = Constant_id().cookie_id
        iniPath_ssh = os.path.join(LOG_PATH_NEW + "/userinfo/{}/config_ssh_col.ini".format(userid))
        with open(iniPath_ssh, "w+", encoding="utf8") as f:
            config.write(f)
        print('SOURCE COL:', self.s_validator.col_str)
        print('TARGET COL:', self.t_validator.col_str)

    def decorate_col_str(self, col_str, sql_prefix, sql_suffix):
        columns = col_str.split(',')
        for index in range(len(columns)):
            columns[index] = sql_prefix + columns[index] + sql_suffix
        col_str = ','.join(columns)
        return col_str

class BatchChecker_count(BatchChecker):
    def __init__(self, job_configure: dict, c_check_flag=False, v_check_flag=False) -> None:
        super().__init__(job_configure)
        self.c_check_flag = c_check_flag
        self.v_check_flag = v_check_flag
        self.columns_dict = {}

    def check(self):
        s_count_sql = None
        t_count_sql = None
        statuts = None

        # logger.info(
        #     f"{'=' * 20}{self.s_validator.tablename:}:start check{'=' * 20}")
        # logger.info(
        #     f"{'=' * 20}{self.s_validator.tablename:}:start check{'=' * 20}")
        if self.c_check_flag:
            s_count_sql = self.s_validator.get_batch_count_check_sql(
                self.s_validator.verify_tablename, self.s_validator.verifydb)
            t_count_sql = self.t_validator.get_batch_count_check_sql(
                self.t_validator.verify_tablename, self.t_validator.verifydb)
            print("**sql_s_count:", s_count_sql)
            print("**sql_t_count:", t_count_sql)
            # self.count_check()
        if self.v_check_flag:
            # 核心校验
            td_col_set = set(self.s_validator.col_str.split(','))
            # print('SOURCE COL:', td_col_set)
            ali_col_set = set(self.t_validator.col_str.split(','))
            # print('TARGET COL:', ali_col_set)
            final_col_set = td_col_set.intersection(ali_col_set)
            diff = td_col_set.symmetric_difference(ali_col_set)
            # logger.info(
            #     'different columns between Source and Target are: ' + (str(diff) if len(diff) != 0 else 'None'))
            logger.info(
                'different columns between Source and Target are: ' + (str(diff) if len(diff) != 0 else 'None'))
            final_col_list = list(final_col_set)
            final_col_list.sort()
            self.s_validator.col_str = ','.join(final_col_list)
            self.t_validator.col_str = self.s_validator.col_str

            print('SOURCE COL:', self.s_validator.col_str)
            print('TARGET COL:', self.t_validator.col_str)

            # self.s_validator.col_str = self.decorate_col_str(self.s_validator.col_str, 'trim(', ")")

            v_statuts = None
            c_status = self.count_check()

        return s_count_sql, t_count_sql, v_statuts, c_status

    def decorate_col_str(self, col_str, sql_prefix, sql_suffix):
        columns = col_str.split(',')
        for index in range(len(columns)):
            columns[index] = sql_prefix + columns[index] + sql_suffix
        col_str = ','.join(columns)
        return col_str


if __name__ == "__main__":
    pass
