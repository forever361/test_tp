# -*- coding: utf-8 -*-
import os
import configparser as cp
from app.api_check.common import getPath


class GetConfig:

    def __init__(self):
        # 取得配置文件
        config_path = getPath.get_path() + '/config.ini'
        cf = cp.ConfigParser()
        cf.read(config_path, encoding='utf-8')

        # 取得HTTP配置
        self.scheme = cf.get('HTTP', 'scheme')
        self.base_url = cf.get('HTTP', 'baseUrl')
        self.url = self.scheme + self.base_url

        # 取得email相关配置
        self.email_flag = cf.get('EMAIL', 'email_flag')
        self.email_subject = cf.get('EMAIL', 'subject')
        self.email_app = cf.get('EMAIL', 'app')
        self.email_addr = cf.get('EMAIL', 'address')
        self.email_cc = cf.get('EMAIL', 'cc')

        # 取得测试用例excel文件名
        self.test_case_file = cf.get('TEST_CASE_FILE_NAME', 'test_case_file')
        self.case_ptl_search = cf.get('TEST_CASE_FILE_NAME', 'case_ptl_search')
        self.case_ptl_towerContain = cf.get('TEST_CASE_FILE_NAME', 'case_ptl_towerContain')
        self.case_ptl_batchCommandLight = cf.get('TEST_CASE_FILE_NAME', 'case_ptl_batchCommandLight')
        self.case_ptl_batchCommandLightBubble = cf.get('TEST_CASE_FILE_NAME', 'case_ptl_batchCommandLightBubble')

    # def get_base_url(self):
    #     scheme = self.conf.get('HTTP', 'scheme')
    #     base_url = self.conf.get('HTTP', 'baseUrl')
    #     url = scheme + base_url
    #     # print(url)
    #     return url


if __name__ == '__main__':
    print(GetConfig())
    print(GetConfig().url)
