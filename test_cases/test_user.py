import allure
import pytest
from utils.read_yaml import read_yaml


@allure.epic("api automation")
@allure.feature("用户管理模块")
@allure.story("用户登录，并提取token")
@pytest.mark.parametrize('set_env', ['TEST_ENV'], indirect=True)
@pytest.mark.parametrize('data', read_yaml('user.yaml')["user_tests"], ids=lambda c: c['case-id'])
def test_login(api, set_env, data):
    with allure.step("发送登录请求"):
        resp = api.do_post(path=data["path"], json=data["json"])
    with allure.step("校验code==200"):
        assert resp.status_code == 200
    with allure.step("提取token并注入client"):
        token = api.get_text(resp.json(), 'token')
        api.set_token(token)  # ← 关键：注入到实例
        assert api.token == token  # ← 确认注入成功


@pytest.mark.parametrize('set_env', ['TEST_ENV'], indirect=True)
def test_login2(api, set_env):
    print(api.token)
    json = {
        "items": [
            {
                "product_id": 1,
                "quantity": 1
            }
        ]
    }
    api.do_post(path="/add_to_cart", json=json)

