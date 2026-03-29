"""
天气查询 API - WeatherCN
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.weather_service import WeatherService
from app.utils.weather_rules import (
    get_activity_recommendation,
    is_outdoor_suitable,
    get_weather_score,
)

router = APIRouter(prefix="", tags=["天气查询"])


@router.get("/")
async def get_weather(
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    获取实时天气 (含指数和空气质量)

    - location: 城市名 (可选，默认南京)
    """
    service = WeatherService()

    weather_data = await service.get_weather(location)

    if not weather_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法获取天气数据，请检查城市名或 API 配置",
        )

    # 解析天气条件
    weather_condition = service.parse_weather_condition(weather_data)

    # 获取活动建议
    activity_rec = get_activity_recommendation(weather_condition) if weather_condition else None

    # 构建返回数据
    now = weather_data.get("now", {})
    indices = weather_data.get("indices", {})
    air_quality = weather_data.get("air_quality", {})

    return {
        "status": "success",
        "data": {
            "location": weather_data.get("location"),
            "city_key": weather_data.get("city_key"),
            # 当前天气
            "now": {
                "weather_text": now.get("WeatherText", ""),
                "weather_icon": now.get("WeatherIcon", 1),
                "temperature": now.get("Temperature", {}).get("Value", 0),
                "temperature_unit": now.get("Temperature", {}).get("Unit", "C"),
                "real_feel": now.get("RealFeelTemperature", {}).get("Value", 0),
                "humidity": now.get("RelativeHumidity", 50),
                "wind": {
                    "direction": now.get("Wind", {}).get("Direction", {}).get("Localized", ""),
                    "speed": now.get("Wind", {}).get("Speed", {}).get("Value", 0),
                    "unit": now.get("Wind", {}).get("Speed", {}).get("Unit", "km/h"),
                },
                "pressure": now.get("Pressure", {}).get("Value", 0),
                "visibility": now.get("Visibility", {}).get("Value", 10),
            },
            # 天气指数
            "indices": [
                {
                    "id": idx.get("ID", 0),
                    "name": idx.get("Name", ""),
                    "value": idx.get("Value", ""),
                    "category": idx.get("Category", ""),
                    "text": idx.get("Text", ""),
                }
                for idx in indices.get("Indices", [])
            ] if indices else [],
            # 空气质量
            "air_quality": {
                "aqi": air_quality.get("Index", 0),
                "pm25": air_quality.get("ParticulateMatter2_5", 0),
                "pm10": air_quality.get("ParticulateMatter10", 0),
                "co": air_quality.get("CarbonMonoxide", 0),
                "no2": air_quality.get("NitrogenDioxide", 0),
                "o3": air_quality.get("Ozone", 0),
                "so2": air_quality.get("SulfurDioxide", 0),
            } if air_quality else {},
            # 活动推荐
            "activity_recommendation": activity_rec,
            "outdoor_suitable": is_outdoor_suitable(weather_condition) if weather_condition else None,
            "weather_score": get_weather_score(weather_condition) if weather_condition else None,
        },
    }


@router.get("/city")
async def search_city(
    q: str,
    db: Session = Depends(get_db),
):
    """
    搜索城市获取 Key

    - q: 城市名称
    """
    service = WeatherService()

    city_key = await service.get_city_key(q)

    if not city_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到城市: {q}",
        )

    return {
        "status": "success",
        "data": {
            "city_name": q,
            "city_key": city_key,
        },
    }


@router.get("/alert")
async def get_weather_alert(
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    获取天气预警

    - location: 城市名 (可选，默认南京)
    """
    service = WeatherService()

    alert_data = await service.get_weather_alert(location)

    if alert_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法获取预警数据",
        )

    return {
        "status": "success",
        "data": alert_data,
    }


@router.get("/recommendation")
async def get_weather_recommendation(
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    获取天气活动推荐

    - location: 城市名 (可选，默认南京)
    """
    service = WeatherService()

    weather_data = await service.get_weather(location)

    if not weather_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法获取天气数据",
        )

    weather_condition = service.parse_weather_condition(weather_data)

    if not weather_condition:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="天气数据解析失败",
        )

    recommendation = get_activity_recommendation(weather_condition)

    now = weather_data.get("now", {})
    air_quality = weather_data.get("air_quality", {})

    return {
        "status": "success",
        "data": {
            "weather": {
                "text": weather_condition.text,
                "temp": weather_condition.temp,
                "humidity": weather_condition.humidity,
                "aqi": air_quality.get("AQI", 0),
                "aqi_category": air_quality.get("Category", ""),
            },
            "recommendation": recommendation,
            "outdoor_suitable": is_outdoor_suitable(weather_condition),
            "weather_score": get_weather_score(weather_condition),
        },
    }


@router.get("/indices")
async def get_weather_indices(
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    获取天气指数 (运动指数、紫外线指数等)

    - location: 城市名 (可选，默认南京)
    """
    service = WeatherService()

    city_name = location or service.default_city
    city_key = await service.get_city_key(city_name)

    if not city_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到城市: {city_name}",
        )

    indices = await service.get_indices(city_key)

    if not indices:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法获取天气指数",
        )

    return {
        "status": "success",
        "data": {
            "location": city_name,
            "indices": [
                {
                    "name": idx.get("Name", ""),
                    "value": idx.get("Value", ""),
                    "category": idx.get("Category", ""),
                    "text": idx.get("Text", ""),
                }
                for idx in indices.get("Indices", [])
            ],
        },
    }


@router.get("/air")
async def get_air_quality(
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    获取空气质量

    - location: 城市名 (可选，默认南京)
    """
    service = WeatherService()

    city_name = location or service.default_city
    city_key = await service.get_city_key(city_name)

    if not city_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到城市: {city_name}",
        )

    air_quality = await service.get_air_quality(city_key)

    if not air_quality:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法获取空气质量数据",
        )

    return {
        "status": "success",
        "data": {
            "location": city_name,
            "aqi": air_quality.get("AQI", 0),
            "aqi_category": air_quality.get("Category", ""),
            "pm25": air_quality.get("PM25", {}),
            "pm10": air_quality.get("PM10", {}),
            "co": air_quality.get("CO", {}),
            "no2": air_quality.get("NO2", {}),
            "o3": air_quality.get("O3", {}),
            "so2": air_quality.get("SO2", {}),
        },
    }