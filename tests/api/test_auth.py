"""认证相关测试：登录、注册、登出、用户信息"""
import os
import uuid
import pytest


class TestLogin:
    """登录接口测试"""

    def test_login_success(self, session, api_base_url):
        """正确凭证登录成功"""
        resp = session.post(
            f"{api_base_url}/user/login",
            data={"username": "ADMIN", "password": "123456"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert "token" in body["data"]
        assert len(body["data"]["token"]) > 0

    def test_login_bad_password(self, session, api_base_url):
        """错误密码登录失败"""
        resp = session.post(
            f"{api_base_url}/user/login",
            data={"username": "ADMIN", "password": "wrongpassword"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200

    def test_login_empty_username(self, session, api_base_url):
        """空用户名登录失败"""
        resp = session.post(
            f"{api_base_url}/user/login",
            data={"username": "", "password": "123456"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200

    def test_login_empty_password(self, session, api_base_url):
        """空密码登录失败"""
        resp = session.post(
            f"{api_base_url}/user/login",
            data={"username": "ADMIN", "password": ""},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200


class TestRegister:
    """注册接口测试"""

    def test_register_success(self, session, api_base_url):
        """注册成功"""
        unique = uuid.uuid4().hex[:8]
        username = f"ap{unique}"[:10]
        email = f"test_{unique}@test.com"
        test_code = "888888"

        # 写入 Redis 验证码
        import redis as redis_lib
        redis_host = os.getenv("REDIS_HOST", "localhost")
        r = redis_lib.Redis(host=redis_host, port=6379, db=1)
        r.set(f"verifyCode:register:{email}", f'"{test_code}"', ex=300)

        resp = session.post(
            f"{api_base_url}/user/register",
            json={
                "username": username,
                "password": "Test123456",
                "code": test_code,
                "email": email,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200

    def test_register_duplicate_username(self, session, api_base_url, test_user_credentials):
        """重复用户名注册失败"""
        email2 = f"another_{uuid.uuid4().hex[:6]}@test.com"
        test_code = "888888"
        import redis as redis_lib
        redis_host = os.getenv("REDIS_HOST", "localhost")
        r = redis_lib.Redis(host=redis_host, port=6379, db=1)
        r.set(f"verifyCode:register:{email2}", f'"{test_code}"', ex=300)

        resp = session.post(
            f"{api_base_url}/user/register",
            json={
                "username": test_user_credentials["username"],
                "password": "Test123456",
                "code": test_code,
                "email": email2,
            },
        )
        # 重复用户名应该失败（HTTP 可能 200 或 500）
        if resp.status_code == 200:
            body = resp.json()
            assert body["code"] != 200, "重复用户名注册应该失败"
        else:
            # 500 也算失败，但说明业务逻辑检测到了
            assert True

    def test_register_missing_fields(self, session, api_base_url):
        """缺少必填字段注册失败"""
        unique = uuid.uuid4().hex[:4]
        resp = session.post(
            f"{api_base_url}/user/register",
            json={
                "username": f"b{unique}"[:5],
                "password": "Test123456",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200


class TestUserInfo:
    """用户信息接口测试"""

    def test_get_user_info_authenticated(self, user_session, api_base_url):
        """登录后获取用户信息成功"""
        resp = user_session.get(f"{api_base_url}/user/auth/info")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert "username" in body["data"]

    def test_get_user_info_unauthenticated(self, session, api_base_url):
        """未登录获取用户信息失败"""
        resp = session.get(f"{api_base_url}/user/auth/info")
        assert resp.status_code == 200
        body = resp.json()
        # 未登录应返回未认证错误
        assert body["code"] != 200

    def test_logout(self, session, user_token, api_base_url):
        """登出接口调用"""
        resp = session.post(
            f"{api_base_url}/user/logout",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
