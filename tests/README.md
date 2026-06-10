# Ruyu-Blog 自动化测试

> SpringBoot3 + Vue3 个人博客系统 — 接口测试 + UI 自动化测试

---

## 项目概述

本目录包含 Ruyu-Blog 项目的完整自动化测试体系，涵盖 **Pytest API 接口测试** 和 **Playwright UI 自动化测试**，用于保障博客前台和后台管理系统的质量。

| 指标 | 数据 |
|------|------|
| API 测试用例 | 57 个 |
| UI 测试用例 | 25 个 |
| API 通过率 | 98%（56 passed, 1 skipped） |
| UI 通过率 | 100%（25 passed） |
| 测试框架 | Pytest + Playwright |
| 测试报告 | Allure |
| CI/CD | GitHub Actions |

---

## 目录结构

```
tests/
├── README.md                         # 本文件
├── .env.test                         # 测试环境配置
├── pytest.ini                        # Pytest + Allure 配置
├── requirements-test.txt             # Python 依赖
├── conftest.py                       # 全局共享 fixtures
│
├── api/                              # Pytest API 接口测试
│   ├── conftest.py                   # API 认证 fixtures（token、session）
│   ├── test_auth.py                  # 登录/注册/登出/用户信息（10）
│   ├── test_articles.py              # 文章列表/详情/搜索/热门（9）
│   ├── test_comments.py              # 评论读取/添加/权限（5）
│   ├── test_likes_favorites.py       # 点赞/收藏/取消/权限（8）
│   ├── test_categories_tags.py       # 分类/标签/筛选（4）
│   ├── test_public_endpoints.py      # Banner/友链/相册/树洞/留言（7）
│   ├── test_admin_crud.py            # 后台管理 CRUD（8）
│   └── test_error_cases.py           # 异常情况（5）
│
└── ui/                               # Playwright UI 自动化测试
    ├── conftest.py                   # Playwright fixtures（浏览器配置）
    ├── helpers.py                    # 登录辅助函数
    ├── test_blog_home.py             # 博客首页（3）
    ├── test_blog_article.py          # 文章详情页（2）
    ├── test_blog_auth_flow.py        # 登录/注册/重置流程（6）
    ├── test_blog_pages.py            # 时间轴/树洞/友链/相册等（8）
    ├── test_admin_login.py           # 后台登录（3）
    └── test_admin_crud.py            # 后台管理操作（3）
```

---

## 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 测试运行环境 |
| 后端服务 | SpringBoot 3.1.4 | http://localhost:8088 |
| 博客前端 | Vue3 + Vite | http://localhost:5173（或其他端口） |
| 后台前端 | Vue3 + Ant Design | http://localhost:6678（或其他端口） |
| MySQL | 8.0 | 含 blog 数据库 |
| Redis | 7.x | localhost:6379（Docker） |
| RabbitMQ | 3.13 | localhost:5672（Docker） |
| MinIO | latest | localhost:9000（Docker） |
| Playwright 浏览器 | Chromium | `playwright install chromium` |

---

## 安装

```bash
# 1. 安装 Python 依赖
pip install -r tests/requirements-test.txt

# 2. 安装 Playwright 浏览器（仅 UI 测试需要）
playwright install chromium

# 3. 确认 .env.test 中服务地址正确
# 默认值：API=http://localhost:8088, Blog=http://localhost:5173, Admin=http://localhost:6678
```

---

## 运行测试

### 全部测试

```bash
# API + UI 全部
pytest

# 仅 API
pytest tests/api/

# 仅 UI（有头模式，能看到浏览器操作）
pytest tests/ui/ --headed
pytest tests/ui/ -q              # 无头模式，终端简洁输出
```

### 按标签筛选

```bash
pytest -m smoke          # 冒烟测试
pytest -m auth           # 需要认证的测试
pytest -m slow           # 慢速测试
pytest -m "not slow"     # 跳过慢速测试
```

### 单文件/单用例

```bash
pytest tests/api/test_auth.py                           # 单个测试文件
pytest tests/api/test_auth.py::TestLogin::test_login_success  # 单个用例
```

---

## Allure 测试报告

```bash
# 安装 Allure
# macOS:  brew install allure
# Windows: scoop install allure
# 或下载：https://github.com/allure-framework/allure2/releases

# 运行测试（自动生成 allure-results）
pytest tests/api/ --alluredir=tests/allure-results

# 生成 HTML 报告
allure generate tests/allure-results -o tests/allure-report --clean

# 打开报告
allure open tests/allure-report
```

---

## CI/CD（GitHub Actions）

提交代码到 `master`/`main` 分支自动触发 `.github/workflows/test.yml`：

1. 启动 MySQL + Redis + RabbitMQ 服务容器
2. 设置 JDK 17 + Python 3.11
3. 导入数据库 SQL
4. 构建并启动后端
5. 运行全部 API 测试
6. 生成 Allure 报告并部署到 GitHub Pages

支持手动触发：GitHub → Actions → "API & UI 自动化测试" → Run workflow。

---

## 测试设计

### 认证流程

```
session（公共）  ──→ POST /user/login ──→ admin_token
                                    ──→ user_token
                                    ↓
                              所有请求带 Authorization: Bearer <token>
```

- `session`：公共请求（无需登录）
- `admin_session`：管理员请求（ADMIN / 123456）
- `user_session`：普通用户请求（自动创建测试用户，会话结束清理）

### 响应格式

```json
// 成功
{"code": 200, "msg": "success", "data": {...}

// 业务错误（HTTP 仍为 200）
{"code": 1001, "msg": "用户名或密码错误"}
{"code": 1002, "msg": "未登录"}
{"code": 1005, "msg": "验证码错误"}
{"code": 1007, "msg": "参数错误"}
```

### 测试数据管理

- 所有数据通过 API 创建和清理，不直连数据库
- `test_user_credentials` fixture 自动创建测试用户，会话结束时通过管理员删除
- 注册测试通过 Redis 注入验证码绕过邮件服务

---

## API 测试覆盖

### 认证模块（10 用例）

| 接口 | 用例 | 覆盖 |
|------|------|------|
| POST /user/login | 4 | 成功、错误密码、空用户名、空密码 |
| POST /user/register | 3 | 成功、重复用户名、缺少字段 |
| GET /user/auth/info | 2 | 已登录、未登录 |
| POST /user/logout | 1 | 正常登出 |

### 文章模块（9 用例）

| 接口 | 覆盖 |
|------|------|
| GET /article/list | 分页、页大小正确 |
| GET /article/detail/{id} | 无效 ID 处理 |
| GET /article/hot | 热门文章 |
| GET /article/recommend | 推荐文章 |
| GET /article/random | 随机文章 |
| GET /article/timeLine | 时间轴 |
| GET /article/search/init/title | 标题搜索初始化 |
| GET /article/search/by/content | 内容搜索 |

### 互动模块（12 用例）

| 模块 | 覆盖 |
|------|------|
| 评论 | 获取、分页、添加（auth）、未登录拒绝 |
| 点赞 | 点赞、取消、查询状态、未登录拒绝 |
| 收藏 | 收藏、取消、查询状态、未登录拒绝 |

### 后台管理（8 用例）

| 模块 | 覆盖 |
|------|------|
| 文章管理 | 列表、非管理员拒绝 |
| 用户管理 | 列表、用户详情 |
| 分类/标签 | 创建、非管理员拒绝 |
| 服务监控 | 服务器状态查询 |

### 公共接口 + 异常（18 用例）

| 模块 | 覆盖 |
|------|------|
| Banner/友链/相册/树洞/留言/网站信息 | 全部可访问 |
| 异常处理 | 无效 token、过期 token、空搜索、限流 |

---

## UI 测试覆盖

### 博客前台（17 用例）

| 模块 | 用例 | 说明 |
|------|------|------|
| 首页 | 3 | 标题检查、页面加载、smoke 测试 |
| 文章页 | 2 | 直接访问、从首页跳转 |
| 登录流程 | 3 | 登录成功、错误密码、登录页加载 |
| 注册流程 | 2 | 页面加载、表单渲染 |
| 重置密码 | 1 | 页面加载 |
| 页面巡检 | 8 | 时间轴、分类、标签、树洞、友链、关于、相册、留言 |

### 后台管理（8 用例）

| 模块 | 用例 | 说明 |
|------|------|------|
| 登录 | 3 | 登录成功、错误密码、登录页加载 |
| 仪表盘 | 3 | 页面加载、菜单可见、文章管理页 |

---

## 常见问题

**Q: 测试报 `1002` 未登录？**
检查后端是否运行中（`http://localhost:8088`）。

**Q: 测试报 `Connection refused`？**
确保后端、前台、后台三个服务都在运行。

**Q: 注册测试失败？**
检查 Redis 容器是否运行（`docker ps | grep redis`），test_conftest 需要通过 Docker 写入  Redis。

**Q: UI 测试超时？**
Playwright 默认等待 30 秒。如果页面加载慢，可以增加超时：`pytest --timeout=60`。

**Q: 数据库没文章怎么办？**
文章列表返回空数据（`"page": [], "total": 0`），测试兼容空数据场景。想测试详情页可以先通过后台发布文章。

---

## 依赖清单

```
# requirements-test.txt
pytest>=7.4.0
requests>=2.31.0
pytest-playwright>=0.4.0
python-dotenv>=1.0.0
allure-pytest>=2.13.0
```

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 测试框架 | Pytest 9.x |
| API 测试 | requests + session fixtures |
| UI 测试 | Playwright + pytest-playwright |
| 报告 | Allure Framework |
| CI/CD | GitHub Actions |
| 被测系统 | SpringBoot 3.1.4 + Vue 3 + MySQL + Redis + RabbitMQ + MinIO |
