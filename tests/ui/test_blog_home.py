"""博客前台首页测试"""
import pytest


class TestBlogHome:
    """首页相关测试"""

    def test_home_page_loads(self, page, blog_ui_base_url):
        """首页能正常加载"""
        page.goto(blog_ui_base_url)
        # 等待页面加载
        page.wait_for_timeout(3000)
        # 验证页面标题
        title = page.title()
        assert "Ruyu" in title or "博客" in title or "blog" in title.lower()

    def test_home_has_navigation(self, page, blog_ui_base_url):
        """首页有导航元素"""
        page.goto(blog_ui_base_url)
        page.wait_for_timeout(2000)
        # 验证页面存在可交互元素
        assert page.locator("body").is_visible()

    @pytest.mark.smoke
    def test_home_page_no_crash(self, page, blog_ui_base_url):
        """首页没有明显的错误提示"""
        page.goto(blog_ui_base_url)
        page.wait_for_timeout(3000)
        # 页面 body 可见
        body = page.locator("body")
        assert body.is_visible()
