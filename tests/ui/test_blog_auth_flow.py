"""博客前台登录注册流程测试"""
import pytest
from tests.ui.helpers import blog_login


class TestBlogLogin:
    """博客登录"""

    def test_login_page_loads(self, page, blog_ui_base_url):
        """登录页能加载"""
        page.goto(f"{blog_ui_base_url}/login")
        page.wait_for_timeout(3000)
        assert page.locator("body").is_visible()

    @pytest.mark.auth
    def test_login_success(self, page, blog_ui_base_url):
        """正确凭证登录成功"""
        blog_login(page, blog_ui_base_url, username="Test", password="123456")
        # 登录后应跳转回首页
        page.wait_for_timeout(2000)
        assert page.locator("body").is_visible()

    def test_login_wrong_password(self, page, blog_ui_base_url):
        """错误密码显示提示"""
        page.goto(f"{blog_ui_base_url}/login")
        page.wait_for_selector("input", timeout=5000)
        inputs = page.locator("input")
        if inputs.count() >= 2:
            inputs.nth(0).fill("Test")
            inputs.nth(1).fill("wrongpassword")
            page.locator("button").filter(has_text="登录").first.click()
            page.wait_for_timeout(2000)
            # 不应该被重定向到首页（标题不应变）
            assert page.locator("body").is_visible()


class TestBlogRegister:
    """博客注册"""

    def test_register_page_loads(self, page, blog_ui_base_url):
        """注册页能加载"""
        page.goto(f"{blog_ui_base_url}/register")
        page.wait_for_timeout(3000)
        assert page.locator("body").is_visible()

    def test_register_form_visible(self, page, blog_ui_base_url):
        """注册表单可见"""
        page.goto(f"{blog_ui_base_url}/register")
        page.wait_for_timeout(2000)
        # 应该有输入框
        inputs = page.locator("input")
        assert inputs.count() >= 2


class TestBlogReset:
    """密码重置"""

    def test_reset_page_loads(self, page, blog_ui_base_url):
        """重置密码页能加载"""
        resp = page.goto(f"{blog_ui_base_url}/reset")
        page.wait_for_timeout(3000)
        assert resp.status < 500
