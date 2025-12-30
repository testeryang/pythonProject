import json

import requests


def sendlark(msg,robotrul,resulturl,uid=None):
    # 发送POST请求
    if uid!=None:
        payload = {
            "msg_type": "text",  # 消息类型：文本
            "content": {
                "text": msg + "接口报错了,测试报告地址为：" + resulturl + "<at user_id=" + uid + ">负责人</at>"
            }
        }
    else:
        payload = {
            "msg_type": "text",  # 消息类型：文本
            "content": {
                "text": msg + "接口报错了,测试报告地址为：" + resulturl
            }
        }
    response = requests.post(
        url=robotrul,
        headers={"Content-Type": "application/json"},  # 必须指定JSON格式
        data=json.dumps(payload),  # 序列化JSON
        timeout=10  # 超时时间，避免脚本卡死
    )
    # 校验响应结果
    response.raise_for_status()  # 状态码非2xx时抛异常
    result = response.json()
    print(result)