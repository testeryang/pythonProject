import unittest
import time

from src.core.config import config


class BaseData(unittest.TestCase):
    base_url = config.get_url()  # 替换为实际接口域名
    headers = {"Content-Type": "application/json"}  # 请求头
    def setUp(self):
        # 前置条件：初始化接口基础 URL
        self.start_time = time.time()

    def tearDown(self):
        # 后置条件：可选（如清理测试数据）
        end_time = time.time()
        run_time = round(end_time - self.start_time, 3)
        print(self._testMethodName+"脚本完成")
        print("该脚本总共用时："+str(run_time))
        pass
