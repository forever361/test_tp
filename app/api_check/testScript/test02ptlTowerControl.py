import os
import unittest
import json
import paramunittest


from common import readExcel, readConfig, requestResult, getPath

base_url = readConfig.GetConfig().url    # 取得base url
test_case_file = readConfig.GetConfig().test_case_file    # 取得测试用例excel文件名
case_sheet = readConfig.GetConfig().case_ptl_towerContain    # 取得excel的sheet名
case_xls = readExcel.ReadExcel().get_xls(test_case_file, case_sheet)

@paramunittest.parametrized(*case_xls)
class test_ptl_tower_control(unittest.TestCase):
    def setParameters(self, case_name, path, method, headers, param, status_code, expectation, remark):
        """
        set params
        :param case_name:
        :param path:
        :param method:
        :param headers:
        :param param:
        :param status_code:
        :param expectation:
        :param remark:
        :return:
        """
        self.case_name = str(case_name)
        self.path = str(path)
        self.method = str(method)
        if str(headers) != '':
            self.headers = eval(str(headers))
        else:
            self.headers = ''

        if str(param) != '':
            self.param = eval(str(param))
            """
            eval可以将参数字符串当成有效的表达式来求值并返回计算结果.
            例：
                1）可以将字符串形式的"{1:'a', 2:'b'}"转化为字典dict格式的值，{1:'a', 2:'b'}；
                2）可以将字符串形式的"[1,'a', 2,'b']"转化为列表list格式的值，[1,'a', 2,'b']
                3）可以将字符串形式的"(1,'a', 2,'b')"转化为元组tuple格式的值，(1,'a', 2,'b')
            # eval用法参考：https://www.jianshu.com/p/b2d3a77f76f8
            """

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
        print("\n【" + self.case_name + "】测试开始前准备")

    def test01case(self):
        self.checkResult()

    def tearDown(self):
        print("    【" + self.remark + "】")
        print("\n【测试结束, 输出log完结】\n\n")

    def checkResult(self):  # 断言
        """
        check test report
        :return:
        """
        url = base_url + self.path
        print('【url】', url)
        r = requestResult.run(self.method, url, self.param)

        # 断言请求返回值和excel中的status_code一致
        self.assertEqual(r.status_code, self.status_code)

        if r.status_code == 200:
            # print('r', r)
            if 'red/s' not in url:
                result = r.json()
                self.assertNotEqual(len(result), 0)
                self.assertNotEqual(len(self.expectation), 0)
                self.assertEqual(result, self.expectation)

                # for key, value in self.expectation.items():
                #     self.assertNotEqual(report[key], value)
                # self.assertEqual(result['msg'], '接口返回成功')
                # self.assertEqual(result['code'], '200')
            else:
                # 更新代码后else的情况将不复存在。
                self.assertIn(b'page500', r.content)
        else:
            print("【" + self.case_name + "】 --- 测试用例接口请求失败！")


if __name__ == '__main__':
    test_ptl_tower_control().run()
