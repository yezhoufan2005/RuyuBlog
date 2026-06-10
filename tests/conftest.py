"""共享 fixtures，API 和 UI 测试共用"""
import os
import pytest
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env.test"))


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL", "http://localhost:8088")


@pytest.fixture(scope="session")
def blog_ui_base_url():
    return os.getenv("BLOG_UI_BASE_URL", "http://localhost:5173")


@pytest.fixture(scope="session")
def admin_ui_base_url():
    return os.getenv("ADMIN_UI_BASE_URL", "http://localhost:6678")
