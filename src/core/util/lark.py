import json

import requests

payload = {
    "msg_type": "text",  # 消息类型：文本
    "content": {
        "text": "有区块浏览器接口报错了"  # 文本内容
    }
}
def sendlark():
    # 发送POST请求
    response = requests.post(
        url="https://open.larksuite.com/open-apis/bot/v2/hook/757b2b75-a512-48c5-a788-0bbac2c4fbbc",
        headers={"Content-Type": "application/json"},  # 必须指定JSON格式
        data=json.dumps(payload),  # 序列化JSON
        timeout=10  # 超时时间，避免脚本卡死
    )
    # 校验响应结果
    response.raise_for_status()  # 状态码非2xx时抛异常
    result = response.json()