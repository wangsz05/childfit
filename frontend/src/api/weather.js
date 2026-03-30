import api from './index'

export const weatherApi = {
  // 获取实时天气
  getCurrentWeather(location) {
    return api.get('/api/weather', { params: { location } })
  },

  // 获取天气预警
  getWeatherAlert(location) {
    return api.get('/api/weather/alert', { params: { location } })
  },

  // 获取天气推荐
  getWeatherRecommendation(location) {
    return api.get('/api/weather/recommendation', { params: { location } })
  },
}
