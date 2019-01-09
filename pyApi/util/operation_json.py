# coding=utf-8
import json


class OpenJson:

    def __init__(self):
        self.data = self.operation_json()

    # 读取json
    def operation_json(self):
        with open("../test_file/data.json") as fp:
            data = json.load(fp)
            return data

    # 根据关键字获取数据
    def get_data(self, ids):
        return self.data[ids]


# if __name__ == '__main__':
#     op = OpenJson()
#     print(op.get_data('login'))
