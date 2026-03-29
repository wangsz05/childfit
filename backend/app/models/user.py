"""
用户模型
"""
from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    wx_openid = Column(String(64), unique=True, nullable=False, comment="微信 OpenID")
    phone = Column(String(20), comment="手机号")
    nickname = Column(String(50), comment="昵称")
    avatar_url = Column(String(255), comment="头像")
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 关系
    children = relationship("ChildProfile", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, nickname={self.nickname})>"
