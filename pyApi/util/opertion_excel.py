# coding=utf-8
import json
import xlrd
from xlutils.copy import copy

"""读取和写入Excel文件"""


class OperationExcel:

    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = '../test_file/case.xlsx'
            self.sheet_id = 0
        self.data = self.get_data()

    # 获取sheet的内容
    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables

    # 获取表格的行数
    def get_lines(self):
        tables = self.get_data()
        return tables.nrows

    # 获取某一单元格内容
    def get_cell_value(self, row, col):
        return self.data.cell_value(row, col)

    # 返回数据写入Excel实际结果
    def write_value(self, row, col, value):
        read_data = xlrd.open_workbook(self.file_name, formatting_info=True)    # formatting_info=True:保持表格的单元格格式
        write_data = copy(read_data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(row, col, value)
        write_data.save(self.file_name)


# 获取依赖的case_id 的对应行的行号
class GetRowNum(OperationExcel):

    # 根据对应的case_id 找到对应的行号
    def get_row_num(self, case_id):
        row_nom = 0
        col_value = self.get_cols_data()
        for i in col_value:
            if case_id == i:
                return row_nom
            else:
                row_nom += 1

    # 获取某一列的内容
    def get_cols_data(self, col_id=None):
        if col_id:
            col_value = self.data.cell_value(col_id)
        else:
            col_value = self.data.col_values(0)
        return col_value

    # 获取依赖对应的值
    def get_depen_value(self, row, col):
        return self.data.cell_value(row, col)
