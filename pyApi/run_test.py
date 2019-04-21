# coding=utf-8
from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from util.send_mail import SendEmail
from data.dependat_data import DependatData
from util.log import Log
import json


class RunTest:

    def __init__(self):
        self.run_method = RunMethod()
        self.data = GetData()
        self.expcet = CommonUtil()           # 预期结果
        self.depen = DependatData()
        self.sendemail = SendEmail()
        self.log_file = Log()
        self.pass_count = []
        self.fail_count = []
        self.notrun_count = []

    def go_on_run(self, url_name, file_name):
        row_count = self.data.get_case_lines()
        for i in range(1, row_count):
            not_re_data, yw, re = None, None, None
            is_run = self.data.get_is_run(i)
            if is_run:                                  # 判断是否执行
                method = self.data.get_request_method(i)
                api = self.data.get_url(i)
                urls = url_name + api
                header = self.data.is_header(i)
                depen_data = self.depen.run_depend_value(i, url_name)               # 处理有依赖的接口数据
                if depen_data is None:
                    data = self.data.get_data_json(i)
                    if data is None:
                        not_re_data = "第%s行缺少请求参数！" % i
                    else:        
                        re = self.run_method.run_main(method, urls, data, header)    # 实际返回
                else:
                    re = self.run_method.run_main(method, urls, depen_data, header)  # 有依赖的实际返回
                expcet_data = self.data.get_expcet_data(i)                          # 预期结果
                if re is not None:
                    yq = self.expcet.is_contain(expcet_data, re)
                    self.check(yq, re, i, not_re_data, file_name)
            else:
                not_run_log = ('Test-%s:Not running！' % i)
                self.log_file.mylog(not_run_log, file_name)
                self.notrun_count.append(i)
        self.sendemail.send_main(len(self.pass_count), len(self.fail_count))                         # 发送邮件
        run_final = "\n执行通过： %d\n" \
                    "执行失败： %d\n" \
                    "未执行： %d" % (len(self.pass_count), len(self.fail_count), len(self.notrun_count))
        self.log_file.mylog(run_final, file_name)
        print(run_final)

    def check(self, yq, re, i, not_re_data, file_name):
        print(re)
        if re is None:
            self.notrun_count.append(i)
            not_re_data_log = ('Test-%s:' % i, not_re_data)
            self.log_file.mylog(not_re_data_log, file_name)
        else:
            if yq:
                self.data.write_data(i, 'pass -->> %s' % re)
                self.pass_count.append(i)
                pass_log = 'Test-%s: pass -->> ' % i + re
                self.log_file.mylog(pass_log, file_name)

            else:
                self.data.write_data(i, 'fail -->> %s' % re)
                self.fail_count.append(i)
                fail_log = 'Test-%s: fail -->> ' % i + re
                self.log_file.mylog(fail_log, file_name)


if __name__ == '__main__':
    with open("../test_file/data_config.json") as fp:
            data_cnf = json.load(fp)
    url_names = data_cnf['url_test']
    url = data_cnf['url']
    log = Log()
    file_names = log.logfile()
    run = RunTest()
    run.go_on_run(url_names, file_names)
