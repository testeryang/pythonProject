# 接口自动化测试框架（Python + unittest）

## 功能概述
- 配置集中管理（YAML + .env）
- HTTP 客户端封装（会话、重试、超时、日志）
- Pytest 夹具与用例组织
- JSON 架构校验与断言工具
- Allure 报告集成

## 快速开始（Windows / PowerShell）
```powershell
# 1) 创建虚拟环境（可选）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) 安装依赖
pip install -r requirements.txt

# 3) 运行测试并生成HTML报告
python runner.py

# 指定测试目录或模式
python runner.py --start-dir tests --pattern "test_*.py"
```

## 目录结构（拟）
```
.
├─ src/
│  ├─ core/
│  │  ├─ config.py           # 配置加载
│  │  ├─ http_client.py      # HTTP 客户端
│  │  └─ logger.py           # 日志
│  └─ utils/
│     └─ schema.py           # JSON 架构校验
├─ tests/
│  └─ test_example_api.py    # 示例用例（unittest）
├─ config/
│  └─ config.yaml            # 基础配置
├─ .env.example              # 环境变量示例
├─ runner.py                 # unittest 运行器（HtmlTestRunner）
├─ requirements.txt
└─ README.md
```

## 约定
- 使用 `BASE_URL` 环境变量覆盖 YAML 中的基础地址
- 测试数据可放置在 `tests/data/` 下，支持参数化
- 统一通过 `client` 夹具发起请求

## 运行参数示例
```powershell
# 指定环境文件
$env:ENV_FILE=".env.dev"
pytest -m api -q

# 指定 base url（优先级高于 YAML）
$env:BASE_URL="https://httpbin.org"
pytest -k example -q
```

