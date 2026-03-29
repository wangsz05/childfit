"""
孩子档案模型（简化版 - 只保留年级和性别）
"""
from sqlalchemy import Column, String, Enum, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ChildProfile(Base):
    """孩子档案模型"""
    __tablename__ = "child_profiles"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="所属用户 ID")
    grade = Column(String(30), nullable=False, comment="年级")
    gender = Column(Enum("male", "female"), nullable=False, comment="性别")
    school_id = Column(String(36), ForeignKey("schools.id"), nullable=True, comment="学校 ID")
    class_id = Column(String(36), ForeignKey("classes.id"), nullable=True, comment="班级 ID")
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 关系
    user = relationship("User", back_populates="children")
    daily_plans = relationship("DailyPlan", back_populates="child", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="child", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="child", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ChildProfile(id={self.id}, grade={self.grade})>"