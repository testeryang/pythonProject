import unittest
from unittest import TestCase

from src.core.config import config
from src.core.logger import logger

class Login(unittest.TestCase):
    def test_login(self):
        """用户登录接口"""
        logger.info("这是登录接口")
        data = {"username": config.get_username(), "password": config.get_password()}
        print(data)
        assert data!=None
        return data
