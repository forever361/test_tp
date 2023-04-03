#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(basepath)
import unittest
from selenium import webdriver


class TestGetElementInfo(unittest.TestCase):

    def setUp(self):
        # setUp是一个初始化方法，为test案例做数据准备
        # 当前方法的数据准备动作是：启动chrome浏览器
        self.b=webdriver.Chrome()

    def test_get_element_info(self):
        url="http://www.baidu.com"
        # 访问百度
        self.b.get(url)
        # 定位百度首页的【新闻】链接
        element=self.b.find_element_by_xpath("//div[@id='s-top-left']/a[1]")
        # 获取元素的文本
        ele_text=element.text
        print("元素的文本是：",ele_text)
        # 断言元素的文本，是否跟预期结果一样（这里的预期结果是“新闻”）
        self.assertEqual(ele_text,u"新闻")

