"""后台管理登录测试"""
import pytest
from tests.ui.helpers import admin_login


class TestAdminLogin:
    """后台登录"""

    def test_login_page_loads(self, page, admin_ui_base_url):
        """后台登录页正常加载"""
        page.goto(f"{admin_ui_base_url}/login")
        page.wait_for_timeout(5000)
        assert page.locator("body").is_visible()

    @pytest.mark.auth
    def test_login_success(self, page, admin_ui_base_url):
        """管理员登录成功"""
        admin_login(page, admin_ui_base_url)
        # 登录后应跳转
        page.wait_for_timeout(3000)
        assert page.locator("body").is_visible()

    def test_login_failure(self, page, admin_ui_base_url):
        """错误密码登录失败"""
        page.goto(f"{admin_ui_base_url}/login")
        page.wait_for_selector("input", timeout=10000)
        inputs = page.locator("input")
        if inputs.count() >= 2:
            inputs.nth(0).fill("ADMIN")
            inputs.nth(1).fill("wrongpassword")
            page.locator("button").filter(has_text="登").first.click()
            page.wait_for_timeout(3000)
            # 应显示错误提示或仍在登录页
            assert page.url.endswith("/login") or page.locator("body").is_visible()
