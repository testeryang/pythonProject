import json
import unittest
from datetime import datetime

from unittestreport import TestRunner

from src.core.util.lark import sendlark

def nowtime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H.%M")
    return formatted_time

suite = unittest.TestSuite()

# suite.addTest(GetLatestBlocks('test_getLatestBlocks'))
# suite.addTest(GetLatestBlockHeight('test_getLatestBlockHeight'))
# suite.addTest(GetAccountBalances('test_GetAccountBalances'))
# suite.addTest(GetAccountInfo('test_GetAccountInfo'))
# suite.addTest(GetAccountTransactions('test_GetAccountTransactions'))
# suite.addTest(GetBlockbyHeight('test_getblockbyheight'))
# suite.addTest(GetLatestTransactions('test_GetLatestTransactions'))
# suite.addTest(GetTransactionbyHash('test_GetTransactionbyHash'))
# # suite.addTest(Getvalidators("test_Getvalidators"))
# suite.addTest(Test_QuKuaiLian("test_tui_blocks"))
# suite.addTest(Test_QuKuaiLian("test_health"))

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