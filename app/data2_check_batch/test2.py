
import sys
from time import sleep

from app.data2_check_batch.parameter import Parameter_pg_pg
from app.util import global_manager


user_id = sys.argv[1]
global_manager._init()
global_manager.set_value('user_id', user_id)

from app.util.log_util.new_log import logger
from app.util.log_util.all_new_log import logger_all

def testrun():
    logger.info('9' * 99)
    a=1/0
    print(a)
    logger_all.info('8' * 88)


def para_test():
    P = Parameter_pg_pg()

    DB_S = P.db_s
    USER_S = P.user_s
    PASSWORD_S = P.pwd_s
    HOST_S = P.host_s
    PORT_S = P.port_s

    DB_T = P.db_t
    USER_T = P.user_t
    PASSWORD_T = P.pwd_t
    HOST_T = P.host_t
    PORT_T = P.port_t

    logger_all.info([DB_S,USER_S,PASSWORD_S,HOST_S,PORT_S])

    logger_all.info('*'*88)
    logger_all.info('*' * 88)


if __name__ == "__main__":

    # logger.info("||||||||||||||||||Start checking||||||||||||||||||")
    testrun()
    sleep(1.6)