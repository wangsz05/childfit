"""
活动 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class ActivityBase(BaseModel):
    """活动基础 Schema"""
    name: str = Field(..., max_length=100, description="活动名称")
    description: Optional[str] = Field(None, description="活动描述")
    age_min: int = Field(..., ge=0, le=18, description="最小年龄")
    age_max: int = Field(..., ge=0, le=18, description="最大年龄")
    type: Literal["indoor", "outdoor", "any"] = Field(..., description="活动类型")
    cost_level: Literal["free", "low", "medium", "high"] = Field(..., description="成本等级")
    duration_min: Optional[int] = Field(None, ge=1, description="推荐时长 (分钟)")


class ActivityCreate(ActivityBase):
    """活动创建 Schema"""
    pass


class ActivityUpdate(BaseModel):
    """活动更新 Schema"""
    name: Optional[str] = Field(None, max_length=100, description="活动名称")
    description: Optional[str] = Field(None, description="活动描述")
    age_min: Optional[int] = Field(None, ge=0, le=18, description="最小年龄")
    age_max: Optional[int] = Field(None, ge=0, le=18, description="最大年龄")
    type: Optional[Literal["indoor", "outdoor", "any"]] = Field(None, description="活动类型")
    cost_level: Optional[Literal["free", "low", "medium", "high"]] = Field(None, description="成本等级")
    duration_min: Optional[int] = Field(None, ge=1, description="推荐时长 (分钟)")
    status: Optional[Literal["active", "inactive"]] = Field(None, description="状态")


class ActivityResponse(ActivityBase):
    """活动响应 Schema"""
    id: str
    status: Literal["active", "inactive"] = "active"
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ActivityListResponse(BaseModel):
    """活动列表响应"""
    status: str = "success"
    data: list[ActivityResponse]
