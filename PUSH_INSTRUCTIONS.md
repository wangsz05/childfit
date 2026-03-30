# 推送代码到远程仓库

## 当前状态

本地代码已完成重构，包含 2 个新提交：

```
6fc6e3a docs: 添加前端重构报告
a81ddbd feat: 重构前端为 Vue 3 + Vite 实现
```

## 推送方法

### 方法 1: 使用 HTTPS (推荐)

```bash
cd /root/.openclaw/workspace/childfit-repo

# 配置 Git 用户信息 (首次使用)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 推送到远程仓库
git push origin main
```

系统会提示输入 GitHub 用户名和密码 (或个人访问 token)。

### 方法 2: 使用 SSH

如果已配置 SSH key:

```bash
# 更改远程仓库为 SSH 地址
git remote set-url origin git@github.com:wangsz05/childfit.git

# 推送
git push origin main
```

### 方法 3: 使用 Personal Access Token

1. 在 GitHub 生成 Personal Access Token:
   - 访问 https://github.com/settings/tokens
   - 生成新 token (勾选 repo 权限)
   - 复制 token

2. 推送时使用 token 作为密码:
```bash
git push origin main
# Username: your-github-username
# Password: <paste-your-token>
```

### 方法 4: 使用 Git Credential Helper

```bash
# 配置凭据缓存 (1 小时)
git config --global credential.helper cache

# 或配置凭据存储 (永久)
git config --global credential.helper store

# 推送
git push origin main
```

## 验证推送

推送成功后，访问 https://github.com/wangsz05/childfit 查看最新提交。

## 前端部署

### 开发环境
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:8082
```

### 生产环境
```bash
cd frontend
npm install
npm run build
# 部署 dist/ 目录到服务器
```

## 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 完整测试流程

1. 启动后端 (端口 8000)
2. 启动前端 (端口 8082)
3. 访问 http://localhost:8082
4. 测试登录功能
5. 测试孩子档案管理
6. 测试天气展示
7. 测试计划生成
8. 测试打卡功能
9. 测试成就系统

---

**注意**: 推送需要 GitHub 仓库的写权限。如果没有权限，请联系仓库管理员。
