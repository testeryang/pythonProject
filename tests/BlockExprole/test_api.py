import requests
from config.url import *
from grpc_client.explorer_client import ExplorerGRPCClient
from 简单示例 import result


def get_blocks_latest(a):
    '''获取区块交易列表'''
    url = host + url_blocks_latest
    r = requests.get(url= url,params=a)
    # 将r的返回内容获取，获取完成后对内容进行断言
    assert r.status_code == 200,f'请求失败，响应状态码为：{r.status_code}'
    return r.text

def get_health(service):
    '''获取服务器状态'''
    url = host + url_health
    # 调用get访问
    r = requests.get(url=url,params=service)
    assert r.status_code == 200,f'请求失败，响应状态码为：{r.status_code}'
    return r.text

def get_tui_blocks(max_messages):
    '''推送最新的区块信息'''
    # 与grpc服务器建立连接
    with ExplorerGRPCClient() as client:
        # 发送请求 返回的直接是Python字典，无需解析
        result1 = client.stream_latest_blocks(max_messages=max_messages)
        result = []
        for r in result1:
            result.append(r)
    return result

def get_Latest_Transactions(max_messages):
    '''实时获取链上交易信息'''
    with ExplorerGRPCClient() as r:
        a = r.stream_latest_transactions(None,max_messages)
        result = []
        for r1 in a :
            result.append(r1)
    return result
    '''这是正常 grpc接口的写法，流式接口需要在他的基础上去加for循环
    with ExplorerGRPCClient() as clinet:
        result = clinet.get_latest_block_height()
    assert result['code'] == 200
    return result
    '''

def get_Account_Updates(address,max_messages):
    '''返回指定账户的交易信息'''
    with ExplorerGRPCClient() as clinet:
        r = clinet.stream_account_updates(
            address = address,
            max_messages = max_messages,
            timeout = 100
        )
        result = []
        for r1 in r :
            result.append(r1)
    return result
    '''这是正常 grpc接口的写法，流式接口需要在他的基础上去加for循环
    with ExplorerGRPCClient() as clinet:
        address = 1
        page = 1
        page_size = 10
        result = clinet.get_account_transactions(address,page,page_size)
        assert result['code'] == 200
        return result
    '''