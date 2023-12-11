import json
import unittest
from datetime import datetime

from app.api_check.common import readConfig, requestResult
import paramunittest

from app.api_check.common.Constant_api import Constant_api
from app.db.tanos_manage import tanos_manage

base_url = readConfig.GetConfig().url

job_id = Constant_api().job_id


rows = tanos_manage().show_api_batch_result_in_job_id(job_id)
keys = (
    'user_id', 'case_id', 'job_id', 'url', 'methods', 'request_body', 'headers', 'expected_result', 'test_result','create_date')
result_list = []
for row in rows:
    # Assuming create_date is the fourth element in the row
    create_date_str = row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")
    # Convert create_date string to datetime object
    create_date_datetime = datetime.strptime(create_date_str, "%a, %d %b %Y %H:%M:%S GMT")
    # Format datetime object as needed
    formatted_create_date = create_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Update the row with the formatted create_date
    row_with_formatted_date = (*row[:8], formatted_create_date)
    # Create a dictionary from keys and updated row
    result_dict = dict(zip(keys, row_with_formatted_date))
    # Append the result dictionary to the list
    result_list.append(result_dict)

json_data = result_list

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

print(formatted_data)

# 获取Token的相关信息
token_data = tanos_manage().get_api_batch_token(job_id)

@paramunittest.parametrized(*formatted_data)
class test_ptl_search(unittest.TestCase):

    def setParameters(self, case_name, path, method, headers, param, status_code, expectation, remark):
        # print(11111,case_name)
        self.case_name = str(case_name)
        self.path = str(path)
        self.method = str(method)
        if str(headers) == '':
            self.headers = {'Content-Type': 'application/json'}

        if str(param) != '':
            self.param =  json.loads(param)
        else:
            self.param = ''

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

        if token_data is not None:
            token_url, token_body, test_rule= token_data

            if token_url:
                # 发送请求获取Token，这里你可能需要调用具体的获取Token的函数，以下是一个示例
                token_response = requestResult.run('post', url=token_url, param=json.loads(token_body))

                # 检查请求是否成功
                if token_response and token_response.status_code == 200:
                    try:
                        # 尝试获取Token，如果返回的不是JSON数据，这里可能会引发异常
                        token = token_response.json().get('token')

                        # 更新请求头，添加Token
                        if token:
                            self.headers = {'Content-Type': 'application/json', 'token': f'{token}'}
                        else:
                            # 如果无法获取Token，可以根据实际需求进行处理，这里简单地将headers置为空字符串
                            self.headers = {'Content-Type': 'application/json'}
                    except json.JSONDecodeError:
                        print("Error decoding JSON response when attempting to retrieve the token.")
                        self.headers = ''
                else:
                    print("Error obtaining the token. Status code:", token_response.status_code)
                    self.headers = ''

        print("\nStart test case")



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


        if token_data is not None:
            test_rule = token_data[2]
            print('【testRule】', test_rule)


            if test_rule=='onlyRetAndBody':
                url = self.path
                print('【url】', url)
                print('【headers】', self.headers)
                # print('【request_body】', self.param, type(self.param))
                r = requestResult.run(self.method, url=url, headers=self.headers, param=self.param)
                print('【response】', r.json())
                print('【status_code】', r.status_code)
                print('*'*20)

                # 断言请求返回值和excel中的status_code一致
                self.assertEqual(r.status_code, self.status_code)

                if r.status_code == 200:
                    result = r.json()
                    self.assertNotEqual(len(result), 0)
                    self.assertNotEqual(len(self.expectation), 0)

                    actual_body = result.get('body', {})
                    actual_ret = result.get('sysHead', {}).get('ret', [])


                    expectation_result = json.loads(self.expectation)
                    expectation_body = expectation_result.get('body', {})
                    expectation_ret = expectation_result.get('sysHead', {}).get('ret', [])

                    print('【actual_body】', actual_body)
                    print('【expect_body】', expectation_body)

                    print('【actual_ret】', actual_ret)
                    print('【expect_ret】', expectation_ret)

                    # 断言 body 和 ret 是否一致
                    self.assertEqual(actual_body, expectation_body)
                    self.assertEqual(actual_ret, expectation_ret)

                else:
                    print("【" + self.case_name + "】 --- 测试用例接口请求失败！")

            elif test_rule=='onlyRetAndBodyStructure':
                url = self.path
                print('【url】', url)
                print('【headers】', self.headers)
                # print('【request_body】', self.param, type(self.param))
                r = requestResult.run(self.method, url=url, headers=self.headers, param=self.param)
                print('【response】', r.json())
                print('【status_code】', r.status_code)
                print('*' * 40)

                # 断言请求返回值和excel中的status_code一致
                self.assertEqual(r.status_code, self.status_code)

                if r.status_code == 200:
                    result = r.json()
                    self.assertNotEqual(len(result), 0)
                    self.assertNotEqual(len(self.expectation), 0)

                    actual_result = result
                    expectation_result = json.loads(self.expectation)

                    # 验证 ret 里包含 retCode 和 retMsg 的所有 key
                    actual_ret = result.get('sysHead', {}).get('ret', [])
                    expectation_ret = expectation_result.get('sysHead', {}).get('ret', [])

                    self.assertEqual(actual_ret, expectation_ret)

                    # 验证 body 里包含所有 key
                    actual_body_keys = set(actual_result['body'].keys())
                    expected_body_keys = set(expectation_result['body'].keys())

                    print('【actual_ret】', actual_ret)
                    print('【expect_ret】', expectation_ret)

                    print('【actual_body_keys】', actual_body_keys)
                    print('【expect_body_keys】', expected_body_keys)
                    self.assertTrue(expected_body_keys.issubset(actual_body_keys))

                else:
                    print("【" + self.case_name + "】 --- 测试用例接口请求失败！")

            else:
                url = self.path
                print('【url】', url)
                print('【headers】', self.headers)
                # print('【request_body】', self.param, type(self.param))
                r = requestResult.run(self.method, url=url, headers=self.headers, param=self.param)
                print('【response】', r.json())
                print('【status_code】', r.status_code)
                print('*' * 40)

                # 断言请求返回值和excel中的status_code一致
                self.assertEqual(r.status_code, self.status_code)

                if r.status_code == 200:
                    result = r.json()
                    self.assertNotEqual(len(result), 0)
                    self.assertNotEqual(len(self.expectation), 0)

                    actual_result = result
                    print('【actual_result】', actual_result)
                    expectation_result = json.loads(self.expectation)
                    print('【expect_result】', expectation_result)
                    self.assertEqual(actual_result, expectation_result)

                else:
                    print("【" + self.case_name + "】 --- 测试用例接口请求失败！")

        else:
            url =  self.path
            print('【url】', url)
            print('【headers】', self.headers)
            # print('【request_body】', self.param, type(self.param))
            r = requestResult.run(self.method, url=url, headers=self.headers, param=self.param)
            print('【response】', r.json())
            print('【status_code】', r.status_code)
            print('*' * 40)

            # 断言请求返回值和excel中的status_code一致
            self.assertEqual(r.status_code, self.status_code)

            if r.status_code == 200:
                result = r.json()
                self.assertNotEqual(len(result), 0)
                self.assertNotEqual(len(self.expectation), 0)

                actual_result = result
                print('【actual_result】', actual_result)
                expectation_result = json.loads(self.expectation)
                print('【expect_result】', expectation_result)
                self.assertEqual(actual_result, expectation_result)

            else:
                print("【" + self.case_name + "】 --- 测试用例接口请求失败！")


if __name__ == '__main__':
    unittest.main()
