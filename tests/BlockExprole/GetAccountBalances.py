
import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions


class GetAccountBalances(BaseData):

    def test_GetAccountBalances(self):
        """获取用户余额"""
        getaddressinfo = GetLatestTransactions()

        address = getaddressinfo.test_GetLatestTransactions()['data']['data'][0]['payer']
        url=self.base_url+"/demo/account/balances?address="+address
        print("请求地址为" + url)
        response=requests.get(url,headers=self.headers)
        print("获取用户余额："+str(response.json()))

        self.assertIsNotNone(response.json()['data'])
