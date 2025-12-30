import requests

from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions

class Getvalidators(BaseData):
    def test_Getvalidators(self):
        """获取区块链验证人"""
        url=self.base_url+"/api/v1/validator/validators?page=1&page_size=5"
        print("请求地址为"+url)
        response=requests.get(url,headers=self.headers)
        print(response.json())
        self.assertEqual(response.status_code,200)
        # self.assertIsNotNone(response.json()['data'])
