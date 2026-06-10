"""分类和标签接口测试"""


class TestCategories:
    """分类接口测试"""

    def test_category_list(self, session, api_base_url):
        """获取分类列表"""
        resp = session.get(f"{api_base_url}/category/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)


class TestTags:
    """标签接口测试"""

    def test_tag_list(self, session, api_base_url):
        """获取标签列表"""
        resp = session.get(f"{api_base_url}/tag/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)


class TestArticleFilter:
    """文章按分类/标签筛选"""

    def test_article_by_category(self, session, api_base_url):
        """按分类筛选文章"""
        resp = session.get(
            f"{api_base_url}/article/where/list/1",
            params={"type": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        # 空分类或不存在时正常返回
        assert "code" in body

    def test_article_by_tag(self, session, api_base_url):
        """按标签筛选文章"""
        resp = session.get(
            f"{api_base_url}/article/where/list/1",
            params={"type": "2"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "code" in body
