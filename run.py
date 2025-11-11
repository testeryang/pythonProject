
import unittest
from datetime import datetime

from unittestreport import TestRunner

from tests.BlockExprole.GetLatestBlocks import TestApi
from tests.login import Login

def nowtime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H.%M")
    return formatted_time

suite = unittest.TestSuite()
# suite.addTest(Login("test_login"))
suite.addTest(TestApi('test_get_LatestBlocks'))

one_runner = TestRunner(suite,
                        filename=nowtime()+"test.html",
                        report_dir=r"reports",
                        title="测试报告",
                        tester="jack",
                        desc="第一个报告",
                        templates=1
                        )
one_runner.run()
