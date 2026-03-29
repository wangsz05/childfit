"""
打卡记录 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class CheckInBase(BaseModel):
    """打卡基础 Schema"""
    plan_id: str = Field(..., description="计划 ID")
    activity_id: Optional[str] = Field(None, description="活动 ID")
    check_in_type: Literal["manual", "photo", "video", "voice"] = Field(
        ..., description="打卡类型"
    )
    media_url: Optional[str] = Field(None, max_length=255, description="媒体文件 URL")
    duration_min: Optional[int] = Field(None, ge=1, description="实际时长 (分钟)")


class CheckInCreate(CheckInBase):
    """打卡创建 Schema"""
    pass


class CheckInResponse(CheckInBase):
    """打卡响应 Schema"""
    id: str
    completed_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class CheckInListResponse(BaseModel):
    """打卡列表响应"""
    status: str = "success"
    data: list[CheckInResponse]


class CheckInStats(BaseModel):
    """打卡统计"""
    total_checkins: int
    this_week: int
    this_month: int
    current_streak: int
    longest_streak: int
