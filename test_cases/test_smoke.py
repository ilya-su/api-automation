import allure
import pytest
from utils.add_balance import add_balance
from utils.read_yaml import read_yaml

@pytest.mark.smoke
@allure.epic("api automation")
@allure.feature("smoke")
@allure.story("冒烟测试：注册-登录-添加购物车-创建订单-支付订单")
@pytest.mark.parametrize('set_env', ['TEST_ENV'], indirect=True)
@pytest.mark.parametrize('data', read_yaml('smoke.yaml')["smoke"])
def test_smoke(api, set_env, data):
    with allure.step("用户注册"):
        resp = api.do_post(path=data['register']['path'], json=data['register']['json'])
        assert resp.status_code == 201,f"注册失败,详情：{resp.text}"
    with allure.step("充值"):
        user_id = api.get_text(resp.json(),'user_id')
        resp = add_balance(10000,user_id)
        assert resp.status_code == 200,"充值失败"
    with allure.step("登录"):
        resp = api.do_post(path=data['login']['path'], json=data['login']['json'])
        assert resp.status_code == 200,f"登录失败,详情：{resp.text}"
    with allure.step("提取token到apiclient实例"):
        token = api.get_text(resp.json(),'token')
        api.set_token(token)
        assert api.token == token,f"提取token失败,详情：{resp.text}"
    with allure.step("添加购物车"):
        resp = api.do_post(path=data['add_to_cart']['path'], json=data['add_to_cart']['json'])
        assert resp.status_code == 201,f"添加购物车失败,详情：{resp.text}"
    with allure.step("创建订单"):
        cart_id = api.get_text(resp.json(),'cart_id')
        data['order']['json']['cart_id'] = cart_id
        resp = api.do_post(path=data['order']['path'], json=data['order']['json'])
        assert resp.status_code == 201,f"订单创建失败,详情：{resp.text}"
    with allure.step("支付订单"):
        main_order_id = api.get_text(resp.json(),'main_order_id')
        data['pay']['json']['main_order_id'] = main_order_id
        resp = api.do_post(path=data['pay']['path'], json=data['pay']['json'])
        assert resp.status_code == 200,f"支付失败,详情：{resp.text}"
    with allure.step("获取用户信息"):
        resp = api.do_get(path=data['user_info']['path'])
        allure.attach(resp.text, name="接口返回", attachment_type=allure.attachment_type.TEXT)
