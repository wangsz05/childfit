# 📦 GitHub 推送指南

本文档指导如何将 ChildFit 项目推送到 GitHub。

---

## 方式一：手动创建仓库 (推荐)

### 步骤 1: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库信息:
   - **Repository name**: `childfit` 或 `child-fit`
   - **Description**: "看天安排孩子运动的公益 App - 天气动态适配 + 运动护眼组合 + 公益普惠"
   - **Visibility**: Public (公开，符合公益开源理念)
   - **不要** 勾选 "Initialize this repository with a README" (我们已有本地仓库)

3. 点击 "Create repository"

### 步骤 2: 关联远程仓库并推送

在终端执行以下命令 (替换 `<your-username>` 为你的 GitHub 用户名):

```bash
cd /root/.openclaw/workspace/projects/child-health-system

# 添加远程仓库
git remote add origin https://github.com/<your-username>/childfit.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 3: 设置仓库信息

在 GitHub 仓库页面:
1. 添加主题标签 (Topics): `child-health`, `fitness`, `public-welfare`, `wechat-miniprogram`, `公益`, `儿童健康`
2. 在 About 区域添加网站链接 (如有)
3. 设置 Branch 保护规则 (可选)

---

## 方式二：使用 GitHub CLI

如果已安装 GitHub CLI (`gh`):

```bash
cd /root/.openclaw/workspace/projects/child-health-system

# 创建仓库并推送
gh repo create childfit --public --source=. --remote=origin --push
```

---

## 方式三：使用 Git 凭证

如果使用 HTTPS 推送时需要凭证:

### 使用 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：`repo` (完整仓库权限)
4. 生成后复制 token (只显示一次)
5. 推送时使用 token 作为密码:
   ```bash
   git push -u origin main
   # Username: <your-username>
   # Password: <your-token>
   ```

---

## 推送后检查清单

- [ ] 所有文件已正确显示在 GitHub 上
- [ ] README.md 在仓库首页正确渲染
- [ ] LICENSE 文件存在
- [ ] CONTRIBUTING.md 文件存在
- [ ] 添加了合适的项目标签 (Topics)
- [ ] 设置了仓库描述
- [ ] (可选) 启用了 GitHub Pages 展示项目
- [ ] (可选) 添加了项目网站链接

---

## 后续操作

### 启用 GitHub Issues

用于收集:
- 功能建议
- Bug 报告
- 内容贡献
- 志愿者报名

### 启用 GitHub Projects

用于项目管理:
- 开发任务跟踪
- 迭代计划
- 志愿者任务分配

### 设置 GitHub Actions (可选)

自动化:
- 文档构建
- 链接检查
- 自动发布

### 添加 Badge

在 README.md 中添加:

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/<your-username>/childfit.svg)](https://github.com/<your-username>/childfit/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/<your-username>/childfit.svg)](https://github.com/<your-username>/childfit/issues)
[![GitHub forks](https://img.shields.io/github/forks/<your-username>/childfit.svg)](https://github.com/<your-username>/childfit/network)
```

---

## 项目推广

推送到 GitHub 后:

1. **社交媒体分享**
   - 微博、微信朋友圈
   - 技术社区 (V2EX、知乎、掘金)
   - 公益组织群

2. **志愿者招募**
   - GitHub Issues 发布招募信息
   - 技术社区发帖
   - 高校社团联系

3. **合作伙伴联系**
   - 基金会项目申请
   - 企业 CSR 合作
   - 学校试点合作

---

## 常见问题

### Q: 仓库名已被占用怎么办？
A: 尝试 `child-fit`、`childfit-app`、`childfit-cn` 等变体

### Q: 推送失败怎么办？
A: 检查网络连接，确认 token 权限，或尝试使用 SSH 方式

### Q: 如何保护项目不被滥用？
A: 
- 使用 MIT 协议 (允许商用，但需保留版权说明)
- 内容使用 CC-BY 协议 (需署名)
- 在 README 中明确公益定位

---

*最后更新：2026-03-26*
