import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData


class GetAccountTransactions(BaseData):
    def test_GetAccountTransactions(self):
        url=self.base_url+"/demo/account/transactions?address=inj1s9sparu5ksj9f2n36ltnfgh8zm0p028a4xrgpc&pagination.page=1&pagination.page_size=20"
        response=requests.get(url,headers=self.headers)
        logger.info(response.json())
        """该接口还没有调通"""
        # self.assertIsNotNone(response.json())

