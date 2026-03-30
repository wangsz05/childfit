import api from './index'

export const checkinApi = {
  // 创建打卡
  createCheckin(data) {
    return api.post('/api/checkins/', data)
  },

  // 获取打卡详情
  getCheckinDetail(checkinId) {
    return api.get(`/api/checkins/${checkinId}`)
  },

  // 获取打卡列表
  getCheckinList(childId) {
    return api.get(`/api/checkins/child/${childId}`)
  },

  // 获取打卡统计
  getCheckinStats(childId) {
    return api.get(`/api/checkins/child/${childId}/stats`)
  },
}
