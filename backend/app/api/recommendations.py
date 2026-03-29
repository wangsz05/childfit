"""
智能推荐 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.database import get_db
from app.services.recommendation_service import RecommendationService
from app.services.weather_service import WeatherService
from app.schemas.daily_plan import (
    PlanGenerateRequest,
    PlanGenerateResponse,
    PlanResponse,
    PlanRecommendation,
)

router = APIRouter(prefix="", tags=["智能推荐"])


@router.post("/generate", response_model=PlanGenerateResponse)
async def generate_recommendation(
    request: PlanGenerateRequest,
    db: Session = Depends(get_db),
):
    """
    生成每日活动推荐
    
    根据孩子的年龄、天气、作息时间表智能推荐适合的活动
    """
    rec_service = RecommendationService(db)
    
    # 获取孩子信息
    from app.models.child_profile import ChildProfile
    child = db.query(ChildProfile).filter(ChildProfile.id == request.child_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="孩子档案不存在",
        )
    
    # 获取天气数据
    weather_data = None
    if child.city:
        weather_service = WeatherService()
        weather_data = await weather_service.get_weather(child.city)
    
    # 使用计划日期或今天
    plan_date = request.plan_date or date.today()
    
    # 生成计划数据
    plan_data = rec_service.generate_daily_plan(
        child_id=request.child_id,
        plan_date=plan_date,
        weather=weather_data,
    )
    
    # 生成推荐列表
    from app.utils.weather_rules import WeatherCondition
    weather_condition = None
    if weather_data:
        weather_condition = weather_service.parse_weather_condition(weather_data)
    
    recommendations = rec_service.generate_recommendations(child, weather_condition)
    
    # 创建或更新计划
    plan = rec_service.create_or_update_plan(
        child_id=request.child_id,
        plan_date=plan_date,
        plan_data=plan_data,
        weather_snapshot=weather_data.get("now", {}) if weather_data else None,
    )
    
    return PlanGenerateResponse(
        status="success",
        data=PlanResponse.model_validate(plan),
        recommendations=recommendations,
    )


@router.get("/list")
async def get_recommendations(
    child_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """
    获取推荐计划列表
    
    - child_id: 孩子 ID
    - start_date: 开始日期 (可选，默认今天)
    - end_date: 结束日期 (可选)
    """
    rec_service = RecommendationService(db)
    
    plans = rec_service.get_plans_by_child(child_id, start_date, end_date)
    
    return {
        "status": "success",
        "data": [
            {
                "id": plan.id,
                "plan_date": plan.plan_date.isoformat(),
                "status": plan.status,
                "plan_data": plan.plan_data,
                "weather_snapshot": plan.weather_snapshot,
                "created_at": plan.created_at.isoformat() if plan.created_at else None,
            }
            for plan in plans
        ],
    }


@router.get("/{plan_id}")
async def get_plan_detail(
    plan_id: str,
    db: Session = Depends(get_db),
):
    """
    获取计划详情
    """
    rec_service = RecommendationService(db)
    
    plan = rec_service.get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在",
        )
    
    return {
        "status": "success",
        "data": {
            "id": plan.id,
            "child_id": plan.child_id,
            "plan_date": plan.plan_date.isoformat(),
            "status": plan.status,
            "plan_data": plan.plan_data,
            "weather_snapshot": plan.weather_snapshot,
            "created_at": plan.created_at.isoformat() if plan.created_at else None,
            "updated_at": plan.updated_at.isoformat() if plan.updated_at else None,
        },
    }


@router.put("/{plan_id}/status")
async def update_plan_status(
    plan_id: str,
    status: str,
    db: Session = Depends(get_db),
):
    """
    更新计划状态
    
    - status: 新状态 (generated, confirmed, completed, skipped)
    """
    valid_statuses = ["generated", "confirmed", "completed", "skipped"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的状态值，必须是：{', '.join(valid_statuses)}",
        )
    
    rec_service = RecommendationService(db)
    
    plan = rec_service.get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在",
        )
    
    plan.status = status  # type: ignore
    db.commit()
    db.refresh(plan)
    
    return {
        "status": "success",
        "message": f"计划状态已更新为：{status}",
        "data": {
            "id": plan.id,
            "status": plan.status,
        },
    }
