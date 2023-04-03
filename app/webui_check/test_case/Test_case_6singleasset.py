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
from PageObject.SingleAssetPage import SingleAsset
from PageObject.HomePage import HomePage

with open(basepath + "/Config/singleasset.csv", "r",encoding="utf-8") as rf:
    myread = csv.reader(rf)
    keylist = list(myread)


class MyTestsingle(BaseCase):
    '''
    @parameterized.expand()
    '''

    @parameterized.expand(keylist)
    # @pytest.mark.run(order=1)
    def test_case_mrflut(self,user,password,Cu,Cu1,Cuname,Cetype,Cenum,AMPS,Aratio,years,Divi,Doset,Curisk,Riskmatch):
        self.open(HomePage.html)
        self.type(HomePage.username_login, user)
        self.type(HomePage.pwd_login, password)
        self.click(HomePage.submit_login)
        self.wait_for_element_visible(SingleAsset.SingleAsset_link)
        self.click(SingleAsset.SingleAsset_link)

        self.wait_for_element_visible(SingleAsset.SingleAsset_title)
        self.assert_text("单一资产管理计划意向确认书")
        # yield filter()
        self.type(SingleAsset.Customer_Number, Cu)
        self.type(SingleAsset.Customer_Number1, Cu1)
        self.click(SingleAsset.Certificate_Go)
        self.type(SingleAsset.Customer_name, Cuname)
        # self.type(SingleAsset.Certificate_type, Cetype)
        self.type(SingleAsset.Certificate_type,Cetype)
        self.type(SingleAsset.Certificate_number, Cenum)
        self.type(SingleAsset.Asset_MP_Strategy, AMPS)
        # time.sleep(5)
        self.type(SingleAsset.Asset_a_ratio, Aratio)
        self.type(SingleAsset.Term_years, years)
        self.type(SingleAsset.Dividend_or_not, Divi)
        self.type(SingleAsset.Downlink_wl_set, Doset)
        self.type(SingleAsset.Customer_risk_tolerance, Curisk)
        self.type(SingleAsset.Risk_level_matching_result, Riskmatch)

        time.sleep(5)
        self.click(SingleAsset.PDF_submit)
        self.wait_for_element_visible(SingleAsset.PDF_download)
        time.sleep(3)
        self.click(SingleAsset.PDF_download)
        time.sleep(2)
        self.click(SingleAsset.Back_HomePage)
        time.sleep(1)





