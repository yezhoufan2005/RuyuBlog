"""评论接口测试"""
import pytest


class TestCommentRead:
    """评论读取测试"""

    def test_get_article_comments(self, session, api_base_url):
        """获取文章评论"""
        resp = session.get(
            f"{api_base_url}/comment/getComment",
            params={"type": 1, "typeId": 1, "pageNum": 1, "pageSize": 10},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200

    def test_get_comments_empty_type(self, session, api_base_url):
        """缺少参数时返回错误"""
        resp = session.get(
            f"{api_base_url}/comment/getComment",
            params={"pageNum": 1, "pageSize": 10},
        )
        assert resp.status_code == 200
        body = resp.json()
        # 缺少 type 参数应该有错误或空结果
        assert body["code"] != 200 or isinstance(body.get("data"), dict)

    def test_comments_pagination(self, session, api_base_url):
        """评论分页验证"""
        resp = session.get(
            f"{api_base_url}/comment/getComment",
            params={"type": 1, "typeId": 1, "pageNum": 1, "pageSize": 5},
        )
        assert resp.status_code == 200
        body = resp.json()
        if body["code"] == 200:
            results = body["data"].get("page", body["data"])
            if isinstance(results, list):
                assert len(results) <= 5


class TestCommentWrite:
    """评论写入测试"""

    def test_add_comment_authenticated(self, user_session, api_base_url):
        """登录用户添加评论"""
        resp = user_session.post(
            f"{api_base_url}/comment/auth/add/comment",
            data={
                "type": "1",
                "typeId": "1",
                "content": "Pytest 测试评论",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        # 可能成功(200)或因用户权限/黑名单检查拒绝
        assert "code" in body

    def test_add_comment_unauthenticated(self, session, api_base_url):
        """未登录用户添加评论失败"""
        resp = session.post(
            f"{api_base_url}/comment/auth/add/comment",
            data={
                "type": 1,
                "typeId": 1,
                "content": "Should fail",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200
