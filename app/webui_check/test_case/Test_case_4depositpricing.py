#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

import time
import pytest
import csv
from seleniumbase import BaseCase
from parameterized import parameterized
from PageObject.DepositPricingPage import DepositPricingPage
from PageObject.HomePage import HomePage
with open(basepath + "/Config/depositpricing.csv", "r", encoding="utf-8") as rf:
    myread = csv.reader(rf)
    keylist = list(myread)


class MyTestdepositpricing(BaseCase):
    '''
    @parameterized.expand(data)
    '''

    @parameterized.expand(keylist)
    # @pytest.mark.run(order=1)
    def test_case_mrflut(self,user,password,CuNo,CuNo1,TPACuTe,TPACuTe1,NewFund,TPAAm,FundArr):
        self.open(HomePage.html)
        self.type(HomePage.username_login, user)
        self.type(HomePage.pwd_login, password)
        self.click(HomePage.submit_login)
        self.wait_for_element_visible(DepositPricingPage.DepositPricingPage_link)
        self.click(DepositPricingPage.DepositPricingPage_link)
        self.assert_text("Application Details")
        # yield filter()
        self.click(DepositPricingPage.Single_Case)
        self.type(DepositPricingPage.Customer_No, CuNo)
        self.type(DepositPricingPage.Customer_No1, CuNo1)
        self.type(DepositPricingPage.TPA_Currency_Tenor, TPACuTe)
        self.type(DepositPricingPage.TPA_Currency_Tenor1,TPACuTe1)
        self.type(DepositPricingPage.New_Fund, NewFund)
        self.type(DepositPricingPage.TPA_Amount, TPAAm)
        time.sleep(2)
        if FundArr == "资金未到账":
            self.click(DepositPricingPage.Funds_not_arrived)
            # self.click(DepositPricingPage.Calculate)
            # self.click(DepositPricingPage.Reset)
            time.sleep(2)
            self.assert_text("TMD Preference Recommendation")
            self.assert_element(DepositPricingPage.TMD_Recommendation)
            self.assert_text(DepositPricingPage.Bulletin_Board)
            self.assert_text(DepositPricingPage.Bulletin_Board_Text1)
            self.assert_text(DepositPricingPage.Bulletin_Board_Text2)
            self.assert_text(DepositPricingPage.TPA_application_process)
            self.assert_text(DepositPricingPage.TPA_application_process1)
            self.assert_text(DepositPricingPage.TPA_application_process2)
            self.assert_text(DepositPricingPage.TPA_application_process3)
            self.assert_text(DepositPricingPage.TPA_application_process4)
            self.assert_element(DepositPricingPage.Useful_Info)
            time.sleep(1)
            self.click(DepositPricingPage.Useful_Info)
            self.click(DepositPricingPage.TPA_application_process5)
            time.sleep(3)

        else:
            self.click(DepositPricingPage.Funds_not_arrived)
            self.click(DepositPricingPage.Calculate)
            time.sleep(1)
            # self.click(DepositPricingPage.Reset)
            self.click(DepositPricingPage.Back_HomePage)





