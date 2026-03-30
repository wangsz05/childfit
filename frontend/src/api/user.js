import api from './index'

export const userApi = {
  // 用户注册
  register(data) {
    return api.post('/api/users/register', data)
  },

  // 用户登录
  login(data) {
    return api.post('/api/users/login', data)
  },

  // 获取用户信息
  getUserInfo(userId) {
    return api.get(`/api/users/${userId}`)
  },

  // 更新用户信息
  updateUserInfo(userId, data) {
    return api.put(`/api/users/${userId}`, data)
  },

  // 获取孩子数量
  getChildrenCount(userId) {
    return api.get(`/api/users/${userId}/children-count`)
  },
}
