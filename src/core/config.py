from __future__ import annotations

import os.path

import yaml

class Config:
    def __init__(self):
        # 1. 获取当前文件（utils.py）的绝对路径
        current_file_path = os.path.abspath(__file__)
        # 2. 获取当前文件所在目录（core/）
        core_dir = os.path.dirname(current_file_path)
        # 3. 向上一级找到项目根目录，再拼接config/config.yaml
        # （根据实际目录结构调整，若core和config同级，则用../config/config.yaml）
        config_path = os.path.join(core_dir, "../../config/config.yaml")
        # 4. 转为绝对路径（处理../等相对符号）
        self.config_path = os.path.abspath(config_path)
        # print(self.config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            # 加载 YAML 内容为 Python 字典/列表
            self.config = yaml.safe_load(f)
        # print(self.config)

    def get_url(self):
        # print( self.config.get("url"))
        return self.config["url"]

    def get_username(self):
        return self.config["username"]
    def get_password(self):
        return self.config["password"]
config = Config()


