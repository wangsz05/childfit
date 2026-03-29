"""
孩子档案 Schema（简化版 - 只保留年级和性别）
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# 年级枚举
GradeLevel = Literal[
    "grade_1", "grade_2", "grade_3", "grade_4", "grade_5", "grade_6",
    "grade_7", "grade_8", "grade_9",
    "grade_10", "grade_11", "grade_12",
    "kindergarten_small", "kindergarten_middle", "kindergarten_big"
]


class ChildBase(BaseModel):
    """孩子档案基础 Schema"""
    grade: GradeLevel = Field(..., description="年级")
    gender: Literal["male", "female"] = Field(..., description="性别")
    school_id: Optional[str] = Field(None, description="学校 ID")
    class_id: Optional[str] = Field(None, description="班级 ID")


class ChildCreate(ChildBase):
    """孩子档案创建 Schema"""
    pass


class ChildUpdate(BaseModel):
    """孩子档案更新 Schema"""
    grade: Optional[GradeLevel] = Field(None, description="年级")
    gender: Optional[Literal["male", "female"]] = Field(None, description="性别")
    school_id: Optional[str] = Field(None, description="学校 ID")
    class_id: Optional[str] = Field(None, description="班级 ID")


class ChildResponse(BaseModel):
    """孩子档案响应 Schema"""
    id: str
    user_id: str
    grade: GradeLevel
    gender: Literal["male", "female"]
    school_id: Optional[str] = None
    class_id: Optional[str] = None
    school_name: Optional[str] = None
    class_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChildListResponse(BaseModel):
    """孩子列表响应"""
    status: str = "success"
    data: list[ChildResponse]