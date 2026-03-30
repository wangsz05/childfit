import api from './index'

export const childApi = {
  // 创建孩子档案
  createChild(data) {
    return api.post('/api/children/', data)
  },

  // 获取孩子列表
  getChildList(userId) {
    return api.get('/api/children/', { params: { user_id: userId } })
  },

  // 获取孩子详情
  getChildDetail(childId) {
    return api.get(`/api/children/${childId}`)
  },

  // 更新孩子档案
  updateChild(childId, data) {
    return api.put(`/api/children/${childId}`, data)
  },

  // 删除孩子档案
  deleteChild(childId) {
    return api.delete(`/api/children/${childId}`)
  },
}
