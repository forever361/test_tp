import configparser
import datetime
import os

from openpyxl import load_workbook
from openpyxl.cell import MergedCell

from app.data2_check.commom.Constant_t import Constant_id
from app.useDB import ConnectSQL
from app.application import app


class Parser(object):
    def __init__(self):
        self._html = ''


        self.STYLESHEET_TMPL = """
                <style type="text/css" media="screen">
                    body { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
                    table { font-size: 100%; }
                    .heading { float:left; width:100%; margin-top: 0ex; margin-bottom: 1ex; }
                    .heading .attribute { margin-top: 1ex; margin-bottom: 0; }
                    #result_table { text-align: center; margin: 1em 0; width: 100%; overflow: hidden; background: #FFF; color: #024457; }
                    #result_table th { border: 1px solid #FFFFFF; background-color: #167F92; color: #FFF; padding: 0.5em; }
                    #result_table td { border: 1px solid #D9E4E6; padding: 0.5em; }
                    #total_row { font-weight: bold; }
                </style>
                """



    def generate_html_from_data(self, result_data, title='Test Report'):
        startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        HEADING_TMPL = """<div class='heading'>
            <p class='attribute'><strong>Test Time: </strong> {}</p>
            <p class='attribute'><strong>Test Details: </strong></p>
            </div>
            """.format(startTime)

        self._html = '<html lang="zh">\n' \
                     '<head>\n' \
                     f'{self.STYLESHEET_TMPL}\n' \
                     f'\t<title>{title}</title>\n' \
                     '\t<style>.topBtn{position: fixed;top: 5rem;right: 0.8rem;width: 3.2rem;height: 2.2rem;background-size: 100% auto;z-index: 9999;-webkit-transition:  opacity .3s ease;}</style>\n' \
                     '</head>\n' \
                     '<body>\n' \
                     '<div style="background-color: #eee; height:100%; width:100%; align-items: center; display:flex;">\n' \
                     '<div style=" height:91%; width:100%;  margin-left: 30px;  margin-right: 30px; margin-top: 10px; margin-bottom: 10px; "class="card">\n' \
                     '<div class="card-body">\n' \
                     '<h4 class="card-title">Test Report</h4>\n' \
                     '<div class="card-text">\n' \
                     f'{HEADING_TMPL}\n' \
                     '\t<table id=result_table>\n' \
                     '<thead>\n' \
                     '<tr>\n'

        # Table headers
        headers = ["Source Table", "Target Table", "Source Count", "Target Count", "Count Result", "Value Result",
                   "Rule", "Value detail"]
        for header in headers:
            self._html += f'\t\t<th>{header}</th>\n'
        self._html += '\t</tr>\n</thead>\n<tbody>\n'

        # Table rows
        for item in result_data['test detail']:
            self._html += '\t<tr>\n'
            for header in headers:
                key = header if header != "Value Result" else "Value Result"
                value = item[key]
                if header == "Value detail":
                    value = f'<a href="{value}" target="_blank">AttachmentLink>></a>'
                self._html += f'\t\t<td>{value}</td>\n'
            self._html += '\t</tr>\n'

        self._html += '\t</tbody>\n</table>\n</body>\n</html>'
        return self._html

    def save_html(self):

        user_id = Constant_id().cookie_id
        folder_path = os.path.join(app.root_path, 'static', 'user_files', str(user_id))
        user_path_html = folder_path + '/html/' 
        # user_path_config = folder_path + '/config/'

        # iniPath = os.path.join(user_path_config + "config.ini")
        # config = configparser.ConfigParser()
        # config.read(iniPath)  # 读取 ini 文件
        # caseid = config.get('default', 'caseid')
        # print(11111, caseid)
        caseid = Constant_id().case_id
        html_dir = os.path.join(user_path_html + "{}_data_test.html").format(caseid)
      
        # print('111save report', html_dir)
        with open(html_dir, 'w', encoding='utf-8') as f:
            f.write(self._html)

    def gen_html(self,result_data=None):
        if result_data:
            self.generate_html_from_data(result_data)
        self.save_html()



if __name__ == '__main__':
    parser = Parser()
    parser.gen_html()

