"""
成就系统服务
"""
import uuid
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.achievement import Achievement
from app.models.child_profile import ChildProfile
from app.models.checkin import CheckIn
from app.models.daily_plan import DailyPlan


class AchievementService:
    """成就系统服务类"""
    
    # 预定义成就类型
    ACHIEVEMENT_TYPES = {
        "first_checkin": {
            "name": "第一次打卡",
            "description": "完成第一次运动打卡",
            "icon": "🎉",
        },
        "week_warrior": {
            "name": "周坚持者",
            "description": "连续打卡 7 天",
            "icon": "💪",
        },
        "month_master": {
            "name": "月达人",
            "description": "单月打卡满 20 次",
            "icon": "🏆",
        },
        "outdoor_lover": {
            "name": "户外爱好者",
            "description": "完成 10 次户外活动",
            "icon": "🌞",
        },
        "early_bird": {
            "name": "早起鸟儿",
            "description": "连续 5 天在 9 点前完成打卡",
            "icon": "🌅",
        },
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_child(self, child_id: str) -> List[Achievement]:
        """
        获取孩子的所有成就
        
        Args:
            child_id: 孩子 ID
            
        Returns:
            成就列表
        """
        return self.db.query(Achievement).filter(
            Achievement.child_id == child_id
        ).order_by(Achievement.achieved_at.desc()).all()
    
    def get_by_id(self, achievement_id: str) -> Optional[Achievement]:
        """
        根据 ID 获取成就
        
        Args:
            achievement_id: 成就 ID
            
        Returns:
            成就对象
        """
        return self.db.query(Achievement).filter(
            Achievement.id == achievement_id
        ).first()
    
    def add_achievement(
        self,
        child_id: str,
        achievement_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Achievement]:
        """
        添加成就
        
        Args:
            child_id: 孩子 ID
            achievement_type: 成就类型
            metadata: 元数据
            
        Returns:
            成就对象，如果已存在返回 None
        """
        # 检查是否已获得该成就
        existing = self.db.query(Achievement).filter(
            and_(
                Achievement.child_id == child_id,
                Achievement.achievement_type == achievement_type,
            )
        ).first()
        
        if existing:
            return None
        
        # 获取成就信息
        achievement_info = self.ACHIEVEMENT_TYPES.get(achievement_type)
        if not achievement_info:
            return None
        
        achievement = Achievement(
            id=str(uuid.uuid4()),
            child_id=child_id,
            achievement_type=achievement_type,
            achievement_name=achievement_info["name"],
            description=achievement_info["description"],
            icon_url=achievement_info["icon"],
            achieved_at=datetime.utcnow(),
            metadata_json=metadata,
        )
        
        self.db.add(achievement)
        self.db.commit()
        self.db.refresh(achievement)
        
        return achievement
    
    def check_and_award_achievements(self, child_id: str) -> List[Achievement]:
        """
        检查并授予成就
        
        Args:
            child_id: 孩子 ID
            
        Returns:
            新获得的成就列表
        """
        new_achievements = []
        
        # 获取打卡统计
        from app.services.checkin_service import CheckInService
        checkin_service = CheckInService(self.db)
        stats = checkin_service.get_stats(child_id)
        
        # 第一次打卡
        if stats.total_checkins == 1:
            achievement = self.add_achievement(child_id, "first_checkin")
            if achievement:
                new_achievements.append(achievement)
        
        # 周坚持者 (连续 7 天)
        if stats.current_streak >= 7:
            achievement = self.add_achievement(child_id, "week_warrior", {
                "streak": stats.current_streak,
            })
            if achievement:
                new_achievements.append(achievement)
        
        # 月达人 (单月 20 次)
        if stats.this_month >= 20:
            achievement = self.add_achievement(child_id, "month_master", {
                "count": stats.this_month,
            })
            if achievement:
                new_achievements.append(achievement)
        
        # 户外爱好者
        outdoor_count = self._count_outdoor_checkins(child_id)
        if outdoor_count >= 10:
            achievement = self.add_achievement(child_id, "outdoor_lover", {
                "outdoor_count": outdoor_count,
            })
            if achievement:
                new_achievements.append(achievement)
        
        return new_achievements
    
    def _count_outdoor_checkins(self, child_id: str) -> int:
        """
        统计户外活动打卡次数
        
        Args:
            child_id: 孩子 ID
            
        Returns:
            户外活动次数
        """
        # 这里简化处理，实际需要关联活动表判断类型
        # 暂时返回 0，后续可以完善
        return 0
    
    def get_achievement_types(self) -> List[Dict[str, Any]]:
        """
        获取所有成就类型定义
        
        Returns:
            成就类型列表
        """
        return [
            {
                "type": key,
                "name": value["name"],
                "description": value["description"],
                "icon": value["icon"],
            }
            for key, value in self.ACHIEVEMENT_TYPES.items()
        ]


def and_(*conditions):
    """SQLAlchemy and_ 函数导入"""
    from sqlalchemy import and_ as sa_and_
    return sa_and_(*conditions)
