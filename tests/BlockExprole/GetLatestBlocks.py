import unittest
import requests  # 需安装：pip install requests

from tests.BlockExprole import BaseData

# 用户接口测试类
class get_LatestBlocks(BaseData):
    # 测试用例1：获取存在的用户信息（正常场景）
    def test_getLatestBlocks(self):
        """获取最新的区块信息"""
        url = self.base_url+"demo/block/latest?page=1&page_size=1"
        # 发送 GET 请求
        response = requests.get(url, headers=self.headers)
        result = response.json()  # 解析 JSON 响应
        # print(result['data'])
        # 断言验证
        self.assertEqual(response.status_code, 200, "状态码应为 200")  # 验证 HTTP 状态码
        self.assertIsNotNone(result['data'],msg="验证首页接口数据")