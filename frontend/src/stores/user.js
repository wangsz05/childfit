import { defineStore } from 'pinia'
import { userApi } from '@/api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    role: localStorage.getItem('role') || 'student', // student or teacher
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    userId: (state) => state.user?.id || null,
    userRole: (state) => state.role,
  },

  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('access_token', token)
    },

    setUser(user) {
      this.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },

    setRole(role) {
      this.role = role
      localStorage.setItem('role', role)
    },

    async login(loginData) {
      try {
        const response = await userApi.login(loginData)
        this.setToken(response.access_token)
        this.setUser(response.user)
        return response
      } catch (error) {
        throw error
      }
    },

    async register(registerData) {
      try {
        const response = await userApi.register(registerData)
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchUserInfo() {
      if (!this.userId) return
      try {
        const user = await userApi.getUserInfo(this.userId)
        this.setUser(user)
        return user
      } catch (error) {
        throw error
      }
    },

    logout() {
      this.token = ''
      this.user = null
      this.role = 'student'
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      localStorage.removeItem('role')
    },
  },
})
