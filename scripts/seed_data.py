"""初始化博客测试数据：分类、标签、文章"""
import requests
import time

BASE = 'http://localhost:8088'
s = requests.Session()

# 登录
r = s.post(f'{BASE}/user/login',
           data={'username': 'ADMIN', 'password': '123456'},
           headers={'X-Client-Type': 'Backend'})
token = r.json()['data']['token']
s.headers.update({
    'Authorization': f'Bearer {token}',
    'X-Client-Type': 'Backend',
    'Content-Type': 'application/json'
})

# 创建分类
cats = ['Java', 'SpringBoot', 'Vue3', 'Python', '数据库', 'Linux']
for name in cats:
    r = s.put(f'{BASE}/category/back/add', json={'categoryName': name})
    print(f'分类 {name}: {r.json()}')
    time.sleep(0.3)

# 创建标签
tags = ['入门', '进阶', '实战', '源码分析', '面试', 'Docker']
for name in tags:
    r = s.put(f'{BASE}/tag/back/add', json={'tagName': name})
    print(f'标签 {name}: {r.json()}')
    time.sleep(0.3)

# 获取分类、标签 ID
cats_resp = s.get(f'{BASE}/category/back/list').json()
data = cats_resp['data']
cats_list = data['page'] if isinstance(data, dict) else data
cat_map = {c['categoryName']: c['id'] for c in cats_list}

tags_resp = s.get(f'{BASE}/tag/back/list').json()
data = tags_resp['data']
tags_list = data['page'] if isinstance(data, dict) else data
tag_map = {t['tagName']: t['id'] for t in tags_list}

print(f'分类ID: {cat_map}')
print(f'标签ID: {tag_map}')

# 文章内容
articles_data = [
    (cat_map['Java'], [tag_map['入门'], tag_map['面试']],
     'Java 基础：从面向对象到集合框架', 1,
     '# Java 基础：从面向对象到集合框架\n\n'
     '## 一、面向对象三大特性\n\n'
     '### 1. 封装\n把对象的属性和方法结合为一个整体，尽可能隐藏内部实现细节。\n\n'
     '```java\n'
     'public class Person {\n'
     '    private String name;\n'
     '    private int age;\n'
     '    public String getName() { return name; }\n'
     '    public void setName(String name) { this.name = name; }\n'
     '}\n'
     '```\n\n'
     '### 2. 继承\n子类继承父类的属性和方法，Java 是单继承机制。\n\n'
     '### 3. 多态\n同一方法调用，不同对象表现不同行为。\n\n'
     '## 二、集合框架\n\n'
     '| 接口 | 实现类 | 特点 |\n'
     '|------|--------|------|\n'
     '| List | ArrayList | 有序、可重复、索引访问快 |\n'
     '| Set | HashSet | 无序、不可重复 |\n'
     '| Map | HashMap | 键值对、键不可重复 |\n\n'
     '## 三、面试常见问题\n\n'
     '1. **ArrayList vs LinkedList**：底层结构不同\n'
     '2. **HashMap 原理**：数组+链表+红黑树\n'
     '3. **== vs equals**：== 比较引用，equals 比较内容'),

    (cat_map['SpringBoot'], [tag_map['进阶'], tag_map['实战']],
     'SpringBoot3 实战：构建 RESTful API 的最佳实践', 0,
     '# SpringBoot3 实战\n\n'
     '## 一、项目结构\n\n'
     '```\n'
     'controller/  -- 接收请求\n'
     'service/     -- 业务逻辑\n'
     'mapper/      -- 数据访问\n'
     'domain/      -- 实体类\n'
     'config/      -- 配置类\n'
     '```\n\n'
     '## 二、统一响应格式\n\n'
     '使用 Result<T> 封装所有接口返回值。\n\n'
     '## 三、全局异常处理\n\n'
     '使用 @RestControllerAdvice 统一处理异常。\n\n'
     '## 四、参数校验\n\n'
     'JSR 303 注解自动校验，无需手写 if-else。\n\n'
     '## 五、接口文档\n\n'
     '集成 Knife4j，访问 /doc.html 即可查看。'),

    (cat_map['Vue3'], [tag_map['入门'], tag_map['Docker']],
     'Vue3 + Vite 项目搭建与 Docker 部署', 1,
     '# Vue3 + Vite 搭建与部署\n\n'
     '## 一、项目初始化\n\n'
     '```bash\n'
     'npm create vue@latest\n'
     'npm install\n'
     'npm run dev\n'
     '```\n\n'
     '## 二、组合式 API\n\n'
     '使用 `<script setup>` 语法糖，代码更简洁。\n\n'
     '## 三、Docker 部署\n\n'
     '使用多阶段构建，减小镜像体积。\n\n'
     '## 四、总结\n\n'
     '前后端分离 + Docker 部署是现代 Web 开发的标准流程。'),

    (cat_map['Python'], [tag_map['进阶'], tag_map['源码分析']],
     'Python 自动化测试框架 pytest 深度解析', 0,
     '# pytest 深度解析\n\n'
     '## 一、为什么选 pytest\n\n'
     '- 简洁的断言语法（assert）\n'
     '- 强大的 fixture 机制\n'
     '- 丰富的插件生态\n\n'
     '## 二、Fixture 机制\n\n'
     'Fixture 是 pytest 的核心概念，用于管理测试前置条件和清理工作。\n\n'
     '```python\n'
     '@pytest.fixture(scope="session")\n'
     'def admin_token():\n'
     '    return login_and_get_token()\n'
     '```\n\n'
     '## 三、conftest.py\n\n'
     'conftest.py 中的 fixture 会被同目录下的所有测试文件自动发现。\n\n'
     '## 四、参数化测试\n\n'
     '```python\n'
     '@pytest.mark.parametrize("input,expected", [(1,2),(2,3)])\n'
     'def test_add(input, expected):\n'
     '    assert input + 1 == expected\n'
     '```'),

    (cat_map['数据库'], [tag_map['入门'], tag_map['实战']],
     'MySQL 索引优化实战：从原理到执行计划', 0,
     '# MySQL 索引优化实战\n\n'
     '## 一、索引的原理\n\n'
     'MySQL 默认使用 B+Tree 索引。叶子节点存储数据，非叶子节点存储键值。\n\n'
     '## 二、常见索引类型\n\n'
     '| 索引类型 | 特点 |\n'
     '|----------|------|\n'
     '| 主键索引 | 唯一、不为空 |\n'
     '| 唯一索引 | 值唯一 |\n'
     '| 普通索引 | 加速查询 |\n'
     '| 联合索引 | 最左前缀原则 |\n\n'
     '## 三、EXPLAIN 执行计划\n\n'
     '```sql\n'
     'EXPLAIN SELECT * FROM article WHERE category_id = 1;\n'
     '```\n\n'
     '关注 type、key、rows 三个字段。\n\n'
     '## 四、优化建议\n\n'
     '1. 避免 SELECT *\n'
     '2. 合理使用覆盖索引\n'
     '3. 注意索引失效场景（LIKE %开头、OR、函数等）'),

    (cat_map['Linux'], [tag_map['入门'], tag_map['Docker'], tag_map['实战']],
     'Docker 入门到实践：容器化你的应用', 0,
     '# Docker 入门到实践\n\n'
     '## 一、什么是 Docker\n\n'
     'Docker 是一个容器化平台，可以把应用及其依赖打包在一起运行。\n\n'
     '## 二、核心概念\n\n'
     '- **镜像（Image）**：应用的只读模板\n'
     '- **容器（Container）**：镜像的运行实例\n'
     '- **仓库（Registry）**：存储镜像的地方\n\n'
     '## 三、常用命令\n\n'
     '```bash\n'
     'docker pull nginx          # 拉取镜像\n'
     'docker run -d -p 80:80 nginx  # 运行容器\n'
     'docker ps                  # 查看容器\n'
     'docker exec -it xxx bash   # 进入容器\n'
     '```\n\n'
     '## 四、Docker Compose\n\n'
     '```yaml\n'
     'version: "3"\n'
     'services:\n'
     '  app:\n'
     '    build: .\n'
     '    ports:\n'
     '      - "8080:8080"\n'
     '  db:\n'
     '    image: mysql:8.0\n'
     '```\n\n'
     '多条命令即可启动整个微服务架构。'),
]

for cat_id, tag_ids, title, is_top, content in articles_data:
    body = {
        'categoryId': cat_id,
        'tagId': tag_ids,
        'articleCover': 'https://picsum.photos/800/400',
        'articleTitle': title,
        'articleContent': content,
        'articleType': 1,
        'isTop': is_top,
        'status': 1,
    }
    r = s.post(f'{BASE}/article/publish', json=body)
    print(f'文章 [{title[:30]}]: {r.json().get("msg", r.text[:80])}')
    time.sleep(0.5)

print('\n=== 数据初始化完成 ===')
print('分类: 6 个 | 标签: 6 个 | 文章: 6 篇')
