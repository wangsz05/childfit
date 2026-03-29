"""
用户 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# 用户角色类型
UserRole = Literal["student", "teacher", "parent"]


class UserBase(BaseModel):
    """用户基础 Schema"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像 URL")


class UserCreate(UserBase):
    """用户创建 Schema"""
    wx_openid: str = Field(..., max_length=64, description="微信 OpenID")
    role: Optional[UserRole] = Field("student", description="用户角色")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    school_id: Optional[str] = Field(None, description="学校 ID")
    class_id: Optional[str] = Field(None, description="班级 ID")


class UserUpdate(UserBase):
    """用户更新 Schema"""
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像 URL")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    role: Optional[UserRole] = Field(None, description="用户角色")


class UserResponse(UserBase):
    """用户响应 Schema"""
    id: str
    wx_openid: str
    role: UserRole = "student"
    phone: Optional[str] = None
    school_id: Optional[str] = None
    class_id: Optional[str] = None
    school_name: Optional[str] = None
    class_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """用户登录 Schema"""
    wx_openid: str = Field(..., max_length=64, description="微信 OpenID")


class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token 数据"""
    user_id: Optional[str] = None
