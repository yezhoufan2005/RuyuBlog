# Ruyu-Blog（如雨博客）

基于 SpringBoot3 + Vue3 的前后端分离个人博客系统。

## 项目截图

### 博客前台

| 首页 | 文章详情 |
|------|----------|
| ![首页](img/new/前台首页.png) | ![文章](img/new/前台文章.png) |

| 评论 | 树洞 | 相册 |
|------|------|------|
| ![评论](img/new/前台评论表情包.png) | ![树洞](img/new/前台树洞.png) | ![相册](img/new/前台相册.png) |

### 后台管理

| 发布文章 | 文章列表 | 服务监控 |
|----------|----------|----------|
| ![发布](img/new/后台发布文章.png) | ![列表](img/new/后台文章列表.png) | ![监控](img/new/后台服务监控.png) |

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | SpringBoot 3.1.4 + MyBatis-Plus 3.5 + SpringSecurity + JWT |
| 数据库 | MySQL 8.0 + Redis 7.2 + RabbitMQ 3.13 |
| 存储 | MinIO（本地对象存储） |
| 博客前台 | Vue 3 + Element Plus + TypeScript + Pinia + TailwindCSS |
| 后台管理 | Vue 3 + Ant Design Vue + Antdv Pro |
| 测试 | Pytest + Playwright + Allure |
| 部署 | Docker + GitHub Actions |

## 功能模块

- **文章**：Markdown 编辑、代码高亮、分类标签、时间轴、搜索
- **互动**：评论（表情包 + Markdown）、点赞、收藏
- **权限**：RBAC 动态权限、动态菜单路由、黑名单管理
- **友链**：申请/审核/邮件通知
- **树洞**：匿名发布、弹幕展示
- **相册**：图片上传压缩、瀑布流展示
- **系统**：操作日志、登录日志、服务监控、定时任务
- **其他**：黑夜模式、音乐播放器、第三方登录（Gitee/GitHub）

## 运行环境

| 服务 | 版本 | 端口 |
|------|------|------|
| MySQL | 8.0 | 3306 |
| Redis | 7.2 | 6379 |
| RabbitMQ | 3.13 | 5672 (管理: 15672) |
| MinIO | latest | 9000 (控制台: 9001) |
| JDK | 17+ | - |
| Node.js | 16.17+ | - |

## 快速开始

### 1. 启动中间件

```bash
docker run -d --name redis -p 6379:6379 --restart unless-stopped redis:7.2-alpine
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 --restart unless-stopped rabbitmq:3.13-management-alpine
docker run -d --name minio -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin123 --restart unless-stopped minio/minio server /data --console-address ":9001"
```

### 2. 初始化数据库

```sql
CREATE DATABASE blog DEFAULT CHARACTER SET utf8mb4;
-- 导入 sql/v1.5.0/Ruyu-Blog_v1.5.0.sql
-- 导入 sql/v1.6.0/t_photo.sql
```

### 3. 配置并启动后端

```bash
cd blog-backend
# 编辑 src/main/resources/application-dev.yml 配置数据库连接
mvn clean package -DskipTests
java -jar target/blog-backend-0.0.1-SNAPSHOT.jar
# 后端运行在 http://localhost:8088
# API 文档: http://localhost:8088/doc.html
```

### 4. 启动前端

```bash
# 博客前台
cd blog-frontend/kuailemao-blog
pnpm install && pnpm dev
# 运行在 http://localhost:5173

# 后台管理
cd blog-frontend/kuailemao-admin
pnpm install --ignore-scripts && npx mist
# 运行在 http://localhost:6678
```

### 默认账号

- 后台管理：`ADMIN` / `123456`
- 测试账号：`Test` / `123456`

## 自动化测试

项目集成完整的自动化测试体系，详见 [tests/README.md](tests/README.md)。

```bash
pip install -r tests/requirements-test.txt
playwright install chromium

# 接口测试（57 用例，3.6 秒）
pytest tests/api/ -q

# UI 测试（25 用例）
pytest tests/ui/ -q --headed

# 生成 Allure 报告
allure generate tests/allure-results -o tests/allure-report --clean
allure open tests/allure-report
```

| 指标 | 数据 |
|------|------|
| API 用例 | 57 个 |
| UI 用例 | 25 个 |
| API 通过率 | 98% |
| UI 通过率 | 100% |

## 项目结构

```
Ruyu-Blog-master/
├── blog-backend/          # SpringBoot 后端
│   └── src/main/java/xyz/kuailemao/
│       ├── controller/    # REST 接口
│       ├── service/       # 业务逻辑
│       ├── mapper/        # MyBatis 数据层
│       ├── domain/        # 实体/DTO/VO
│       ├── config/        # Spring 配置
│       └── utils/         # 工具类
├── blog-frontend/
│   ├── kuailemao-blog/    # Vue3 博客前台
│   └── kuailemao-admin/   # Vue3 后台管理
├── sql/                   # 数据库脚本
├── tests/                 # 自动化测试
│   ├── api/               # Pytest 接口测试
│   └── ui/                # Playwright UI 测试
└── .github/workflows/     # CI/CD 流水线
```

## License

本项目基于原作者 [kuailemao/Ruyu-Blog](https://github.com/kuailemao/Ruyu-Blog) 二次开发，保留原有 MIT 协议。