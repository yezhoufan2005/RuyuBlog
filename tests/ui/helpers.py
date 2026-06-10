"""Playwright UI 测试辅助函数"""


def blog_login(page, base_url, username="Test", password="123456"):
    """博客前台登录"""
    page.goto(f"{base_url}/login")
    page.wait_for_selector("input", timeout=5000)
    inputs = page.locator("input")
    if inputs.count() >= 2:
        inputs.nth(0).fill(username)
        inputs.nth(1).fill(password)
    page.locator("button").filter(has_text="登录").first.click()
    page.wait_for_timeout(2000)


def admin_login(page, base_url, username="ADMIN", password="123456"):
    """后台管理登录"""
    page.goto(f"{base_url}/login")
    page.wait_for_selector("input", timeout=10000)
    inputs = page.locator("input")
    if inputs.count() >= 2:
        inputs.nth(0).fill(username)
        inputs.nth(1).fill(password)
    # Ant Design 按钮可能有多种写法
    login_btn = page.locator("button").filter(has_text="登").first
    if login_btn.is_visible():
        login_btn.click()
    else:
        # fallback: 点击任意 type=submit 按钮
        page.locator("button[type='submit']").first.click()
    page.wait_for_timeout(3000)
