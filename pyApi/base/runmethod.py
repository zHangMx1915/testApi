# coding=utf-8
import requests
import json
'''主流程，执行接口请求'''


class RunMethod:

    def post_main(self, url, data, header=None):
        if header is None:
            return requests.post(url=url, data=data).json()
        else:
            return requests.post(url=url, data=data, headers=header).json()

    def get_mian(self, url, data=None, header=None):
        if header is None:
            a = requests.get(url, data).json()
            return a
        else:
            return requests.get(url, data, headers=header).json()

    def run_main(self, method, url, data=None, header=None):
        if method == 'post':
            re = self.post_main(url, data, header)
        else:
            re = self.get_mian(url, data, header)
        return json.dumps(re, ensure_ascii=False, sort_keys=True, indent=2)
