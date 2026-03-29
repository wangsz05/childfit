"""
孩子档案模型
"""
from sqlalchemy import Column, String, Date, Numeric, Enum, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ChildProfile(Base):
    """孩子档案模型"""
    __tablename__ = "child_profiles"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="所属用户 ID")
    name = Column(String(50), nullable=False, comment="孩子姓名")
    birth_date = Column(Date, nullable=False, comment="出生日期")
    gender = Column(Enum("male", "female"), nullable=False, comment="性别")
    height = Column(Numeric(5, 2), comment="身高 (cm)")
    weight = Column(Numeric(5, 2), comment="体重 (kg)")
    city = Column(String(50), comment="城市")
    family_structure = Column(
        Enum("two_parent", "single_parent", "left_behind", "other"),
        comment="家庭结构"
    )
    economic_status = Column(
        Enum("low", "medium", "high"),
        comment="经济状况"
    )
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 关系
    user = relationship("User", back_populates="children")
    daily_plans = relationship("DailyPlan", back_populates="child", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="child", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="child", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ChildProfile(id={self.id}, name={self.name})>"
