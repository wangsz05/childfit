"""
成就 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AchievementBase(BaseModel):
    """成就基础 Schema"""
    achievement_type: str = Field(..., max_length=50, description="成就类型")
    achievement_name: str = Field(..., max_length=100, description="成就名称")
    description: Optional[str] = Field(None, description="成就描述")
    icon_url: Optional[str] = Field(None, max_length=255, description="图标 URL")


class AchievementResponse(AchievementBase):
    """成就响应 Schema"""
    id: str
    child_id: str
    achieved_at: datetime
    metadata: Optional[Dict[str, Any]] = Field(None, alias="metadata_json")

    class Config:
        from_attributes = True
        populate_by_name = True


class AchievementListResponse(BaseModel):
    """成就列表响应"""
    status: str = "success"
    data: list[AchievementResponse]


class AchievementType(BaseModel):
    """成就类型定义"""
    type: str
    name: str
    description: str
    icon: str
    condition: Dict[str, Any]
