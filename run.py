import json
import unittest
from datetime import datetime

from unittestreport import TestRunner

from tests.BlockExprole.GetAccountBalances import GetAccountBalances
from tests.BlockExprole.GetAccountInfo import GetAccountInfo
from tests.BlockExprole.GetAccountTransactions import GetAccountTransactions
from tests.BlockExprole.GetBlockbyHeight import  GetBlockbyHeight
from tests.BlockExprole.GetLatestBlockHeight import GetLatestBlockHeight
from tests.BlockExprole.GetLatestBlocks import GetLatestBlocks
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions
from tests.BlockExprole.GetTransactionbyHash import GetTransactionbyHash

from tests.BlockExprole.test_play import *

def nowtime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H.%M")
    return formatted_time


def send_lark_text_webhook(webhook_url, content):
    """
    发送飞书文本类型Webhook消息
    :param webhook_url: 飞书机器人Webhook地址
    :param content: 消息内容（支持换行、@所有人等）
    """
    # 构造消息体（飞书文本消息格式）
    payload = {
        "msg_type": "text",  # 消息类型：文本
        "content": {
            "text": content  # 文本内容
        }
    }

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

suite = unittest.TestSuite()
suite.addTest(GetLatestBlocks('test_getLatestBlocks'))
suite.addTest(GetLatestBlockHeight('test_getLatestBlockHeight'))
suite.addTest(GetAccountBalances('test_GetAccountBalances'))
suite.addTest(GetAccountInfo('test_GetAccountInfo'))
suite.addTest(GetAccountTransactions('test_GetAccountTransactions'))
suite.addTest(GetBlockbyHeight('test_getblockbyheight'))
suite.addTest(GetLatestTransactions('test_GetLatestTransactions'))
suite.addTest(GetTransactionbyHash('test_GetTransactionbyHash'))
# suite.addTest(Getvalidators("test_Getvalidators"))
suite.addTest(Test_QuKuaiLian("test_blocks"))
suite.addTest(Test_QuKuaiLian("test_health"))

one_runner = TestRunner(suite,
                        filename=nowtime()+"测试报告.html",
                        report_dir=r"reports",
                        title="测试报告",
                        tester="杨杰",
                        desc="这里是接口自动化运行后获得的测试报告结果",
                        templates=1
                        )
test=one_runner.run()

if test['fail']>0 or test['error']>0:
    sendlark()