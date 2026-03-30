<template>
  <div class="plan-page">
    <div class="container">
      <h1 class="page-title">📅 运动计划</h1>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <div v-else-if="plans.length === 0" class="empty-state">
        <p class="empty-text">暂无计划</p>
        <p class="empty-hint">在首页生成今日计划</p>
      </div>

      <div v-else class="plans-list">
        <div v-for="plan in plans" :key="plan.id" class="plan-card">
          <div class="plan-date">
            <span class="date-day">{{ formatDate(plan.plan_date) }}</span>
            <span class="date-status" :class="plan.status">
              {{ getStatusText(plan.status) }}
            </span>
          </div>
          <div class="plan-activities">
            <div v-for="(activity, index) in plan.plan_data?.activities || []" :key="index" class="activity-item">
              <span class="activity-bullet">●</span>
              <span class="activity-name">{{ activity.name }}</span>
              <span class="activity-duration">{{ activity.duration_min }}分钟</span>
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
      <router-link to="/plan" class="tab-bar-item active">
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
import { recommendationApi } from '@/api/recommendation'

const childStore = useChildStore()
const loading = ref(false)
const plans = ref([])

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  
  if (dateStr === today.toISOString().split('T')[0]) {
    return '今天'
  } else if (dateStr === yesterday.toISOString().split('T')[0]) {
    return '昨天'
  }
  
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const getStatusText = (status) => {
  const map = {
    generated: '已生成',
    confirmed: '已确认',
    completed: '已完成',
    skipped: '已跳过',
  }
  return map[status] || status
}

onMounted(async () => {
  if (!childStore.currentChild) return
  
  loading.value = true
  try {
    const data = await recommendationApi.getRecommendationList(childStore.currentChild.id)
    plans.value = data
  } catch (error) {
    console.error('Fetch plans error:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.plan-page {
  min-height: 100vh;
  padding: 20px 0 80px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.plans-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.plan-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.plan-date {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e0e0e0;
}

.date-day {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.date-status {
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 20px;
  background: #E8F5E9;
  color: #4CAF50;
}

.date-status.completed {
  background: #E3F2FD;
  color: #2196F3;
}

.date-status.skipped {
  background: #FFEBEE;
  color: #f44336;
}

.plan-activities {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #666;
}

.activity-bullet {
  color: #4CAF50;
  font-size: 12px;
}

.activity-name {
  flex: 1;
}

.activity-duration {
  font-size: 13px;
  color: #999;
}
</style>
