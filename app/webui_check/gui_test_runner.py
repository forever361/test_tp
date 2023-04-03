"""
GUI TEST RUNNER
Run by Typing: "python gui_test_runner.py"
"""

import os
import sys
sys.path.append("../")

if sys.version_info[0] >= 3:
    from tkinter import *
else:
    from tkinter import Tk, Frame, Button, Label


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.label = Label(root, width=40).pack()
        self.title = Label(frame, text="Run UI Automation Framework", fg="black").pack()

        # 设置 label 标题样式
        self.title0 = Label(
            frame,
            text=("Run a module in Chrome: 0Login"),
            fg="gray",
        ).pack()

        # 设置 Button 执行哪个py文件及样式
        self.run0 = Button(
            frame,
            command=self.run_0,
            text=("pytest Test_case_0Login.py --generate report"),
            fg="green",
            cursor="circle"
        ).pack()

        #
        self.title1 = Label(
            frame,
            text="Run a module in Chrome: 1RewardPoints",
            fg="gray",
        ).pack()

        self.run1 = Button(
            frame,
            command=self.run_1,
            text=("pytest Test_case_1rewardpoints.py --generate report"),
            fg="green",
        ).pack()


        self.title2 = Label(
            frame,
            text="Run a module in Chrome: 2CustomerProfiles2",
            fg="gray",
        ).pack()

        self.run2 = Button(
            frame,
            command=self.run_2,
            text=("pytest Test_case_2customerprofiles2.py --generate report"),
            fg="green",
        ).pack()

        self.title3 = Label(
            frame,
            text="Run a module in Chrome: 3PortfolioReview",
            fg="gray",
        ).pack()

        self.run3 = Button(
            frame,
            command=self.run_3,
            text=("pytest Test_case_3portfolioreview.py --generate report"),
            fg="green",
        ).pack()

        self.title4 = Label(
            frame,
            text="Run a module in Chrome: 4DepositPricing",
            fg="gray",
        ).pack()

        self.run4 = Button(
            frame,
            command=self.run_4,
            text=("pytest Test_case_4depositpricing.py --generate report"),
            fg="green",
        ).pack()

        self.title5 = Label(
            frame,
            text="Run a module in Chrome: 5MRFLUT",
            fg="gray",
        ).pack()

        self.run5 = Button(
            frame,
            command=self.run_5,
            text=("pytest Test_case_5mrflut.py --generate report"),
            fg="green",
        ).pack()


        self.title6 = Label(
            frame,
            text="Run a module in Chrome: 6SingleAsset",
            fg="gray",
        ).pack()
        
        self.run6 = Button(
            frame,
            command=self.run_6,
            text=("pytest Test_case_6singleasset.py --generate report"),
            fg="green"
            # fg="dark orange",
        ).pack()


        self.title7 = Label(
            frame,
            text="pytest ./test_case/test2.py --browser=chrome",
            fg="gray",
        ).pack()

        self.run7 = Button(
            frame,
            command=self.run_7,
            text=("pytest ./test_case/test2.py --generate report.html"),
            fg="dark red",
        ).pack()

        self.run8 = Button(
            frame,
            command=self.run_8,
            text=("pytest ./test_case/test2.py --generate report.html"),
            fg="dark red",
        ).pack()

        '''
        self.title8 = Label(
            frame,
            text="pytest ./test_case/Test_case_singleasset.py --browser=chrome",
            fg="blue",
        ).pack()

        self.run8 = Button(
            frame,
            command=self.run_8,
            text=("pytest ./test_case/Test_case_depositpricing.py --generate report.html"),
            fg="dark orange",
        ).pack()


        self.title9 = Label(
            frame,
            text="Run a Test with Report Mode:all_testcase",
            fg="blue",
        ).pack()

        self.run9 = Button(
            frame,
            command=self.run_9,
            text=("pytest Test_suite.py --browser=chrome --html=./Report/testlogin.html"),
            fg="dark orange",
        ).pack()
        '''
        self.end_title = Label(frame, text="", fg="black").pack()
        self.quit = Button(frame, text="QUIT", command=frame.quit).pack()

    def run_0(self):
        os.system("pytest ./test_case/Test_case_0Login.py  --dashboard --html=./Report/Test_case_0Login.html")

    def run_1(self):
        os.system("pytest ./test_case/Test_case_1rewardpoints.py --dashboard --html=./Report/Test_case_1rewardpoints.html")

    def run_2(self):
        os.system("pytest ./test_case/Test_case_2customerprofiles2.py --dashboard --html=./Report/Test_case_2customerprofiles2.html")

    def run_3(self):
        os.system("pytest ./test_case/Test_case_3portfolioreview.py --dashboard --html=./Report/Test_case_3portfolioreview.html")

    def run_4(self):
        os.system("pytest ./test_case/Test_case_4depositpricing.py --dashboard --html=./Report/Test_case_4depositpricing.html")

    def run_5(self):
        os.system("pytest ./test_case/Test_case_5mrflut.py --dashboard --html=./Report/Test_case_5mrflut.html")

    def run_6(self):
        os.system("pytest ./test_case/Test_case_6singleasset.py --dashboard --html=./Report/Test_case_6singleasset.html")

    def run_7(self):
        os.system("pytest ./test_case/test2.py  -v  --browser=chrome --demo_mode")

    def run_8(self):
        os.system("pytest ./test_case/test2.py  -v   --html=./Report/test3.html --demo_mode")

    '''
    def run_8(self):
        os.system("")

    def run_9(self):
        os.system("")

    def run_10(self):
        os.system("")

    def run_11(self):
        os.system("pytest ./test_case/Test_case_rewardportfolio.py  -v  --browser=chrome --demo_mode")

    def run_12(self):
        os.system("python ./test_case_keyword.py  -v --browser=chrome --slow_mode --html=./Report/Test_case_keyword.html")
    '''


if __name__ == "__main__":
    root = Tk()
    root.title("Select Test Job To Run")
    root.minsize(500, 220)
    app = App(root)
    root.mainloop()
