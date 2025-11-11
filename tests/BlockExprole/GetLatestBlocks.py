import unittest
import requests  # 需安装：pip install requests

from tests.BlockExprole import BaseData

# 用户接口测试类
class TestApi(BaseData):
    # 测试用例1：获取存在的用户信息（正常场景）
    def test_get_LatestBlocks(self):
        url = self.base_url+"demo/block/latest?page=1&page_size=1"
        print(url)
        # 发送 GET 请求
        response = requests.get(url, headers=self.headers)
        result = response.json()  # 解析 JSON 响应
        # print(result['data'])
        # 断言验证
        self.assertEqual(response.status_code, 200, "状态码应为 200")  # 验证 HTTP 状态码
        self.assertIsNotNone(result['data'],msg="验证首页接口数据")
        # self.assertEqual(result["data"], 200, "接口返回 code 应为 200")  # 验证业务 code
        # self.assertEqual(result["data"]["name"], "张三", "用户名应为张三")  # 验证具体数据
        # self.assertIsInstance(result["data"]["age"], int, "年龄应为整数类型")  # 验证数据类型

# 执行测试
if __name__ == "__main__":
    unittest.main()  # 运行所有测试用例