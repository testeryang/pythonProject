import requests

from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions

class GetAccountInfo(BaseData):
    def test_GetAccountInfo(self):
        """获取用户详细信息"""
        getaddressinfo = GetLatestTransactions()
        address=getaddressinfo.test_GetLatestTransactions()['data']['data'][0]['payer']

        url=self.base_url+"/demo/account/info?address="+address
        print("请求地址为" + url)
        print(url)
        response=requests.get(url,headers=self.headers)
        print(response.json())
        self.assertIsNotNone(response.json()['data'])
