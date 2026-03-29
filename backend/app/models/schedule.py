"""
作息时间表模型
"""
from sqlalchemy import Column, String, Integer, Time, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Schedule(Base):
    """作息时间表模型"""
    __tablename__ = "schedules"

    id = Column(String(36), primary_key=True)
    child_id = Column(String(36), ForeignKey("child_profiles.id"), nullable=False, comment="孩子 ID")
    weekday = Column(Integer, nullable=False, comment="星期几 (0=周一，6=周日)")
    activity_name = Column(String(100), nullable=False, comment="活动名称")
    start_time = Column(Time, nullable=False, comment="开始时间")
    end_time = Column(Time, nullable=False, comment="结束时间")
    description = Column(Text, comment="活动描述")
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 关系
    child = relationship("ChildProfile", back_populates="schedules")

    def __repr__(self) -> str:
        return f"<Schedule(id={self.id}, activity={self.activity_name})>"
