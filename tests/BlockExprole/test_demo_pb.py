"""
Playwright 服务使用示例
演示如何使用 PlaywrightService 进行浏览器自动化测试
"""

import unittest
from src.core.playwright_service import PlaywrightService
from src.core.config import config


class TestPlaywrightDemo(unittest.TestCase):
    """Playwright 服务测试示例"""
    
    def setUp(self):
        """测试前置准备"""
        # 创建 Playwright 服务实例
        self.service = PlaywrightService(
            browser_type="chromium",
            headless=True,  # 设置为 False 可以看到浏览器操作过程
            viewport_width=1920,
            viewport_height=1080,
            timeout=30000,
            screenshot_dir="reports/screenshots"
        )
        self.service.start()
        self.base_url = config.get_url()
        
    def tearDown(self):
        """测试后置清理"""
        if self.service:
            self.service.close()
    
    def test_open_page(self):
        """测试打开网页并截图"""
        # 导航到测试页面
        test_url = f"{self.base_url}demo/block/latest?page=1&page_size=1"
        self.service.goto(test_url)
        
        # 获取页面标题
        title = self.service.get_title()
        print(f"页面标题: {title}")
        
        # 获取当前 URL
        current_url = self.service.get_url()
        print(f"当前 URL: {current_url}")
        
        # 截图
        screenshot_path = self.service.screenshot()
        print(f"截图保存到: {screenshot_path}")
        
        # 断言
        self.assertIsNotNone(title)
        self.assertIn(self.base_url, current_url)
    
    def test_wait_for_element(self):
        """测试等待元素出现"""
        test_url = f"{self.base_url}demo/block/latest?page=1&page_size=1"
        self.service.goto(test_url)
        
        # 等待页面 body 元素出现
        self.service.wait_for_selector("body", state="visible")
        
        # 等待页面加载完成
        self.service.wait_for_load_state("networkidle")
        
        # 截图
        screenshot_path = self.service.screenshot(full_page=True)
        print(f"全页截图保存到: {screenshot_path}")
        
        self.assertTrue(True)
    
    def test_get_page_content(self):
        """测试获取页面内容"""
        test_url = f"{self.base_url}demo/block/latest?page=1&page_size=1"
        self.service.goto(test_url)
        
        # 获取页面文本内容
        body_text = self.service.get_text("body")
        print(f"页面内容长度: {len(body_text)}")
        
        # 执行 JavaScript 获取页面信息
        page_info = self.service.evaluate("""
            () => {
                return {
                    title: document.title,
                    url: window.location.href,
                    width: window.innerWidth,
                    height: window.innerHeight
                }
            }
        """)
        print(f"页面信息: {page_info}")
        
        # 截图
        screenshot_path = self.service.screenshot()
        print(f"截图保存到: {screenshot_path}")
        
        self.assertGreater(len(body_text), 0)
        self.assertIsNotNone(page_info)
    
    def test_context_manager(self):
        """测试使用上下文管理器"""
        with PlaywrightService(headless=True) as service:
            service.goto(f"{self.base_url}demo/block/latest?page=1&page_size=1")
            title = service.get_title()
            print(f"使用上下文管理器 - 页面标题: {title}")
            self.assertIsNotNone(title)
        # 自动关闭，无需手动调用 close()


if __name__ == "__main__":
    unittest.main()

