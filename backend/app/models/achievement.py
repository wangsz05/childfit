"""
成就模型
"""
from sqlalchemy import Column, String, Text, JSON, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Achievement(Base):
    """成就模型"""
    __tablename__ = "achievements"

    id = Column(String(36), primary_key=True)
    child_id = Column(String(36), ForeignKey("child_profiles.id"), nullable=False, comment="孩子 ID")
    achievement_type = Column(String(50), nullable=False, comment="成就类型")
    achievement_name = Column(String(100), nullable=False, comment="成就名称")
    description = Column(Text, comment="成就描述")
    icon_url = Column(String(255), comment="图标 URL")
    achieved_at = Column(TIMESTAMP, default=func.current_timestamp(), comment="获得时间")
    metadata_json = Column("metadata", JSON, comment="元数据")

    # 关系
    child = relationship("ChildProfile", back_populates="achievements")

    def __repr__(self) -> str:
        return f"<Achievement(id={self.id}, name={self.achievement_name})>"
