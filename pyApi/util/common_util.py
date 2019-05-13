# coding=utf-8
import json
"""
判断返回数据与预期结果是否一致
"""


class CommonUtil:

    def is_contain(self, expcet, re):
        mx = ''
        dicts = json.loads(re, strict=False)
        context = dicts.get('context')
        str_expcet = self.change_type(expcet)
        message = dicts.get('message')
        if expcet:
            if str_expcet == message:
                mx = 1
            else:
                mx = 0
        elif expcet is None:
            mx = 2
        else:
            if isinstance(context, dict):
                for i in context.values():
                    if str_expcet == self.change_type(i):
                        mx = 1
                    else:
                        mx = 0
            elif isinstance(context, list):
                mx = self.is_contain_list(context, expcet)
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
                        mx = 1
                    else:
                        mx = 0
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
