
import unittest
from datetime import datetime

from unittestreport import TestRunner

from tests.BlockExprole.GetAccountBalances import GetAccountBalances
from tests.BlockExprole.GetAccountInfo import GetAccountInfo
from tests.BlockExprole.GetAccountTransactions import GetAccountTransactions
from tests.BlockExprole.GetBlockbyHeight import get_BlockbyHeight
from tests.BlockExprole.GetLatestBlockHeight import GetLatestBlockHeight
from tests.BlockExprole.GetLatestBlocks import get_LatestBlocks
from tests.BlockExprole.GetLatestTransactions import GetLatestTransactions
from tests.BlockExprole.GetTransactionbyHash import GetTransactionbyHash
from tests.BlockExprole.Getvalidators import Getvalidators
from tests.BlockExprole.test_play import *

def nowtime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H.%M")
    return formatted_time

suite = unittest.TestSuite()
suite.addTest(get_LatestBlocks('test_getLatestBlocks'))
suite.addTest(GetLatestBlockHeight('test_getLatestBlockHeight'))
suite.addTest(GetAccountBalances('test_GetAccountBalances'))
suite.addTest(GetAccountInfo('test_GetAccountInfo'))
suite.addTest(GetAccountTransactions('test_GetAccountTransactions'))
suite.addTest(get_BlockbyHeight('test_getblockbyheight'))
suite.addTest(GetLatestTransactions('test_GetLatestTransactions'))
suite.addTest(GetTransactionbyHash('test_GetTransactionbyHash'))
suite.addTest(Getvalidators("test_Getvalidators"))
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
one_runner.run()
