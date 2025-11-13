import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData


class GetLatestTransactions(BaseData):
    def test_GetLatestTransactions(self):
        """获取最新5条trans信息"""
        url=self.base_url+"/demo/transaction/latest?page=1&page_size=5"
        response=requests.get(url,headers=self.headers)
        print(response.json()['data'])
        self.assertIsNotNone(response.json()['data'])
        return response.json()