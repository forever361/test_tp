#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(basepath)

import pytest
import csv
import time
import pandas as pd
from seleniumbase import BaseCase
from selenium import webdriver
from parameterized import parameterized
from PageObject.HomePage import HomePage
from PageObject.CustomerProfilesPage import CustomerProfilesPage

with open(basepath + "/Config/customerprofiles02.csv", "r", encoding="utf-8") as rf2:
    myread2 = csv.reader(rf2)
    mylist2 = list(myread2)

with open(basepath + "/Config/customerprofiles03.csv", "r", encoding="utf-8") as rf3:
    myread3 = csv.reader(rf3)
    mylist3 = list(myread3)


class MyTestSuite(BaseCase):

    # @pytest.fixture(scope='function')
    def test_case_homelogin(self):
        self.message_duration = 0.5
        self.highlights = 1

        self.open(HomePage.html)
        self.type(HomePage.username_login, "43917800")
        self.type(HomePage.pwd_login, "P@ssword12")
        self.click(HomePage.submit_login)
        self.wait_for_element_visible(CustomerProfilesPage.CP_link)
        self.click(CustomerProfilesPage.CP_link)
        self.assert_text("条件查询")

    @parameterized.expand(mylist2)
    @pytest.mark.run(order=1)
    def test_case_CustomerProfiles_search(self,PanelT,Cus1,Cus2,Cusname,CusAr,CusArp,TRBB,AUDD,TRBBIn1,TRBBIn2,TMDti1,TMDti2,TMDti3,Cusla1,Cusla2,Currca,Fundf):
        self.message_duration = 0.5
        self.highlights = 1

        self.test_case_homelogin()
        self.click(CustomerProfilesPage.PanelToggle)
        if PanelT == "General":
            self.click(CustomerProfilesPage.General)
        elif PanelT == "QDUT":
            self.click(CustomerProfilesPage.QDUT)
        elif PanelT == "CPI":
            self.click(CustomerProfilesPage.CPI)
        elif PanelT == "Insurance":
            self.click(CustomerProfilesPage.Insurance)
        elif PanelT == "Leads":
            self.click(CustomerProfilesPage.Leads)
        elif PanelT == "SPI":
            self.click(CustomerProfilesPage.SPI)
        self.type(CustomerProfilesPage.Custinfo_id1, Cus1)
        self.type(CustomerProfilesPage.Custinfo_id2, Cus2)
        self.type(CustomerProfilesPage.Custinfo_name, Cusname)
        self.type(CustomerProfilesPage.Custinfo_Archives, CusAr)
        self.type(CustomerProfilesPage.Custinfo_Archives_input, CusArp)
        self.type(CustomerProfilesPage.TRB, TRBB)
        self.type(CustomerProfilesPage.AUD, AUDD)
        self.type(CustomerProfilesPage.TRB_Input1, TRBBIn1)
        self.type(CustomerProfilesPage.TRB_Input2, TRBBIn2)
        self.type(CustomerProfilesPage.TMD_to_time1, TMDti1)
        self.type(CustomerProfilesPage.TMD_to_time2, TMDti2)
        self.type(CustomerProfilesPage.TMD_to_time3, TMDti3)
        self.type(CustomerProfilesPage.Custinfo_label1, Cusla1)
        self.type(CustomerProfilesPage.Custinfo_label2, Cusla2)
        if Currca == "CPI":
            self.click(CustomerProfilesPage.Current_hold_category1)
        elif Currca == "QDUT":
            self.click(CustomerProfilesPage.Current_hold_category2)
        elif Currca == "INS":
            self.click(CustomerProfilesPage.Current_hold_category3)
        elif Currca == "TMD":
            self.click(CustomerProfilesPage.Current_hold_category4)
        elif Currca == "CC":
            self.click(CustomerProfilesPage.Current_hold_category5)
        if Fundf == "三个月内超过十万":
            self.click(CustomerProfilesPage.Fund_flow)
        time.sleep(2)
        self.click(CustomerProfilesPage.search_button)
        # for i in range(0,0):
        if self.is_element_visible('a[id="custinfosearch:_idJsp502:1:_idJsp504"]'):
            self.click('a[id="custinfosearch:_idJsp502:1:_idJsp504"]')
            # self.assert_text("已选择客户: {}-{} {}".format(Cus1, Cus2, Cusname))
            self.assert_element('a[id="custinfosearch:_idJsp502:1:_idJsp504"]')
            time.sleep(2)
        else:
            self.assert_text_not_visible("Customer is empty")

    @parameterized.expand(mylist3)
    @pytest.mark.run(order=2)
    def test_case_CustomerProfiles_sort(self,Sort1,Sort2,Custy,Gender,age,country,birthday,career,PRQ,TRB,RM,Resident,source):
        self.test_case_homelogin()
        self.click(CustomerProfilesPage.clear_button)
        self.click(CustomerProfilesPage.search_button)
        time.sleep(2)
        self.type(CustomerProfilesPage.Sort_list1, Sort1)
        self.type(CustomerProfilesPage.Sort_list2, Sort2)
        self.type(CustomerProfilesPage.Customertype_list, Custy)
        self.type(CustomerProfilesPage.Gender_list, Gender)
        self.type(CustomerProfilesPage.age_list, age)
        self.type(CustomerProfilesPage.country_list, country)
        self.type(CustomerProfilesPage.birthday_list, birthday)
        self.type(CustomerProfilesPage.career_list, career)
        self.type(CustomerProfilesPage.RPQ_list, PRQ)
        self.type(CustomerProfilesPage.TRB_list, TRB)
        self.type(CustomerProfilesPage.RM_list, RM)
        self.type(CustomerProfilesPage.Resident_list, Resident)
        self.type(CustomerProfilesPage.source_list, source)

        # 选择和断言客户
        # for i in range(0, 0):
        if self.is_element_visible('a[id="custinfosearch:_idJsp502:1:_idJsp504"]'):
            self.click('a[id="custinfosearch:_idJsp502:1:_idJsp504"]')
            # self.assert_text("已选择客户: {}-{} {}".format(Cus1, Cus2, Cusname))
            self.assert_element('a[id="custinfosearch:_idJsp502:1:_idJsp504"]')
            # self.test_customer_detail_tab1()
            # self.test_customer_detail_tab2()
        else:
            self.assert_text_not_visible("Customer is empty")

    # 执行所有detail
    def test_customer_detail(self):
        self.test_case_homelogin()
        self.click(CustomerProfilesPage.clear_button)
        self.click(CustomerProfilesPage.search_button)
        time.sleep(2)
        if self.is_element_visible('a[id="custinfosearch:_idJsp502:1:_idJsp504"]'):
            self.click('a[id="custinfosearch:_idJsp502:1:_idJsp504"]')
            self.assert_element('a[id="custinfosearch:_idJsp502:1:_idJsp504"]')
            self.test_customer_detail_tab1()
            self.test_customer_detail_tab2()
        else:
            self.assert_text_not_visible("Customer is empty")

    def test_customer_detail_tab1(self):
        self.test_case_homelogin()
        self.click(CustomerProfilesPage.C_tab1)
        self.assert_text("父母情况及供养计划")
        # self.type(CustomerProfilesPage.C_tab1_1, )
        # self.type(CustomerProfilesPage.C_tab1_2, )
        # self.type(CustomerProfilesPage.C_tab1_3, )
        # self.type(CustomerProfilesPage.C_tab1_4, )
        # self.type(CustomerProfilesPage.C_tab1_5, )
        # self.type(CustomerProfilesPage.C_tab1_6, )

        self.click(CustomerProfilesPage.C_tab2)
        self.assert_text("职业及收入")
        # self.type(CustomerProfilesPage.C_tab2_1, )
        # self.type(CustomerProfilesPage.C_tab2_2, )
        # self.type(CustomerProfilesPage.C_tab2_3, )
        # self.type(CustomerProfilesPage.C_tab2_4, )
        # self.type(CustomerProfilesPage.C_tab2_5, )
        # self.type(CustomerProfilesPage.C_tab2_6, )

        self.click(CustomerProfilesPage.C_tab3)
        self.assert_text("理财目标")
        # self.type(CustomerProfilesPage.C_tab3_1, )
        # self.type(CustomerProfilesPage.C_tab3_2, )
        # self.type(CustomerProfilesPage.C_tab3_3, )
        # self.type(CustomerProfilesPage.C_tab3_4, )
        # self.type(CustomerProfilesPage.C_tab3_5, )
        # self.type(CustomerProfilesPage.C_tab3_6, )

        self.click(CustomerProfilesPage.C_tab4)
        self.assert_element('textarea[name="custinfosearch:_idJsp818"]')
        # self.type(CustomerProfilesPage.C_tab4_1, )

        self.click(CustomerProfilesPage.C_tab5)
        self.assert_text("客户在财富传承规划中希望达成的目标")
        # self.type(CustomerProfilesPage.C_tab5_1, )
        # self.type(CustomerProfilesPage.C_tab5_2, )
        # self.type(CustomerProfilesPage.C_tab5_3, )
        # self.type(CustomerProfilesPage.C_tab5_4, )
        # self.type(CustomerProfilesPage.C_tab5_5, )
        # self.type(CustomerProfilesPage.C_tab5_6, )

        self.click(CustomerProfilesPage.C_tab6)
        self.assert_text("个人客户是否为企业主")
        # self.type(CustomerProfilesPage.C_tab6_1, )
        # self.type(CustomerProfilesPage.C_tab6_2, )
        # self.type(CustomerProfilesPage.C_tab6_3, )
        # self.type(CustomerProfilesPage.C_tab6_4, )
        # self.type(CustomerProfilesPage.C_tab6_5, )
        # self.type(CustomerProfilesPage.C_tab6_6, )

    def test_customer_detail_tab2(self):
        self.test_case_homelogin()
        self.click(CustomerProfilesPage.E_tab1)
        self.assert_text("Structure Deposit")
        self.click(CustomerProfilesPage.E_tab2)
        self.assert_text("Joint / Sole 关系")
        self.click(CustomerProfilesPage.E_tab3)
        self.click(CustomerProfilesPage.E_tab4)
        self.click(CustomerProfilesPage.E_tab5)
        self.assert_text("保单号")
        self.click(CustomerProfilesPage.E_tab6)
        self.assert_text("币种")
        self.click(CustomerProfilesPage.E_tab7)
        self.assert_text("近3个月内单笔等值人民币超过十万")
        self.click(CustomerProfilesPage.E_tab8)
        self.assert_text("WeChat")
        self.click(CustomerProfilesPage.E_tab9)
        self.assert_text("信用卡积分")
        self.click(CustomerProfilesPage.E_tab10)
        self.assert_text("Serial No.")
        self.click(CustomerProfilesPage.E_tab11)
        self.assert_text("Contacted / Appointment")
        self.click(CustomerProfilesPage.E_tab12)
        self.assert_text("SPI Info")
        self.click(CustomerProfilesPage.E_tab13)
        self.assert_text("Contact History")
        self.click(CustomerProfilesPage.E_tab14)
        self.assert_text("企业账户相关信息")
        self.click(CustomerProfilesPage.E_tab15)
        self.assert_text("是否持有信用卡")

        time.sleep(2)
        self.click(CustomerProfilesPage.exit_button)




