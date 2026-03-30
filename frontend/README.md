# ChildFit Frontend

🎗️ 儿童运动健康推荐系统 - Vue 3 前端

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Vue Router 4** - 官方路由管理器
- **Pinia** - Vue 官方状态管理库
- **Axios** - HTTP 客户端

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置 API 地址
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:8082

### 4. 构建生产版本

```bash
npm run build
```

### 5. 预览生产构建

```bash
npm run preview
```

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口封装
│   │   ├── index.js      # Axios 实例配置
│   │   ├── user.js       # 用户相关 API
│   │   ├── weather.js    # 天气相关 API
│   │   ├── child.js      # 孩子档案 API
│   │   ├── recommendation.js  # 推荐 API
│   │   ├── checkin.js    # 打卡 API
│   │   └── achievement.js # 成就 API
│   ├── stores/           # Pinia 状态管理
│   │   ├── user.js       # 用户状态
│   │   └── child.js      # 孩子档案状态
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── components/       # 可复用组件
│   ├── pages/            # 页面组件
│   │   ├── Login.vue     # 登录页
│   │   ├── Children.vue  # 孩子管理页
│   │   ├── Home.vue      # 首页
│   │   ├── Plan.vue      # 计划页
│   │   ├── CheckIn.vue   # 打卡页
│   │   ├── Achievements.vue # 成就页
│   │   └── Profile.vue   # 个人中心页
│   ├── assets/           # 静态资源
│   │   └── styles/
│   │       └── main.css  # 全局样式
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── public/               # 公共静态文件
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 功能模块

### 1. 用户认证
- 微信 OpenID 登录/注册
- 角色选择（家长/老师）
- JWT Token 认证

### 2. 孩子档案管理
- 创建/编辑/删除孩子档案
- 多孩子支持
- 年龄自动计算

### 3. 天气适配
- 实时天气显示
- 空气质量 (AQI) 展示
- 天气图标自动匹配

### 4. 智能推荐
- 根据天气生成运动计划
- 年龄适配活动推荐
- 室内/户外活动分类

### 5. 打卡系统
- 多种打卡类型（手动/照片/视频）
- 运动时长记录
- 打卡统计

### 6. 成就系统
- 成就徽章展示
- 成就类型预览
- 成就解锁追踪

## API 配置

默认 API 地址：http://localhost:8000

在 `.env` 文件中配置：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 开发指南

### 添加新页面

1. 在 `src/pages/` 创建新的 Vue 组件
2. 在 `src/router/index.js` 添加路由
3. 在 Tab Bar 中添加导航（如需要）

### 添加新 API

1. 在 `src/api/` 创建新的 API 模块
2. 使用 Axios 实例进行请求
3. 在 Store 或组件中调用

### 状态管理

使用 Pinia 管理全局状态：

- `user` store: 用户信息、认证状态
- `child` store: 孩子档案列表、当前选择的孩子

## 构建部署

### Docker 部署

```bash
# 构建
docker build -t childfit-frontend .

# 运行
docker run -p 80:80 childfit-frontend
```

### Nginx 配置

```nginx
server {
    listen 80;
    server_name childfit.example.com;
    
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## License

MIT
