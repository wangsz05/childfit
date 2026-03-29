"""
用户管理服务
"""
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.jwt_utils import create_access_token


class UserService:
    """用户管理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_wx_openid(self, wx_openid: str) -> Optional[User]:
        """
        根据微信 OpenID 获取用户
        
        Args:
            wx_openid: 微信 OpenID
            
        Returns:
            用户对象，不存在返回 None
        """
        return self.db.query(User).filter(User.wx_openid == wx_openid).first()
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        根据 ID 获取用户
        
        Args:
            user_id: 用户 ID
            
        Returns:
            用户对象，不存在返回 None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        创建新用户

        Args:
            user_data: 用户创建数据

        Returns:
            创建的用户对象
        """
        user = User(
            id=str(uuid.uuid4()),
            wx_openid=user_data.wx_openid,
            role=user_data.role or "student",
            phone=user_data.phone,
            nickname=user_data.nickname,
            avatar_url=user_data.avatar_url,
            school_id=user_data.school_id,
            class_id=user_data.class_id,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """
        更新用户信息
        
        Args:
            user_id: 用户 ID
            user_data: 用户更新数据
            
        Returns:
            更新后的用户对象，失败返回 None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def login(self, wx_openid: str) -> Optional[tuple[User, str]]:
        """
        用户登录
        
        Args:
            wx_openid: 微信 OpenID
            
        Returns:
            (用户对象，access_token)，失败返回 None
        """
        user = self.get_by_wx_openid(wx_openid)
        if not user:
            return None
        
        # 创建 access token
        access_token = create_access_token(
            data={"sub": user.id, "wx_openid": user.wx_openid}
        )
        
        return user, access_token
    
    def get_user_count(self) -> int:
        """
        获取用户总数
        
        Returns:
            用户总数
        """
        return self.db.query(func.count(User.id)).scalar() or 0
