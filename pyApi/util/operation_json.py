# coding=utf-8
import json


class OpenJson:

    def __init__(self):
        self.data = self.operation_json()

    # 读取json
    def operation_json(self):
        with open("../test_file/data.json", 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            return data

    # 根据关键字获取数据
    def get_data(self, ids):
        """
        请求参数直接写在用例表格中时，写在{}中，判断如字符首尾为{}时，
        将建字符串转换为dict格式后直接返回，否则再去json文件中读取参数
        """
        if ids == None:
            return None
        else:
            if ids.startswith('{') and ids.endswith('}'):   # 判断是否以{}开头和结尾
                return eval(ids)                            # 将str转换为dict格式
            else:
                return self.data[ids]


# if __name__ == '__main__':
#     op = OpenJson()
#     print(op.get_data('login'))
