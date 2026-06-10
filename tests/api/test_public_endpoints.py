"""其他公开接口测试：Banner、友链、相册、树洞、留言、网站信息"""
import pytest


class TestBanners:
    """Banner 横幅接口"""

    def test_banners_list(self, session, api_base_url):
        """获取前台 Banner 列表"""
        resp = session.get(f"{api_base_url}/banners/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)


class TestLink:
    """友链接口"""

    def test_link_list(self, session, api_base_url):
        """获取友链列表"""
        resp = session.get(f"{api_base_url}/link/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert isinstance(body["data"], list)


class TestPhoto:
    """相册接口"""

    def test_photo_list(self, session, api_base_url):
        """获取相册/照片列表"""
        resp = session.get(
            f"{api_base_url}/photo/list",
            params={"pageNum": 1, "pageSize": 16},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200


class TestTreeHole:
    """树洞接口"""

    def test_treehole_list(self, session, api_base_url):
        """获取树洞列表"""
        resp = session.get(f"{api_base_url}/treeHole/getTreeHoleList")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200

    @pytest.mark.auth
    def test_add_treehole_authenticated(self, user_session, api_base_url):
        """登录用户添加树洞"""
        resp = user_session.post(
            f"{api_base_url}/treeHole/auth/addTreeHole",
            json={"content": "Pytest 测试树洞内容"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "code" in body


class TestLeaveWord:
    """留言接口"""

    def test_leaveword_list(self, session, api_base_url):
        """获取留言列表"""
        resp = session.get(f"{api_base_url}/leaveWord/list")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200


class TestWebsiteInfo:
    """网站信息接口"""

    def test_website_info_front(self, session, api_base_url):
        """获取前台网站信息"""
        resp = session.get(f"{api_base_url}/websiteInfo/front")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
