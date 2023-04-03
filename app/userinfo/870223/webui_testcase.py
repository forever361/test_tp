#----Case_name: you must define a unique casename------------
#Case_name= casename2022_9_27_15_36

'''
This function is used to edit test cases
'''
from seleniumbase import BaseCase

class MyTestSuite(BaseCase):
	def test_case1(self):
	#----please edit your code here:----
	#####################################
		self.open("http://hkl20081427.hk.hsbc:20101/RBTools/pages/points/search.jsf")
		self.type("#login\:usr", "43917800")
		self.type("#login\:pwd", "********")
		self.click("#login\:rb")
		self.assert_exact_text("RBWM Web Tools", "h2")
