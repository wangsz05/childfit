"""
用户管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
)

router = APIRouter(tags=["用户管理"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    微信小程序用户注册
    """
    service = UserService(db)
    
    # 检查用户是否已存在
    existing_user = service.get_by_wx_openid(user_data.wx_openid)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户已注册",
        )
    
    # 创建用户
    user = service.create_user(user_data)
    
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    用户登录
    
    使用微信 OpenID 登录，返回 access token
    """
    service = UserService(db)
    
    result = service.login(login_data.wx_openid)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在，请先注册",
        )
    
    user, access_token = result
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    获取用户详细信息
    """
    service = UserService(db)
    
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    更新用户信息
    """
    service = UserService(db)
    
    user = service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    return UserResponse.model_validate(user)


@router.get("/{user_id}/children-count")
async def get_children_count(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    获取用户的孩子数量
    """
    service = UserService(db)
    
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    from app.services.child_service import ChildService
    child_service = ChildService(db)
    count = child_service.get_child_count_by_user(user_id)
    
    return {
        "status": "success",
        "data": {
            "user_id": user_id,
            "children_count": count,
        },
    }
