# coding=utf-8
import json
"""
判断返回数据与预期结果是否一致
"""


class CommonUtil:

    # 判断返回数据与预期结果是否一致
    def is_contain(self, expcet, re):
        """
        :param expcet: 预期结果中的数据
        :param re: 实际返回的数据
        :return: 接口返回数据中包含预期数据，返回True，否则返回False
        """
        mx = None
        dicts = json.loads(re, strict=False)
        context = dicts.get('context')
        str_expcet = self.change_type(expcet)
        if expcet is None:
            if dicts.get('status') == '200':
                return True
            else:
                return False
        else:
            if isinstance(context, dict):
                for i in context.values():
                    str_i = self.change_type(i)
                    if str_expcet == str_i:
                        return True
                    else:
                        mx = False
            elif isinstance(context, list):
                return self.is_contain_list(context, expcet)

            return mx

    # 返回数据json中包含列表，遍历列表查看预期结果是否一致
    def is_contain_list(self, data, want):
        """
        :param data:    传入实际返回数据 context 中为列表的数据
        :param want:    预期结果中的数据
        :return:
        """
        mx = None
        wants = self.change_type(want)
        for i in data:                  # 取出列表中的每个字典
            if type(i) == dict:
                for j in i.values():    # 判断每个字典中是否包含预期结果
                    mxc = self.change_type(j)
                    if wants == mxc:
                        return True
                    else:
                        mx = False
        return mx

    # 将excel中读取的数据转换为str 类型
    def change_type(self, value):
        if value is None:
            return value
        else:
            if isinstance(value, str):
                return value
            elif isinstance(value, int):
                return str(value)
            else:
                return str(int(value))
