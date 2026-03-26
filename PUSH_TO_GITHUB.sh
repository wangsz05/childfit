#!/bin/bash

# ChildFit 项目 GitHub 推送脚本
# 使用方法：
# 1. 先在 GitHub 创建仓库 (https://github.com/new)
# 2. 替换下面的 GITHUB_USERNAME 和 REPO_NAME
# 3. 运行此脚本：bash PUSH_TO_GITHUB.sh

# ============ 配置区域 ============
# 替换为你的 GitHub 用户名
GITHUB_USERNAME="your-username"

# 仓库名称
REPO_NAME="childfit"

# GitHub Token (可选，如需自动创建仓库则填写)
# 获取方式：https://github.com/settings/tokens
GITHUB_TOKEN=""
# ==================================

echo "🎗️ ChildFit - GitHub 推送脚本"
echo "=============================="
echo ""

# 检查是否配置了用户名
if [ "$GITHUB_USERNAME" = "your-username" ]; then
    echo "❌ 错误：请先编辑此脚本，设置你的 GitHub 用户名"
    echo ""
    echo "手动推送步骤："
    echo "1. 访问 https://github.com/new 创建仓库"
    echo "2. 仓库名：childfit"
    echo "3. 执行以下命令："
    echo ""
    echo "   cd /root/.openclaw/workspace/projects/child-health-system"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/childfit.git"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

# 设置 Git 用户信息
git config user.name "ChildFit Contributors"
git config user.email "childfit@contributors.org"

echo "✅ Git 用户信息已设置"

# 检查是否已有远程仓库
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ -n "$REMOTE_URL" ]; then
    echo "ℹ️  已存在远程仓库：$REMOTE_URL"
    read -p "是否覆盖？(y/n): " OVERWRITE
    if [ "$OVERWRITE" != "y" ]; then
        echo "❌ 已取消"
        exit 1
    fi
    git remote remove origin
fi

# 添加远程仓库
REMOTE_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
echo ""
echo "📦 添加远程仓库：$REMOTE_URL"
git remote add origin "$REMOTE_URL"

# 尝试推送
echo ""
echo "🚀 推送到 GitHub..."
echo "⚠️  如需身份验证，请使用 GitHub Personal Access Token"
echo "   获取：https://github.com/settings/tokens"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "📍 仓库地址：https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
    echo ""
    echo "下一步："
    echo "1. 访问仓库页面"
    echo "2. 添加 Topics: child-health, fitness, public-welfare, wechat-miniprogram, 公益，儿童健康"
    echo "3. 在 About 区域添加项目描述"
    echo "4. 启用 Issues 和 Projects"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能原因："
    echo "1. 仓库不存在 - 请先在 GitHub 创建仓库"
    echo "2. 需要身份验证 - 请使用 Personal Access Token"
    echo "3. 网络问题 - 请检查网络连接"
    echo ""
    echo "手动推送命令："
    echo "  git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
    echo "  git push -u origin main"
    echo ""
fi
