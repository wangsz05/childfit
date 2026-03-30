<template>
  <div class="home-page">
    <div class="container">
      <!-- Weather Card -->
      <div class="weather-card">
        <div class="weather-main">
          <div class="weather-icon">{{ weatherIcon }}</div>
          <div class="weather-temp">{{ weather.temp || '--' }}°</div>
        </div>
        <div class="weather-info">
          <div class="weather-condition">{{ weather.condition || '获取中...' }}</div>
          <div class="weather-location">📍 {{ currentChild?.city || '未设置城市' }}</div>
          <div class="weather-aqi" v-if="weather.aqi">
            AQI: {{ weather.aqi }} {{ getAqiLevel(weather.aqi) }}
          </div>
        </div>
      </div>

      <!-- Today's Plan -->
      <div class="card">
        <div class="card-header">
          <h2>📅 今日计划</h2>
          <button class="btn btn-primary btn-sm" @click="generatePlan" :disabled="generating">
            {{ generating ? '生成中...' : '生成计划' }}
          </button>
        </div>
        <div class="card-body">
          <div v-if="loading" class="loading">
            <div class="spinner"></div>
          </div>
          <div v-else-if="!plan" class="empty-state">
            <p>点击上方按钮生成今日运动计划</p>
          </div>
          <div v-else class="plan-content">
            <div class="plan-summary">
              <div class="plan-item">
                <span class="plan-icon">🏃</span>
                <span>推荐活动：{{ plan.activities?.length || 0 }} 个</span>
              </div>
              <div class="plan-item">
                <span class="plan-icon">☀️</span>
                <span>户外时间：{{ plan.outdoor_time || 0 }} 分钟</span>
              </div>
            </div>
            
            <div class="activity-list">
              <div 
                v-for="(activity, index) in plan.activities" 
                :key="index"
                class="activity-card"
                @click="selectActivity(activity)"
              >
                <div class="activity-header">
                  <h3 class="activity-name">{{ activity.name }}</h3>
                  <span class="activity-tag" :class="activity.type">
                    {{ activity.type === 'outdoor' ? '户外' : '室内' }}
                  </span>
                </div>
                <p class="activity-desc">{{ activity.description }}</p>
                <div class="activity-meta">
                  <span>⏱️ {{ activity.duration_min }}分钟</span>
                  <span>💪 {{ getDifficultyText(activity.difficulty) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Eye Care Reminder -->
      <div class="card eye-care-card">
        <div class="card-header">
          <h2>👁️ 护眼提醒</h2>
        </div>
        <div class="card-body">
          <div class="eye-care-tips">
            <div class="tip-item">
              <span class="tip-icon">🌳</span>
              <span>每日户外活动 2 小时，预防近视</span>
            </div>
            <div class="tip-item">
              <span class="tip-icon">👀</span>
              <span>眼保健操每天 2 次，每次 5 分钟</span>
            </div>
            <div class="tip-item">
              <span class="tip-icon">📱</span>
              <span>屏幕时间不超过 60 分钟/天</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Bar -->
    <div class="tab-bar">
      <router-link to="/home" class="tab-bar-item active">
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
      <router-link to="/profile" class="tab-bar-item">
        <span class="icon">👤</span>
        <span>我的</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useChildStore } from '@/stores/child'
import { weatherApi } from '@/api/weather'
import { recommendationApi } from '@/api/recommendation'

const childStore = useChildStore()

const loading = ref(false)
const generating = ref(false)
const weather = ref({})
const plan = ref(null)

const currentChild = computed(() => childStore.currentChild)

const weatherIcon = computed(() => {
  const condition = weather.value.condition || ''
  if (condition.includes('晴')) return '☀️'
  if (condition.includes('云')) return '☁️'
  if (condition.includes('雨')) return '🌧️'
  if (condition.includes('雪')) return '❄️'
  if (condition.includes('雾') || condition.includes('霾')) return '🌫️'
  return '🌤️'
})

const getAqiLevel = (aqi) => {
  if (aqi <= 50) return '(优)'
  if (aqi <= 100) return '(良)'
  if (aqi <= 150) return '(轻度污染)'
  if (aqi <= 200) return '(中度污染)'
  return '(重度污染)'
}

const getDifficultyText = (difficulty) => {
  const map = {
    easy: '简单',
    medium: '中等',
    hard: '困难',
  }
  return map[difficulty] || '未知'
}

const fetchWeather = async () => {
  if (!currentChild.value?.city) return
  
  try {
    const data = await weatherApi.getCurrentWeather(currentChild.value.city)
    weather.value = data
  } catch (error) {
    console.error('Fetch weather error:', error)
    // Use mock data for demo
    weather.value = {
      temp: 25,
      condition: '晴',
      aqi: 45,
    }
  }
}

const generatePlan = async () => {
  if (!currentChild.value) {
    alert('请先选择孩子')
    return
  }

  generating.value = true
  
  try {
    const data = await recommendationApi.generateRecommendation({
      child_id: currentChild.value.id,
    })
    plan.value = data
  } catch (error) {
    console.error('Generate plan error:', error)
    // Use mock data for demo
    plan.value = {
      date: new Date().toISOString().split('T')[0],
      weather: weather.value,
      activities: [
        { name: '跳绳', description: '增强心肺功能', type: 'outdoor', duration_min: 15, difficulty: 'easy' },
        { name: '仰卧起坐', description: '锻炼核心力量', type: 'indoor', duration_min: 10, difficulty: 'medium' },
        { name: '户外跑步', description: '有氧运动', type: 'outdoor', duration_min: 30, difficulty: 'medium' },
      ],
      outdoor_time: 120,
    }
  } finally {
    generating.value = false
  }
}

const selectActivity = (activity) => {
  // Navigate to checkin page with activity
  localStorage.setItem('selectedActivity', JSON.stringify(activity))
  window.location.href = '/checkin'
}

onMounted(async () => {
  loading.value = true
  await fetchWeather()
  loading.value = false
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  padding: 20px 0 80px;
}

.weather-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.weather-main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.weather-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.weather-temp {
  font-size: 48px;
  font-weight: 300;
}

.weather-info {
  text-align: right;
}

.weather-condition {
  font-size: 18px;
  margin-bottom: 4px;
}

.weather-location {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.weather-aqi {
  font-size: 13px;
  opacity: 0.8;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

.plan-summary {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 16px;
  background: #F1F8E9;
  border-radius: 12px;
}

.plan-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
}

.plan-icon {
  font-size: 20px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.activity-card:hover {
  border-color: #4CAF50;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.activity-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.activity-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.activity-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #999;
}

.eye-care-card {
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
}

.eye-care-tips {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #333;
}

.tip-icon {
  font-size: 20px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}
</style>
