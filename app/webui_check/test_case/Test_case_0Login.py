#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import time
import pytest
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(basepath)

import time
import csv
from seleniumbase import BaseCase
from parameterized import parameterized
from PageObject.HomePage import HomePage
from capabilities import cap_file

with open(basepath + "/Config/loginhome.csv", "r", encoding="utf-8") as rf:
    myread = csv.reader(rf)
    keylist = list(myread)

def average_time (csv):
    f = open(csv,"a",encoding='utf-8-sig')
    Sum = 0
    row_count = 0
    for row in f:
        n=float(row)
        Sum += n
        row_count += 1
    print(row_count)
    average = Sum / row_count
    f.close()
    return average

class MyTestSuite(BaseCase):

    #DDT参数化,传一次参数执行一次用例
    '''
    @parameterized.expand(
        [
            ["43917800","P@ssword12"],
            ["","P@ssword12"],
            ["43917800",""],
            ["4391780","P@ssword12"]
        ]
    )
    '''
    @parameterized.expand(keylist)
    # @pytest.mark.skip()
    # @pytest.mark.run(order=1)
    #不同用户名密码组合
    def test_case_login(self,name,pwd):
        self.open(HomePage.html)
        self.type(HomePage.username_login, name)
        self.type(HomePage.pwd_login, pwd)

        startTmie = int(time.time() * 1000)
        self.click(HomePage.submit_login)
        self.sleep(3)
        finishTime = int(time.time() * 1000)
        respinseTime = finishTime - startTmie

        list = []
        list.append(respinseTime)

        with open(basepath + "/Report/RM360_Page__response_time.csv", "a", newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(list)

        # with open("/Report/RM360_Page__response_time.csv", "r") as f:
        #     reader = csv.reader(f)
        #     # 这里不需要readlines
        #     for line in reader:
        #         print(line,"****************")


        # if "43917800" == name and "P@ssword12" == pwd:
        #     self.assert_text('RBWM Web Tools')
        #     self.sleep(5)
        # elif "" == name:
        #     self.assert_text('"usr": Value is required.')
        # elif "" == pwd:
        #     self.click(HomePage.pwd_login)
        #     self.assert_text('"pwd": Value is required.')
        # elif "4391780" == name:
        #     self.assert_text("Your ID/Password is incorrect.")
        # elif "P@ssword" == pwd:
        #     self.assert_text("Your ID/Password is incorrect.")
        # elif "4391780" == name and "P@ssword12" == pwd:
        #     self.assert_text("You are not authenticated user.")

        if "4391" == name and "P@ssword12" == pwd:
            self.assert_text("Yaou are not authenticated user.")

    # @pytest.mark.skip()
    # def test_response_time(self):
    #     avetime = average_time(basepath + "/Report/RM360_Page__response_time.csv")
    #     new_list = ['average_response_time：',avetime]
    #     with open(basepath + "/Report/RM360_Page__response_time.csv", "a", newline='',encoding="utf-8") as f:
    #         csv_writer = csv.writer(f)
    #         csv_writer.writerow(new_list)
