# coding=utf-8
from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from util.send_mail import SendEmail
from data.dependat_data import DependatData
from util.log import Log
import json
import threading


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

    def log_and_notrun(self, log_type, i, re, file_name):
        log_text = ''
        if log_type == 'pass':          
            self.pass_count.append(i)
            log_text = 'pass -->> ' + re
        elif log_type == 'fail' or log_type == 'Error':
            self.fail_count.append(i)
            log_text = 'fail -->> ' + re
        elif log_type == 'notrun':
            self.notrun_count.append(i)
            log_text = 'Not running！'
        self.log_file.mylog('Test-%s: ' % i + log_text, file_name)
        self.data.write_data(i, log_text)

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
                    # if type(re).__name__ == 'str':   # 判断type
                    if re.startswith('{') and re.endswith('}'):   # 判断是否以{}开头和结尾
                        yq = self.expcet.is_contain(expcet_data, re)
                        self.check(yq, re, i, not_re_data, file_name)
                    else:
                        self.log_and_notrun('Error', i, re, file_name)
                        print('Test-%s:  -->> fail  ' % i + re)
            else:
                self.log_and_notrun('notrun', i, re, file_name)
        self.sendemail.send_main(len(self.pass_count), len(self.fail_count))                         # 发送邮件
        run_final = "\n执行通过： %d\n" \
                    "执行失败： %d\n" \
                    "未执行： %d" % (len(self.pass_count), len(self.fail_count), len(self.notrun_count))
        self.log_file.mylog(run_final, file_name)
        print(run_final)

    def check(self, yq, re, i, not_re_data, file_name):
        if re is None:
            self.notrun_count.append(i)
            not_re_data_log = ('Test-%s:' % i, not_re_data)
            self.log_file.mylog(not_re_data_log, file_name)
        else:
            if yq == 1:
                self.log_and_notrun('pass', i, re, file_name)
                print('Test-%s:  -->> pass' % i)
            elif yq == 0:
                self.log_and_notrun('fail', i, re, file_name)
                print('Test-%s:  -->> fail' % i)
            elif yq == 2:
                re = "缺少预期结果！" + re
                self.log_and_notrun('fail', i, re, file_name)
                print('Test-%s:  -->> fail: 缺少预期结果！' % i)


def my_run(test_url):
    log_path = "../test_file/log_file/"
    threadLock.acquire()                # 获取锁，用于线程同步
    with open("../test_file/data_config.json") as fp:
        data_cnf = json.load(fp)
    url_names = data_cnf[test_url]
    log = Log()
    file_names = log.logfile(log_path)
    run = RunTest()
    run.go_on_run(url_names, file_names)
    threadLock.release()                # 释放锁，开启下一个线程


def case_0():
    my_run('url_test')


def case_1():
    my_run('url_test')


threadLock = threading.Lock()           # 多线程资源锁


if __name__ == '__main__':
    t1 = threading.Thread(target=case_0)
    t2 = threading.Thread(target=case_1)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
