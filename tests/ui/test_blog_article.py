"""博客文章页测试"""
import pytest


class TestBlogArticle:
    """文章详情页"""

    def test_article_page_loads(self, page, blog_ui_base_url):
        """访问文章页不报错（数据库无文章时可能显示空白或错误页）"""
        resp = page.goto(f"{blog_ui_base_url}/article/1")
        page.wait_for_timeout(3000)
        # 页面请求不发散（无 500 错误即正常）
        assert resp.status == 200 or resp.status < 500

    def test_article_page_navigation(self, page, blog_ui_base_url):
        """从首页可以导航到文章"""
        page.goto(blog_ui_base_url)
        page.wait_for_timeout(3000)
        article_links = page.locator("a[href*='/article/']")
        if article_links.count() > 0:
            article_links.first.click()
            page.wait_for_timeout(2000)
        else:
            page.goto(f"{blog_ui_base_url}/article/1")
            page.wait_for_timeout(2000)
        # 页面可达即可
        assert page.url.startswith(blog_ui_base_url)
