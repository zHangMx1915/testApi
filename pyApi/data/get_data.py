# coding=utf-8
from util.opertion_excel import OperationExcel
from data import data_config
from util import operation_json
"""
获取表格数据
"""


class GetData:

    def __init__(self):
        self.opera_excel = OperationExcel()

    # 获取excel行数,就是case的条数
    def get_case_lines(self):
        return self.opera_excel.get_lines()

    # 获取case是否执行
    def get_is_run(self, row):
        col = data_config.get_run()
        data = self.opera_excel.get_cell_value(row, col)
        if data == 'yes':
            flag = True
        else:
            flag = False
        return flag

    # 是否携带header
    def is_header(self, row):
        col = data_config.get_header()
        data = self.opera_excel.get_cell_value(row, col)
        if data == 'yes':
            return data_config.get_header()
        else:
            return None

    # 获取request方式
    def get_request_method(self, row):
        col = int(data_config.get_request_way())
        return self.opera_excel.get_cell_value(row, col)

    # 获取url
    def get_url(self, row):
        col = data_config.get_url()
        return self.opera_excel.get_cell_value(row, col)

    # 获取请求data
    def get_request_data(self, row):
        col = data_config.get_data()
        data = self.opera_excel.get_cell_value(row, col)
        if data == '':
            return None
        return data

    # 获取依赖case_id
    def get_depende_data(self, row):
        col = data_config.get_case_depend()
        return self.opera_excel.get_cell_value(row, col)

    # 获取依赖的值
    def get_value_depen(self, row):
        col = data_config.get_data_depend()
        return self.opera_excel.get_cell_value(row, col)

    # 获取依赖数据所属字段
    def get_field_belong_depend(self, row):
        col = data_config.get_field_depend()
        return self.opera_excel.get_cell_value(row, col)

    # 通过获取关键字拿到data数据
    def get_data_json(self, row):
        oper = operation_json.OpenJson()
        return oper.get_data(self.get_request_data(row))

    # 获取预期结果
    def get_expcet_data(self, row):
        col = data_config.get_expect()
        data = self.opera_excel.get_cell_value(row, col)
        if data == '':
            return None
        return data

    # 向Excel写入实际结果
    def write_data(self, row, value):
        col = data_config.get_result()
        self.opera_excel.write_value(row, col, value)
