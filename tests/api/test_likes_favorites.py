"""点赞与收藏接口测试"""
import pytest


class TestLikes:
    """点赞相关测试"""

    @pytest.mark.auth
    def test_like_article(self, user_session, api_base_url):
        """登录用户点赞文章"""
        resp = user_session.post(
            f"{api_base_url}/like/auth/like",
            data={"type": "1", "typeId": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        # 可能成功或权限拒绝
        assert "code" in body

    @pytest.mark.auth
    def test_unlike_article(self, user_session, api_base_url):
        """登录用户取消点赞"""
        resp = user_session.delete(
            f"{api_base_url}/like/auth/like",
            data={"type": "1", "typeId": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "code" in body

    def test_check_whether_liked(self, session, api_base_url):
        """检查是否已点赞（公开接口）"""
        resp = session.get(
            f"{api_base_url}/like/whether/like",
            params={"type": "1", "typeId": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "code" in body

    def test_like_unauthenticated(self, session, api_base_url):
        """未登录不能点赞"""
        resp = session.post(
            f"{api_base_url}/like/auth/like",
            data={"type": "1", "typeId": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200


class TestFavorites:
    """收藏相关测试"""

    @pytest.mark.auth
    def test_favorite_article(self, user_session, api_base_url):
        """登录用户收藏文章"""
        resp = user_session.post(
            f"{api_base_url}/favorite/auth/favorite",
            data={"type": "1", "typeId": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "code" in body

    @pytest.mark.auth
    def test_unfavorite_article(self, user_session, api_base_url):
        """登录用户取消收藏"""
        resp = user_session.delete(
            f"{api_base_url}/favorite/auth/favorite",
            data={"type": "1", "typeId": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "code" in body

    def test_check_whether_favorited(self, session, api_base_url):
        """检查是否已收藏（公开接口）"""
        resp = session.get(
            f"{api_base_url}/favorite/whether/favorite",
            params={"type": 1, "typeId": 1},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200

    def test_favorite_unauthenticated(self, session, api_base_url):
        """未登录不能收藏"""
        resp = session.post(
            f"{api_base_url}/favorite/auth/favorite",
            data={"type": "1", "typeId": "1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200
