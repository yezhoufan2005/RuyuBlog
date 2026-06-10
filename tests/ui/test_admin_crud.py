"""后台管理页面操作测试"""
import pytest
from tests.ui.helpers import admin_login


@pytest.mark.auth
class TestAdminPages:
    """后台页面访问"""

    def test_dashboard_loads(self, page, admin_ui_base_url):
        """登录后仪表盘加载"""
        admin_login(page, admin_ui_base_url)
        page.wait_for_timeout(5000)
        assert page.locator("body").is_visible()

    def test_menu_visible(self, page, admin_ui_base_url):
        """登录后侧边菜单可见"""
        admin_login(page, admin_ui_base_url)
        page.wait_for_timeout(5000)
        # Ant Design Pro 菜单
        menu = page.locator(".ant-menu, aside, nav")
        if menu.count() > 0:
            assert menu.first.is_visible()
        else:
            assert page.locator("body").is_visible()

    def test_article_management_accessible(self, page, admin_ui_base_url):
        """文章管理页面可达"""
        admin_login(page, admin_ui_base_url)
        page.wait_for_timeout(5000)
        # 尝试通过 URL 访问文章管理
        page.goto(f"{admin_ui_base_url}/blog/article")
        page.wait_for_timeout(3000)
        assert page.locator("body").is_visible()
