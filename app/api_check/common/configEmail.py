import os
import win32com.client as win32
from common import readConfig, getPath


subject = readConfig.GetConfig().email_subject
print(subject)
email_flag = readConfig.GetConfig().email_flag
app = readConfig.GetConfig().email_app
addr = readConfig.GetConfig().email_addr
cc = readConfig.GetConfig().email_cc
path = getPath.get_path()


class SendEmail:
    def __init__(self, attachment):
        outlook = win32.Dispatch("%s.Application" % app)
        # mail = outlook.CreateItem(win32.constants.olMailItem)
        self.mail = outlook.CreateItem(0)
        self.mail.To = addr
        self.mail.CC = cc
        self.mail.Subject = subject
        self.attachment_path = os.path.join(path, 'report', attachment)
        print('attachment_path', self.attachment_path)

    def outlook(self):
        self.mail.Attachments.Add(self.attachment_path, 1, 1, "myFile")     # 设置邮件附件
        self.mail.Body = self.get_content()

        # self.mail.BodyFormat = 2         # 邮件使用HTML格式
        # content = self.get_content()     # HTML格式内容设置为测试报告HTML文件的内容
        # c1 = """
        #     <html>
        #     <title>this is title
        #     </title>
        #     <body>
        #     <h2>this is body(h2）</h2>
        #     <iframe src="F:/workspaceForPython/pyApiTest/autoApiTest/report/1.html"""
        # c2 = """" width="800" height="600"
        #     frameborder="1" name="demo"
        #     scrolling="auto">
        #     </iframe>
        #     </body>
        #     </html>
        #     """
        # self.mail.HTMLBody = """
        #                 <html>
        #                 <title>this is title
        #                 </title>
        #                 <body>
        #                 <h2>this is body(h2)
        #                 <iframe src="self.get_content()">
        #                 </iframe>
        #                 </body>
        #                 </html>
        #                 """
        # content = c1 + c2
        # self.mail.HTMLBody = content
        # print('content', content)
        self.mail.Send()

    def get_content(self):
        # 设置默认邮件正文
        content = """
                    测试报告结果请参考附件。
                    """

        # 从测试报告（HTML文件）中取出文本内容
        # try:
        #     with open(self.attachment_path, "r", encoding="utf-8") as f:
        #         content = f.read()
        # except FileNotFoundError:
        #     # raise
        #     print('\n以下路径中找不到文件attachment_path:\n', self.attachment_path)
        #     pass

        return content


if __name__ == '__main__':
    SendEmail('2020-02-26 16_15_52_report.html').outlook()
    print("send mail ok!")
