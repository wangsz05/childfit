<template>
  <div class="children-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">👶 孩子档案</h1>
        <button class="btn btn-primary" @click="showAddModal = true">
          + 添加孩子
        </button>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <div v-else-if="children.length === 0" class="empty-state">
        <p class="empty-text">暂无孩子档案</p>
        <p class="empty-hint">点击上方按钮添加第一个孩子</p>
      </div>

      <div v-else class="children-list">
        <div 
          v-for="child in children" 
          :key="child.id"
          class="child-card"
          :class="{ active: currentChild?.id === child.id }"
          @click="selectChild(child)"
        >
          <div class="child-avatar">
            {{ child.name?.charAt(0) || '👶' }}
          </div>
          <div class="child-info">
            <h3 class="child-name">{{ child.name }}</h3>
            <p class="child-age">{{ getAgeText(child.birth_date) }} · {{ child.gender === 'male' ? '男孩' : '女孩' }}</p>
            <p class="child-city">📍 {{ child.city || '未设置城市' }}</p>
          </div>
          <div class="child-action">
            <span class="arrow">›</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Child Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>添加孩子档案</h2>
          <button class="modal-close" @click="showAddModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">孩子姓名</label>
            <input v-model="newChild.name" type="text" class="input" placeholder="请输入姓名" />
          </div>
          <div class="form-group">
            <label class="form-label">出生日期</label>
            <input v-model="newChild.birth_date" type="date" class="input" />
          </div>
          <div class="form-group">
            <label class="form-label">性别</label>
            <select v-model="newChild.gender" class="input">
              <option value="male">男孩</option>
              <option value="female">女孩</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">所在城市</label>
            <input v-model="newChild.city" type="text" class="input" placeholder="例如：北京" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showAddModal = false">取消</button>
          <button class="btn btn-primary" @click="handleAddChild" :disabled="saving">
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useChildStore } from '@/stores/child'

const router = useRouter()
const userStore = useUserStore()
const childStore = useChildStore()

const loading = ref(false)
const saving = ref(false)
const showAddModal = ref(false)
const newChild = ref({
  name: '',
  birth_date: '',
  gender: 'male',
  city: '',
})

const children = computed(() => childStore.children)
const currentChild = computed(() => childStore.currentChild)

const getAgeText = (birthDate) => {
  if (!birthDate) return '未知年龄'
  const today = new Date()
  const birth = new Date(birthDate)
  const age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  
  if (age === 0) {
    const months = today.getMonth() - birth.getMonth()
    return `${months}个月`
  }
  return `${age}岁`
}

const selectChild = (child) => {
  childStore.setCurrentChild(child)
  router.push('/home')
}

const handleAddChild = async () => {
  if (!newChild.value.name || !newChild.value.birth_date) {
    alert('请填写姓名和出生日期')
    return
  }

  saving.value = true
  
  try {
    await childStore.addChild({
      ...newChild.value,
      user_id: userStore.userId,
    })
    
    showAddModal.value = false
    newChild.value = {
      name: '',
      birth_date: '',
      gender: 'male',
      city: '',
    }
    
    router.push('/home')
  } catch (error) {
    console.error('Add child error:', error)
    alert('添加失败，请重试')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    await childStore.fetchChildren(userStore.userId)
  } catch (error) {
    console.error('Fetch children error:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.children-page {
  min-height: 100vh;
  padding: 20px 0 80px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.children-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.child-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
}

.child-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.child-card.active {
  border: 2px solid #4CAF50;
}

.child-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  margin-right: 16px;
  flex-shrink: 0;
}

.child-info {
  flex: 1;
  min-width: 0;
}

.child-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.child-age {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.child-city {
  font-size: 13px;
  color: #999;
}

.child-action {
  color: #ccc;
  font-size: 24px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-text {
  font-size: 18px;
  color: #666;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  color: #999;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.modal-close {
  background: none;
  border: none;
  font-size: 28px;
  color: #999;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.modal-body {
  padding: 20px;
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

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}

.modal-footer .btn {
  flex: 1;
}
</style>
