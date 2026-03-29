"""
每日计划 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime, date


class PlanBase(BaseModel):
    """计划基础 Schema"""
    child_id: str = Field(..., description="孩子 ID")
    plan_date: date = Field(..., description="计划日期")


class PlanCreate(PlanBase):
    """计划创建 Schema"""
    plan_data: Dict[str, Any] = Field(..., description="计划内容")
    weather_snapshot: Optional[Dict[str, Any]] = Field(None, description="天气快照")


class PlanUpdate(BaseModel):
    """计划更新 Schema"""
    status: Optional[Literal["generated", "confirmed", "completed", "skipped"]] = Field(
        None, description="状态"
    )
    plan_data: Optional[Dict[str, Any]] = Field(None, description="计划内容")


class PlanResponse(PlanBase):
    """计划响应 Schema"""
    id: str
    weather_snapshot: Optional[Dict[str, Any]] = None
    plan_data: Dict[str, Any]
    status: Literal["generated", "confirmed", "completed", "skipped"] = "generated"
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PlanRecommendation(BaseModel):
    """计划推荐 Schema"""
    activity_id: str
    activity_name: str
    activity_type: Literal["indoor", "outdoor", "any"]
    reason: str = Field(..., description="推荐理由")
    duration_min: Optional[int] = None
    time_slot: Optional[str] = Field(None, description="推荐时间段")
    weather_adaptation: Optional[str] = Field(None, description="天气适配说明")


class PlanGenerateRequest(BaseModel):
    """生成计划请求"""
    child_id: str = Field(..., description="孩子 ID")
    plan_date: Optional[date] = Field(None, description="计划日期 (默认今天)")


class PlanGenerateResponse(BaseModel):
    """生成计划响应"""
    status: str = "success"
    data: PlanResponse
    recommendations: list[PlanRecommendation]
