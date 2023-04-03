import sys
sys.path.append('../')

import pytest
from seleniumbase import BaseCase
from parameterized import parameterized
from PageObject.RewardPointsPage import RewardPointsPage
from PageObject.PortfolioReviewPage import PortfolioReviewPage
from PageObject.HomePage import HomePage
from PageObject.CustomerProfilesPage import CustomerProfilesPage


class MyTestSuite(BaseCase):

    # @pytest.mark.run(order=2)
    def test_case_CustomerProfiles(self):
        self.message_duration = 0.5
        self.highlights = 1
        # self.demo_mode = True
        self.slow_mode = True


        self.open(HomePage.html)
        self.type(HomePage.username_login, "43917800")
        self.type(HomePage.pwd_login, "P@ssword12")
        self.click(HomePage.submit_login)
        self.wait_for_element_visible(CustomerProfilesPage.CP_link)
        self.click(CustomerProfilesPage.CP_link)
        self.assert_text("条件查询")

        self.click(CustomerProfilesPage.PanelToggle)
        self.type(CustomerProfilesPage.Custinfo_id1, "001")
        self.type(CustomerProfilesPage.Custinfo_id2, "002378")
        self.click(CustomerProfilesPage.search_button)

        if self.is_element_visible('a[id="custinfosearch:_idJsp507:1:_idJsp509"]'):
            self.click('a[id="custinfosearch:_idJsp507:1:_idJsp509"]')
        elif self.is_element_visible('a[id="custinfosearch:_idJsp507:18:_idJsp509"]'):
            self.click('a[id="custinfosearch:_idJsp507:18:_idJsp509"]')
        elif self.is_element_visible('a[id="custinfosearch:_idJsp507:0:_idJsp509"]'):
            self.click('a[id="custinfosearch:_idJsp507:0:_idJsp509"]')
        self.assert_text("已选择客户: 001-002378")

        self.click(CustomerProfilesPage.clear_button)
        self.click(CustomerProfilesPage.PanelToggle)
        self.type(CustomerProfilesPage.Custinfo_name,"陈奇伟")
        self.click(CustomerProfilesPage.search_button)
        if self.is_element_visible('a[id="custinfosearch:_idJsp507:1:_idJsp509"]'):
            self.click('a[id="custinfosearch:_idJsp507:1:_idJsp509"]')
        elif self.is_element_visible('a[id="custinfosearch:_idJsp507:18:_idJsp509"]'):
            self.click('a[id="custinfosearch:_idJsp507:18:_idJsp509"]')
        elif self.is_element_visible('a[id="custinfosearch:_idJsp507:0:_idJsp509"]'):
            self.click('a[id="custinfosearch:_idJsp507:0:_idJsp509"]')
        self.assert_text("已选择客户: 001-068809")
        self.sleep(5)





