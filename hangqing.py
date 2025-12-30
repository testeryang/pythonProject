
import unittest
from datetime import datetime

from unittestreport import TestRunner
from tests.test.test import test
from src.core.util.lark import sendlark

def nowtime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H.%M")
    return formatted_time

suite = unittest.TestSuite()
suite.addTest(test("test_1"))

one_runner = TestRunner(suite,
                        filename="行情服务测试报告.html",
                        report_dir=r"reports",
                        title="测试报告",
                        tester="杨杰",
                        desc="这里是接口自动化运行后获得的测试报告结果",
                        templates=1
                        )
test=one_runner.run()
if test['fail']>0 or test['error']>0:
    sendlark("行情服务","https://open.larksuite.com/open-apis/bot/v2/hook/2311af1f-9bdf-4505-8fa7-e77bcdc4839e","http://165.154.5.210:8081/%E8%A1%8C%E6%83%85%E6%9C%8D%E5%8A%A1%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A.html")