"""
Playwright 浏览器自动化服务
提供统一的浏览器操作接口，支持页面导航、元素操作、截图等功能
"""

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
from typing import Optional, Dict, Any, List
import os
from pathlib import Path
import time


class PlaywrightService:
    """
    Playwright 浏览器自动化服务类
    提供完整的浏览器操作功能
    """
    
    def __init__(
        self,
        browser_type: str = "chromium",
        headless: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        timeout: int = 30000,
        navigation_timeout: int = 60000,
        screenshot_dir: str = "reports/screenshots"
    ):
        """
        初始化 Playwright 服务
        
        Args:
            browser_type: 浏览器类型，可选值: chromium, firefox, webkit
            headless: 是否无头模式运行
            viewport_width: 视口宽度
            viewport_height: 视口高度
            timeout: 默认超时时间（毫秒）
            navigation_timeout: 导航超时时间（毫秒）
            screenshot_dir: 截图保存目录
        """
        self.browser_type = browser_type
        self.headless = headless
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.timeout = timeout
        self.navigation_timeout = navigation_timeout
        self.screenshot_dir = screenshot_dir
        
        # Playwright 对象
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def start(self) -> None:
        """启动 Playwright 和浏览器"""
        if self.playwright is not None:
            print("⚠️  Playwright 已经启动")
            return
        
        print(f"🚀 启动 Playwright ({self.browser_type})...")
        self.playwright = sync_playwright().start()
        
        # 根据浏览器类型启动对应的浏览器
        if self.browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox"
                ]
            )
        elif self.browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=self.headless)
        elif self.browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=self.headless)
        else:
            raise ValueError(f"不支持的浏览器类型: {self.browser_type}，支持的类型: chromium, firefox, webkit")
        
        # 创建浏览器上下文
        self.context = self.browser.new_context(
            viewport={
                "width": self.viewport_width,
                "height": self.viewport_height
            }
        )
        
        # 设置超时
        self.context.set_default_timeout(self.timeout)
        
        # 创建页面
        self.page = self.context.new_page()
        self.page.set_default_navigation_timeout(self.navigation_timeout)
        
        print("✅ Playwright 启动成功")
    
    def goto(self, url: str, wait_until: str = "networkidle", timeout: Optional[int] = None) -> None:
        """
        导航到指定 URL
        
        Args:
            url: 目标 URL
            wait_until: 等待条件，可选值: load, domcontentloaded, networkidle, commit
            timeout: 超时时间（毫秒），None 则使用默认值
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        print(f"📍 导航到: {url}")
        timeout = timeout or self.navigation_timeout
        self.page.goto(url, wait_until=wait_until, timeout=timeout)
        print(f"✅ 页面加载完成")
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        点击元素
        
        Args:
            selector: CSS 选择器或文本选择器
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.timeout
        print(f"🖱️  点击元素: {selector}")
        self.page.click(selector, timeout=timeout)
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        填充输入框
        
        Args:
            selector: CSS 选择器
            value: 要填充的值
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.timeout
        print(f"✍️  填充输入框 {selector}: {value}")
        self.page.fill(selector, value, timeout=timeout)
    
    def type(self, selector: str, text: str, delay: int = 100, timeout: Optional[int] = None) -> None:
        """
        模拟键盘输入
        
        Args:
            selector: CSS 选择器
            text: 要输入的文本
            delay: 每个字符之间的延迟（毫秒）
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.timeout
        print(f"⌨️  输入文本到 {selector}")
        self.page.type(selector, text, delay=delay, timeout=timeout)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        获取元素文本内容
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间（毫秒）
            
        Returns:
            元素的文本内容
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.timeout
        text = self.page.locator(selector).text_content(timeout=timeout) or ""
        return text
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        获取元素属性值
        
        Args:
            selector: CSS 选择器
            attribute: 属性名
            timeout: 超时时间（毫秒）
            
        Returns:
            属性值，如果不存在返回 None
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.timeout
        return self.page.locator(selector).get_attribute(attribute, timeout=timeout)
    
    def wait_for_selector(self, selector: str, timeout: Optional[int] = None, state: str = "visible") -> None:
        """
        等待元素出现
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间（毫秒）
            state: 等待状态，可选值: attached, detached, visible, hidden
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.timeout
        print(f"⏳ 等待元素: {selector} (状态: {state})")
        self.page.wait_for_selector(selector, timeout=timeout, state=state)
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: Optional[int] = None) -> None:
        """
        等待页面加载状态
        
        Args:
            state: 加载状态，可选值: load, domcontentloaded, networkidle
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.navigation_timeout
        print(f"⏳ 等待页面加载状态: {state}")
        self.page.wait_for_load_state(state, timeout=timeout)
    
    def screenshot(self, path: Optional[str] = None, full_page: bool = False) -> str:
        """
        截图
        
        Args:
            path: 截图保存路径，None 则自动生成
            full_page: 是否截取整个页面
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        if path is None:
            # 自动生成截图路径
            os.makedirs(self.screenshot_dir, exist_ok=True)
            timestamp = int(time.time() * 1000)
            path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")
        
        print(f"📸 截图保存到: {path}")
        self.page.screenshot(path=path, full_page=full_page)
        return path
    
    def evaluate(self, script: str) -> Any:
        """
        在页面中执行 JavaScript 代码
        
        Args:
            script: JavaScript 代码
            
        Returns:
            执行结果
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        return self.page.evaluate(script)
    
    def get_title(self) -> str:
        """获取页面标题"""
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        return self.page.title()
    
    def get_url(self) -> str:
        """获取当前页面 URL"""
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        return self.page.url
    
    def reload(self, wait_until: str = "networkidle", timeout: Optional[int] = None) -> None:
        """
        重新加载页面
        
        Args:
            wait_until: 等待条件
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.navigation_timeout
        print("🔄 重新加载页面")
        self.page.reload(wait_until=wait_until, timeout=timeout)
    
    def go_back(self, wait_until: str = "networkidle", timeout: Optional[int] = None) -> None:
        """
        返回上一页
        
        Args:
            wait_until: 等待条件
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.navigation_timeout
        print("⬅️  返回上一页")
        self.page.go_back(wait_until=wait_until, timeout=timeout)
    
    def go_forward(self, wait_until: str = "networkidle", timeout: Optional[int] = None) -> None:
        """
        前进到下一页
        
        Args:
            wait_until: 等待条件
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，请先调用 start() 方法")
        
        timeout = timeout or self.navigation_timeout
        print("➡️  前进到下一页")
        self.page.go_forward(wait_until=wait_until, timeout=timeout)
    
    def close(self) -> None:
        """关闭浏览器和 Playwright"""
        print("🛑 关闭 Playwright 服务...")
        
        if self.page:
            self.page.close()
            self.page = None
        
        if self.context:
            self.context.close()
            self.context = None
        
        if self.browser:
            self.browser.close()
            self.browser = None
        
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
        
        print("✅ Playwright 服务已关闭")
    
    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
    
    def __del__(self):
        """析构函数，确保资源被释放"""
        if self.playwright is not None:
            try:
                self.close()
            except:
                pass

