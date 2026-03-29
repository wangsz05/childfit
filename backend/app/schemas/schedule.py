"""
作息时间表 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time


class ScheduleBase(BaseModel):
    """作息基础 Schema"""
    child_id: str = Field(..., description="孩子 ID")
    weekday: int = Field(..., ge=0, le=6, description="星期几 (0=周一，6=周日)")
    activity_name: str = Field(..., max_length=100, description="活动名称")
    start_time: time = Field(..., description="开始时间")
    end_time: time = Field(..., description="结束时间")
    description: Optional[str] = Field(None, description="活动描述")


class ScheduleCreate(ScheduleBase):
    """作息创建 Schema"""
    pass


class ScheduleUpdate(BaseModel):
    """作息更新 Schema"""
    weekday: Optional[int] = Field(None, ge=0, le=6, description="星期几")
    activity_name: Optional[str] = Field(None, max_length=100, description="活动名称")
    start_time: Optional[time] = Field(None, description="开始时间")
    end_time: Optional[time] = Field(None, description="结束时间")
    description: Optional[str] = Field(None, description="活动描述")


class ScheduleResponse(ScheduleBase):
    """作息响应 Schema"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScheduleListResponse(BaseModel):
    """作息列表响应"""
    status: str = "success"
    data: list[ScheduleResponse]
