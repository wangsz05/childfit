"""
每日计划模型
"""
from sqlalchemy import Column, String, Date, Enum, JSON, TIMESTAMP, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class DailyPlan(Base):
    """每日计划模型"""
    __tablename__ = "daily_plans"

    id = Column(String(36), primary_key=True)
    child_id = Column(String(36), ForeignKey("child_profiles.id"), nullable=False, comment="孩子 ID")
    plan_date = Column(Date, nullable=False, comment="计划日期")
    weather_snapshot = Column(JSON, comment="天气快照")
    plan_data = Column(JSON, nullable=False, comment="计划内容")
    status = Column(
        Enum("generated", "confirmed", "completed", "skipped"),
        default="generated",
        comment="状态"
    )
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 关系
    child = relationship("ChildProfile", back_populates="daily_plans")
    check_ins = relationship("CheckIn", back_populates="plan", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("child_id", "plan_date", name="uk_child_date"),
    )

    def __repr__(self) -> str:
        return f"<DailyPlan(id={self.id}, plan_date={self.plan_date})>"
