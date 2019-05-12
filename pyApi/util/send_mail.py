# coding=utf-8
import smtplib
from email.mime.text import MIMEText
import json
import re
"""发送邮件"""


class SendEmail:

    def __init__(self):
        with open("../test_file/data_config.json") as fp:
            email_data = json.load(fp)
        data = email_data['email']
        self.send_users = data.get("send_user")
        self.passwords = data.get("password")
        self.user_list = data.get("Receipt")        # 收件人邮箱
        self.email_user = []

    # 发送邮件
    def send_email(self, sub, content):
        for i in self.user_list:
            str = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
            if re.match(str, i):
                self.email_user.append(i)
            else:
                print('Error！请检查接收的邮箱账号!你这样写:%s' % i)
        email_host = 'smtp.163.com'
        user = 'ZhangMx' + '<' + self.send_users + '>'
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ';'.join(self.email_user)
        server = smtplib.SMTP()
        server.connect(host=email_host)
        server.login(self.send_users, self.passwords)
        server.sendmail(user, self.email_user, message.as_string())
        server.close()

    # 计算通过率
    def send_main(self, pass_count, fail_count):
        pass_num, fail_num = pass_count, fail_count
        count_num = pass_num + fail_num
        if count_num > 0:
            pass_result = "%.2f%%" %(pass_num / count_num * 100)
            fail_result = "%.2f%%" %(fail_num / count_num * 100)
            sub = "接口测试执行结果！"
            content = "测试结果：\n" \
                      "本次共测试接口数：%s\n" \
                      "通过：%s\n" \
                      "失败：%s\n" \
                      "通过率：%s\n" \
                      "失败率：%s" \
                     % (int(count_num), int(pass_num), int(fail_num), pass_result, fail_result)
            self.send_email(sub, content)


# if __name__ == '__main__':
#     a = SendEmail()
#     a.send_email(1, 1)
