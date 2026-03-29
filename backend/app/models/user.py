"""
用户模型
"""
from sqlalchemy import Column, String, TIMESTAMP, func, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    wx_openid = Column(String(64), unique=True, nullable=False, comment="微信 OpenID")
    role = Column(String(20), default="student", comment="用户角色")
    phone = Column(String(20), comment="手机号")
    nickname = Column(String(50), comment="昵称")
    avatar_url = Column(String(255), comment="头像")
    school_id = Column(String(36), comment="学校 ID")
    class_id = Column(String(36), comment="班级 ID")
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 关系
    children = relationship("ChildProfile", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, nickname={self.nickname}, role={self.role})>"
