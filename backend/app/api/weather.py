"""
天气查询 API
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
    location: str,
    db: Session = Depends(get_db),
):
    """
    获取实时天气
    
    - location: 城市名或经纬度
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
    
    return {
        "status": "success",
        "data": {
            "location": weather_data.get("location"),
            "city_id": weather_data.get("city_id"),
            "now": weather_data.get("now", {}),
            "forecast": weather_data.get("forecast", [])[:3],  # 最近 3 天预报
            "activity_recommendation": activity_rec,
            "outdoor_suitable": is_outdoor_suitable(weather_condition) if weather_condition else None,
            "weather_score": get_weather_score(weather_condition) if weather_condition else None,
        },
    }


@router.get("/alert")
async def get_weather_alert(
    location: str,
    db: Session = Depends(get_db),
):
    """
    获取天气预警
    
    - location: 城市名或经纬度
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
    location: str,
    db: Session = Depends(get_db),
):
    """
    获取天气活动推荐
    
    - location: 城市名或经纬度
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
    
    return {
        "status": "success",
        "data": {
            "weather": {
                "text": weather_condition.text,
                "temp": weather_condition.temp,
                "humidity": weather_condition.humidity,
            },
            "recommendation": recommendation,
        },
    }
