<template>
  <div class="achievements-page">
    <div class="container">
      <h1 class="page-title">🏆 成就系统</h1>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <div v-else-if="achievements.length === 0" class="empty-state">
        <p class="empty-text">暂无成就</p>
        <p class="empty-hint">完成更多打卡来解锁成就</p>
      </div>

      <div v-else class="achievements-grid">
        <div v-for="achievement in achievements" :key="achievement.id" class="achievement-badge">
          <div class="achievement-icon">{{ getAchievementIcon(achievement.achievement_type) }}</div>
          <div class="achievement-name">{{ achievement.achievement_name }}</div>
          <div class="achievement-date">{{ formatDate(achievement.achieved_at) }}</div>
        </div>
      </div>

      <!-- Achievement Types Preview -->
      <div class="card mt-4">
        <div class="card-header">
          <h2>🎯 可解锁成就</h2>
        </div>
        <div class="card-body">
          <div class="achievement-types">
            <div class="type-item">
              <span class="type-icon">🎉</span>
              <div class="type-info">
                <div class="type-name">第一次打卡</div>
                <div class="type-desc">完成首次运动打卡</div>
              </div>
            </div>
            <div class="type-item">
              <span class="type-icon">💪</span>
              <div class="type-info">
                <div class="type-name">周坚持者</div>
                <div class="type-desc">连续打卡 7 天</div>
              </div>
            </div>
            <div class="type-item">
              <span class="type-icon">🏆</span>
              <div class="type-info">
                <div class="type-name">月达人</div>
                <div class="type-desc">单月打卡 20 次</div>
              </div>
            </div>
            <div class="type-item">
              <span class="type-icon">🌞</span>
              <div class="type-info">
                <div class="type-name">户外爱好者</div>
                <div class="type-desc">完成 10 次户外活动</div>
              </div>
            </div>
            <div class="type-item">
              <span class="type-icon">🌅</span>
              <div class="type-info">
                <div class="type-name">早起鸟儿</div>
                <div class="type-desc">连续 5 天 9 点前打卡</div>
              </div>
            </div>
          </div>
        </div>
      </div>
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
      <router-link to="/achievements" class="tab-bar-item active">
        <span class="icon">🏆</span>
        <span>成就</span>
      </router-link>
      <router-link to="/profile" class="tab-bar-item">
        <span class="icon">👤</span>
        <span>我的</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useChildStore } from '@/stores/child'
import { achievementApi } from '@/api/achievement'

const childStore = useChildStore()
const loading = ref(false)
const achievements = ref([])

const getAchievementIcon = (type) => {
  const icons = {
    first_checkin: '🎉',
    weekly_streak: '💪',
    monthly_master: '🏆',
    outdoor_lover: '🌞',
    early_bird: '🌅',
  }
  return icons[type] || '⭐'
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

onMounted(async () => {
  if (!childStore.currentChild) return
  
  loading.value = true
  try {
    const data = await achievementApi.getChildAchievements(childStore.currentChild.id)
    achievements.value = data
  } catch (error) {
    console.error('Fetch achievements error:', error)
    // Mock data for demo
    achievements.value = [
      { id: '1', achievement_type: 'first_checkin', achievement_name: '第一次打卡', achieved_at: new Date().toISOString() },
    ]
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.achievements-page {
  min-height: 100vh;
  padding: 20px 0 80px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
}

.achievement-badge {
  background: white;
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.achievement-badge:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.achievement-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.achievement-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.achievement-date {
  font-size: 12px;
  color: #999;
}

.achievement-types {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.type-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 12px;
  background: #F5F5F5;
  border-radius: 8px;
}

.type-icon {
  font-size: 32px;
}

.type-info {
  flex: 1;
}

.type-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.type-desc {
  font-size: 13px;
  color: #666;
}
</style>
