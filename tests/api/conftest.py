"""API 测试专用 fixtures"""
import os
import uuid
import pytest
import requests


@pytest.fixture(scope="session")
def session():
    """基础 HTTP session"""
    s = requests.Session()
    s.headers.update({"X-Client-Type": "Frontend"})
    return s


@pytest.fixture(scope="session")
def admin_token(session, api_base_url):
    """管理员登录获取 token，整个测试会话复用"""
    resp = session.post(
        f"{api_base_url}/user/login",
        data={"username": "ADMIN", "password": "123456"},
    )
    assert resp.status_code == 200, f"Admin login failed: {resp.text}"
    data = resp.json()
    assert data["code"] == 200, f"Admin login error: {data}"
    return data["data"]["token"]


@pytest.fixture(scope="session")
def admin_session(admin_token, api_base_url):
    """携带管理员 token 的 session"""
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {admin_token}",
        "X-Client-Type": "Backend",
    })
    return s


@pytest.fixture(scope="session")
def test_user_credentials(session, admin_session, api_base_url):
    """创建测试用户，会话结束后清理"""
    unique = uuid.uuid4().hex[:8]
    username = f"tu{unique}"[:10]  # 用户名最长10字符
    email = f"testuser_{unique}@test.com"
    password = "Test123456"

    # 通过 ask-code API 生成验证码并存入 Redis
    import os
    session.get(f"{api_base_url}/public/ask-code", params={"email": email, "type": "register"})

    # 直连 Redis 读取验证码（兼容本地 Docker 和 CI 环境）
    import redis as redis_lib
    redis_host = os.getenv("REDIS_HOST", "localhost")
    r = redis_lib.Redis(host=redis_host, port=6379, db=1, decode_responses=True)
    test_code = r.get(f"verifyCode:register:{email}")

    if not test_code:
        # FastJson 序列化格式：值带 JSON 引号
        test_code = "888888"
        r.setex(f"verifyCode:register:{email}", 300, f'"{test_code}"')
    else:
        # FastJson 反序列化：去除 JSON 引号
        test_code = test_code.strip('"')

    # 注册
    resp = session.post(
        f"{api_base_url}/user/register",
        json={
            "username": username,
            "password": password,
            "code": test_code,
            "email": email,
        },
    )
    assert resp.status_code == 200, f"Register failed: {resp.text}"
    body = resp.json()
    assert body["code"] == 200, f"Register error: {body}"

    yield {"username": username, "password": password, "email": email}

    # 清理：用管理员删除用户（如果存在）
    try:
        # 先查用户 ID
        resp = admin_session.get(f"{api_base_url}/user/list")
        if resp.status_code == 200:
            users = resp.json().get("data", {}).get("page", [])
            for u in users:
                if u.get("username") == username:
                    admin_session.delete(
                        f"{api_base_url}/user/delete",
                        data={"ids": str(u["id"])},
                    )
                    break
    except Exception:
        pass


@pytest.fixture(scope="session")
def user_token(session, test_user_credentials, api_base_url):
    """测试用户登录获取 token"""
    resp = session.post(
        f"{api_base_url}/user/login",
        data={
            "username": test_user_credentials["username"],
            "password": test_user_credentials["password"],
        },
    )
    assert resp.status_code == 200, f"User login failed: {resp.text}"
    data = resp.json()
    assert data["code"] == 200, f"User login error: {data}"
    return data["data"]["token"]


@pytest.fixture(scope="session")
def user_session(user_token, api_base_url):
    """携带测试用户 token 的 session"""
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {user_token}",
        "X-Client-Type": "Frontend",
    })
    return s


@pytest.fixture(scope="function")
def article_id(session, api_base_url):
    """获取第一篇文章的 ID，没有文章则返回 None"""
    resp = session.get(f"{api_base_url}/article/list", params={"pageNum": 1, "pageSize": 1})
    if resp.status_code == 200:
        body = resp.json()
        if body["code"] == 200 and body["data"]["page"]:
            return body["data"]["page"][0]["id"]
    return None
