import unittest

from src.core.config import config


class BaseData(unittest.TestCase):
    def setUp(self):
        # 前置条件：初始化接口基础 URL
        self.base_url = config.get_url()  # 替换为实际接口域名
        self.headers = {"Content-Type": "application/json"}  # 请求头

    def tearDown(self):
        # 后置条件：可选（如清理测试数据）
        print("case完成")
        pass
