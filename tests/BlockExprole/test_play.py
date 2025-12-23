from contextlib import nullcontext
from http.client import responses

import requests

from tests.BlockExprole import BaseData
from tests.BlockExprole.test_api import *

class Test_QuKuaiLian(BaseData):
    # 获取区块交易列表
    def test_blocks_latest(self):
        a = {'page':1,'page_size':1}
        print(get_blocks_latest(a))

    # 获取服务器状态
    def test_health(self):
        service = None
        print(get_health(service))

    # 推送最新的区块信息
    def test_tui_blocks(self):
        # 这里我也可以将形参直接写入，然后在函数外input传入
        max_messages = 10
        get_tui_blocks(max_messages)
        # print(get_tui_blocks(max_messages))


    # 实时获取链上交易信息
    def test_Latest_Transactions(self):
        max_messages = 10
        block = get_Latest_Transactions(max_messages)
        print(f"从链上接收到{len(block)}条交易信息")
        for a in block:
            print(f"接收的交易哈希为: {a.transaction.hash[:70]} ")

    # 返回指定账户的交易信息
    def test_Account_Updates(self):
        address = 'inj1ur4tlhwy6e0jw9txmn5slvnkgahlqcq7q2stnd'
        max_messages = 10
        hash = get_Account_Updates(address,max_messages)
        print(f'当前获取交易信息的地址为：{address}')
        print(f'获取了{max_messages}条交易信息')
        for hash1 in hash:
            print(f'获取的交易信息哈希为{hash1.data.transaction.hash[:70]}')

    # def test_YC_tui_blocks(self):
    #     from tests.BlockExprole.试手 import YC_TUI_blocks
    #     max_count = 10
    #     thread_count = 10
    #     YC_TUI_blocks(max_count=max_count,thread_count=thread_count)
    #
    # def test_YC_Latest_Transactions(self):
    #     from tests.BlockExprole.试手 import YC_Latest_Transactions
    #     max_shuliang = 5
    #     thread_count = 20
    #     YC_Latest_Transactions(max_shuliang=max_shuliang,thread_count=thread_count)
    #
    # def test_YC_Account_Updates(self):
    #     from tests.BlockExprole.试手 import YC_Account_Updates
    #     address = 'inj1ur4tlhwy6e0jw9txmn5slvnkgahlqcq7q2stnd'
    #     max_messages = 7
    #     thread_count = 8
    #     YC_Account_Updates(address=address,max_messages=max_messages,thread_count=thread_count)