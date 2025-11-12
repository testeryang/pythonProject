import requests

from src.core.logger import logger
from tests.BlockExprole import BaseData


class GetLatestTransactions(BaseData):
    def test_GetLatestTransactions(self):
        url=self.base_url+"/demo/transaction/latest?page=1&page_size=5"
        response=requests.get(url,headers=self.headers)

        self.assertIsNotNone(response.json()['data'])
        logger.info(response.json()['data'])
        return response.json()