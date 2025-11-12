import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData

class GetAccountBalances(BaseData):
    def test_GetAccountBalances(self):
        url=self.base_url+"/demo/account/balances?address=inj1s9sparu5ksj9f2n36ltnfgh8zm0p028a4xrgpc"
        response=requests.get(url,headers=self.headers)
        logger.info(response.json())
        self.assertIsNotNone(response.json()['data'])
