"""
打卡记录模型
"""
from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CheckIn(Base):
    """打卡记录模型"""
    __tablename__ = "check_ins"

    id = Column(String(36), primary_key=True)
    plan_id = Column(String(36), ForeignKey("daily_plans.id"), nullable=False, comment="计划 ID")
    activity_id = Column(String(36), ForeignKey("activities.id"), comment="活动 ID")
    check_in_type = Column(
        Enum("manual", "photo", "video", "voice"),
        nullable=False,
        comment="打卡类型"
    )
    media_url = Column(String(255), comment="媒体文件 URL")
    duration_min = Column(Integer, comment="实际时长 (分钟)")
    completed_at = Column(TIMESTAMP, default=func.current_timestamp(), comment="完成时间")
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

    # 关系
    plan = relationship("DailyPlan", back_populates="check_ins")
    activity = relationship("Activity")

    def __repr__(self) -> str:
        return f"<CheckIn(id={self.id}, plan_id={self.plan_id})>"
