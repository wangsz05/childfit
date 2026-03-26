# 🏗️ ChildFit 技术架构与实施方案

**文档版本**: v1.0  
**创建时间**: 2026-03-26  
**基于**: 28 轮迭代成果

---

## 第一部分：技术架构

### 1.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  微信小程序   │  │     H5       │  │  管理后台    │      │
│  │  (家长/孩子) │  │  (分享/备选) │  │    (Web)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        API 网关层                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  限流 | 鉴权 | 日志 | 监控 | SSL 终止                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      业务服务层                              │
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
│  │ PostgreSQL   │  │    Redis     │  │  MongoDB     │      │
│  │  (主数据库)  │  │  (缓存/会话) │  │  (日志/行为) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │   OSS 存储    │  │   消息队列    │                         │
│  │ (图片/视频)  │  │  (异步任务)  │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈选型

| 层级 | 技术 | 选型理由 | 成本 |
|------|------|----------|------|
| **前端** | 微信小程序原生 | 覆盖广，无需安装 | 免费 |
| **前端** | Taro/uni-app | 一套代码多端部署 | 免费 |
| **后端** | Node.js + NestJS | 开发效率高，生态好 | 免费 |
| **数据库** | PostgreSQL | 开源，功能强大 | 免费 |
| **缓存** | Redis | 高性能缓存 | 免费 |
| **日志** | MongoDB | 灵活存储行为日志 | 免费 |
| **存储** | 腾讯云 COS | 公益额度支持 | 公益免费 |
| **云服务** | 腾讯云 Lighthouse | 性价比高，公益支持 | 约 100 元/月 |
| **天气 API** | 和风天气 | 免费额度足够 | 免费 |
| **推送** | 微信模板消息 | 免费，到达率高 | 免费 |

### 1.3 核心服务设计

#### 1.3.1 天气服务

```typescript
// 天气服务接口设计
interface WeatherService {
  // 获取实时天气
  getCurrentWeather(city: string): Promise<WeatherData>;
  
  // 获取天气预报
  getForecast(city: string, days: number): Promise<ForecastData[]>;
  
  // 获取天气预警
  getWarnings(city: string): Promise<WarningData[]>;
  
  // 天气适配推荐 (核心)
  getRecommendation(weather: WeatherData, profile: UserProfile): Promise<Activity[]>;
}

// 天气数据结构
interface WeatherData {
  city: string;
  condition: string;        // 晴/多云/雨/雪等
  temp: number;             // 温度
  feelsLike: number;        // 体感温度
  aqi: number;              // 空气质量指数
  humidity: number;         // 湿度
  windSpeed: number;        // 风速
  uvIndex: number;          // 紫外线指数
  warning?: WarningData;    // 预警信息
  updateTime: Date;         // 更新时间
}

// 缓存策略
const CACHE_CONFIG = {
  currentWeather: 1800,     // 30 分钟
  forecast: 3600,           // 1 小时
  warning: 900,             // 15 分钟
  recommendation: 3600,     // 1 小时 (同条件复用)
};
```

#### 1.3.2 推荐引擎

```typescript
// 推荐引擎接口
interface RecommendationEngine {
  // 生成每日计划
  generateDailyPlan(userId: string, date: Date): Promise<DailyPlan>;
  
  // 实时推荐 (天气突变时)
  getRealtimeRecommendation(userId: string): Promise<Activity[]>;
  
  // 个性化排序
  personalizeRanking(activities: Activity[], userPrefs: UserPrefs): Activity[];
}

// 推荐规则引擎 (MVP 用规则，后期加 ML)
class RuleEngine {
  private rules: WeatherRule[] = [];
  
  // 初始化规则
  initRules() {
    // 雾霾规则
    this.rules.push({
      condition: (w) => w.aqi > 150,
      action: 'indoor_only',
      priority: 100,
    });
    
    // 高温规则
    this.rules.push({
      condition: (w) => w.temp > 40,
      action: 'cancel_outdoor',
      priority: 100,
    });
    
    // 雷电规则
    this.rules.push({
      condition: (w) => w.warning?.type === 'thunder',
      action: 'indoor_only',
      priority: 100,
    });
    
    // ... 更多规则
  }
  
  // 执行规则
  execute(weather: WeatherData, profile: UserProfile): Recommendation {
    const matchedRules = this.rules.filter(r => r.condition(weather));
    const highestPriority = Math.max(...matchedRules.map(r => r.priority));
    const criticalRules = matchedRules.filter(r => r.priority === highestPriority);
    
    // 执行最高优先级规则
    return this.applyRules(criticalRules, profile);
  }
}
```

#### 1.3.3 用户服务

```typescript
// 用户档案结构
interface UserProfile {
  // 基础信息
  id: string;
  childName: string;
  birthDate: Date;
  gender: 'male' | 'female';
  height?: number;
  weight?: number;
  
  // 健康信息
  disabilities?: Disability[];
  chronicDiseases?: Disease[];
  allergies?: Allergy[];
  recentInjury?: Injury;
  doctorRestrictions?: string;
  medications?: Medication[];
  
  // 家庭信息
  familyStructure: FamilyStructure;
  economicStatus: EconomicStatus;
  city: string;
  livingEnvironment: LivingEnv;
  facilities: Facility[];
  caregiver: Caregiver;
  
  // 偏好设置
  likedActivities: string[];
  dislikedActivities: string[];
  availableTimeSlots: TimeSlot[];
  fontSize: FontSize;
  language: Language;
  
  // 计算字段
  age: number;              // 自动计算
  ageGroup: AgeGroup;       // 自动分组
  bmi?: number;             // 自动计算
}

// 健康问卷 (注册时填写)
interface HealthQuestionnaire {
  hasDisability: boolean;
  hasChronicDisease: boolean;
  hasAllergies: boolean;
  recentInjury: boolean;
  doctorRestrictions: string;
  emergencyContact: string;
  parentConsent: boolean;   // 家长授权确认
}
```

### 1.4 数据库设计

#### 核心表结构

```sql
-- 用户表
CREATE TABLE users (
  id UUID PRIMARY KEY,
  wx_openid VARCHAR(64) UNIQUE NOT NULL,
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 孩子档案表
CREATE TABLE child_profiles (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(50) NOT NULL,
  birth_date DATE NOT NULL,
  gender VARCHAR(10),
  height DECIMAL(5,2),
  weight DECIMAL(5,2),
  city VARCHAR(50),
  family_structure VARCHAR(20),
  economic_status VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 健康信息表
CREATE TABLE health_records (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES child_profiles(id),
  disabilities JSONB,
  chronic_diseases JSONB,
  allergies JSONB,
  doctor_restrictions TEXT,
  emergency_contact VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- 活动库表
CREATE TABLE activities (
  id UUID PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  age_range INT4RANGE,
  type VARCHAR(20),  -- indoor/outdoor
  cost_level VARCHAR(10),  -- free/low/medium/high
  duration_min INT,
  equipment JSONB,
  weather_requirements JSONB,
  special_groups JSONB,
  benefits TEXT[],
  difficulty VARCHAR(20),
  safety_tips TEXT[],
  video_url VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- 每日计划表
CREATE TABLE daily_plans (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES child_profiles(id),
  date DATE NOT NULL,
  weather_snapshot JSONB,
  plan_data JSONB NOT NULL,
  status VARCHAR(20),  -- generated/confirmed/completed
  created_at TIMESTAMP DEFAULT NOW()
);

-- 打卡记录表
CREATE TABLE check_ins (
  id UUID PRIMARY KEY,
  plan_id UUID REFERENCES daily_plans(id),
  activity_id UUID REFERENCES activities(id),
  check_in_type VARCHAR(20),  -- manual/photo/video/voice
  media_url VARCHAR(255),
  completed_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW()
);

-- 成就表
CREATE TABLE achievements (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES child_profiles(id),
  achievement_type VARCHAR(50),
  achieved_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB
);

-- 索引优化
CREATE INDEX idx_child_profiles_user ON child_profiles(user_id);
CREATE INDEX idx_daily_plans_child_date ON daily_plans(child_id, date);
CREATE INDEX idx_check_ins_plan ON check_ins(plan_id);
CREATE INDEX idx_activities_age ON activities USING GIST(age_range);
```

---

## 第二部分：开发实施

### 2.1 MVP 开发计划 (6 周)

#### Week 1-2: 基础框架

| 任务 | 负责人 | 交付物 |
|------|--------|--------|
| 项目初始化 | 后端 | 代码仓库、开发环境 |
| 数据库设计 | 后端 | 表结构、ER 图 |
| 小程序框架搭建 | 前端 | 基础页面、路由 |
| 天气 API 接入 | 后端 | 天气服务、缓存 |
| 用户档案 CRUD | 全栈 | 增删改查接口 |

#### Week 3-4: 核心功能

| 任务 | 负责人 | 交付物 |
|------|--------|--------|
| 天气规则引擎 | 后端 | 规则配置、执行逻辑 |
| 活动库搭建 (50 个) | 内容 | 活动数据、分类 |
| 推荐算法 V1 | 后端 | 规则推荐接口 |
| 一键生成计划 | 全栈 | 前端页面 + 后端接口 |
| 打卡功能 | 全栈 | 打卡流程、记录 |

#### Week 5: 辅助功能

| 任务 | 负责人 | 交付物 |
|------|--------|--------|
| 成就系统 | 全栈 | 徽章、进度追踪 |
| 数据可视化 | 前端 | 周报图表 |
| 通知推送 | 后端 | 模板消息推送 |
| 特殊儿童活动 (20 个) | 内容 | 专属活动数据 |

#### Week 6: 测试上线

| 任务 | 负责人 | 交付物 |
|------|--------|--------|
| 功能测试 | 测试 | 测试报告 |
| 性能优化 | 全栈 | 响应时间<200ms |
| 安全审查 | 安全 | 漏洞扫描报告 |
| 小范围内测 | 全体 | 10-20 个种子用户 |
| 正式上线 | 全体 | 正式发布 |

### 2.2 人员配置

| 角色 | 人数 | 职责 | 来源 |
|------|------|------|------|
| 产品负责人 | 1 | 需求、优先级、协调 | 核心发起 |
| 前端开发 | 2 | 小程序、H5、后台 | 志愿者 |
| 后端开发 | 2 | API、数据库、部署 | 志愿者 |
| UI 设计师 | 1 | 界面、图标、视觉 | 志愿者 |
| 内容运营 | 2 | 活动库、饮食库整理 | 志愿者 |
| 测试 | 1 | 测试用例、质量 | 志愿者 |
| 专家顾问 | 5-10 | 内容审核、专业指导 | 邀请 |

### 2.3 开发规范

#### 代码规范

```
- 语言：TypeScript (前后端统一)
- 代码风格：ESLint + Prettier
- Git 流程：Feature Branch + PR Review
- 提交规范：Conventional Commits
- 文档：代码注释 + API 文档 (Swagger)
```

#### 安全规范

```
- 认证：微信登录 + JWT
- 授权：RBAC 角色权限
- 加密：HTTPS + AES-256 (敏感数据)
- 输入验证：所有接口参数校验
- SQL 注入：参数化查询
- XSS 防护：输出转义
```

#### 测试规范

```
- 单元测试：覆盖率>80%
- 集成测试：核心流程覆盖
- E2E 测试：关键用户路径
- 性能测试：并发 1000+ 用户
- 安全测试：OWASP Top 10 检查
```

---

## 第三部分：运营与推广

### 3.1 冷启动策略

#### 种子用户获取 (100 人)

| 渠道 | 目标 | 方法 |
|------|------|------|
| 朋友圈 | 30 人 | 发起人和团队邀请 |
| 家长群 | 30 人 | 公益项目介绍，免费体验 |
| 学校合作 | 20 人 | 1-2 所试点学校 |
| 公益组织 | 20 人 | 合作机构推荐 |

#### 早期用户获取 (1000 人)

| 渠道 | 目标 | 方法 |
|------|------|------|
| 口碑传播 | 500 人 | 邀请好友机制 |
| 学校推广 | 300 人 | 5-10 所学校合作 |
| 媒体曝光 | 200 人 | 公益故事报道 |

### 3.2 合作伙伴拓展

#### 基金会 (资金支持)

| 基金会 | 方向 | 接触策略 |
|--------|------|----------|
| 腾讯公益 | 儿童健康/教育 | 公益平台申请 |
| 阿里巴巴公益 | 科技公益 | 公益项目大赛 |
| 中国青少年发展基金会 | 青少年健康 | 项目合作申请 |

#### 企业 CSR (资金 + 技术)

| 企业 | 方向 | 合作点 |
|------|------|--------|
| 腾讯云 | 云服务支持 | 公益额度申请 |
| 和风天气 | 天气 API | 公益免费额度 |
| 华为/小米 | 终端支持 | 预装/推广 |

#### 学校 (落地场景)

| 学校类型 | 目标 | 合作方式 |
|----------|------|----------|
| 城市小学 | 10 所 | 体育课补充工具 |
| 农村小学 | 20 所 | 公益帮扶项目 |
| 特殊教育学校 | 5 所 | 专属活动合作 |

#### 专家顾问 (专业背书)

| 领域 | 人数 | 职责 |
|------|------|------|
| 儿科医生 | 2-3 | 健康内容审核 |
| 运动专家 | 2-3 | 活动库审核 |
| 营养师 | 2-3 | 饮食建议审核 |
| 眼科医生 | 1-2 | 护眼内容审核 |
| 心理专家 | 1-2 | 心理健康内容 |

### 3.3 影响力评估

#### 核心指标

| 指标 | 目标 (1 年) | 测量方式 |
|------|-------------|----------|
| 覆盖孩子数 | 50,000+ | 注册用户统计 |
| 农村/留守占比 | 30%+ | 用户调研 |
| 合作学校 | 50+ | 合作协议 |
| 日均运动时长 | 60 分钟+ | 打卡数据 |
| 户外达标率 | 50%+ | 2 小时目标追踪 |
| 用户满意度 | 4.5/5.0+ | NPS 调研 |

#### 影响力报告

- **频率**: 季度发布
- **内容**: 用户数据、健康改善、典型案例
- **渠道**: 官网、公众号、合作媒体
- **用途**: 资助申请、合作伙伴沟通

---

## 第四部分：风险管理

### 4.1 风险识别

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|----------|
| 运动受伤 | 中 | 高 | 免责 + 保险 + 安全提示 |
| 数据泄露 | 低 | 极高 | 加密 + 合规 + 审计 |
| 资金断裂 | 中 | 高 | 多元化资金来源 |
| 核心团队流失 | 中 | 高 | 文档化 + 多人备份 |
| 用户增长缓慢 | 中 | 中 | 调整推广策略 |
| 竞品模仿 | 高 | 中 | 快速迭代 + 公益壁垒 |

### 4.2 法律合规

| 合规项 | 状态 | 负责人 |
|--------|------|--------|
| 隐私政策 | 待制定 | 法律顾问 |
| 用户协议 | 待制定 | 法律顾问 |
| 儿童信息保护 | 待合规审查 | 安全负责人 |
| 内容版权 | 待梳理 | 内容负责人 |
| 公众责任险 | 待购买 | 运营负责人 |

### 4.3 应急预案

| 事件 | 响应流程 |
|------|----------|
| 用户受伤 | 1. 紧急联系 2. 协助就医 3. 保险理赔 4. 事件复盘 |
| 数据泄露 | 1. 立即止损 2. 通知用户 3. 报告监管 4. 修复漏洞 |
| 服务中断 | 1. 切换备用 2. 通知用户 3. 恢复服务 4. 原因分析 |
| 负面舆情 | 1. 快速响应 2. 事实核查 3. 公开说明 4. 改进措施 |

---

## 第五部分：预算与资金

### 5.1 成本估算 (年)

| 项目 | 金额 | 说明 |
|------|------|------|
| 云服务器 | 1,200 元 | 腾讯云 Lighthouse |
| 域名/SSL | 200 元 | 域名 + 证书 |
| 短信费用 | 500 元 | 验证码/通知 |
| OSS 存储 | 300 元 | 图片/视频存储 |
| 公众责任险 | 2,000 元 | 公益保险 |
| 法律费用 | 3,000 元 | 条款审核 |
| 运营推广 | 5,000 元 | 物料/活动 |
| 应急储备 | 5,000 元 | 不可预见 |
| **合计** | **17,200 元/年** | 约 1,433 元/月 |

### 5.2 资金来源

| 来源 | 目标金额 | 状态 |
|------|----------|------|
| 基金会资助 | 10,000 元/年 | 筹备中 |
| 企业 CSR | 5,000 元/年 | 筹备中 |
| 个人捐赠 | 2,000 元/年 | 筹备中 |
| 云服务公益额度 | 抵扣服务器 | 申请中 |
| **合计** | **17,000 元/年** | - |

---

## 第六部分：附录

### 6.1 相关文档

| 文档 | 链接 |
|------|------|
| 项目规划 v4.0 | ./PROJECT_PLAN.md |
| 竞品分析报告 | ./COMPETITOR_ANALYSIS.md |
| 迭代笔记 (28 轮) | ./ITERATION_*.md |
| README | ./README.md |

### 6.2 联系方式

- 项目官网：待上线
- GitHub: 待开源
- 邮箱：待设置
- 微信公众号：待注册

---

*文档版本：v1.0*  
*创建时间：2026-03-26*  
*状态：规划完成，待执行*  
*下一步：启动 MVP 开发*
