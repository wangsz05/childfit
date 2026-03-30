import api from './index'

export const recommendationApi = {
  // 生成每日推荐
  generateRecommendation(data) {
    return api.post('/api/recommendations/generate', data)
  },

  // 获取推荐列表
  getRecommendationList(childId) {
    return api.get('/api/recommendations/list', { params: { child_id: childId } })
  },

  // 获取计划详情
  getPlanDetail(planId) {
    return api.get(`/api/recommendations/${planId}`)
  },

  // 更新计划状态
  updatePlanStatus(planId, data) {
    return api.put(`/api/recommendations/${planId}/status`, data)
  },
}
