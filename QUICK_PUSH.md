# 🚀 快速推送到 GitHub

## 方式一：手动推送 (推荐，最简单)

### 第 1 步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写:
   - **Repository name**: `childfit`
   - **Description**: `看天安排孩子运动的公益 App - 天气动态适配 + 运动护眼组合 + 公益普惠`
   - **Visibility**: ✅ **Public**
   - ❌ **不要勾选** "Initialize this repository with a README"
3. 点击 **Create repository**

### 第 2 步：复制推送命令

在 GitHub 仓库页面，找到 "**…or push an existing repository from the command line**"，复制命令:

```bash
git remote add origin https://github.com/YOUR_USERNAME/childfit.git
git branch -M main
git push -u origin main
```

### 第 3 步：执行推送

在本地终端执行 (替换 `YOUR_USERNAME` 为你的 GitHub 用户名):

```bash
cd /root/.openclaw/workspace/projects/child-health-system

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/childfit.git

# 推送到 GitHub
git push -u origin main
```

### 第 4 步：验证

访问 `https://github.com/YOUR_USERNAME/childfit` 确认文件已上传。

---

## 方式二：使用脚本推送

```bash
cd /root/.openclaw/workspace/projects/child-health-system

# 编辑脚本，设置你的 GitHub 用户名
nano PUSH_TO_GITHUB.sh

# 运行脚本
bash PUSH_TO_GITHUB.sh
```

---

## 身份验证问题

### 使用 Personal Access Token

推送时如需密码，使用 Token 而非账号密码:

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 填写 Note: `ChildFit Push`
4. 选择权限: ✅ `repo` (全选)
5. 点击 **Generate token**
6. **复制 Token** (只显示一次，保存好!)
7. 推送时:
   - Username: 你的 GitHub 用户名
   - Password: 粘贴 Token

### 或使用 SSH (如已配置)

```bash
# 改用 SSH 方式
git remote set-url origin git@github.com:YOUR_USERNAME/childfit.git
git push -u origin main
```

---

## 推送后操作

### 1. 添加项目标签 (Topics)

在 GitHub 仓库页面，点击齿轮图标⚙️，添加:
```
child-health, fitness, public-welfare, wechat-miniprogram, 公益，儿童健康，天气适配，开源项目
```

### 2. 完善 About 区域

在仓库首页右侧 About 区域:
- 添加项目描述
- 添加网站链接 (如有)
- 添加社交媒体链接

### 3. 启用功能

- ✅ **Issues**: 功能建议、Bug 报告、志愿者报名
- ✅ **Projects**: 任务跟踪、迭代计划
- ✅ **Discussions**: 社区讨论 (可选)

### 4. 添加 Badge 到 README

在 README.md 顶部添加:

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/childfit.svg?style=social)](https://github.com/YOUR_USERNAME/childfit/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/childfit.svg)](https://github.com/YOUR_USERNAME/childfit/issues)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/childfit.svg?style=social)](https://github.com/YOUR_USERNAME/childfit/network)
```

---

## 常见问题

### Q: 推送时提示 "repository not found"
A: 请确认:
1. 已在 GitHub 创建仓库
2. 用户名和仓库名正确
3. 仓库可见性为 Public

### Q: 推送时提示需要密码
A: 使用 Personal Access Token，参考上文"身份验证问题"

### Q: 推送速度慢
A: 检查网络连接，或使用代理

### Q: 仓库名已被占用
A: 尝试 `child-fit`、`childfit-app`、`childfit-cn`、`childfit-github`

---

## 推送完成后的宣传文案

**微博/朋友圈**:

```
🎗️ 新项目上线！ChildFit - 看天安排孩子运动的公益 App

🌤️ 雾霾天不知道让孩子干嘛？用它！
👁️ 运动 + 护眼组合拳
🍲 气候饮食推荐
🎗️ 所有功能永久免费

28 轮迭代，15 份文档，~120KB 完整规划
MIT 开源，欢迎志愿者参与！

GitHub: https://github.com/YOUR_USERNAME/childfit
#公益 #儿童健康 #开源项目 #微信小程序
```

**技术社区 (知乎/掘金/V2EX)**:

```
标题：开源公益项目 ChildFit 上线 - 看天安排孩子运动的微信小程序

正文：
经过 28 轮深度迭代，ChildFit 公益项目完整规划已完成并开源！

核心亮点:
- 天气动态适配 (所有竞品都没有!)
- 运动 + 护眼组合
- 气候饮食推荐
- 特殊儿童关怀
- 永久免费，农村城市同等可用

技术栈：微信小程序 + Node.js + PostgreSQL
文档：15 份，~120KB
协议：MIT 开源

现招募志愿者:
- 前端开发 (微信小程序)
- 后端开发 (Node.js)
- UI 设计师
- 内容运营 (活动库/食谱库)
- 专家顾问 (儿科/营养师/眼科)

GitHub: https://github.com/YOUR_USERNAME/childfit
欢迎 Star、Fork、PR！
```

---

*最后更新：2026-03-26*
