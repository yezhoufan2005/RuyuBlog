"""博客其他公开页面测试"""
import pytest


class TestBlogPages:
    """页面可访问性测试"""

    @pytest.mark.parametrize("path,description", [
        ("/timeline", "时间轴"),
        ("/tree-hole", "树洞"),
        ("/link", "友链"),
        ("/about", "关于"),
        ("/photo", "相册"),
        ("/message", "留言板"),
    ])
    def test_page_loads(self, page, blog_ui_base_url, path, description):
        """各页面正常加载"""
        resp = page.goto(f"{blog_ui_base_url}{path}")
        page.wait_for_timeout(3000)
        # 页面可达且无服务端错误
        assert resp.status < 500, f"{description} 页面加载失败 (status={resp.status})"

    def test_category_page_loads(self, page, blog_ui_base_url):
        """分类页加载"""
        page.goto(f"{blog_ui_base_url}/category")
        page.wait_for_timeout(3000)
        assert page.locator("body").is_visible()

    def test_tags_page_loads(self, page, blog_ui_base_url):
        """标签页加载"""
        page.goto(f"{blog_ui_base_url}/tags")
        page.wait_for_timeout(3000)
        assert page.locator("body").is_visible()
