import requests

from tests.BlockExprole import BaseData


class GetLatestBlockHeight(BaseData):
    def test_getLatestBlockHeight(self):
        """获取最新的区块高度"""
        url=self.base_url+"/demo/block/latest-height"
        print("请求地址为" + url)
        response=requests.get(url,headers=self.headers)
        print(response.json()['data']['height'])
        self.assertTrue(int(response.json()['data']['height'])>0)