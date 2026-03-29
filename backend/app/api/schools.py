"""
学校和班级 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db

router = APIRouter(prefix="/api/schools", tags=["学校管理"])


# 模拟学校数据
MOCK_SCHOOLS = [
    {"id": "school-001", "name": "南京市第一小学"},
    {"id": "school-002", "name": "南京市实验小学"},
    {"id": "school-003", "name": "南京市育才小学"},
    {"id": "school-004", "name": "南京市朝阳小学"},
    {"id": "school-005", "name": "南京市阳光小学"},
]

# 模拟班级数据
MOCK_CLASSES = {
    "school-001": [
        {"id": "class-001-1", "name": "一年级1班"},
        {"id": "class-001-2", "name": "一年级2班"},
        {"id": "class-001-3", "name": "二年级1班"},
        {"id": "class-001-4", "name": "二年级2班"},
    ],
    "school-002": [
        {"id": "class-002-1", "name": "一年级1班"},
        {"id": "class-002-2", "name": "二年级1班"},
    ],
    "school-003": [
        {"id": "class-003-1", "name": "一年级1班"},
        {"id": "class-003-2", "name": "二年级1班"},
        {"id": "class-003-3", "name": "三年级1班"},
    ],
}


@router.get("/")
async def get_schools(
    db: Session = Depends(get_db),
):
    """
    获取学校列表
    """
    return MOCK_SCHOOLS


@router.get("/{school_id}/classes")
async def get_classes(
    school_id: str,
    db: Session = Depends(get_db),
):
    """
    获取学校的班级列表
    """
    classes = MOCK_CLASSES.get(school_id, [])
    return classes