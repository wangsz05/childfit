"""
孩子档案管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.child_service import ChildService
from app.schemas.child_profile import (
    ChildCreate,
    ChildUpdate,
    ChildResponse,
    ChildListResponse,
)

router = APIRouter(prefix="", tags=["孩子档案"])


@router.post("/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def create_child(
    child_data: ChildCreate,
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    创建孩子档案
    """
    service = ChildService(db)
    
    try:
        child = service.create_child(user_id, child_data)
        return ChildResponse.model_validate(child)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建失败：{str(e)}",
        )


@router.get("/", response_model=ChildListResponse)
async def get_children(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    获取用户的孩子列表
    """
    service = ChildService(db)
    
    children = service.get_by_user(user_id)
    
    return ChildListResponse(
        status="success",
        data=[ChildResponse.model_validate(c) for c in children],
    )


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(
    child_id: str,
    db: Session = Depends(get_db),
):
    """
    获取孩子档案详情
    """
    service = ChildService(db)
    
    child = service.get_by_id(child_id)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="孩子档案不存在",
        )
    
    return ChildResponse.model_validate(child)


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child(
    child_id: str,
    child_data: ChildUpdate,
    db: Session = Depends(get_db),
):
    """
    更新孩子档案
    """
    service = ChildService(db)
    
    child = service.update_child(child_id, child_data)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="孩子档案不存在",
        )
    
    return ChildResponse.model_validate(child)


@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_child(
    child_id: str,
    db: Session = Depends(get_db),
):
    """
    删除孩子档案
    """
    service = ChildService(db)
    
    success = service.delete_child(child_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="孩子档案不存在",
        )
