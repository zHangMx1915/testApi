# coding=utf-8
import requests
import json
'''主流程，执行接口请求'''


class RunMethod:

    def post_main(self, url, data, header=None):
        # requests.packages.urllib3.disable_warnings()  # 禁用HTTPS证书警告
        if header is None:
            return requests.post(url=url, data=data, verify=False).json()
        else:
            return requests.post(url=url, data=data, headers=header, verify=False).json()   # verify=False 忽略https

    def get_mian(self, url, data=None, header=None):
        if header is None:
            a = requests.get(url, data).json()
            return a
        else:
            return requests.get(url, data, headers=header, verify=False).json()

    def run_main(self, method, url, data=None, header=None):
        sre = ''
        try:  
            if method == 'post':
                re = self.post_main(url, data, header)
            else:
                re = self.get_mian(url, data, header)
            sre =  json.dumps(re, ensure_ascii=False, sort_keys=True, indent=2)
        except json.decoder.JSONDecodeError as e:
            e = str(e)
            sre = '请检查接口URL及路径！' + 'json.decoder.JSONDecodeError:' + e
        except Exception as e:
            sre = e
        return sre


# if __name__ == '__main__':
#     method = 'get'
#     url = 'www.baidu,com'

#     a = RunMethod()
#     a.run_main(method, url)
