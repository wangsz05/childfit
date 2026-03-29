"""
活动库模型
"""
from sqlalchemy import Column, String, Text, Integer, Enum, TIMESTAMP, func
from app.database import Base


class Activity(Base):
    """活动库模型"""
    __tablename__ = "activities"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False, comment="活动名称")
    description = Column(Text, comment="活动描述")
    age_min = Column(Integer, nullable=False, comment="最小年龄")
    age_max = Column(Integer, nullable=False, comment="最大年龄")
    type = Column(Enum("indoor", "outdoor", "any"), nullable=False, comment="活动类型")
    cost_level = Column(
        Enum("free", "low", "medium", "high"),
        nullable=False,
        comment="成本等级"
    )
    duration_min = Column(Integer, comment="推荐时长 (分钟)")
    status = Column(
        Enum("active", "inactive"),
        default="active",
        comment="状态"
    )
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self) -> str:
        return f"<Activity(id={self.id}, name={self.name})>"
