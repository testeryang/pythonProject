import requests

from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions

class GetAccountInfo(BaseData):
    def test_GetAccountInfo(self):
        # getaddressinfo = GetLatestTransactions()
        # address=getaddressinfo.test_GetLatestTransactions()
        # print(address['data']['data'][0])
        url=self.base_url+"/demo/account/info?address=inj1s9sparu5ksj9f2n36ltnfgh8zm0p028a4xrgpc"
        response=requests.get(url,headers=self.headers)
        print(response.json())
        self.assertIsNotNone(response.json()['data'])
