import sys
sys.path.append('../')


from seleniumbase import BaseCase

class MyTestSuite(BaseCase):

    # @pytest.mark.run(order=2)
    def test_case_CustomerProfiles(self):
        # self.message_duration = 0.5
        # self.highlights = 1
        # self.demo_mode = True
        # # self.slow_mode = True


        self.open("http://hkl20081427.hk.hsbc:20101/RBTools/pages/points/search.jsf")
        self.type('#login\\:usr', "43917800")
        self.type("#login\\:pwd", "P@ssword12")
        self.click("#login\\:rb")

        self.assert_exact_text("RBWM Web Tools", "h2")









