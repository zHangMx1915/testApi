# coding=utf-8
from util.opertion_excel import GetRowNum
from data.get_data import GetData
from base import runmethod
import json

"""处理所有数据依赖问题"""


class DependatData:

    def __init__(self):
        self.data = GetData()
        self.depen_value = GetRowNum()
        self.run_method = runmethod.RunMethod()

    # 从依赖接口的返回的数据中查找依赖的值并返回
    def run_depend_value(self, row):
        """
        如依赖所属的字段有值，则在返回值中先查找到所属字段的集合，再在该集合中查找依赖所需要的数据，
        如依赖所属的字段为空，则直接在返回值中查找依赖的值
        如依赖字段
        :param row: 行号
        :return: 查找到依赖数据则将其返回，否则返回 False
        """
        mx = {}
        da = None
        data = self.get_case_id(row)
        if data is '':
            return None
        else:
            depend_data = self.get_depen_data(row)                          # 依赖的值
            depend_belong = self.get_depend_belong(row)                     # 依赖所属的字段
            request_data = self.depen_request(row)                          # 依赖接口返回的数据
            depend_request_data = json.loads(request_data)
            depend_request_context = depend_request_data.get('context')     # 取出context返回数据
            if depend_belong is '':
                if depend_request_data.get('status') == '200':
                    dicts = json.loads(depend_request_context)
                    mx[depend_data] = dicts.get(depend_data)
                    return mx
                else:
                    return False
            else:
                for i in depend_request_context:
                    for j in i.values():
                        a = self.data_type(j)
                        b = self.data_type(depend_belong)
                        if a == b:
                            mx[depend_data] = i.get(depend_data)
                            return mx
                        else:
                            da = False
                return da

    # 执行依赖的case
    def depen_request(self, row):
        """
        1、根据依赖的行号获取对应的请求参数
        2、请求依赖的接口获取返回参数
        3、在返回参数中获取到需要的参数值
        4、将获取的值返回给主程序作为依赖的参数进行接口的请求
        5、依赖接口不须判断是否执行，全部直接执行
        """
        rows = self.get_depen_row_value(row)
        method = self.data.get_request_method(rows)
        url = self.data.get_url(rows)
        data = self.data.get_data_json(rows)
        header = self.data.is_header(rows)
        re = self.run_method.run_main(method, url, data, header)
        return re

    # 获取依赖的返回对应的依赖数据
    def get_depen_data(self, row):
        return self.data.get_value_depen(row)

    # 获取表格中依赖数据所属的字段
    def get_depend_belong(self, row):
        return self.data.get_field_belong_depend(row)

    # 获取case_id
    def get_case_id(self, row):
        return self.data.get_depende_data(row)

    # 获取依赖的行号
    def get_depen_row_value(self, row):
        case_id = self.get_case_id(row)
        return self.depen_value.get_row_num(case_id)

    # 将excel中读取的数据转换为str 类型
    def data_type(self, value):
        if value is None:
            return value
        else:
            if isinstance(value, str):
                return value
            elif isinstance(value, int):
                return str(value)
            else:
                return str(int(value))
