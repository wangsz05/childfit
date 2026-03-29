"""
学校和班级模型
"""
from sqlalchemy import Column, String, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class School(Base):
    """学校模型"""
    __tablename__ = "schools"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False, comment="学校名称")
    address = Column(String(200), comment="地址")
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

    # 关系
    classes = relationship("Class", back_populates="school", cascade="all, delete-orphan")


class Class(Base):
    """班级模型"""
    __tablename__ = "classes"

    id = Column(String(36), primary_key=True)
    school_id = Column(String(36), ForeignKey("schools.id"), nullable=False, comment="学校 ID")
    name = Column(String(50), nullable=False, comment="班级名称")
    grade = Column(String(30), comment="年级")
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

    # 关系
    school = relationship("School", back_populates="classes")