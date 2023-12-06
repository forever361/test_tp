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

@paramunittest.parametrized(*formatted_data)
class test_ptl_search(unittest.TestCase):
    def setParameters(self, case_name, path, method, headers, param, status_code, expectation, remark):
        # print(11111,case_name)
        self.case_name = str(case_name)
        self.path = str(path)
        self.method = str(method)
        if str(headers) != '':
            self.headers = {'Content-Type': 'application/json'}
        else:
            self.headers = ''

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
        """

        :return:
        """

        self.api_test_count += 1  # 每次执行一个API测试，计数加1

        if self.api_test_count % 5 == 0:
            self.update_token()  # 在每执行5个API测试之后更新一次token

        print("\n【" + self.case_name + "】Start test case")

    def update_token(self):
        # 发送请求获取新的token
        # 这里假设获取token的接口为 '/get_token'
        token_url = base_url + '/get_token'
        token_response = requestResult.run('GET', url=token_url)
        new_token = token_response.json().get('token')

        # 将新的token设置到headers中
        if new_token:
            self.headers = {'Content-Type': 'application/json', 'token': new_token}
            print('Updated Token:', new_token)

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
        print('【request_body】', self.param,type(self.param))
        r = requestResult.run(self.method, url=url, headers=self.headers, param=self.param)
        print ('【response】', r.json())
        print('【status_code】', r.status_code)

        # 断言请求返回值和excel中的status_code一致
        self.assertEqual(r.status_code, self.status_code)

        if r.status_code == 200:
            result = r.json()
            self.assertNotEqual(len(result), 0)
            self.assertNotEqual(len(self.expectation), 0)

            # self.expectation = json.loads(self.expectation)
            # actual_result = f'"{json.dumps(result, sort_keys=True,indent=4)}"'.replace("'", "\"")
            actual_result = result

            print('【actual_result】',actual_result)
            # expectation_result= json.dumps(self.expectation, sort_keys=True,indent=4).replace("'", "\"")
            expectation_result = json.loads(self.expectation)
            print('【expectation_result】',expectation_result)

            self.assertEqual(actual_result,expectation_result)

            # for key, value in self.expectation.items():
            #     self.assertNotEqual(report[key], value)
            # self.assertNotEqual(result['result'], '')
            # self.assertEqual(result['code'], 200)
        else:
            print("【" + self.case_name + "】 --- 测试用例接口请求失败！")



if __name__ == '__main__':
    unittest.main()
