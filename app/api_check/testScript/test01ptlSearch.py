import os
import unittest
import json
import paramunittest


from common import readExcel, readConfig, requestResult, getPath

base_url = readConfig.GetConfig().url    # 取得base url
test_case_file = readConfig.GetConfig().test_case_file    # 取得测试用例excel文件名
case_sheet = readConfig.GetConfig().case_ptl_search    # 取得excel的sheet名
case_xls = readExcel.ReadExcel().get_xls(test_case_file, case_sheet)
print(22222222222,case_xls)

@paramunittest.parametrized(*case_xls)
class test_ptl_search(unittest.TestCase):
    def setParameters(self, case_name, path, method, headers, param, status_code, expectation, remark):
        print(11111,case_name)
        self.case_name = str(case_name)
        self.path = str(path)
        self.method = str(method)
        if str(headers) != '':
            self.headers = eval(str(headers))
        else:
            self.headers = ''
        if str(param) != '':
            self.param = eval(str(param))


        else:
            self.param = ''
        self.status_code = status_code
        if str(expectation) != '':
            self.expectation = eval(str(expectation))
        else:
            self.expectation = ''
        self.remark = str(remark)

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        print("\n【" + self.case_name + "】Start test case")

    def test01case(self):
        self.checkResult()

    def tearDown(self):
        # print("    【" + self.remark + "】")
        print("\n【Test completed】\n\n")

    def checkResult(self):  # 断言
        """
        check test report
        :return:
        """
        url = base_url + self.path
        print('【url】', url)
        print('【headers】', self.headers)
        r = requestResult.run(self.method, url=url, headers=self.headers, data=self.param)
        print ('【response】', r.json())
        print('【status_code】', r.status_code)

        # 断言请求返回值和excel中的status_code一致
        self.assertEqual(r.status_code, self.status_code)

        if r.status_code == 200:
            # print('r', r)
            result = r.json()
            self.assertNotEqual(len(result), 0)
            self.assertNotEqual(len(self.expectation), 0)

            # for key, value in self.expectation.items():
            #     self.assertNotEqual(report[key], value)
            # self.assertNotEqual(result['result'], '')
            # self.assertEqual(result['code'], 200)
        else:
            print("【" + self.case_name + "】 --- 测试用例接口请求失败！")


if __name__ == '__main__':
    test_ptl_search().run()
