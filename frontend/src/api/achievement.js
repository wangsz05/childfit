import api from './index'

export const achievementApi = {
  // 获取成就类型
  getAchievementTypes() {
    return api.get('/api/achievements/types')
  },

  // 获取孩子成就
  getChildAchievements(childId) {
    return api.get(`/api/achievements/child/${childId}`)
  },

  // 检查并授予成就
  checkAndGrantAchievement(childId) {
    return api.post(`/api/achievements/child/${childId}/check`)
  },
}
