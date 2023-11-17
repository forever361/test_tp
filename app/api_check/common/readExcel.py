import os
import common.getPath as getPath
from xlrd import open_workbook


# 取得项目根目录
path = getPath.get_path()


class ReadExcel():
    def get_xls(self, xls_name, sheet_name):
        cls = []
        # 获取用例文件路径
        xlsPath = os.path.join(path, 'case', xls_name)
        file = open_workbook(xlsPath)
        sheet = file.sheet_by_name(sheet_name)
        # 取得这个sheet内容行数
        rows = sheet.nrows
        for i in range(rows):
            if sheet.row_values(i)[0] != u'case_name':
                cls.append(sheet.row_values(i))
        return cls


if __name__ == '__main__':
    # 测试下取到的excel值是否正确
    print(ReadExcel().get_xls('ptl.xlsx', 'Sheet1'))
    print(ReadExcel().get_xls('ptl.xlsx', 'Sheet1')[0][1])
    print(ReadExcel().get_xls('ptl.xlsx', 'Sheet1')[1][2])
    param = ReadExcel().get_xls('ptl.xlsx', 'Sheet1')[3][3]
    print(param)
    print(type(param))
    print(type(eval(param)))
