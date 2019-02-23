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
        self.pass_count = []
        self.fail_count = []
        self.notrun_count = []

    def go_on_run(self, url_name):
        row_count = self.data.get_case_lines()
        for i in range(1, row_count):
            not_re_data, yw, re = None, None, None
            is_run = self.data.get_is_run(i)
            if is_run:                                  # 判断是否执行
                method = self.data.get_request_method(i)
                api = self.data.get_url(i)
                url = url_name + api
                header = self.data.is_header(i)
                depen_data = self.depen.run_depend_value(i, url_name)               # 处理有依赖的接口数据
                if depen_data == None:
                    data = self.data.get_data_json(i)
                    if data == None:
                        not_re_data = ("第%s行的请求数据为空！" % i)
                    else:        
                        re = self.run_method.run_main(method, url, data, header)    # 实际返回
                else:
                    re = self.run_method.run_main(method, url, depen_data, header)  # 实际返回
                expcet_data = self.data.get_expcet_data(i)                          # 预期结果
                if re != None:
                    yq = self.expcet.is_contain(expcet_data, re)
                self.check(yq, expcet_data, re, i, not_re_data)
            else:
                print('Test-%s:Not running！' % i)
                self.notrun_count.append(i)
        # self.sendemail.send_main(pass_count, fail_count)                         # 发送邮件
        print('执行通过：', len(self.pass_count))
        print('执行失败：', len(self.fail_count))
        print('未执行：', len(self.notrun_count))

    def check(self, yq, expcet_data, re, i, not_re_data):
        if re == None:
            self.notrun_count.append(i)
            print('Test-%s:' % i, not_re_data)
        else:
            if yq:
                self.data.write_data(i, 'pass%s' % re)
                self.pass_count.append(i)
                print('Test-%s: Pass!' % i, re)
            else:
                self.data.write_data(i, 'fail%s' % re)
                self.fail_count.append(i)
                print('Test-%s: Fail!' % i, re)


if __name__ == '__main__':
    with open("../test_file/data_config.json") as fp:
            data = json.load(fp)
    url_name = data['url_test']
    url = data['url']
    run = RunTest()
    run.go_on_run(url_name)
