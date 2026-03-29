# 🏗️ ChildFit 技术架构与实施方案 (v2.0 - Python + MySQL)

**文档版本**: v2.0  
**创建时间**: 2026-03-26  
**更新时间**: 2026-03-26 (Python + MySQL 方案)  
**基于**: 28 轮迭代成果  
**决策人**: 大王总 👑

---

## 第一部分：技术架构

### 1.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  微信小程序   │  │   Web 页面    │  │  管理后台    │      │
│  │  (家长/孩子) │  │  (H5/PC)     │  │    (Web)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        API 网关层                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Nginx | 限流 | 鉴权 | 日志 | 监控 | SSL 终止           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      业务服务层 (Python + FastAPI)           │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │用户服务│ │天气服务│ │推荐服务│ │打卡服务│ │通知服务│   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │活动服务│ │饮食服务│ │成就服务│ │数据服务│ │内容服务│   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    MySQL     │  │    Redis     │  │  文件存储    │      │
│  │  (主数据库)  │  │  (缓存/会话) │  │  (COS/OSS)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

### 1.2 技术栈选型

| 层级 | 技术 | 选型理由 | 成本 |
|------|------|----------|------|
| **前端框架** | uni-app + Vue 3 | 一套代码编译到小程序 + H5 + Web | 免费 |
| **前端语言** | TypeScript | 类型安全，开发效率高 | 免费 |
| **UI 框架** | uni-ui + uView | 跨端组件库 | 免费 |
| **后端框架** | Python + FastAPI | 开发速度快，AI 集成方便，大王总熟悉 | 免费 |
| **Web 框架** | Uvicorn + Gunicorn | ASGI 服务器，高性能 | 免费 |
| **数据库** | MySQL 8.0 | 成熟稳定，生态完善，运维简单 | 免费 |
| **ORM** | SQLAlchemy 2.0 + Alembic | Python 最佳实践，迁移管理 | 免费 |
| **缓存** | Redis 7 | 高性能缓存，会话管理 | 免费 |
| **认证** | JWT + PyJWT | 无状态认证，小程序友好 | 免费 |
| **存储** | 腾讯云 COS | 公益额度支持，图片/视频存储 | 公益免费 |
| **云服务** | 腾讯云 Lighthouse | 性价比高，公益支持 | 约 100 元/月 |
| **天气 API** | 和风天气 | 免费额度足够 | 免费 |
| **推送** | 微信模板消息 | 免费，到达率高 | 免费 |
| **部署** | Docker + Docker Compose | 一键部署，环境一致 | 免费 |
| **CI/CD** | GitHub Actions | 自动构建、测试、部署 | 免费 |

---

### 1.3 核心服务设计

#### 1.3.1 天气服务 (Python)

```python
# app/services/weather_service.py
from typing import Optional
from datetime import datetime
import httpx
import redis
import json

class WeatherService:
    """天气服务 - 接入和风天气 API"""
    
    def __init__(self):
        self.api_key = "YOUR_HEFENG_API_KEY"
        self.base_url = "https://devapi.qweather.com/v7"
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    async def get_current_weather(self, city: str) -> dict:
        """获取实时天气"""
        # 先查缓存
        cache_key = f"weather:current:{city}"
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # 调用 API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/weather/now",
                params={"location": city, "key": self.api_key}
            )
            data = response.json()
        
        # 缓存 30 分钟
        self.redis_client.setex(cache_key, 1800, json.dumps(data))
        return data
    
    async def get_forecast(self, city: str, days: int = 3) -> list:
        """获取天气预报"""
        cache_key = f"weather:forecast:{city}:{days}"
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/weather/3d",
                params={"location": city, "key": self.api_key}
            )
            data = response.json()
        
        self.redis_client.setex(cache_key, 3600, json.dumps(data))
        return data
    
    async def get_air_quality(self, city: str) -> dict:
        """获取空气质量 (AQI)"""
        cache_key = f"weather:aqi:{city}"
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/air/now",
                params={"location": city, "key": self.api_key}
            )
            data = response.json()
        
        self.redis_client.setex(cache_key, 1800, json.dumps(data))
        return data
```

#### 1.3.2 推荐引擎 (Python)

```python
# app/services/recommendation_engine.py
from typing import List
from datetime import datetime
from app.models.activity import Activity
from app.models.child_profile import ChildProfile

class RecommendationEngine:
    """智能推荐引擎 - 根据天气 + 作息 + 年龄段生成推荐"""
    
    def __init__(self):
        self.rules = self._init_rules()
    
    def _init_rules(self) -> list:
        """初始化推荐规则"""
        return [
            # 雾霾规则
            {
                "name": "雾霾天室内活动",
                "condition": lambda w: w.get("aqi", 0) > 150,
                "action": "indoor_only",
                "priority": 100,
            },
            # 高温规则
            {
                "name": "高温天避免户外",
                "condition": lambda w: w.get("temp", 0) > 35,
                "action": "avoid_outdoor",
                "priority": 90,
            },
            # 低温规则
            {
                "name": "低温天保暖活动",
                "condition": lambda w: w.get("temp", 0) < 5,
                "action": "warm_indoor",
                "priority": 90,
            },
            # 雷电规则
            {
                "name": "雷电天禁止户外",
                "condition": lambda w: w.get("warning") == "thunder",
                "action": "indoor_only",
                "priority": 100,
            },
            # 晴天优先户外
            {
                "name": "晴天鼓励户外",
                "condition": lambda w: w.get("condition") == "sunny",
                "action": "prefer_outdoor",
                "priority": 50,
            },
        ]
    
    def generate_daily_plan(
        self, 
        profile: ChildProfile, 
        weather: dict,
        date: datetime
    ) -> dict:
        """生成每日计划"""
        # 1. 匹配规则
        matched_rules = [
            rule for rule in self.rules 
            if rule["condition"](weather)
        ]
        
        # 2. 按优先级排序
        matched_rules.sort(key=lambda x: x["priority"], reverse=True)
        
        # 3. 获取活动类型限制
        activity_type = self._determine_activity_type(matched_rules)
        
        # 4. 根据年龄段筛选活动
        activities = self._filter_activities_by_age(
            profile.age_group, 
            activity_type
        )
        
        # 5. 根据偏好排序
        activities = self._personalize_ranking(
            activities, 
            profile.liked_activities
        )
        
        # 6. 生成计划
        return {
            "date": date.isoformat(),
            "weather": weather,
            "activities": activities[:5],  # 推荐 Top 5
            "outdoor_time": self._calc_outdoor_time(weather),
            "eye_care": self._generate_eye_care_plan(),
        }
    
    def _determine_activity_type(self, rules: list) -> str:
        """根据规则确定活动类型"""
        for rule in rules:
            if rule["action"] == "indoor_only":
                return "indoor"
            elif rule["action"] == "prefer_outdoor":
                return "outdoor"
        return "any"
    
    def _filter_activities_by_age(
        self, 
        age_group: str, 
        activity_type: str
    ) -> List[Activity]:
        """根据年龄段和活动类型筛选"""
        # TODO: 从数据库查询
        pass
    
    def _personalize_ranking(
        self, 
        activities: List[Activity], 
        liked: List[str]
    ) -> List[Activity]:
        """个性化排序"""
        # TODO: 根据偏好排序
        pass
    
    def _calc_outdoor_time(self, weather: dict) -> int:
        """计算推荐户外时间 (分钟)"""
        if weather.get("aqi", 0) > 150:
            return 0
        elif weather.get("temp", 20) > 35:
            return 30
        elif weather.get("temp", 20) < 5:
            return 30
        else:
            return 120  # 推荐每日 2 小时户外
    
    def _generate_eye_care_plan(self) -> dict:
        """生成护眼计划"""
        return {
            "outdoor_time": 120,  # 每日户外 2 小时
            "eye_exercises": [
                {"name": "眼保健操", "duration": 5, "times": 2},
                {"name": "远眺", "duration": 3, "times": 5},
            ],
            "screen_time_limit": 60,  # 每日屏幕时间不超过 60 分钟
        }
```

#### 1.3.3 用户服务 (FastAPI)

```python
# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/users", tags=["用户管理"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查是否已存在
    existing = db.query(User).filter(
        User.wx_openid == user_data.wx_openid
    ).first()
    if existing:
        raise HTTPException(400, "用户已存在")
    
    # 创建用户
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """获取用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "用户不存在")
    return user
```

---

### 1.4 数据库设计 (MySQL)

#### 核心表结构

```sql
-- 用户表
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    wx_openid VARCHAR(64) UNIQUE NOT NULL COMMENT '微信 OpenID',
    phone VARCHAR(20) COMMENT '手机号',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar_url VARCHAR(255) COMMENT '头像',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_wx_openid (wx_openid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 孩子档案表
CREATE TABLE child_profiles (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL COMMENT '所属用户 ID',
    name VARCHAR(50) NOT NULL COMMENT '孩子姓名',
    birth_date DATE NOT NULL COMMENT '出生日期',
    gender ENUM('male', 'female') NOT NULL COMMENT '性别',
    height DECIMAL(5,2) COMMENT '身高 (cm)',
    weight DECIMAL(5,2) COMMENT '体重 (kg)',
    bmi DECIMAL(5,2) GENERATED ALWAYS AS (weight / POW(height/100, 2)) COMMENT 'BMI',
    city VARCHAR(50) COMMENT '城市',
    family_structure ENUM('two_parent', 'single_parent', 'left_behind', 'other') 
        COMMENT '家庭结构',
    economic_status ENUM('low', 'medium', 'high') COMMENT '经济状况',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_birth_date (birth_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='孩子档案表';

-- 健康信息表
CREATE TABLE health_records (
    id VARCHAR(36) PRIMARY KEY,
    child_id VARCHAR(36) NOT NULL COMMENT '孩子 ID',
    disabilities JSON COMMENT '残疾信息',
    chronic_diseases JSON COMMENT '慢性病',
    allergies JSON COMMENT '过敏史',
    doctor_restrictions TEXT COMMENT '医生建议限制',
    emergency_contact VARCHAR(50) COMMENT '紧急联系人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES child_profiles(id) ON DELETE CASCADE,
    INDEX idx_child_id (child_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康信息表';

-- 活动库表
CREATE TABLE activities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '活动名称',
    description TEXT COMMENT '活动描述',
    age_min INT NOT NULL COMMENT '最小年龄',
    age_max INT NOT NULL COMMENT '最大年龄',
    type ENUM('indoor', 'outdoor', 'any') NOT NULL COMMENT '活动类型',
    cost_level ENUM('free', 'low', 'medium', 'high') NOT NULL COMMENT '成本等级',
    duration_min INT COMMENT '推荐时长 (分钟)',
    equipment JSON COMMENT '所需装备',
    weather_requirements JSON COMMENT '天气要求',
    special_groups JSON COMMENT '特殊群体适配',
    benefits JSON COMMENT '益处',
    difficulty ENUM('easy', 'medium', 'hard') COMMENT '难度',
    safety_tips JSON COMMENT '安全提示',
    video_url VARCHAR(255) COMMENT '教学视频 URL',
    image_url VARCHAR(255) COMMENT '封面图 URL',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_age_range (age_min, age_max),
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='活动库表';

-- 每日计划表
CREATE TABLE daily_plans (
    id VARCHAR(36) PRIMARY KEY,
    child_id VARCHAR(36) NOT NULL COMMENT '孩子 ID',
    plan_date DATE NOT NULL COMMENT '计划日期',
    weather_snapshot JSON COMMENT '天气快照',
    plan_data JSON NOT NULL COMMENT '计划内容',
    status ENUM('generated', 'confirmed', 'completed', 'skipped') 
        DEFAULT 'generated' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES child_profiles(id) ON DELETE CASCADE,
    UNIQUE KEY uk_child_date (child_id, plan_date),
    INDEX idx_plan_date (plan_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日计划表';

-- 打卡记录表
CREATE TABLE check_ins (
    id VARCHAR(36) PRIMARY KEY,
    plan_id VARCHAR(36) NOT NULL COMMENT '计划 ID',
    activity_id VARCHAR(36) COMMENT '活动 ID',
    check_in_type ENUM('manual', 'photo', 'video', 'voice') 
        NOT NULL COMMENT '打卡类型',
    media_url VARCHAR(255) COMMENT '媒体文件 URL',
    duration_min INT COMMENT '实际时长 (分钟)',
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '完成时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES daily_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE SET NULL,
    INDEX idx_plan_id (plan_id),
    INDEX idx_completed_at (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='打卡记录表';

-- 成就表
CREATE TABLE achievements (
    id VARCHAR(36) PRIMARY KEY,
    child_id VARCHAR(36) NOT NULL COMMENT '孩子 ID',
    achievement_type VARCHAR(50) NOT NULL COMMENT '成就类型',
    achievement_name VARCHAR(100) NOT NULL COMMENT '成就名称',
    description TEXT COMMENT '成就描述',
    icon_url VARCHAR(255) COMMENT '图标 URL',
    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '获得时间',
    metadata JSON COMMENT '元数据',
    FOREIGN KEY (child_id) REFERENCES child_profiles(id) ON DELETE CASCADE,
    INDEX idx_child_id (child_id),
    INDEX idx_achievement_type (achievement_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成就表';

-- 天气缓存表 (可选，用于离线查询)
CREATE TABLE weather_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    weather_data JSON NOT NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    UNIQUE KEY uk_city (city),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='天气缓存表';
```

---

## 第二部分：项目结构

### 2.1 后端目录结构

```
childfit-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── child_profile.py
│   │   ├── health_record.py
│   │   ├── activity.py
│   │   ├── daily_plan.py
│   │   └── check_in.py
│   ├── schemas/                # Pydantic 模式
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── child_profile.py
│   │   └── ...
│   ├── api/                    # API 路由
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── children.py
│   │   ├── weather.py
│   │   ├── recommendations.py
│   │   ├── check_ins.py
│   │   └── achievements.py
│   ├── services/               # 业务服务
│   │   ├── __init__.py
│   │   ├── weather_service.py
│   │   ├── recommendation_engine.py
│   │   ├── user_service.py
│   │   └── ...
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── auth.py
│       ├── logger.py
│       └── ...
├── tests/                      # 测试
│   ├── __init__.py
│   ├── test_users.py
│   └── ...
├── alembic/                    # 数据库迁移
│   ├── versions/
│   └── ...
├── requirements.txt            # Python 依赖
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 2.2 前端目录结构

```
childfit-frontend/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── pages/                  # 页面
│   │   ├── index/              # 首页
│   │   ├── plan/               # 今日计划
│   │   ├── checkin/            # 打卡
│   │   ├── achievement/        # 成就
│   │   └── profile/            # 个人中心
│   ├── components/             # 组件
│   │   ├── WeatherCard.vue
│   │   ├── ActivityList.vue
│   │   └── ...
│   ├── store/                  # Vuex 状态管理
│   │   ├── index.js
│   │   ├── user.js
│   │   └── ...
│   ├── api/                    # API 调用
│   │   ├── index.js
│   │   ├── user.js
│   │   └── ...
│   ├── utils/                  # 工具函数
│   └── static/                 # 静态资源
├── static/                     # 小程序静态文件
├── manifest.json               # uni-app 配置
├── pages.json                  # 页面配置
├── package.json
└── README.md
```

---

## 第三部分：部署方案

### 3.1 Docker Compose 配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  # MySQL 数据库
  mysql:
    image: mysql:8.0
    container_name: childfit-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: childfit
      MYSQL_USER: childfit
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      TZ: Asia/Shanghai
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./backend/scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - childfit-net
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: childfit-redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - childfit-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: childfit-backend
    restart: always
    environment:
      DATABASE_URL: mysql+pymysql://childfit:${MYSQL_PASSWORD}@mysql:3306/childfit
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      TZ: Asia/Shanghai
    ports:
      - "8000:8000"
    volumes:
      - ./backend/logs:/app/logs
      - ./uploads:/app/uploads
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - childfit-net
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: childfit-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
    networks:
      - childfit-net

networks:
  childfit-net:
    driver: bridge

volumes:
  mysql_data:
  redis_data:
```

### 3.2 后端 Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 创建日志目录
RUN mkdir -p /app/logs

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.3 Python 依赖

```txt
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
gunicorn==21.2.0
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0

# 数据库
sqlalchemy==2.0.25
alembic==1.13.1
pymysql==1.1.0
cryptography==42.0.0

# HTTP 客户端
httpx==0.26.0
requests==2.31.0

# 缓存
redis==5.0.1

# 认证
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# 工具
python-dotenv==1.0.0
python-dateutil==2.8.2
aiofiles==23.2.1

# 日志
loguru==0.7.2

# 测试
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

---

## 第四部分：API 设计

### 4.1 API 概览

| 模块 | 前缀 | 说明 |
|------|------|------|
| 用户 | `/api/users` | 用户注册、登录、信息 |
| 孩子 | `/api/children` | 孩子档案管理 |
| 天气 | `/api/weather` | 天气查询 |
| 推荐 | `/api/recommendations` | 智能推荐 |
| 计划 | `/api/plans` | 每日计划 |
| 打卡 | `/api/checkins` | 打卡记录 |
| 成就 | `/api/achievements` | 成就系统 |

### 4.2 核心 API 接口

```yaml
# 用户注册
POST /api/users/register
Body: { wx_openid, nickname, avatar_url }
Response: { id, wx_openid, created_at }

# 获取用户信息
GET /api/users/{user_id}
Response: { id, nickname, avatar_url, children: [...] }

# 创建孩子档案
POST /api/children
Body: { user_id, name, birth_date, gender, city, ... }
Response: { id, name, age_group, ... }

# 获取今日推荐
GET /api/recommendations/today?child_id=xxx
Response: { 
  date, 
  weather, 
  activities: [...], 
  outdoor_time,
  eye_care 
}

# 生成每日计划
POST /api/plans/generate
Body: { child_id, date }
Response: { plan_id, activities: [...] }

# 提交打卡
POST /api/checkins
Body: { plan_id, activity_id, type, media_url, duration }
Response: { id, completed_at }

# 获取成就列表
GET /api/achievements?child_id=xxx
Response: [{ id, name, icon_url, achieved_at }]
```

---

## 第五部分：开发计划

### 5.1 MVP 开发 (6 周)

| 周次 | 任务 | 交付物 |
|------|------|--------|
| Week 1 | 项目初始化、数据库设计 | 代码仓库、表结构 |
| Week 2 | 用户服务、天气服务 | 用户 CRUD、天气 API |
| Week 3 | 推荐引擎 V1、活动库 | 规则引擎、50 个活动 |
| Week 4 | 前端框架、首页 | 小程序 + Web 首页 |
| Week 5 | 打卡功能、成就系统 | 完整打卡流程 |
| Week 6 | 测试、部署、上线 | 生产环境、种子用户 |

---

## 第六部分：成本估算

| 项目 | 月成本 | 年成本 | 说明 |
|------|--------|--------|------|
| 云服务器 | 80-100 元 | 1,000 元 | 腾讯云 Lighthouse 2C4G |
| 域名 | 5 元 | 60 元 | .com/.cn 域名 |
| SSL 证书 | 0 元 | 0 元 | Let's Encrypt 免费 |
| 对象存储 | 0-30 元 | 300 元 | 腾讯云 COS (公益额度) |
| 短信 | 0-50 元 | 500 元 | 验证码 (可选) |
| **合计** | **~150 元/月** | **~1,860 元/年** | 公益项目可进一步降低 |

---

*文档版本：v2.0*  
*创建时间：2026-03-26*  
*决策人：大王总 👑*  
*下一步：启动 MVP 开发*
