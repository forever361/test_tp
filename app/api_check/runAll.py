from common import getPath, HTMLTestRunner, configEmail, readConfig
import unittest
import os
import time

path = getPath.get_path()
report_path = os.path.join(path, 'report')


class AllTest:
    def __init__(self):
        #result dir
        global resultPath
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        self.filename = now + '_report.html'
        # resultPath = os.path.join(report_path, self.filename)

        resultPath='2023-11-16 10_12_58_report.html'

        #总case list
        self.caseListFile = os.path.join(path, "case/caselist.txt")
        # print('caseListFile', self.caseListFile)
        self.caseFileDir = os.path.join(path, "testScript")  # 测试结果断言文件路径，根据不同用例（接口）分别编写
        self.caseList = []

    def set_case_list(self):
        """
        读取caselist.txt文件中的用例套件，并添加到caselist列表
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):  # data非空且不以“#”开头
                self.caseList.append(data.replace("\n", ""))    # 读取每行数据时换行符会变为\n, 去掉每行数据中的\n
        fb.close()

    def set_case_suite(self):
        """

        :return:
        """
        self.set_case_list()    # 执行set_case_List()，拿到caselist列表
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:  # 从caselist中循环取出所有case
            case_name = case.split("/")[-1] # 通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
            print(case_name + ".py")    # 打印出取出来的名称
            # 批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFileDir, pattern=case_name+'.py', top_level_dir=None)
            suite_module.append(discover)
            # print('suite_module', str(suite_module))

        if len(suite_module) > 0:   # 判断suite_module元素组是否存在元素
            for suite in suite_module:  # 如果suite_module存在元素，依次取出所有suite
                for test_name in suite: # 从discover中取出test_name，使用addTest添加到测试集
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        return test_suite   # 返回测试集

    def run(self):
        """
        run test
        :return:
        """
        print("******TEST START******")
        try:
            suit = self.set_case_suite()
            # print('try')
            # print(str(suit))
            if suit is not None:
                # print('if-suit')
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                       title='Test Report',
                                                       description='Test Description')
                runner.run(suit, 0, False)
            else:
                print("Have no case to test.")
        except Exception as e:
            print(str(e))

        finally:
            print("******TEST END******")
            fp.close()

        # 根据配置文件config.ini中的email_flag判断是否需要发送邮件
        # email_flag = readConfig.GetConfig().email_flag
        # if email_flag == 'on':
        #     configEmail.SendEmail(self.filename).outlook()
        # #


if __name__ == '__main__':
    AllTest().run()

