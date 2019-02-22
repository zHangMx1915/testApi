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
        if ids == None:
            return None
        else:
            return self.data[ids]


# if __name__ == '__main__':
#     op = OpenJson()
#     print(op.get_data('login'))
