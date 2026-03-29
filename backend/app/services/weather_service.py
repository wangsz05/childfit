"""
天气数据服务 - WeatherCN API
"""
import httpx
import logging
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.weather_rules import WeatherCondition
import random

logger = logging.getLogger(__name__)

# API Key (固定值)
WEATHER_API_KEY = "0LaQKA2AUmvSUuLO3B1Kj5dJiJiINPPS"
WEATHER_BASE_URL = "https://openapi.weathercn.com"

# 城市 Key 缓存 (模拟数据)
CITY_KEY_MAP = {
    "南京": "105570",
    "北京": "101010100",
    "上海": "101020100",
    "广州": "101280101",
    "深圳": "101280601",
    "杭州": "101210101",
    "成都": "101270101",
    "武汉": "101200101",
    "西安": "101110101",
    "苏州": "101190401",
}


class WeatherService:
    """天气数据服务类 - WeatherCN"""

    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_BASE_URL
        self.default_city = settings.WEATHER_DEFAULT_CITY or "南京"

    async def get_city_key(self, city_name: str) -> Optional[str]:
        """
        Step 1: 获取城市 Key

        GET https://openapi.weathercn.com/locations/v1/cities/search.json
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/locations/v1/cities/search.json"
                params = {
                    "apikey": self.api_key,
                    "q": city_name,
                    "language": "zh-cn",
                }

                resp = await client.get(url, params=params, timeout=10.0)
                resp.raise_for_status()
                data = resp.json()

                if data and len(data) > 0:
                    # 返回第一个匹配城市的 Key
                    return data[0].get("Key")

                logger.warning(f"未找到城市: {city_name}")
                # 使用模拟数据
                return CITY_KEY_MAP.get(city_name, "105570")

        except Exception as e:
            logger.warning(f"城市 Key 查询失败，使用模拟数据: {e}")
            # API 失败时使用模拟数据
            return CITY_KEY_MAP.get(city_name, "105570")

    async def get_current_conditions(self, city_key: str) -> Optional[Dict[str, Any]]:
        """
        Step 2: 获取当前天气情况

        GET https://openapi.weathercn.com/currentconditions/v1/{key}.json
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/currentconditions/v1/{city_key}.json"
                params = {
                    "apikey": self.api_key,
                    "language": "zh-cn",
                    "details": "false",
                }

                resp = await client.get(url, params=params, timeout=10.0)
                resp.raise_for_status()
                data = resp.json()

                return data

        except Exception as e:
            logger.warning(f"天气情况查询失败，使用模拟数据: {e}")
            # 返回模拟天气数据
            return [self._generate_mock_weather()]

    def _generate_mock_weather(self) -> Dict[str, Any]:
        """生成模拟天气数据"""
        weather_types = [
            {"text": "晴", "icon": 1},
            {"text": "多云", "icon": 3},
            {"text": "阴", "icon": 6},
            {"text": "小雨", "icon": 12},
        ]
        weather = random.choice(weather_types)
        temp = random.randint(15, 28)

        return {
            "WeatherText": weather["text"],
            "WeatherIcon": weather["icon"],
            "Temperature": {"Value": temp, "Unit": "C"},
            "RealFeelTemperature": {"Value": temp + random.randint(-2, 2), "Unit": "C"},
            "RelativeHumidity": random.randint(40, 70),
            "Wind": {
                "Direction": {"Localized": random.choice(["东北", "东南", "西", "北"])},
                "Speed": {"Value": random.randint(5, 15), "Unit": "km/h"},
            },
            "Pressure": {"Value": random.randint(1000, 1020)},
            "Visibility": {"Value": random.randint(5, 15)},
        }

    async def get_indices(self, city_key: str) -> Optional[Dict[str, Any]]:
        """
        Step 3: 获取天气指数

        GET https://openapi.weathercn.com/indices/v1/daily/1day/{key}/100
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/indices/v1/daily/1day/{city_key}/100"
                params = {
                    "apikey": self.api_key,
                    "language": "zh-cn",
                    "details": "false",
                }

                resp = await client.get(url, params=params, timeout=10.0)
                resp.raise_for_status()
                data = resp.json()

                # 确保返回格式统一：如果是列表，包装成 {"Indices": [...]}
                if isinstance(data, list):
                    return {"Indices": data}
                return data

        except Exception as e:
            logger.warning(f"天气指数查询失败，使用模拟数据: {e}")
            # 返回模拟指数数据
            return self._generate_mock_indices()

    def _generate_mock_indices(self) -> Dict[str, Any]:
        """生成模拟天气指数数据"""
        indices = [
            {"ID": 1, "Name": "晨练指数", "Value": 3, "Category": "较适宜", "Text": "天气较适宜晨练"},
            {"ID": 2, "Name": "运动指数", "Value": 2, "Category": "适宜", "Text": "天气适宜户外运动"},
            {"ID": 3, "Name": "紫外线指数", "Value": 3, "Category": "中等", "Text": "建议涂抹防晒霜"},
            {"ID": 4, "Name": "穿衣指数", "Value": 4, "Category": "舒适", "Text": "建议穿着轻薄衣物"},
            {"ID": 5, "Name": "感冒指数", "Value": 1, "Category": "低", "Text": "感冒风险较低"},
        ]
        return {"Indices": indices}

    async def get_air_quality(self, city_key: str) -> Optional[Dict[str, Any]]:
        """
        Step 4: 获取空气质量

        GET https://openapi.weathercn.com/airquality/v1/current/{key}.json
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/airquality/v1/current/{city_key}.json"
                params = {
                    "apikey": self.api_key,
                    "language": "zh-cn",
                }

                resp = await client.get(url, params=params, timeout=10.0)
                resp.raise_for_status()
                data = resp.json()

                return data

        except Exception as e:
            logger.warning(f"空气质量查询失败，使用模拟数据: {e}")
            # 返回模拟空气质量数据
            return self._generate_mock_air_quality()

    def _generate_mock_air_quality(self) -> Dict[str, Any]:
        """生成模拟空气质量数据"""
        aqi = random.randint(30, 80)
        return {
            "Index": aqi,
            "ParticulateMatter2_5": random.randint(20, 60),
            "ParticulateMatter10": random.randint(40, 100),
            "CarbonMonoxide": random.uniform(0.5, 2.0),
            "NitrogenDioxide": random.randint(20, 50),
            "Ozone": random.randint(50, 100),
            "SulfurDioxide": random.randint(5, 20),
        }

    async def get_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """
        获取完整天气数据

        Args:
            location: 城市名 (如果为空则使用默认城市南京)

        Returns:
            天气数据字典
        """
        # 使用传入城市或默认城市
        city_name = location or self.default_city

        try:
            # Step 1: 获取城市 Key
            city_key = await self.get_city_key(city_name)
            if not city_key:
                # 如果找不到城市，尝试使用默认城市
                if city_name != self.default_city:
                    logger.info(f"尝试使用默认城市: {self.default_city}")
                    city_key = await self.get_city_key(self.default_city)
                    city_name = self.default_city

                if not city_key:
                    logger.error("无法获取城市 Key")
                    return None

            # Step 2: 获取天气情况
            conditions = await self.get_current_conditions(city_key)

            # Step 3: 获取天气指数
            indices = await self.get_indices(city_key)

            # Step 4: 获取空气质量
            air_quality = await self.get_air_quality(city_key)

            # 合并数据
            result = {
                "location": city_name,
                "city_key": city_key,
                "now": conditions[0] if conditions and len(conditions) > 0 else {},
                "indices": indices if indices else {},
                "air_quality": air_quality if air_quality else {},
            }

            return result

        except Exception as e:
            logger.error(f"天气服务异常: {e}")
            return None

    async def get_weather_alert(self, location: str) -> Optional[Dict[str, Any]]:
        """
        获取天气预警 (从指数数据中提取)

        Args:
            location: 城市名

        Returns:
            预警信息
        """
        city_name = location or self.default_city

        try:
            city_key = await self.get_city_key(city_name)
            if not city_key:
                return None

            # 从指数中获取预警相关信息
            indices = await self.get_indices(city_key)

            if indices:
                # 检查是否有极端天气指数
                alerts = []
                for index in indices.get("Indices", []):
                    if index.get("Category") == "高风险" or index.get("Value") in ["不宜", "极不宜"]:
                        alerts.append({
                            "type": index.get("Name", ""),
                            "level": index.get("Category", ""),
                            "text": index.get("Text", ""),
                        })

                return {
                    "has_alert": len(alerts) > 0,
                    "warnings": alerts,
                }

            return {"has_alert": False, "warnings": []}

        except Exception as e:
            logger.error(f"天气预警查询失败: {e}")
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
        air_quality = weather_data.get("air_quality", {})

        # 从 WeatherCN API 解析数据
        try:
            # WeatherIcon 对应天气类型
            weather_text = now.get("WeatherText", "晴")
            temperature = float(now.get("Temperature", {}).get("Value", 20))

            # 相对湿度
            humidity = int(now.get("RelativeHumidity", 50))

            # 风速
            wind_speed = float(now.get("Wind", {}).get("Speed", {}).get("Value", 0))

            # AQI 从空气质量数据获取
            aqi = None
            if air_quality:
                aqi = int(air_quality.get("AQI", 0))

            # UV 指数从指数数据获取
            uv_index = None
            indices = weather_data.get("indices", {})
            if indices:
                for idx in indices.get("Indices", []):
                    if idx.get("Name") == "紫外线指数":
                        uv_index = int(idx.get("Value", "0").replace("级", "").strip() or 0)
                        break

            return WeatherCondition(
                text=weather_text,
                temp=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
                aqi=aqi,
                uv_index=uv_index,
            )

        except Exception as e:
            logger.error(f"天气数据解析失败: {e}")
            # 返回默认值
            return WeatherCondition(
                text="晴",
                temp=20.0,
                humidity=50,
                wind_speed=0.0,
                aqi=None,
                uv_index=None,
            )