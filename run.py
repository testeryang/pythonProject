
import unittest
from datetime import datetime

from unittestreport import TestRunner

from tests.BlockExprole.GetLatestBlocks import get_LatestBlocks

def nowtime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H.%M")
    return formatted_time

suite = unittest.TestSuite()
# suite.addTest(Login("test_login"))
suite.addTest(get_LatestBlocks('test_get_LatestBlocks'))
print(suite.__str__())

one_runner = TestRunner(suite,
                        filename=nowtime()+"测试报告.html",
                        report_dir=r"reports",
                        title="测试报告",
                        tester="杨杰",
                        desc="这里是接口自动化运行后获得的测试报告结果",
                        templates=1
                        )
one_runner.run()
