from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from util.send_mail import SendEmail
from data.dependat_data import DependatData
import json


class RunTest:

    def __init__(self):
        self.run_method = RunMethod()
        self.data = GetData()
        self.expcet = CommonUtil()           # 预期结果
        self.depen = DependatData()
        self.sendemail = SendEmail()

    def go_on_run(self, url_name):
        pass_count = []
        fail_count = []
        notrun_count = []
        row_count = self.data.get_case_lines()
        for i in range(1, row_count):
            is_run = self.data.get_is_run(i)
            if is_run:                                  # 判断是否执行
                method = self.data.get_request_method(i)
                api = self.data.get_url(i)
                url = url_name + api
                header = self.data.is_header(i)
                depen_data = self.depen.run_depend_value(i)                     # 处理有依赖的接口数据
                if depen_data == None:
                    data = self.data.get_data_json(i)
                    re = self.run_method.run_main(method, url, data, header)    # 实际返回
                else:
                    re = self.run_method.run_main(method, url, depen_data, header)  # 实际返回
                expcet_data = self.data.get_expcet_data(i)                          # 预期结果
                yq = self.expcet.is_contain(expcet_data, re)                        # 判断返回结果和预期结果是否一致
                if yq:
                    self.data.write_data(i, 'pass%s' % re)
                    pass_count.append(i)
                    print('第%s条用例: 测试通过!' % i, re)
                else:
                    self.data.write_data(i, 'fail%s' % re)
                    fail_count.append(i)
                    print('第%s条用例: 测试失败!' % i, re)
            else:
                print('第%s条用例未执行！' % i)
                notrun_count.append(i)
        self.sendemail.send_main(pass_count, fail_count)
        print('执行通过：', len(pass_count))
        print('执行失败：', len(fail_count))
        print('未执行：', len(notrun_count))


if __name__ == '__main__':
    with open("../test_file/data_config.json") as fp:
            data = json.load(fp)
    url_name = data['url_test']
    url = data['url']
    run = RunTest()
    run.go_on_run(url_name)
