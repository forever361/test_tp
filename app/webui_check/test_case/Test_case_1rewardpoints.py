#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(basepath)

import pytest
import csv
from seleniumbase import BaseCase
from parameterized import parameterized
from PageObject.RewardPointsPage import RewardPointsPage
from PageObject.HomePage import HomePage
with open(basepath + "/Config/rewardpoints.csv", "r", encoding="utf-8") as rf1:
    myread1 = csv.reader(rf1)
    mylist1 = list(myread1)


class MyTestSuite(BaseCase):

    @parameterized.expand(mylist1)
    # @pytest.mark.skip("skip")
    @pytest.mark.run(order=1)
    def test_case_RewardPoints(self, user, pwd, Cnum, Cnum1, Prange):
        self.message_duration = 0.5
        self.highlights = 1

        self.open(HomePage.html)
        self.type(HomePage.username_login, user)
        self.type(HomePage.pwd_login, pwd)
        self.click(HomePage.submit_login)

        self.wait_for_element_visible(RewardPointsPage.RB_link)
        self.click(RewardPointsPage.RB_link)
        self.assert_text("客户经理")
        # self.click(RewardPointsPage.Account_Manager)
        self.click(RewardPointsPage.Points_balance_search)
        self.assert_text("客户号码")
        self.type(RewardPointsPage.Customer_Num, Cnum)
        self.type(RewardPointsPage.Customer_Num1, Cnum1)
        self.click(RewardPointsPage.search_button)
        self.click(RewardPointsPage.exit_button)
        self.assert_text('RBWM Web Tools')

        self.click(RewardPointsPage.RB_link)
        self.assert_text("支行行长")
        self.click(RewardPointsPage.Batch_download)
        self.assert_text("选择积分范围 ( >= )")
        self.type(RewardPointsPage.Points_range, Prange)
        self.click(RewardPointsPage.download_submit)
        self.assert_text("SBM / Division Manager / City Manager use only !")



