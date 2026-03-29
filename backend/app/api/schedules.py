"""
作息时间表管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import time

from app.database import get_db
from app.services.schedule_service import ScheduleService
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    ScheduleListResponse,
)

router = APIRouter(prefix="/schedules", tags=["作息时间表"])


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
):
    """
    创建作息时间安排
    """
    service = ScheduleService(db)
    
    try:
        schedule = service.create_schedule(schedule_data)
        return schedule
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建失败：{str(e)}",
        )


@router.get("/", response_model=ScheduleListResponse)
async def get_schedules(
    child_id: str,
    weekday: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    获取孩子的作息时间表
    
    - child_id: 孩子 ID
    - weekday: 星期几 (0-6，可选)
    """
    service = ScheduleService(db)
    
    schedules = service.get_by_child(child_id, weekday)
    
    return ScheduleListResponse(
        status="success",
        data=[ScheduleResponse.model_validate(s) for s in schedules],
    )


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    db: Session = Depends(get_db),
):
    """
    获取作息记录详情
    """
    service = ScheduleService(db)
    
    schedule = service.get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作息记录不存在",
        )
    
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: str,
    schedule_data: ScheduleUpdate,
    db: Session = Depends(get_db),
):
    """
    更新作息记录
    """
    service = ScheduleService(db)
    
    schedule = service.update_schedule(schedule_id, schedule_data)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作息记录不存在",
        )
    
    return schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: str,
    db: Session = Depends(get_db),
):
    """
    删除作息记录
    """
    service = ScheduleService(db)
    
    success = service.delete_schedule(schedule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作息记录不存在",
        )
