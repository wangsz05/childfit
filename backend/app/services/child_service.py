"""
孩子档案管理服务（简化版）
"""
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.child_profile import ChildProfile
from app.schemas.child_profile import ChildCreate, ChildUpdate


class ChildService:
    """孩子档案管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, child_id: str) -> Optional[ChildProfile]:
        """
        根据 ID 获取孩子档案

        Args:
            child_id: 孩子档案 ID

        Returns:
            孩子档案对象，不存在返回 None
        """
        return self.db.query(ChildProfile).filter(ChildProfile.id == child_id).first()

    def get_by_user(self, user_id: str) -> List[ChildProfile]:
        """
        获取用户的所有孩子档案

        Args:
            user_id: 用户 ID

        Returns:
            孩子档案列表
        """
        return self.db.query(ChildProfile).filter(ChildProfile.user_id == user_id).all()

    def create_child(self, user_id: str, child_data: ChildCreate) -> ChildProfile:
        """
        创建孩子档案

        Args:
            user_id: 用户 ID
            child_data: 孩子档案创建数据

        Returns:
            创建的孩子档案对象
        """
        child = ChildProfile(
            id=str(uuid.uuid4()),
            user_id=user_id,
            grade=child_data.grade,
            gender=child_data.gender,
            school_id=child_data.school_id,
            class_id=child_data.class_id,
        )

        self.db.add(child)
        self.db.commit()
        self.db.refresh(child)

        return child

    def update_child(self, child_id: str, child_data: ChildUpdate) -> Optional[ChildProfile]:
        """
        更新孩子档案

        Args:
            child_id: 孩子档案 ID
            child_data: 孩子档案更新数据

        Returns:
            更新后的孩子档案对象，失败返回 None
        """
        child = self.get_by_id(child_id)
        if not child:
            return None

        update_data = child_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(child, field, value)

        self.db.commit()
        self.db.refresh(child)

        return child

    def delete_child(self, child_id: str) -> bool:
        """
        删除孩子档案

        Args:
            child_id: 孩子档案 ID

        Returns:
            是否删除成功
        """
        child = self.get_by_id(child_id)
        if not child:
            return False

        self.db.delete(child)
        self.db.commit()

        return True

    def get_child_count_by_user(self, user_id: str) -> int:
        """
        获取用户的孩子数量

        Args:
            user_id: 用户 ID

        Returns:
            孩子数量
        """
        return self.db.query(func.count(ChildProfile.id)).filter(
            ChildProfile.user_id == user_id
        ).scalar() or 0