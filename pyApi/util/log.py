# coding=utf-8
import time


class Log:

    # 创建log文件
    def logfile(self):
        test_time = (time.strftime("%Y.%m.%d %H-%M", time.localtime()))
        file_name = ("../test_file/log_file/" + test_time + ".txt")
        open(file_name, "a", encoding='utf-8')                                   # 创建log的txt文件
        return file_name

    # 写入日志
    def mylog(self, log, file_name):
        test_time = (time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))       # 系统当前时间
        with open(file_name, "a", encoding='utf-8') as f:
            f.write("\n%s :   %s" % (test_time, log))                            # 写入txt
