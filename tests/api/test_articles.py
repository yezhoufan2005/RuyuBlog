"""文章相关公开接口测试"""
import pytest


class TestArticleList:
    """文章列表接口"""

    def test_article_list_pagination(self, session, api_base_url):
        """分页获取文章列表"""
        resp = session.get(
            f"{api_base_url}/article/list",
            params={"pageNum": 1, "pageSize": 10},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert "page" in body["data"]
        assert "total" in body["data"]

    def test_article_list_first_page(self, session, api_base_url):
        """第一页数据量与 pageSize 一致"""
        resp = session.get(
            f"{api_base_url}/article/list",
            params={"pageNum": 1, "pageSize": 5},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert len(body["data"]["page"]) <= 5


class TestArticleDetail:
    """文章详情接口"""

    @pytest.mark.skip(reason="数据库无文章数据，需先通过后台发布文章")
    def test_article_detail(self, session, article_id, api_base_url):
        """获取文章详情"""
        if article_id is None:
            pytest.skip("No articles in database")
        resp = session.get(f"{api_base_url}/article/detail/{article_id}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        data = body["data"]
        assert "articleTitle" in data or "article_title" in data

    def test_article_detail_invalid_id(self, session, api_base_url):
        """不存在的文章 ID 返回错误"""
        resp = session.get(f"{api_base_url}/article/detail/999999")
        assert resp.status_code == 200
        body = resp.json()
        # 不存在文章时返回错误码或空数据
        assert "code" in body


class TestFeaturedArticles:
    """推荐文章相关"""

    def test_hot_articles(self, session, api_base_url):
        """获取热门文章"""
        resp = session.get(f"{api_base_url}/article/hot")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)

    def test_recommend_articles(self, session, api_base_url):
        """获取推荐文章"""
        resp = session.get(f"{api_base_url}/article/recommend")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)

    def test_random_articles(self, session, api_base_url):
        """获取随机文章"""
        resp = session.get(f"{api_base_url}/article/random")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)

    def test_article_timeline(self, session, api_base_url):
        """获取时间轴数据"""
        resp = session.get(f"{api_base_url}/article/timeLine")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)


class TestArticleSearch:
    """文章搜索相关"""

    def test_search_init_title(self, session, api_base_url):
        """初始化标题搜索数据"""
        resp = session.get(f"{api_base_url}/article/search/init/title")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200

    def test_search_by_content(self, session, api_base_url):
        """按内容搜索文章"""
        resp = session.get(
            f"{api_base_url}/article/search/by/content",
            params={"content": "测试"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
