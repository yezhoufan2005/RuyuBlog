"""Playwright UI 测试 fixtures"""
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """自定义浏览器上下文"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
    }
