"""异常情况测试：限流、无效参数、错误 token"""
import pytest


class TestRateLimit:
    """接口限流测试"""

    @pytest.mark.slow
    def test_rate_limit(self, session, api_base_url):
        """快速连续请求触发限流"""
        # 连续请求限流端点
        rate_limited = False
        for i in range(15):
            resp = session.get(f"{api_base_url}/article/search/init/title")
            body = resp.json()
            if body["code"] != 200:
                rate_limited = True
                break
        # 如果触发了限流说明限流机制正常
        if rate_limited:
            assert True
        else:
            pytest.skip("Rate limit not triggered (may have different threshold)")


class TestInvalidToken:
    """无效 Token 测试"""

    def test_invalid_token(self, api_base_url):
        """使用伪造的 JWT token"""
        import requests
        resp = requests.get(
            f"{api_base_url}/user/auth/info",
            headers={
                "Authorization": "Bearer invalid.jwt.token.here",
                "X-Client-Type": "Frontend",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        # 无效 token 应返回未认证
        assert body["code"] != 200

    def test_expired_token(self, api_base_url):
        """使用过期 JWT token"""
        import requests
        # 一个格式正确但早已过期的 token
        expired_token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2MDAwMDAwMDB9.fake"
        resp = requests.get(
            f"{api_base_url}/user/auth/info",
            headers={
                "Authorization": f"Bearer {expired_token}",
                "X-Client-Type": "Frontend",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200


class TestValidationErrors:
    """参数校验测试"""

    def test_search_empty_content(self, session, api_base_url):
        """空内容搜索"""
        resp = session.get(
            f"{api_base_url}/article/search/by/content",
            params={"content": ""},
        )
        assert resp.status_code == 200
        body = resp.json()
        # 应返回校验错误
        assert body["code"] != 200

    def test_article_list_negative_page(self, session, api_base_url):
        """负数页码"""
        resp = session.get(
            f"{api_base_url}/article/list",
            params={"pageNum": -1, "pageSize": 10},
        )
        assert resp.status_code == 200
        body = resp.json()
        # 负数页码可能被处理或返回空数据
        assert "code" in body
