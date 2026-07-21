# 接口自动化测试框架

基于 **Requests + Pytest + Allure + JsonPath + YAML** 的接口自动化测试框架，以本地部署的黑核商城 API 为被测对象，覆盖注册登录、商品管理、购物车、订单支付等完整电商业务链路。

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.10+ | 开发语言 |
| Requests | HTTP 请求 |
| Pytest | 测试框架（fixture / parametrize / hook / mark） |
| Allure | 可视化测试报告 |
| JsonPath | 响应数据提取与断言 |
| PyYAML | 测试数据驱动 |
| conf.ini | 多环境配置管理（TEST / DEV） |

---

## 框架分层

```
┌─────────────────────────────────┐
│         Allure 报告层            │  ← 步骤、请求详情、失败响应自动抓取
├─────────────────────────────────┤
│        Test Cases 测试层         │  ← 业务场景组装
├─────────────────────────────────┤
│        Test Data 数据层          │  ← YAML 数据驱动，新增用例不改代码
├─────────────────────────────────┤
│        ApiClient 请求层          │  ← requests 封装 / Token 管理 / JsonPath 断言
├─────────────────────────────────┤
│        Config 配置层             │  ← conf.ini 多环境切换（TEST_ENV / DEV_ENV）
└─────────────────────────────────┘
```

---

## 目录结构

```
heicore-mall-api-automation/
├── api/
│   └── api_client.py        # HTTP 请求封装（GET/POST/JsonPath提取/断言）
├── conf/
│   └── conf.ini             # 多环境配置（host / headers）
├── test_data/
│   ├── user.yaml            # 用户模块测试数据
│   └── smoke.yaml           # 冒烟测试数据
├── test_cases/
│   ├── conftest.py          # fixture（环境切换 / 登录前置 / 失败响应捕获钩子）
│   ├── test_user.py         # 用户模块（登录/注册/用户信息）
│   └── test_smoke.py        # 冒烟测试
├── utils/
│   ├── read_conf.py         # conf.ini 读取工具
│   ├── read_yaml.py         # YAML 读取工具
│   └── add_balance.py       # 管理员充值工具
├── reports/                 # Allure 报告输出
├── main.py                  # 运行入口
├── pytest.ini               # Pytest 配置（markers / addopts）
├── requirements.txt         # 依赖
└── README.md
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行测试

```bash
# 全部用例
python main.py

# 指定模块
python main.py user

# 冒烟测试
python main.py smoke
```

### 3. 查看 Allure 报告

```bash
# 方式一：自动生成并打开
python main.py

# 方式二：手动生成
allure generate ./reports/allure-results -o ./reports/allure_report --clean
allure open ./reports/allure_report
```

---

## 多环境切换

`conf/conf.ini` 中定义环境：

```ini
[TEST_ENV]
host = http://localhost:5050/

[DEV_ENV]
host = http://192.168.3.36:5050/
```

用例中通过 parametrize 切换：

```python
@pytest.mark.parametrize('set_env', ['TEST_ENV'], indirect=True)
def test_login(api, set_env, data):
    ...
```

---

## 核心特性

### Token 自动管理

登录成功后 `api.set_token(token)` 注入 Token，后续所有请求自动携带。

### 失败响应自动抓取

`conftest.py` 注册 `pytest_runtest_makereport` 钩子，用例失败时自动抓取最后一次请求的 URL、状态码、请求体、响应体，写入 Allure 报告。

### 数据驱动

新增测试场景只需在 YAML 文件中添加数据，无需修改用例代码：

```yaml
user_tests:
  - case-id: "USER-001"
    desc: "正常登录流程"
    path: "user_services/login"
    json:
      username: "user1"
      password: "password123"
```

### 接口串联

JsonPath 提取上一步响应数据 → 传给下一步请求：

```python
token = api.get_text(resp.json(), 'token')
api.set_token(token)
resp = api.do_get(path="/user_services/user_info")
```

---

