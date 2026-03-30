<template>
  <div class="checkin-page">
    <div class="container">
      <h1 class="page-title">✅ 运动打卡</h1>

      <div class="card">
        <div class="card-header">
          <h2>选择活动</h2>
        </div>
        <div class="card-body">
          <div v-if="selectedActivity" class="selected-activity">
            <h3 class="activity-name">{{ selectedActivity.name }}</h3>
            <p class="activity-desc">{{ selectedActivity.description }}</p>
            <div class="activity-meta">
              <span>⏱️ {{ selectedActivity.duration_min }}分钟</span>
              <span>💪 {{ selectedActivity.difficulty }}</span>
            </div>
          </div>
          <div v-else class="empty-state">
            <p>请在首页选择要打卡的活动</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h2>打卡信息</h2>
        </div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">打卡类型</label>
            <select v-model="checkinForm.check_in_type" class="input">
              <option value="manual">手动打卡</option>
              <option value="photo">照片打卡</option>
              <option value="video">视频打卡</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">实际时长（分钟）</label>
            <input v-model.number="checkinForm.duration_min" type="number" class="input" placeholder="例如：15" />
          </div>

          <div class="form-group">
            <label class="form-label">感受</label>
            <select v-model="checkinForm.feeling" class="input">
              <option value="great">很棒 😄</option>
              <option value="good">不错 🙂</option>
              <option value="okay">一般 😐</option>
              <option value="tired">有点累 😫</option>
            </select>
          </div>
        </div>
      </div>

      <button class="btn btn-primary btn-block" @click="submitCheckin" :disabled="!canSubmit || submitting">
        {{ submitting ? '提交中...' : '完成打卡' }}
      </button>

      <div class="stats-card" v-if="stats">
        <h3>📊 本周统计</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-value">{{ stats.total_checkins || 0 }}</span>
            <span class="stat-label">打卡次数</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.total_minutes || 0 }}</span>
            <span class="stat-label">运动分钟</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.outdoor_count || 0 }}</span>
            <span class="stat-label">户外活动</span>
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
      <router-link to="/checkin" class="tab-bar-item active">
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
import { checkinApi } from '@/api/checkin'

const childStore = useChildStore()

const submitting = ref(false)
const selectedActivity = ref(null)
const stats = ref(null)
const checkinForm = ref({
  check_in_type: 'manual',
  duration_min: 15,
  feeling: 'good',
})

const canSubmit = computed(() => {
  return selectedActivity.value && checkinForm.value.duration_min > 0
})

const submitCheckin = async () => {
  if (!canSubmit.value) return
  
  submitting.value = true
  
  try {
    await checkinApi.createCheckin({
      child_id: childStore.currentChild.id,
      activity_id: selectedActivity.value.id,
      check_in_type: checkinForm.value.check_in_type,
      duration_min: checkinForm.value.duration_min,
    })
    
    alert('打卡成功！🎉')
    // Reset form
    selectedActivity.value = null
    localStorage.removeItem('selectedActivity')
    checkinForm.value = {
      check_in_type: 'manual',
      duration_min: 15,
      feeling: 'good',
    }
    // Refresh stats
    fetchStats()
  } catch (error) {
    console.error('Checkin error:', error)
    alert('打卡失败，请重试')
  } finally {
    submitting.value = false
  }
}

const fetchStats = async () => {
  if (!childStore.currentChild) return
  
  try {
    const data = await checkinApi.getCheckinStats(childStore.currentChild.id)
    stats.value = data
  } catch (error) {
    console.error('Fetch stats error:', error)
  }
}

onMounted(() => {
  // Load selected activity from localStorage
  const activityStr = localStorage.getItem('selectedActivity')
  if (activityStr) {
    try {
      selectedActivity.value = JSON.parse(activityStr)
    } catch (e) {
      console.error('Parse activity error:', e)
    }
  }
  
  fetchStats()
})
</script>

<style scoped>
.checkin-page {
  min-height: 100vh;
  padding: 20px 0 80px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.selected-activity {
  padding: 16px;
  background: #F1F8E9;
  border-radius: 12px;
  margin-bottom: 16px;
}

.activity-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
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

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.stats-card {
  margin-top: 24px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.stats-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #4CAF50;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #999;
}
</style>
