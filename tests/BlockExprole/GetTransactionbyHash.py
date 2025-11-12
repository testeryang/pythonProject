
import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions

class GetTransactionbyHash(BaseData):
    def test_GetTransactionbyHash(self):
        gethash = GetLatestTransactions()
        hash_data=gethash.test_GetLatestTransactions()
        logger.info(hash_data['data']['data'][0]['hash'])
        url=self.base_url+"/demo/transaction/by-hash?hash="+hash_data['data']['data'][0]['hash']
        response=requests.get(url,headers=self.headers)
        logger.info(response.json())
        self.assertIsNotNone(response.json()['data'])