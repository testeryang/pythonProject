
import requests
from tests.BlockExprole import BaseData

# 用户接口测试类
class get_BlockbyHeight(BaseData):
    # 测试用例1：获取存在的用户信息（正常场景）
    def test_get_blockbyheight(self):
        url = self.base_url + "/demo/block/by-height?height=1"
        # 发送 GET 请求
        response = requests.get(url, headers=self.headers)
        result = response.json()  # 解析 JSON 响应
        print(result)
        # 断言验证
        self.assertEqual(response.status_code, 200, "状态码应为 200")  # 验证 HTTP 状态码
        self.assertIsNotNone(result['data'], msg="验证首页接口数据")
