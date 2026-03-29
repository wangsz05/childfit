# ChildFit Backend API

🎗️ 孩子运动健康推荐系统 - 后端服务

## 项目简介

ChildFit 是一个智能的孩子运动健康推荐系统，根据天气、作息时间表、年龄段等因素，为孩子推荐适合的运动活动。

## 技术栈

- **Python 3.12**
- **FastAPI 0.109** - 现代高性能 Web 框架
- **SQLAlchemy 2.0** - ORM 框架
- **MySQL 8.0** - 数据库
- **Redis 7** - 缓存
- **Pydantic** - 数据验证

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── users.py         # 用户管理 API
│   │   ├── children.py      # 孩子档案 API
│   │   ├── weather.py       # 天气查询 API
│   │   ├── recommendations.py  # 智能推荐 API
│   │   ├── checkins.py      # 打卡记录 API
│   │   ├── achievements.py  # 成就系统 API
│   │   └── schedules.py     # 作息时间表 API
│   ├── models/              # 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── child_profile.py
│   │   ├── activity.py
│   │   ├── daily_plan.py
│   │   ├── checkin.py
│   │   ├── achievement.py
│   │   └── schedule.py
│   ├── schemas/             # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── child_profile.py
│   │   ├── activity.py
│   │   ├── daily_plan.py
│   │   ├── checkin.py
│   │   ├── achievement.py
│   │   └── schedule.py
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── child_service.py
│   │   ├── weather_service.py
│   │   ├── recommendation_service.py  # 核心推荐引擎
│   │   ├── checkin_service.py
│   │   ├── achievement_service.py
│   │   └── schedule_service.py
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── jwt_utils.py     # JWT 认证
│       ├── age_calculator.py  # 年龄计算
│       └── weather_rules.py   # 天气规则引擎
├── scripts/
│   └── init.sql             # 数据库初始化脚本
├── logs/                    # 日志目录 (运行时创建)
├── requirements.txt         # Python 依赖
├── .env.example            # 环境配置示例
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库、API Key 等
```

### 3. 初始化数据库

```bash
mysql -u root -p < scripts/init.sql
```

### 4. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

### 用户管理
- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/users/{user_id}` - 获取用户信息
- `PUT /api/users/{user_id}` - 更新用户信息

### 孩子档案
- `POST /api/children/` - 创建孩子档案
- `GET /api/children/?user_id=xxx` - 获取孩子列表
- `GET /api/children/{child_id}` - 获取孩子详情
- `PUT /api/children/{child_id}` - 更新孩子档案
- `DELETE /api/children/{child_id}` - 删除孩子档案

### 天气查询
- `GET /api/weather/?location=北京` - 获取实时天气
- `GET /api/weather/alert?location=北京` - 获取天气预警
- `GET /api/weather/recommendation?location=北京` - 获取天气活动推荐

### 智能推荐
- `POST /api/recommendations/generate` - 生成每日推荐
- `GET /api/recommendations/list?child_id=xxx` - 获取推荐列表
- `GET /api/recommendations/{plan_id}` - 获取计划详情
- `PUT /api/recommendations/{plan_id}/status` - 更新计划状态

### 打卡记录
- `POST /api/checkins/` - 创建打卡
- `GET /api/checkins/{checkin_id}` - 获取打卡详情
- `GET /api/checkins/child/{child_id}` - 获取打卡列表
- `GET /api/checkins/child/{child_id}/stats` - 获取打卡统计

### 成就系统
- `GET /api/achievements/types` - 获取成就类型
- `GET /api/achievements/child/{child_id}` - 获取孩子成就
- `POST /api/achievements/child/{child_id}/check` - 检查并授予成就

### 作息时间表
- `POST /api/schedules/` - 创建作息安排
- `GET /api/schedules/?child_id=xxx` - 获取作息列表
- `GET /api/schedules/{schedule_id}` - 获取作息详情
- `PUT /api/schedules/{schedule_id}` - 更新作息安排
- `DELETE /api/schedules/{schedule_id}` - 删除作息安排

## 核心功能

### 智能推荐引擎

推荐引擎位于 `app/services/recommendation_service.py`，核心逻辑：

1. **年龄适配**: 根据孩子年龄筛选适合的活动
2. **天气适配**: 
   - 晴天/多云 → 推荐户外活动
   - 雨天/雪天 → 推荐室内活动
   - 雾霾/沙尘暴 → 强制室内活动
3. **作息整合**: 结合孩子的作息时间表安排活动时段
4. **个性化推荐**: 根据家庭结构、经济状况等因素调整推荐

### 天气规则引擎

位于 `app/utils/weather_rules.py`：

- 解析天气类型 (晴、雨、雪、雾、霾等)
- 判断是否适合户外活动
- 提供天气相关建议 (防晒、保暖、防暑等)
- 计算天气适宜度评分 (0-100)

### 成就系统

预定义成就类型：
- 🎉 第一次打卡
- 💪 周坚持者 (连续 7 天)
- 🏆 月达人 (单月 20 次)
- 🌞 户外爱好者 (10 次户外活动)
- 🌅 早起鸟儿 (连续 5 天 9 点前打卡)

## 环境配置

### 必需配置

```env
# 数据库
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/childfit

# JWT
SECRET_KEY=your-secret-key-change-in-production

# 和风天气 API (可选，但推荐)
HEFENG_API_KEY=your-hefeng-api-key
```

### 可选配置

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# 腾讯云 COS (用于存储打卡媒体文件)
COS_BUCKET=your-bucket
COS_REGION=ap-guangzhou
COS_SECRET_ID=your-secret-id
COS_SECRET_KEY=your-secret-key
```

## 开发指南

### 添加新 API

1. 在 `app/api/` 创建新的路由文件
2. 在 `app/main.py` 中注册路由
3. 创建对应的 Service 层逻辑
4. 定义 Pydantic Schema

### 添加新模型

1. 在 `app/models/` 创建模型类
2. 在 `app/schemas/` 创建对应的 Schema
3. 更新 `scripts/init.sql`
4. 运行数据库迁移

### 测试

```bash
# 运行测试 (待实现)
pytest

# 检查代码风格
flake8 app/
```

## 注意事项

1. **生产环境**: 务必修改 `SECRET_KEY`，配置合适的 CORS 策略
2. **数据库**: 生产环境建议使用 Alembic 进行迁移管理
3. **API Key**: 和风天气 API Key 需要自行申请 (https://dev.qweather.com/)
4. **安全性**: 当前版本认证较简单，生产环境需加强安全措施

## License

MIT
