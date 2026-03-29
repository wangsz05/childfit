"""
天气规则引擎
根据天气条件判断适合的活动类型
"""
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass


@dataclass
class WeatherCondition:
    """天气条件"""
    text: str  # 天气描述
    temp: float  # 温度
    humidity: int  # 湿度
    wind_speed: float  # 风速
    aqi: Optional[int] = None  # 空气质量指数
    uv_index: Optional[int] = None  # 紫外线指数


# 天气文本到类型的映射
WEATHER_TYPE_MAP = {
    # 晴天类
    "晴": "sunny",
    "晴间多云": "sunny",
    "多云": "cloudy",
    
    # 雨天类
    "小雨": "rainy",
    "中雨": "rainy",
    "大雨": "rainy",
    "暴雨": "rainy",
    "雷阵雨": "rainy",
    
    # 雪天类
    "小雪": "snowy",
    "中雪": "snowy",
    "大雪": "snowy",
    
    # 恶劣天气
    "雾": "foggy",
    "霾": "hazy",
    "沙尘暴": "sandstorm",
    "台风": "typhoon",
}

# 不适合户外活动的天气
BAD_OUTDOOR_WEATHER = ["hazy", "sandstorm", "typhoon", "foggy", "rainy", "snowy"]

# 适合户外活动的天气
GOOD_OUTDOOR_WEATHER = ["sunny", "cloudy"]


def parse_weather_type(weather_text: str) -> str:
    """
    解析天气文本为类型
    
    Args:
        weather_text: 天气描述文本
        
    Returns:
        天气类型标识
    """
    return WEATHER_TYPE_MAP.get(weather_text, "unknown")


def is_outdoor_suitable(weather: WeatherCondition) -> bool:
    """
    判断是否适合户外活动
    
    Args:
        weather: 天气条件
        
    Returns:
        是否适合
    """
    weather_type = parse_weather_type(weather.text)
    
    # 恶劣天气不适合户外
    if weather_type in BAD_OUTDOOR_WEATHER:
        return False
    
    # AQI 过高不适合户外
    if weather.aqi and weather.aqi > 150:
        return False
    
    # 温度极端不适合户外
    if weather.temp < 5 or weather.temp > 35:
        return False
    
    # 紫外线过强需要注意
    if weather.uv_index and weather.uv_index > 8:
        return False
    
    return True


def get_activity_recommendation(weather: WeatherCondition) -> Dict[str, Any]:
    """
    根据天气获取活动推荐建议
    
    Args:
        weather: 天气条件
        
    Returns:
        推荐建议
    """
    weather_type = parse_weather_type(weather.text)
    is_outdoor = is_outdoor_suitable(weather)
    
    recommendation = {
        "outdoor_suitable": is_outdoor,
        "recommended_type": "outdoor" if is_outdoor else "indoor",
        "reason": "",
        "warnings": [],
        "suggestions": [],
    }
    
    # 根据天气类型给出具体建议
    if weather_type == "sunny":
        recommendation["reason"] = "晴朗天气，非常适合户外活动"
        recommendation["suggestions"] = [
            "注意防晒，涂抹防晒霜",
            "适时补充水分",
            "避免正午时段剧烈运动"
        ]
        if weather.uv_index and weather.uv_index > 5:
            recommendation["warnings"].append(f"紫外线较强 (指数:{weather.uv_index})，注意防护")
    
    elif weather_type == "cloudy":
        recommendation["reason"] = "多云天气，适合户外活动"
        recommendation["suggestions"] = [
            "温度适宜，适合各种户外运动",
            "注意适时增减衣物"
        ]
    
    elif weather_type == "rainy":
        recommendation["reason"] = "雨天，建议室内活动"
        recommendation["warnings"].append("路面湿滑，注意出行安全")
        recommendation["suggestions"] = [
            "选择室内运动如瑜伽、跳绳",
            "可以进行室内游戏或亲子活动"
        ]
    
    elif weather_type == "snowy":
        recommendation["reason"] = "雪天，注意保暖"
        recommendation["warnings"].append("路面结冰，注意防滑")
        recommendation["suggestions"] = [
            "做好保暖措施",
            "可以选择室内活动或雪地游戏"
        ]
    
    elif weather_type == "hazy":
        recommendation["reason"] = "雾霾天气，不适合户外活动"
        recommendation["warnings"].append(f"空气质量较差 (AQI:{weather.aqi})，减少外出")
        recommendation["suggestions"] = [
            "关闭门窗，使用空气净化器",
            "进行室内轻度运动",
            "外出时佩戴口罩"
        ]
    
    elif weather_type == "foggy":
        recommendation["reason"] = "大雾天气，能见度低"
        recommendation["warnings"].append("能见度低，注意交通安全")
        recommendation["suggestions"] = [
            "建议室内活动",
            "如外出注意交通安全"
        ]
    
    elif weather_type in ["sandstorm", "typhoon"]:
        recommendation["reason"] = "极端天气，请勿外出"
        recommendation["warnings"].append("极端天气，待在室内最安全")
        recommendation["suggestions"] = [
            "关闭门窗",
            "避免一切户外活动",
            "关注天气预警信息"
        ]
    
    else:
        recommendation["reason"] = "天气情况不明，建议谨慎选择活动类型"
    
    # 温度相关建议
    if weather.temp < 10:
        recommendation["suggestions"].append("天气较冷，注意保暖")
    elif weather.temp > 30:
        recommendation["suggestions"].append("天气炎热，注意防暑降温")
    
    return recommendation


def filter_activities_by_weather(
    activities: List[Dict[str, Any]],
    weather: WeatherCondition
) -> List[Dict[str, Any]]:
    """
    根据天气过滤活动列表
    
    Args:
        activities: 活动列表
        weather: 天气条件
        
    Returns:
        过滤后的活动列表
    """
    is_outdoor = is_outdoor_suitable(weather)
    
    filtered = []
    for activity in activities:
        activity_type = activity.get("type", "any")
        
        # 如果适合户外，推荐户外和通用活动
        if is_outdoor:
            if activity_type in ["outdoor", "any"]:
                filtered.append(activity)
        # 如果不适合户外，推荐室内和通用活动
        else:
            if activity_type in ["indoor", "any"]:
                filtered.append(activity)
    
    return filtered


def get_weather_score(weather: WeatherCondition) -> int:
    """
    计算天气适宜度评分 (0-100)
    
    Args:
        weather: 天气条件
        
    Returns:
        适宜度评分
    """
    score = 100
    
    weather_type = parse_weather_type(weather.text)
    
    # 天气类型扣分
    if weather_type in ["typhoon", "sandstorm"]:
        score -= 50
    elif weather_type in ["hazy", "foggy"]:
        score -= 30
    elif weather_type == "rainy":
        score -= 20
    elif weather_type == "snowy":
        score -= 15
    
    # AQI 扣分
    if weather.aqi:
        if weather.aqi > 200:
            score -= 40
        elif weather.aqi > 150:
            score -= 25
        elif weather.aqi > 100:
            score -= 10
    
    # 温度扣分
    if weather.temp < 0:
        score -= 30
    elif weather.temp < 5:
        score -= 15
    elif weather.temp > 35:
        score -= 25
    elif weather.temp > 30:
        score -= 10
    
    # 紫外线扣分
    if weather.uv_index:
        if weather.uv_index > 10:
            score -= 20
        elif weather.uv_index > 8:
            score -= 10
    
    return max(0, min(100, score))
