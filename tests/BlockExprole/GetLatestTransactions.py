import requests

from tests.BlockExprole import BaseData


class GetLatestTransactions(BaseData):
    def test_GetLatestTransactions(self):
        """获取最新5条trans信息"""
        url=self.base_url+"/api/v1/transaction/latest?page=1&page_size=5"
        print("请求地址为：" + url)
        response=requests.get(url,headers=self.headers)
        print(response.json()['data'])
        self.assertIsNotNone(response.json()['data'])
        return response.json()
