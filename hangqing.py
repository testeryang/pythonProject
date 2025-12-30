
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
                        filename=nowtime()+"测试报告.html",
                        report_dir=r"reports",
                        title="测试报告",
                        tester="杨杰",
                        desc="这里是接口自动化运行后获得的测试报告结果",
                        templates=1
                        )
test=one_runner.run()

if test['fail']>0 or test['error']>0:
    print("测试完成")
    # sendlark()