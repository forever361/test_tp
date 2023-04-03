#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(basepath)

import pytest
import csv
import pandas as pd
from seleniumbase import BaseCase
from selenium import webdriver
from parameterized import parameterized
from PageObject.HomePage import HomePage
from PageObject.CustomerProfilesPage import CustomerProfilesPage
from Config.ts_time import Ts_time
Time = Ts_time()

with open(basepath + "/Config/customerprofiles_test.csv", "r", encoding="utf-8") as rf:
    myread = csv.reader(rf)
    mylist = list(myread)

def xh_avg():
    with open(basepath + "/Report/Page2_res_time.csv",'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
        print("rows::::",rows)
        row_number = rows
        row_numberss = row_number[1][2]
        print("row_numberss>>>>>",row_numberss)
        row_s = len(row_number)
        print("row_s:::",row_number)
        columns = row_number[1]
        # columns_s = len(columns)
        print("columns_s:::",columns)
        # for A1 in range(0,row_s-1):
        #     for C1 in range(0,columns_s-1):
        BBB = 0
        CCC = 0
        DDD = 0
        # EEE = 0
        # FFF = 0
        # for C1 in range(0, columns_s):
        for A1 in range(0, row_s):
            BBB += int(row_number[A1][0])
            print("BBB>>>",BBB)
            CCC += int(row_number[A1][1])
            print("CCC>>>", CCC)
            DDD += int(row_number[A1][2])
            print("DDD>>>", DDD)
            # EEE += int(row_number[A1][3])
            # print("EEE>>>", EEE)
            # FFF += int(row_number[A1][4])
            # print("FFF>>>", FFF)
        avg = BBB / row_s
        avg1 = CCC / row_s
        avg2 = DDD / row_s

        av = 'Cus_Responsetime:'+ str(int(avg))
        av1 = 'SecB_Responsetime:' + str(int(avg1))
        av2 = 'Exit_Responsetime:' + str(int(avg2))
        # av3 = 'xxx:' + str(int(avg))
        list = [av, av1, av2]
        # avg4 = FFF / row_s
        print("avg:::::",avg,avg1,avg2)
        return list

class MyTestSuite(BaseCase):
    @parameterized.expand(mylist)
    @pytest.mark.run(order=1)
    def test_case_CustomerProfiles(self,user,password,PanelT,Cus1,Cus2,Cusname,CusAr,CusArp,TRBB,AUDD,TRBBIn1,TRBBIn2,TMDti1,TMDti2,TMDti3,Cusla1,Cusla2,Currca,Fundf,
                                   Sort1,Sort2,Custy,Gender,age,country,birthday,career,PRQ,TRB,RM,Resident,source):
        self.message_duration = 0.5
        self.highlights = 1
        self.open(HomePage.html)
        self.type(HomePage.username_login, user)
        self.type(HomePage.pwd_login, password)
        self.click(HomePage.submit_login)
        self.assert_element(CustomerProfilesPage.CP_link)
        # self.wait_for_element_visible(CustomerProfilesPage.CP_link)
        start_Time = Time.Times()
        self.click(CustomerProfilesPage.CP_link)
        self.assert_text("条件查询")
        end_Time = Time.Times()
        Page2_onload_time = end_Time - start_Time
        print("Page2_Response_time：",Page2_onload_time)

        #入参查询
        self.click(CustomerProfilesPage.PanelToggle)
        self.type(CustomerProfilesPage.Custinfo_id1, Cus1)
        self.type(CustomerProfilesPage.Custinfo_id2, Cus2)
        start_Time1 = Time.Times()
        self.click(CustomerProfilesPage.search_button)
        end_Time1 = Time.Times()
        Ser_res_time = end_Time1 - start_Time1
        print("Search_B_Response_time：",Ser_res_time)
        # list1 = []
        # list1.append(Ser_res_time)
        # self.click(CustomerProfilesPage.clear_button)

        ##重置后无参查询响应时间
        # start_Time2 = Time.Times()
        # self.click(CustomerProfilesPage.search_button)
        # end_Time2 = Time.Times()
        # Ser2_res_time = end_Time2 - start_Time2
        # print("无参查询响应时间：",Ser2_res_time)
        # list2 = []
        # list2.append(Ser2_res_time)
        ####退出Page2页面响应时间

        EXIT_start_Time = Time.Times()
        self.click(CustomerProfilesPage.exit_button)
        EXIT_end_Time = Time.Times()
        Exit_res_time = EXIT_end_Time - EXIT_start_Time
        print("ExitCusPro_Response_time：",Exit_res_time)
        # list = [Ser_res_time,Ser2_res_time,Exit_res_time]
        # list = []
        # list.append([Ser_res_time,Ser2_res_time,Exit_res_time])

        with open(basepath + "/Report/Page2_res_time.csv", "a", newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([Page2_onload_time,Ser_res_time,Exit_res_time])

    def test_response_time(self):
        Avgstime = xh_avg()
        # new_list = [avgtime]
        with open(basepath + "/Report/Page2_res_time.csv", "a", newline='', encoding="utf-8") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(Avgstime)
            print(Avgstime)
            f.close()


