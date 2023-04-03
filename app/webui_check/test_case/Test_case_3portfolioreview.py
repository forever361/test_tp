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
from PageObject.PortfolioReviewPage import PortfolioReviewPage
from PageObject.HomePage import HomePage
from PageObject.CustomerProfilesPage import CustomerProfilesPage

with open(basepath + "/Config/portfolioreview.csv", "r", encoding="utf-8") as rf3:
    myread3 = csv.reader(rf3)
    mylist3 = list(myread3)


class MyTestSuite(BaseCase):

    @parameterized.expand(mylist3)
    @pytest.mark.run(order=3)
    # @pytest.mark.skip("skip")
    def test_case_PortfolioReview(self,user,pwd,region,division,branch,RM):
        self.message_duration = 0.5
        self.highlights = 1

        self.open(HomePage.html)
        self.type(HomePage.username_login, user)
        self.type(HomePage.pwd_login, pwd)
        self.click(HomePage.submit_login)
        self.wait_for_element_visible(PortfolioReviewPage.PR_link)
        self.click(PortfolioReviewPage.PR_link)

        self.type(PortfolioReviewPage.Region_list, region)
        self.type(PortfolioReviewPage.Division_list, division)
        self.type(PortfolioReviewPage.Branch_list, branch)
        self.type(PortfolioReviewPage.RM_list, RM)

        self.click(PortfolioReviewPage.Confirm_button)

        self.click(PortfolioReviewPage.Tab1)
        # self.assert_text("Sub Asset Class")
        self.click(PortfolioReviewPage.Tab2)
        # self.assert_element('div[id="holding:_idJsp56"]')
        self.click(PortfolioReviewPage.Tab3)
        # self.assert_text('Grand Total')
        self.click(PortfolioReviewPage.Tab4)
        # self.assert_element('div[id="holding:_idJsp85"]')
        self.click(PortfolioReviewPage.Tab5)
        # self.assert_text('Core Class')
        self.click(PortfolioReviewPage.Tab6)
        # self.assert_element('div[id="holding:_idJsp199"]')
        self.click(PortfolioReviewPage.Tab7)
        # self.assert_text('Structure')
        self.click(PortfolioReviewPage.Tab8)
        # self.assert_element('div[id="holding:_idJsp492"]')
        self.click(PortfolioReviewPage.Tab9)
        # self.assert_element('div[id="holding:_idJsp494"]')
        self.click(PortfolioReviewPage.Tab10)
        # self.assert_element('div[id="holding:_idJsp496"]')
        self.click(PortfolioReviewPage.Tab11)
        self.assert_element('div[id="holding:_idJsp498"]')

