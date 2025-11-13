import os
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import time
import sys


class TestLogger:
    """自动化测试框架日志类"""
    def __init__(self, logger_name="test_framework", log_dir="logs"):
        # 确保日志目录存在
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 日志文件名（包含当前日期）
        self.current_date = time.strftime("%Y%m%d")
        self.log_file = os.path.join(self.log_dir, f"{logger_name}_{self.current_date}.log")
        self.error_log_file = os.path.join(self.log_dir, f"{logger_name}_error_{self.current_date}.log")

        # 创建logger实例
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)  # 全局最低日志级别

        # 避免日志重复输出
        if self.logger.handlers:
            return

        # 日志格式：时间 - 级别 - 模块 - 函数 - 内容
        self.formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 添加控制台处理器
        self._add_console_handler()

        # 添加文件处理器（按时间轮转）
        self._add_file_handler()

        # 添加错误日志处理器（单独记录错误级别日志）
        self._add_error_file_handler()

    def _add_console_handler(self):
        """添加控制台输出处理器"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)  # 控制台只输出INFO及以上级别
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self):
        """添加文件输出处理器（按时间轮转，保留7天日志）"""
        # TimedRotatingFileHandler参数说明：
        # when='D' 每天轮转；interval=1 间隔1天；backupCount=7 保留7个备份
        file_handler = TimedRotatingFileHandler(
            self.log_file,
            when='D',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)  # 文件记录DEBUG及以上级别
        file_handler.setFormatter(self.formatter)
        # 自定义轮转文件名（如：test_20231001.log.20231002）
        file_handler.suffix = "%Y%m%d"
        self.logger.addHandler(file_handler)

    def _add_error_file_handler(self):
        """添加错误日志处理器（只记录ERROR及以上级别）"""
        error_handler = RotatingFileHandler(
            self.error_log_file,
            maxBytes=5 * 1024 * 1024,  # 单个文件最大5MB
            backupCount=3,  # 保留3个备份
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)  # 只记录ERROR及以上
        error_handler.setFormatter(self.formatter)
        self.logger.addHandler(error_handler)

    def get_logger(self):
        """获取logger实例"""
        return self.logger


# 单例模式：全局唯一日志实例
logger = TestLogger().get_logger()

# 测试日志功能
if __name__ == "__main__":
    logger.debug("这是DEBUG级别日志（仅文件输出）")
    logger.info("这是INFO级别日志（控制台+文件）")
    logger.warning("这是WARNING级别日志")
    logger.error("这是ERROR级别日志（同时写入错误日志文件）")
    logger.critical("这是CRITICAL级别日志")

