<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-header">
        <div class="user-avatar">
          {{ userNickname?.charAt(0) || '👤' }}
        </div>
        <div class="user-info">
          <h2 class="user-name">{{ userNickname || '用户' }}</h2>
          <p class="user-role">{{ userRole === 'student' ? '家长' : '老师' }}</p>
        </div>
      </div>

      <div class="menu-list">
        <div class="menu-item" @click="navigateTo('/children')">
          <span class="menu-icon">👶</span>
          <span class="menu-label">孩子管理</span>
          <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item" @click="navigateTo('/plan')">
          <span class="menu-icon">📅</span>
          <span class="menu-label">运动计划</span>
          <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item" @click="navigateTo('/checkin')">
          <span class="menu-icon">✅</span>
          <span class="menu-label">打卡记录</span>
          <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item" @click="navigateTo('/achievements')">
          <span class="menu-icon">🏆</span>
          <span class="menu-label">成就系统</span>
          <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item">
          <span class="menu-icon">⚙️</span>
          <span class="menu-label">设置</span>
          <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item">
          <span class="menu-icon">❓</span>
          <span class="menu-label">帮助与反馈</span>
          <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item">
          <span class="menu-icon">ℹ️</span>
          <span class="menu-label">关于我们</span>
          <span class="menu-arrow">›</span>
        </div>
      </div>

      <div class="card mt-4">
        <div class="card-body text-center">
          <p class="version-info">ChildFit v1.0.0</p>
          <p class="copyright">🎗️ 公益项目 · 永久免费</p>
        </div>
      </div>

      <button class="btn btn-outline btn-block" @click="handleLogout">
        退出登录
      </button>
    </div>

    <!-- Tab Bar -->
    <div class="tab-bar">
      <router-link to="/home" class="tab-bar-item">
        <span class="icon">🏠</span>
        <span>首页</span>
      </router-link>
      <router-link to="/plan" class="tab-bar-item">
        <span class="icon">📅</span>
        <span>计划</span>
      </router-link>
      <router-link to="/checkin" class="tab-bar-item">
        <span class="icon">✅</span>
        <span>打卡</span>
      </router-link>
      <router-link to="/achievements" class="tab-bar-item">
        <span class="icon">🏆</span>
        <span>成就</span>
      </router-link>
      <router-link to="/profile" class="tab-bar-item active">
        <span class="icon">👤</span>
        <span>我的</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const userNickname = computed(() => userStore.user?.nickname)
const userRole = computed(() => userStore.role)

const navigateTo = (path) => {
  router.push(path)
}

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  padding: 20px 0 80px;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  margin-bottom: 20px;
  color: white;
}

.user-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 600;
  margin-right: 16px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 4px;
}

.user-role {
  font-size: 14px;
  opacity: 0.9;
}

.menu-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: background 0.3s ease;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover {
  background: #f9f9f9;
}

.menu-icon {
  font-size: 24px;
  margin-right: 16px;
  width: 32px;
  text-align: center;
}

.menu-label {
  flex: 1;
  font-size: 16px;
  color: #333;
}

.menu-arrow {
  font-size: 24px;
  color: #ccc;
}

.version-info {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.copyright {
  font-size: 13px;
  color: #999;
}

.btn-outline {
  margin-top: 20px;
}
</style>
