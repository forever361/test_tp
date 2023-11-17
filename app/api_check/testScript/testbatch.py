import json
import unittest
from common import readConfig, requestResult
import paramunittest

base_url = readConfig.GetConfig().url

json_data = [
    {
        "case_id": "10014",
        "expected_result": [
            {
                "connect_id": 1,
                "connect_name": "Item 1",
                "connect_type": "My connection",
                "dblibrary": "test1",
                "dbtype": "PostgreSQL",
                "host": "host1",
                "pwd": "54uru",
                "username": "hsh"
            },
            {
                "connect_id": 2,
                "connect_name": "Item 2",
                "connect_type": "My connection",
                "dblibrary": "test2",
                "dbtype": "AliCloud",
                "host": "host2",
                "pwd": "we643w623",
                "username": "hsh"
            }
        ],
        "headers": "yes",
        "job_id": "10024",
        "methods": "get",
        "request_body": "{\"exchangeId\": \"4170\", \"companyTaxNo\":\"91310113MA1GLFN21P\", \"signType\":\"1\", \"signInfo\":\"24d9415fb799bed2f931b321b909d39c\"}",
        "test_result": "2023-11-15 08:05:32",
        "url": "apitest111",
        "user_id": "590011"
    },
    {
        "case_id": "10013",
        "expected_result": [
            {
                "connect_id": 1,
                "connect_name": "Item 1",
                "connect_type": "My connection",
                "dblibrary": "test1",
                "dbtype": "PostgreSQL",
                "host": "host1",
                "pwd": "54uru",
                "username": "hsh"
            },
            {
                "connect_id": 2,
                "connect_name": "Item 2",
                "connect_type": "My connection",
                "dblibrary": "test2",
                "dbtype": "AliCloud",
                "host": "host2",
                "pwd": "we643w623",
                "username": "hsh"
            }
        ],
        "headers": "yes",
        "job_id": "10024",
        "methods": "get",
        "request_body": "{\"exchangeId\": \"4170\", \"companyTaxNo\":\"91310113MA1GLFN21P\", \"signType\":\"1\", \"signInfo\":\"24d9415fb799bed2f931b321b909d39c\"}",
        "test_result": "2023-11-15 08:05:33",
        "url": "apitest222",
        "user_id": "590011"
    }
]

# Convert JSON data to a list of lists
formatted_data = [[
    item.get("case_id"),
    item.get("url"),
    item.get("methods"),
    item.get("headers"),
    item.get("request_body"),
    200,
    item.get("expected_result"),
    item.get("test_result"),
] for item in json_data]

@paramunittest.parametrized(*formatted_data)
class test_ptl_search(unittest.TestCase):
    def setParameters(self, case_name, path, method, headers, param, status_code, expectation, remark):
        # print(11111,case_name)
        self.case_name = str(case_name)
        self.path = str(path)
        self.method = str(method)
        if str(headers) != '':
            self.headers = ''
        else:
            self.headers = ''
        self.param = str(param)
        self.status_code = status_code
        self.expectation = str(expectation)
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
        print(url)
        print('【url】', url)
        print('【headers】', self.headers)
        r = requestResult.run(self.method, url=url, headers=self.headers, data=self.param)
        print ('【response】', r.json())
        print('【status_code】', r.status_code)

        # 断言请求返回值和excel中的status_code一致
        self.assertEqual(r.status_code, self.status_code)

        if r.status_code == 200:
            result = r.json()
            self.assertNotEqual(len(result), 0)
            self.assertNotEqual(len(self.expectation), 0)

            # self.expectation = json.loads(self.expectation)
            actual_result = f'"{json.dumps(result, sort_keys=True)}"'.replace("'", "\"")
            expectation_result= json.dumps(self.expectation, sort_keys=True).replace("'", "\"")

            self.assertEqual(actual_result,expectation_result)

            # for key, value in self.expectation.items():
            #     self.assertNotEqual(report[key], value)
            # self.assertNotEqual(result['result'], '')
            # self.assertEqual(result['code'], 200)
        else:
            print("【" + self.case_name + "】 --- 测试用例接口请求失败！")



if __name__ == '__main__':
    unittest.main()
