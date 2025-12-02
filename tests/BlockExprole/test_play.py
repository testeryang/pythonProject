from contextlib import nullcontext

import requests

from tests.BlockExprole import BaseData
from tests.BlockExprole.test_api import *

class Test_QuKuaiLian(BaseData):
    '''获取区块交易列表'''
    def test_blocks(self):
        a = {'page':1,'page_size':1}
        response = get_blkocks(a)
        '''print(response)'''

    '''获取服务器状态'''
    def test_health(self):
        service = None
        response = get_health(service)


