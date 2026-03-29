"""
天气数据服务
"""
import httpx
import logging
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.weather_rules import WeatherCondition

logger = logging.getLogger(__name__)


class WeatherService:
    """天气数据服务类"""
    
    def __init__(self):
        self.api_key = settings.HEFENG_API_KEY
        self.base_url = settings.HEFENG_BASE_URL
    
    async def get_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """
        获取天气数据
        
        Args:
            location: 地点 (城市名或经纬度)
            
        Returns:
            天气数据字典，失败返回 None
        """
        if not self.api_key:
            logger.warning("和风天气 API Key 未配置")
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                # 先获取 location ID
                location_url = f"{self.base_url}/geo/city-lookup"
                location_params = {
                    "location": location,
                    "key": self.api_key,
                }
                
                location_resp = await client.get(location_url, params=location_params)
                location_resp.raise_for_status()
                location_data = location_resp.json()
                
                if location_data.get("code") != "200" or not location_data.get("location"):
                    logger.error(f"地点查询失败：{location}")
                    return None
                
                city_id = location_data["location"][0]["id"]
                
                # 获取实时天气
                weather_url = f"{self.base_url}/weather/now"
                weather_params = {
                    "location": city_id,
                    "key": self.api_key,
                }
                
                weather_resp = await client.get(weather_url, params=weather_params)
                weather_resp.raise_for_status()
                weather_data = weather_resp.json()
                
                if weather_data.get("code") != "200":
                    logger.error(f"天气查询失败：{weather_data}")
                    return None
                
                # 获取天气预报
                forecast_url = f"{self.base_url}/weather/3d"
                forecast_resp = await client.get(forecast_url, params=weather_params)
                forecast_resp.raise_for_status()
                forecast_data = forecast_resp.json()
                
                result = {
                    "location": location,
                    "city_id": city_id,
                    "now": weather_data.get("now", {}),
                    "forecast": forecast_data.get("daily", []),
                }
                
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"天气 API 请求失败：{e}")
            return None
        except Exception as e:
            logger.error(f"天气服务异常：{e}")
            return None
    
    async def get_weather_alert(self, location: str) -> Optional[Dict[str, Any]]:
        """
        获取天气预警
        
        Args:
            location: 地点
            
        Returns:
            预警信息，无预警返回 None
        """
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                # 先获取 location ID
                location_url = f"{self.base_url}/geo/city-lookup"
                location_params = {
                    "location": location,
                    "key": self.api_key,
                }
                
                location_resp = await client.get(location_url, params=location_params)
                location_resp.raise_for_status()
                location_data = location_resp.json()
                
                if not location_data.get("location"):
                    return None
                
                city_id = location_data["location"][0]["id"]
                
                # 获取预警
                alert_url = f"{self.base_url}/warning/now"
                alert_params = {
                    "location": city_id,
                    "key": self.api_key,
                }
                
                alert_resp = await client.get(alert_url, params=alert_params)
                alert_resp.raise_for_status()
                alert_data = alert_resp.json()
                
                if alert_data.get("code") == "200" and alert_data.get("warning"):
                    return {
                        "has_alert": True,
                        "warnings": alert_data.get("warning", []),
                    }
                
                return {"has_alert": False, "warnings": []}
                
        except Exception as e:
            logger.error(f"天气预警查询失败：{e}")
            return None
    
    def parse_weather_condition(self, weather_data: Dict[str, Any]) -> Optional[WeatherCondition]:
        """
        解析天气数据为 WeatherCondition 对象
        
        Args:
            weather_data: 天气数据
            
        Returns:
            WeatherCondition 对象
        """
        now = weather_data.get("now", {})
        
        return WeatherCondition(
            text=now.get("text", ""),
            temp=float(now.get("temp", 20)),
            humidity=int(now.get("humidity", 50)),
            wind_speed=float(now.get("windSpeed", 0)),
            aqi=None,  # 和风天气免费版 AQI 需要单独接口
            uv_index=int(now.get("uvIndex", 0)) if now.get("uvIndex") else None,
        )
