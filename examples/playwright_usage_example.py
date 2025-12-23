"""
Playwright 服务使用示例
演示如何使用 PlaywrightService 进行浏览器自动化操作
"""

from src.core.playwright_service import PlaywrightService


def example_basic_usage():
    """基本使用示例"""
    print("=" * 50)
    print("示例 1: 基本使用")
    print("=" * 50)
    
    # 创建服务实例
    service = PlaywrightService(
        browser_type="chromium",
        headless=True,  # False 可以看到浏览器操作
        viewport_width=1920,
        viewport_height=1080
    )
    
    try:
        # 启动浏览器
        service.start()
        
        # 导航到页面
        service.goto("https://example.com")
        
        # 获取页面标题
        title = service.get_title()
        print(f"页面标题: {title}")
        
        # 截图
        screenshot_path = service.screenshot()
        print(f"截图保存到: {screenshot_path}")
        
    finally:
        # 关闭浏览器
        service.close()


def example_context_manager():
    """使用上下文管理器示例（推荐）"""
    print("\n" + "=" * 50)
    print("示例 2: 使用上下文管理器（推荐）")
    print("=" * 50)
    
    # 使用 with 语句，自动管理资源
    with PlaywrightService(headless=True) as service:
        service.goto("https://example.com")
        
        # 获取页面信息
        title = service.get_title()
        url = service.get_url()
        
        print(f"页面标题: {title}")
        print(f"页面 URL: {url}")
        
        # 执行 JavaScript
        page_info = service.evaluate("""
            () => {
                return {
                    title: document.title,
                    url: window.location.href,
                    userAgent: navigator.userAgent
                }
            }
        """)
        print(f"页面信息: {page_info}")
        
        # 截图
        service.screenshot()
    
    # 自动关闭，无需手动调用 close()


def example_element_operations():
    """元素操作示例"""
    print("\n" + "=" * 50)
    print("示例 3: 元素操作")
    print("=" * 50)
    
    with PlaywrightService(headless=True) as service:
        # 导航到测试页面
        service.goto("https://example.com")
        
        # 等待元素出现
        service.wait_for_selector("body", state="visible")
        
        # 获取元素文本
        body_text = service.get_text("body")
        print(f"Body 文本长度: {len(body_text)}")
        
        # 获取元素属性（如果有的话）
        # href = service.get_attribute("a", "href")
        # print(f"链接地址: {href}")


def example_form_operations():
    """表单操作示例（需要实际的表单页面）"""
    print("\n" + "=" * 50)
    print("示例 4: 表单操作")
    print("=" * 50)
    
    with PlaywrightService(headless=True) as service:
        # 导航到包含表单的页面
        # service.goto("https://example.com/form")
        
        # 填充输入框
        # service.fill("input#username", "testuser")
        # service.fill("input#password", "testpass")
        
        # 点击按钮
        # service.click("button#submit")
        
        # 等待页面跳转
        # service.wait_for_load_state("networkidle")
        
        print("表单操作示例（需要实际的表单页面）")


def example_screenshot_options():
    """截图选项示例"""
    print("\n" + "=" * 50)
    print("示例 5: 截图选项")
    print("=" * 50)
    
    with PlaywrightService(headless=True) as service:
        service.goto("https://example.com")
        
        # 普通截图
        path1 = service.screenshot("reports/screenshots/normal.png")
        print(f"普通截图: {path1}")
        
        # 全页截图
        path2 = service.screenshot("reports/screenshots/full_page.png", full_page=True)
        print(f"全页截图: {path2}")


def example_navigation():
    """页面导航示例"""
    print("\n" + "=" * 50)
    print("示例 6: 页面导航")
    print("=" * 50)
    
    with PlaywrightService(headless=True) as service:
        # 导航到第一个页面
        service.goto("https://example.com")
        print(f"当前页面: {service.get_url()}")
        
        # 导航到第二个页面
        service.goto("https://www.python.org")
        print(f"当前页面: {service.get_url()}")
        
        # 返回上一页
        service.go_back()
        print(f"返回后页面: {service.get_url()}")
        
        # 前进到下一页
        service.go_forward()
        print(f"前进后页面: {service.get_url()}")
        
        # 重新加载页面
        service.reload()
        print(f"重新加载后页面: {service.get_url()}")


if __name__ == "__main__":
    # 运行所有示例
    example_basic_usage()
    example_context_manager()
    example_element_operations()
    example_form_operations()
    example_screenshot_options()
    example_navigation()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)

