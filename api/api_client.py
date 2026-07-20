import jsonpath
import requests

from utils.read_conf import read_conf


class ApiClient:
    def __init__(self):
        self.last_response = None
        self.env = None
        self.token = None

    # 实现自定义测试环境
    def set_env(self, env):
        self.env = env

    def set_token(self, token):
        self.token = token

    def do_get(self, path=None, params=None, headers=None, **kwargs):
        url = self.set_url(path)
        headers = self.set_headers(headers)
        resp = requests.get(url, params=params, headers=headers, **kwargs)
        self.last_response = resp
        return resp

    # post请求
    def do_post(self, path=None, data=None, headers=None, json=None, **kwargs):
        url = self.set_url(path)
        headers = self.set_headers(headers)
        resp = requests.post(url, data=data, headers=headers, json=json, **kwargs)
        self.last_response = resp
        return resp

    # url拼接操作
    def set_url(self, path):
        url = read_conf(self.env, 'host')
        if path:
            url = url + path
        return url

    # headers拼接操作
    def set_headers(self, headers):
        # 定义默认请求头
        base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/131.0.0.0 Safari/537.36'  # 定义浏览器属性
        }
        # 读取ApiClient实例中公共token是否存在，如果存在则自动添加到请求头作为关联数据。
        if self.token:
            base_headers['Authorization'] = f"Bearer {self.token}"
        # 基于有新增额外请求头信息的基础上，进行请求头内容添加
        if headers:
            base_headers.update(headers)  # 基于字典添加新的key和value
        return base_headers

    # 封装jsonpath。实现对断言和指定数据获取的功能
    @staticmethod
    def get_text(res, key):
        """
           jsonpath全局递归提取字段
           :param res: dict 接口json字典，不能传response对象
           :param key: 要提取的字段名
           :return: 单个值/列表
           """
        # 基于jsonpath获取所有指定key的对应value
        values = jsonpath.jsonpath(res, f'$..{key}')  # 拼接key的字符串，实现表达式完整性
        # jsonpath获取的数据，进行二次处理
        if values:  # values有值
            if len(values) == 1:  # 如果values只有一个元素
                return values[0]
        return values

    # 断言校验
    def assert_text(self, expected, res, key):
        reality = self.get_text(res, key)
        assert expected == reality, f'''
            预期结果为：{expected}
            实际结果为：{reality}
            断言结果：{expected} != {reality}，断言失败
        '''
