"""
用户 Schema
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础 Schema"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像 URL")


class UserCreate(UserBase):
    """用户创建 Schema"""
    wx_openid: str = Field(..., max_length=64, description="微信 OpenID")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserUpdate(UserBase):
    """用户更新 Schema"""
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像 URL")


class UserResponse(UserBase):
    """用户响应 Schema"""
    id: str
    wx_openid: str
    phone: Optional[str] = None
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
