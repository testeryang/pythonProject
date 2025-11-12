import requests

from tests.BlockExprole import BaseData


class GetLatestBlockHeight(BaseData):
    def test_getLatestBlockHeight(self):
        url=self.base_url+"/demo/block/latest-height"
        response=requests.get(url,headers=self.headers)
        print(response.json()['data']['height'])
        self.assertTrue(int(response.json()['data']['height'])>0)