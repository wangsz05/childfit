"""
孩子档案 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, date


class ChildBase(BaseModel):
    """孩子档案基础 Schema"""
    name: str = Field(..., max_length=50, description="孩子姓名")
    birth_date: date = Field(..., description="出生日期")
    gender: Literal["male", "female"] = Field(..., description="性别")
    height: Optional[float] = Field(None, ge=50, le=250, description="身高 (cm)")
    weight: Optional[float] = Field(None, ge=2, le=150, description="体重 (kg)")
    city: Optional[str] = Field(None, max_length=50, description="城市")
    family_structure: Optional[Literal["two_parent", "single_parent", "left_behind", "other"]] = Field(
        None, description="家庭结构"
    )
    economic_status: Optional[Literal["low", "medium", "high"]] = Field(
        None, description="经济状况"
    )


class ChildCreate(ChildBase):
    """孩子档案创建 Schema"""
    pass


class ChildUpdate(BaseModel):
    """孩子档案更新 Schema"""
    name: Optional[str] = Field(None, max_length=50, description="孩子姓名")
    birth_date: Optional[date] = Field(None, description="出生日期")
    gender: Optional[Literal["male", "female"]] = Field(None, description="性别")
    height: Optional[float] = Field(None, ge=50, le=250, description="身高 (cm)")
    weight: Optional[float] = Field(None, ge=2, le=150, description="体重 (kg)")
    city: Optional[str] = Field(None, max_length=50, description="城市")
    family_structure: Optional[Literal["two_parent", "single_parent", "left_behind", "other"]] = Field(
        None, description="家庭结构"
    )
    economic_status: Optional[Literal["low", "medium", "high"]] = Field(
        None, description="经济状况"
    )


class ChildResponse(ChildBase):
    """孩子档案响应 Schema"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChildListResponse(BaseModel):
    """孩子列表响应"""
    status: str = "success"
    data: list[ChildResponse]
