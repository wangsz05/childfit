"""
打卡记录 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.database import get_db
from app.services.checkin_service import CheckInService
from app.schemas.checkin import (
    CheckInCreate,
    CheckInResponse,
    CheckInListResponse,
    CheckInStats,
)

router = APIRouter(prefix="", tags=["打卡记录"])


@router.post("/", response_model=CheckInResponse, status_code=status.HTTP_201_CREATED)
async def create_checkin(
    checkin_data: CheckInCreate,
    db: Session = Depends(get_db),
):
    """
    创建打卡记录
    
    完成活动后打卡，支持手动、照片、视频、语音等多种打卡方式
    """
    service = CheckInService(db)
    
    try:
        checkin = service.create_checkin(checkin_data)
        return CheckInResponse.model_validate(checkin)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"打卡失败：{str(e)}",
        )


@router.get("/{checkin_id}", response_model=CheckInResponse)
async def get_checkin(
    checkin_id: str,
    db: Session = Depends(get_db),
):
    """
    获取打卡记录详情
    """
    service = CheckInService(db)
    
    checkin = service.get_by_id(checkin_id)
    if not checkin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="打卡记录不存在",
        )
    
    return CheckInResponse.model_validate(checkin)


@router.get("/plan/{plan_id}", response_model=CheckInListResponse)
async def get_checkins_by_plan(
    plan_id: str,
    db: Session = Depends(get_db),
):
    """
    获取计划的打卡记录
    """
    service = CheckInService(db)
    
    checkins = service.get_by_plan(plan_id)
    
    return CheckInListResponse(
        status="success",
        data=[CheckInResponse.model_validate(c) for c in checkins],
    )


@router.get("/child/{child_id}", response_model=CheckInListResponse)
async def get_checkins_by_child(
    child_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """
    获取孩子的打卡记录列表
    
    - child_id: 孩子 ID
    - start_date: 开始日期 (可选)
    - end_date: 结束日期 (可选)
    """
    service = CheckInService(db)
    
    checkins = service.get_by_child(child_id, start_date, end_date)
    
    return CheckInListResponse(
        status="success",
        data=[CheckInResponse.model_validate(c) for c in checkins],
    )


@router.get("/child/{child_id}/stats", response_model=CheckInStats)
async def get_checkin_stats(
    child_id: str,
    db: Session = Depends(get_db),
):
    """
    获取打卡统计
    
    包含总打卡数、本周、本月、连续打卡天数等统计信息
    """
    service = CheckInService(db)
    
    stats = service.get_stats(child_id)
    
    return stats


@router.get("/child/{child_id}/streak")
async def get_checkin_streak(
    child_id: str,
    db: Session = Depends(get_db),
):
    """
    获取打卡连续天数
    """
    service = CheckInService(db)
    
    stats = service.get_stats(child_id)
    
    return {
        "status": "success",
        "data": {
            "child_id": child_id,
            "current_streak": stats.current_streak,
            "longest_streak": stats.longest_streak,
        },
    }
