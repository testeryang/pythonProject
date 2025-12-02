import requests
from config.url import *

def get_blkocks(a):
    url = host + url_blocks
    '''直接调用get发送请求'''
    r = requests.get(url= url,params=a)
    '''将r的返回内容获取，获取完成后对内容进行断言'''
    assert r.status_code == 200,f'请求失败，响应状态码为：{r.status_code}'
    return r.text

def get_health(service):
    url = host + url_health
    '''调用get访问'''
    r = requests.get(url=url,params=service)
    assert r.status_code == 200,f'请求失败，响应状态码为：{r.status_code}'
    return r.text

