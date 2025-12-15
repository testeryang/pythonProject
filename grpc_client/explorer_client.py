# explorer_client.py
"""
gRPC/gRPC-Web客户端封装 - 支持普通RPC和流式RPC
包含区块链浏览器的所有gRPC接口调用方法
支持标准gRPC和gRPC-Web两种协议
"""

import grpc
import yaml
import time
from pathlib import Path
from typing import Iterator, Optional, Dict, Any
from .generated.explorer.v1 import demo_pb2
from .generated.explorer.v1 import demo_pb2_grpc
from .generated.explorer.v1 import common_pb2
from google.protobuf import empty_pb2


class ExplorerGRPCClient:
    """
    区块链浏览器gRPC客户端
    支持普通RPC和流式RPC调用
    支持标准gRPC和gRPC-Web协议
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化gRPC客户端
        
        Args:
            config_path: 配置文件路径，默认为None时自动查找
        """
        # 加载配置
        if config_path is None:
            # 自动查找config.yaml
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "config.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 获取gRPC配置
        grpc_config = self.config.get('grpc', {})
        self.protocol = grpc_config.get('protocol', 'grpc')  # grpc 或 grpc-web
        self.host = grpc_config.get('host', 'localhost')
        self.port = grpc_config.get('port', 50051)
        self.use_tls = grpc_config.get('use_tls', False)
        self.cert_path = grpc_config.get('cert_path')
        self.timeout = grpc_config.get('timeout', 30)
        self.stream_timeout = grpc_config.get('stream_timeout', 60)
        self.max_stream_messages = grpc_config.get('max_stream_messages', 0)
        
        # 构建目标地址
        if self.protocol == 'grpc-web':
            # gRPC-Web使用HTTP(S)协议
            protocol_prefix = "https://" if self.use_tls else "http://"
            # 如果port是标准端口，不添加端口号
            if (self.use_tls and self.port == 443) or (not self.use_tls and self.port == 80):
                self.target = f"{protocol_prefix}{self.host}"
            else:
                self.target = f"{protocol_prefix}{self.host}:{self.port}"
        else:
            # 标准gRPC不需要协议前缀
            self.target = f"{self.host}:{self.port}"
        
        print(f"🔗 正在连接gRPC服务器: {self.target}")
        print(f"   协议类型: {self.protocol}")
        print(f"   使用TLS: {self.use_tls}")
        
        # 创建gRPC通道和stub
        self.channel = self._create_channel()
        self.stub = demo_pb2_grpc.DemoStub(self.channel)
        
        print(f"   ✅ 已创建{'安全' if self.use_tls else '非安全'}通道")
        print(f"   ✅ 已创建gRPC Stub")
    
    def _create_channel(self) -> grpc.Channel:
        """
        创建gRPC通道
        支持标准gRPC和gRPC-Web
        
        Returns:
            grpc.Channel: gRPC通道对象
        """
        if self.protocol == 'grpc-web':
            # gRPC-Web配置
            # Python的grpcio通过标准gRPC + HTTP/2实现gRPC-Web
            # 需要配置特定的metadata和options
            
            if self.use_tls:
                # HTTPS连接
                if self.cert_path and Path(self.cert_path).exists():
                    with open(self.cert_path, 'rb') as f:
                        credentials = grpc.ssl_channel_credentials(f.read())
                else:
                    # 使用系统默认证书
                    credentials = grpc.ssl_channel_credentials()
                
                # gRPC-Web需要特定的channel options
                options = [
                    ('grpc.ssl_target_name_override', self.host),
                    ('grpc.default_authority', self.host),
                ]
                
                # 注意：这里仍使用host:port格式，不使用https://前缀
                channel_target = f"{self.host}:{self.port}"
                return grpc.secure_channel(channel_target, credentials, options=options)
            else:
                # HTTP连接
                channel_target = f"{self.host}:{self.port}"
                return grpc.insecure_channel(channel_target)
        else:
            # 标准gRPC
            if self.use_tls:
                if self.cert_path and Path(self.cert_path).exists():
                    with open(self.cert_path, 'rb') as f:
                        credentials = grpc.ssl_channel_credentials(f.read())
                else:
                    credentials = grpc.ssl_channel_credentials()
                return grpc.secure_channel(self.target, credentials)
            else:
                return grpc.insecure_channel(self.target)
    
    def close(self):
        """关闭gRPC连接"""
        if self.channel:
            self.channel.close()
            print("🔌 gRPC通道已关闭")
    
    def __enter__(self):
        """支持with语句"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出with语句时自动关闭连接"""
        self.close()
    
    # ==================== 普通RPC方法 ====================
    
    def get_latest_blocks(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        获取最新区块列表（分页）
        
        Args:
            page: 页码，从1开始
            page_size: 每页数量
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetLatestBlocks (page={page}, page_size={page_size})")
        
        try:
            # 构建请求
            pagination = common_pb2.PaginationRequest(
                page=page,
                page_size=page_size
            )
            
            # 调用RPC
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetLatestBlocks(pagination, timeout=self.timeout)
            
            # 转换为字典返回
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data  # 这是protobuf的Any类型，可能需要进一步解析
            }
            
            print(f"✅ 成功获取最新区块列表")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def get_latest_block_height(self) -> Dict[str, Any]:
        """
        获取最新区块高度
        
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetLatestBlockHeight")
        
        try:
            # 构建空请求
            request = empty_pb2.Empty()
            
            # 调用RPC
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetLatestBlockHeight(request, timeout=self.timeout)
            
            # 转换为字典返回
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data
            }
            
            print(f"✅ 最新区块高度: {response.data}")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def get_block_by_height(self, height: int) -> Dict[str, Any]:
        """
        根据高度获取区块详情
        
        Args:
            height: 区块高度
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetBlockByHeight (height={height})")
        
        try:
            # 构建请求
            request = demo_pb2.GetBlockByHeightRequest(height=height)
            
            # 调用RPC
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetBlockByHeight(request, timeout=self.timeout)
            
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data
            }
            
            print(f"✅ 成功获取区块 #{height}")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def get_latest_transactions(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        获取最新交易列表（分页）
        
        Args:
            page: 页码
            page_size: 每页数量
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetLatestTransactions (page={page}, page_size={page_size})")
        
        try:
            pagination = common_pb2.PaginationRequest(
                page=page,
                page_size=page_size
            )
            
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetLatestTransactions(pagination, timeout=self.timeout)
            
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data
            }
            
            print(f"✅ 成功获取最新交易列表")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def get_transaction_by_hash(self, tx_hash: str) -> Dict[str, Any]:
        """
        根据哈希获取交易详情
        
        Args:
            tx_hash: 交易哈希
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetTransactionByHash (hash={tx_hash[:10]}...)")
        
        try:
            request = demo_pb2.GetTransactionByHashRequest(hash=tx_hash)
            
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetTransactionByHash(request, timeout=self.timeout)
            
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data
            }
            
            print(f"✅ 成功获取交易详情")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def get_account_info(self, address: str) -> Dict[str, Any]:
        """
        获取账户信息
        
        Args:
            address: 账户地址
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetAccountInfo (address={address[:10]}...)")
        
        try:
            request = demo_pb2.GetAccountInfoRequest(address=address)
            
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetAccountInfo(request, timeout=self.timeout)
            
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data
            }
            
            print(f"✅ 成功获取账户信息")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def get_account_transactions(self, address: str, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        获取账户交易列表
        
        Args:
            address: 账户地址
            page: 页码
            page_size: 每页数量
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetAccountTransactions (address={address[:10]}..., page={page})")
        
        try:
            pagination = common_pb2.PaginationRequest(
                page=page,
                page_size=page_size
            )
            
            request = demo_pb2.GetAccountTransactionsRequest(
                address=address,
                pagination=pagination
            )
            
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetAccountTransactions(request, timeout=self.timeout)
            
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data
            }
            
            print(f"✅ 成功获取账户交易列表")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def get_account_balances(self, address: str) -> Dict[str, Any]:
        """
        获取账户余额
        
        Args:
            address: 账户地址
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 GetAccountBalances (address={address[:10]}...)")
        
        try:
            request = demo_pb2.GetAccountBalancesRequest(address=address)
            
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.GetAccountBalances(request, timeout=self.timeout)
            
            result = {
                'code': response.code,
                'message': response.message,
                'data': response.data
            }
            
            print(f"✅ 成功获取账户余额")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    def check_healthy(self, service: str = "") -> Dict[str, Any]:
        """
        健康检查
        
        Args:
            service: 服务名称（可选）
            
        Returns:
            Dict: 返回结果字典
        """
        print(f"\n📤 调用 CheckHealthy")
        
        try:
            request = demo_pb2.CheckHealthyRequest(service=service)
            
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response = stub.CheckHealthy(request, timeout=self.timeout)
            
            result = {
                'status': response.status,
                'message': getattr(response, 'message', '')
            }
            
            print(f"✅ 健康检查: {response.status}")
            return result
            
        except grpc.RpcError as e:
            print(f"❌ gRPC错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            raise
    
    # ==================== 流式RPC方法 ====================
    
    def stream_latest_blocks(
        self, 
        from_height: int = 0,
        max_messages: int = None,
        timeout: float = None
    ) -> Iterator[Any]:
        """
        流式获取最新区块（服务端流式RPC）
        
        Args:
            from_height: 起始区块高度，0表示从最新区块开始
            max_messages: 最多接收的消息数量，None表示无限制
            timeout: 超时时间（秒），None使用默认配置
            
        Yields:
            BlockUpdateDTO: 区块更新对象
        """
        print(f"\n🌊 开始流式调用 StreamLatestBlocks")
        print(f"   起始高度: {'最新' if from_height == 0 else from_height}")
        print(f"   最大消息数: {max_messages if max_messages else '无限制'}")
        print(f"   超时时间: {timeout if timeout else self.stream_timeout}秒")
        print(f"   ⏳ 等待服务器推送数据...")
        
        try:
            # 构建请求
            request = demo_pb2.StreamLatestBlocksRequest(from_height=from_height)
            
            # 调用流式RPC
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response_stream = stub.StreamLatestBlocks(
                request, 
                timeout=timeout if timeout else self.stream_timeout
            )
            
            # 迭代接收数据
            count = 0
            for block_update in response_stream:
                yield block_update
                count += 1
                
                # 达到最大消息数量时停止
                if max_messages and count >= max_messages:
                    print(f"   ⏹️  已接收{max_messages}条消息，停止接收")
                    break
            
            print(f"   ✅ 流式调用完成，共接收 {count} 条消息")
            
        except grpc.RpcError as e:
            print(f"\n❌ gRPC流式错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"\n❌ 流式调用异常: {e}")
            raise
    
    def stream_latest_transactions(
        self,
        types: list = None,
        max_messages: int = None,
        timeout: float = None
    ) -> Iterator[Any]:
        """
        流式获取最新交易（服务端流式RPC）
        
        Args:
            types: 交易类型过滤列表，空列表表示不过滤
            max_messages: 最多接收的消息数量
            timeout: 超时时间（秒）
            
        Yields:
            TransactionUpdateDTO: 交易更新对象
        """
        if types is None:
            types = []
        
        print(f"\n🌊 开始流式调用 StreamLatestTransactions")
        print(f"   交易类型过滤: {'全部' if not types else types}")
        print(f"   最大消息数: {max_messages if max_messages else '无限制'}")
        print(f"   超时时间: {timeout if timeout else self.stream_timeout}秒")
        print(f"   ⏳ 等待服务器推送数据...")
        
        try:
            # 构建请求
            request = demo_pb2.StreamLatestTransactionsRequest(types=types)
            
            # 调用流式RPC
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response_stream = stub.StreamLatestTransactions(
                request,
                timeout=timeout if timeout else self.stream_timeout
            )
            
            # 迭代接收数据
            count = 0
            for tx_update in response_stream:
                yield tx_update
                count += 1
                
                if max_messages and count >= max_messages:
                    print(f"   ⏹️  已接收{max_messages}条消息，停止接收")
                    break
            
            print(f"   ✅ 流式调用完成，共接收 {count} 条消息")
            
        except grpc.RpcError as e:
            print(f"\n❌ gRPC流式错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"\n❌ 流式调用异常: {e}")
            raise
    
    def stream_account_updates(
        self,
        address: str,
        from_timestamp: int = 0,
        max_messages: int = None,
        timeout: float = None
    ) -> Iterator[Any]:
        """
        流式获取账户更新（服务端流式RPC）
        
        Args:
            address: 账户地址
            from_timestamp: 起始时间戳，0表示从当前时间开始
            max_messages: 最多接收的消息数量
            timeout: 超时时间（秒）
            
        Yields:
            AccountUpdateDTO: 账户更新对象
        """
        print(f"\n🌊 开始流式调用 StreamAccountUpdates")
        print(f"   账户地址: {address}")
        print(f"   起始时间戳: {'最近' if from_timestamp == 0 else from_timestamp}")
        print(f"   最大消息数: {max_messages if max_messages else '无限制'}")
        print(f"   超时时间: {timeout if timeout else self.stream_timeout}秒")
        print(f"   ⏳ 等待服务器推送数据...")
        
        try:
            # 构建请求
            request = demo_pb2.StreamAccountUpdatesRequest(
                address=address,
                from_timestamp=from_timestamp
            )
            
            # 调用流式RPC
            stub = demo_pb2_grpc.DemoStub(self.channel)
            response_stream = stub.StreamAccountUpdates(
                request,
                timeout=timeout if timeout else self.stream_timeout
            )
            
            # 迭代接收数据
            count = 0
            for acc_update in response_stream:
                yield acc_update
                count += 1
                
                if max_messages and count >= max_messages:
                    print(f"   ⏹️  已接收{max_messages}条消息，停止接收")
                    break
            
            print(f"   ✅ 流式调用完成，共接收 {count} 条消息")
            
        except grpc.RpcError as e:
            print(f"\n❌ gRPC流式错误: {e.code()} - {e.details()}")
            raise
        except Exception as e:
            print(f"\n❌ 流式调用异常: {e}")
            raise


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 使用with语句自动管理连接
    with ExplorerGRPCClient() as client:
        # 普通RPC调用示例
        print("=" * 80)
        print("普通RPC调用示例")
        print("=" * 80)
        
        # 健康检查
        health = client.check_healthy()
        print(f"健康状态: {health}")
        
        # 获取最新区块高度
        height = client.get_latest_block_height()
        print(f"最新区块高度: {height}")
        
        # 流式RPC调用示例
        print("\n" + "=" * 80)
        print("流式RPC调用示例")
        print("=" * 80)
        
        # 流式获取最新区块（限制3条）
        for block in client.stream_latest_blocks(max_messages=3):
            print(f"收到区块: 高度={block.block.height}")
