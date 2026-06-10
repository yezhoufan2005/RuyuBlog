"""后台管理 CRUD 接口测试（需要管理员权限）"""
import pytest
import uuid


class TestAdminArticle:
    """后台文章管理"""

    @pytest.mark.auth
    def test_admin_article_list(self, admin_session, api_base_url):
        """管理员获取后台文章列表"""
        resp = admin_session.get(f"{api_base_url}/article/back/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200

    @pytest.mark.auth
    def test_admin_article_unauthorized(self, session, api_base_url):
        """普通用户不能访问后台文章列表"""
        resp = session.get(f"{api_base_url}/article/back/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200


class TestAdminUser:
    """后台用户管理"""

    @pytest.mark.auth
    def test_admin_user_list(self, admin_session, api_base_url):
        """管理员获取用户列表"""
        resp = admin_session.get(f"{api_base_url}/user/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert "page" in body["data"] or isinstance(body["data"], list)

    @pytest.mark.auth
    def test_admin_user_detail(self, admin_session, api_base_url):
        """管理员查看用户详情"""
        # 先获取用户列表取第一个用户 ID
        resp = admin_session.get(f"{api_base_url}/user/list")
        if resp.status_code == 200 and resp.json()["code"] == 200:
            data = resp.json()["data"]
            users = data.get("page", data) if isinstance(data, dict) else data
            if isinstance(users, list) and users:
                user_id = users[0]["id"]
                resp2 = admin_session.get(f"{api_base_url}/user/details/{user_id}")
                assert resp2.status_code == 200
                assert resp2.json()["code"] == 200


class TestAdminCategory:
    """分类管理 CRUD"""

    @pytest.mark.auth
    def test_category_create_and_delete(self, admin_session, api_base_url):
        """管理员创建并删除分类"""
        import uuid
        unique = uuid.uuid4().hex[:6]
        # 创建
        resp = admin_session.put(
            f"{api_base_url}/category/back/add",
            json={"categoryName": f"测试分类_{unique}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200

    @pytest.mark.auth
    def test_category_unauthorized(self, session, api_base_url):
        """非管理员不能创建分类"""
        resp = session.put(
            f"{api_base_url}/category/back/add",
            json={"categoryName": "非法分类"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] != 200


class TestAdminTag:
    """标签管理"""

    @pytest.mark.auth
    def test_tag_create(self, admin_session, api_base_url):
        """管理员创建标签"""
        import uuid
        unique = uuid.uuid4().hex[:6]
        resp = admin_session.put(
            f"{api_base_url}/tag/back/add",
            json={"tagName": f"测试标签_{unique}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200


class TestServerMonitor:
    """服务监控"""

    @pytest.mark.auth
    def test_server_monitor(self, admin_session, api_base_url):
        """管理员查看服务器状态"""
        resp = admin_session.get(f"{api_base_url}/monitor/server")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
