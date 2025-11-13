
import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions

class GetTransactionbyHash(BaseData):
    def test_GetTransactionbyHash(self):
        """根据交易hash获取trans交易信息"""
        gethash = GetLatestTransactions()
        hash_data=gethash.test_GetLatestTransactions()
        print(hash_data['data']['data'][0]['hash'])
        url=self.base_url+"/demo/transaction/by-hash?hash="+hash_data['data']['data'][0]['hash']
        print("请求地址为" + url)
        response=requests.get(url,headers=self.headers)
        print(response.json())
        self.assertIsNotNone(response.json()['data'])