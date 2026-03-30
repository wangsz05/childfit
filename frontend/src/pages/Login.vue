<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1 class="app-title">🎗️ ChildFit</h1>
        <p class="app-subtitle">看天安排孩子运动的公益 App</p>
      </div>

      <div class="login-form">
        <h2 class="form-title">欢迎使用</h2>
        
        <!-- Role Selection -->
        <div class="role-selection">
          <p class="role-label">选择您的身份</p>
          <div class="role-options">
            <div 
              class="role-option" 
              :class="{ active: selectedRole === 'student' }"
              @click="selectedRole = 'student'"
            >
              <span class="role-icon">👨‍🎓</span>
              <span class="role-name">家长</span>
            </div>
            <div 
              class="role-option" 
              :class="{ active: selectedRole === 'teacher' }"
              @click="selectedRole = 'teacher'"
            >
              <span class="role-icon">👩‍🏫</span>
              <span class="role-name">老师</span>
            </div>
          </div>
        </div>

        <!-- Login Form -->
        <div class="form-group">
          <input 
            v-model="loginForm.wx_openid" 
            type="text" 
            class="input" 
            placeholder="请输入微信 OpenID（测试可用：test123）"
          />
        </div>

        <div class="form-group">
          <input 
            v-model="loginForm.nickname" 
            type="text" 
            class="input" 
            placeholder="请输入昵称"
          />
        </div>

        <button 
          class="btn btn-wechat btn-block mt-4" 
          @click="handleLogin"
          :disabled="loading"
        >
          {{ loading ? '登录中...' : '微信一键登录' }}
        </button>

        <p class="login-tip">
          登录即代表您同意
          <a href="#" class="link">《用户协议》</a>
          和
          <a href="#" class="link">《隐私政策》</a>
        </p>
      </div>

      <div class="login-footer">
        <p class="footer-text">🌤️ 雾霾天不知道让孩子干嘛？用它！</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const selectedRole = ref('student')
const loading = ref(false)
const loginForm = ref({
  wx_openid: '',
  nickname: '',
})

const handleLogin = async () => {
  if (!loginForm.value.wx_openid) {
    alert('请输入微信 OpenID')
    return
  }

  loading.value = true
  
  try {
    // Set role
    userStore.setRole(selectedRole.value)
    
    // Try to login
    await userStore.login({
      wx_openid: loginForm.value.wx_openid,
      nickname: loginForm.value.nickname || '用户',
    })
    
    // Navigate to children page or home
    router.push('/children')
  } catch (error) {
    console.error('Login error:', error)
    // If user doesn't exist, try to register
    try {
      await userStore.register({
        wx_openid: loginForm.value.wx_openid,
        nickname: loginForm.value.nickname || '用户',
        avatar_url: '',
      })
      
      // Then login
      await userStore.login({
        wx_openid: loginForm.value.wx_openid,
      })
      
      router.push('/children')
    } catch (registerError) {
      console.error('Register error:', registerError)
      alert('登录失败，请重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.app-title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.app-subtitle {
  font-size: 14px;
  color: #666;
}

.login-form {
  margin-bottom: 24px;
}

.form-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
  text-align: center;
}

.role-selection {
  margin-bottom: 24px;
}

.role-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
  text-align: center;
}

.role-options {
  display: flex;
  gap: 16px;
}

.role-option {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.role-option:hover {
  border-color: #4CAF50;
  background: #F1F8E9;
}

.role-option.active {
  border-color: #4CAF50;
  background: #E8F5E9;
}

.role-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.role-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-group {
  margin-bottom: 16px;
}

.login-tip {
  font-size: 12px;
  color: #999;
  text-align: center;
  margin-top: 16px;
}

.link {
  color: #4CAF50;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.login-footer {
  text-align: center;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.footer-text {
  font-size: 14px;
  color: #666;
}
</style>
