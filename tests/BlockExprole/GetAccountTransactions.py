import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions


class GetAccountTransactions(BaseData):
    def test_GetAccountTransactions(self):
        """获取用户的trans信息"""
        getaddressinfo = GetLatestTransactions()
        address=getaddressinfo.test_GetLatestTransactions()['data']['data'][0]['payer']
        url=self.base_url+"/demo/account/transactions?address="+address+"&pagination.page=1&pagination.page_size=20"
        response=requests.get(url,headers=self.headers)
        print(response.json())
        self.assertIsNotNone(response.json())

