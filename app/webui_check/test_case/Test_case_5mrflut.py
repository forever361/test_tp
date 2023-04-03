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
from PageObject.MRFLUT import MRFLUT
from PageObject.HomePage import HomePage

with open(basepath + "/Config/mrf_lut.csv", "r", encoding="utf-8") as rf:
    myread = csv.reader(rf)
    keylist = list(myread)


class MyTestSuite(BaseCase):
    '''
    @parameterized.expand(
        [
            ["MRF","e.g. PUD","43917800","4516994801","Mr.w"],
            ["LUT","e.g. PUD","43917801","4516994802","Mr.w"]
        ]
    )'''


    @parameterized.expand(keylist)
    # @pytest.mark.run(order=1)
    def test_case_mrflut(self,mrfForm,code,salesname,salesnum,fundsalesoh):
        self.open(HomePage.html)
        self.type(HomePage.username_login,"43917800")
        self.type(HomePage.pwd_login, "P@ssword12")
        self.click(HomePage.submit_login)
        self.wait_for_element_visible(MRFLUT.ML_link)
        self.click(MRFLUT.ML_link)
        self.wait_for_element_visible(MRFLUT.mrfForm_div)
        self.assert_text("类别")
        # yield filter()
        if mrfForm == "MRF":
            self.click(MRFLUT.mrfForm_type, mrfForm)
            self.type(MRFLUT.branch_code, code)
            self.type(MRFLUT.Salesperson_name, salesname)
            self.type(MRFLUT.Salesperson_num, salesnum)
            self.type(MRFLUT.Fundsales_oh, fundsalesoh)
            time.sleep(5)
            self.click(MRFLUT.MRFF_submit)
            self.wait_for_element_visible(MRFLUT.MRFF_download)
            self.click(MRFLUT.MRFF_download)
            time.sleep(5)
            self.click(MRFLUT.Back_HomePage)
        elif mrfForm == "LUT":
            self.click(MRFLUT.mrfForm_type1,mrfForm)
            self.type(MRFLUT.branch_code, code)
            self.type(MRFLUT.Salesperson_name, salesname)
            self.type(MRFLUT.Salesperson_num, salesnum)
            self.type(MRFLUT.Fundsales_oh, fundsalesoh)
            time.sleep(5)
            self.click(MRFLUT.MRFF_submit)
            self.wait_for_element_visible(MRFLUT.MRFF_download)
            self.click(MRFLUT.MRFF_download)
            self.click(MRFLUT.Back_HomePage)





