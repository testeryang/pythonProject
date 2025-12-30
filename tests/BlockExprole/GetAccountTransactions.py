import requests

from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions


class GetAccountTransactions(BaseData):
    def test_GetAccountTransactions(self):
        """获取用户的trans信息"""
        getaddressinfo = GetLatestTransactions()
        address=getaddressinfo.test_GetLatestTransactions()['data']['data'][0]['signer']
        url=self.base_url+"/api/v1account/transactions?address="+address+"&pagination.page=1&pagination.page_size=20"
        print("请求地址为" + url)
        #测试用 url = self.base_url + "/demo/account/transactions?address=inj1s9hhrdgzerf79w963gv6kez4hvp3jds5avsc6e&pagination.page=1&pagination.page_size=20"
        response=requests.get(url,headers=self.headers)
        print(response.json())
        self.assertIsNotNone(response.json())

