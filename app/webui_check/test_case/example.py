# coding=utf-8
from selenium import webdriver
import time
import traceback
from selenium.webdriver.common.by import By
from keywordselenium.actionMethod import ActionMethod
url='http://hkl20081427.hk.hsbc:20100/RBTools/pages/custinfo/mainPage.jsf'

class BasePage:
    def register(self):
        action = ActionMethod()
        self.url = url
        self.driver = webdriver.Chrome()
        # self.driver = action.open_browser('chrome')
        self.driver.get(url)
        self.driver.maximize_window()
        self.timeout = 5
        login = self.driver.find_element_by_id("login:usr")
        login.send_keys("43917800")
        login = self.driver.find_element_by_id("login:pwd")
        login.send_keys("P@ssword12")
        time.sleep(1)
        submit = self.driver.find_element_by_id("login:rb")
        submit.click()
        time.sleep(2)
        self.driver.quit()


if __name__ == '__main__':
    Baa = BasePage()
    Baa.register()