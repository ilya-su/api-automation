import pytest

from api.api_client import ApiClient


@pytest.fixture(scope='session')
def api():
    api = ApiClient()
    return api


@pytest.fixture(scope='session')
def set_env(request, api):
    """修改环境的方法。实现对API的环境读取的切换"""
    env = request.param
    api.set_env(env)


@pytest.fixture(scope='session')
def logged_in_api(api):
    """登录并注入token。所有需要鉴权的用例直接用这个fixture"""
    resp = api.do_post(path="/user_services/login", json={
        "username": "user1",
        "password": "password123"
    })
    assert resp.status_code == 200, f"登录失败: {resp.text}"
    token = api.get_text(resp.json(), 'token')
    api.set_token(token)
    return api


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """用例失败时自动抓取最后一次请求的响应"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        api = item.funcargs.get("api")
        if api and hasattr(api, "last_response") and api.last_response is not None:
            r = api.last_response
            # 写入 Allure 报告
            import allure
            allure.attach(
                f"URL: {r.url}\n"
                f"Status: {r.status_code}\n"
                f"Request Body: {r.request.body}\n"
                f"Response Body: {r.text[:2000]}",
                name=f"失败请求详情_{item.name}",
                attachment_type=allure.attachment_type.TEXT
            )
