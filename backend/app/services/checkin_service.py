"""
打卡管理服务
"""
import uuid
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.checkin import CheckIn
from app.models.daily_plan import DailyPlan
from app.schemas.checkin import CheckInCreate, CheckInStats


class CheckInService:
    """打卡管理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_checkin(self, checkin_data: CheckInCreate) -> CheckIn:
        """
        创建打卡记录
        
        Args:
            checkin_data: 打卡数据
            
        Returns:
            打卡记录对象
        """
        # 验证计划是否存在
        plan = self.db.query(DailyPlan).filter(
            DailyPlan.id == checkin_data.plan_id
        ).first()
        
        if not plan:
            raise ValueError(f"计划不存在：{checkin_data.plan_id}")
        
        checkin = CheckIn(
            id=str(uuid.uuid4()),
            plan_id=checkin_data.plan_id,
            activity_id=checkin_data.activity_id,
            check_in_type=checkin_data.check_in_type,
            media_url=checkin_data.media_url,
            duration_min=checkin_data.duration_min,
            completed_at=datetime.utcnow(),
        )
        
        self.db.add(checkin)
        
        # 更新计划状态
        plan.status = "completed"
        
        self.db.commit()
        self.db.refresh(checkin)
        
        return checkin
    
    def get_by_id(self, checkin_id: str) -> Optional[CheckIn]:
        """
        根据 ID 获取打卡记录
        
        Args:
            checkin_id: 打卡 ID
            
        Returns:
            打卡记录对象
        """
        return self.db.query(CheckIn).filter(CheckIn.id == checkin_id).first()
    
    def get_by_plan(self, plan_id: str) -> List[CheckIn]:
        """
        获取计划的打卡记录
        
        Args:
            plan_id: 计划 ID
            
        Returns:
            打卡记录列表
        """
        return self.db.query(CheckIn).filter(
            CheckIn.plan_id == plan_id
        ).all()
    
    def get_by_child(
        self,
        child_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[CheckIn]:
        """
        获取孩子的打卡记录
        
        Args:
            child_id: 孩子 ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            打卡记录列表
        """
        query = self.db.query(CheckIn).join(DailyPlan).filter(
            DailyPlan.child_id == child_id
        )
        
        if start_date:
            query = query.filter(DailyPlan.plan_date >= start_date)
        if end_date:
            query = query.filter(DailyPlan.plan_date <= end_date)
        
        query = query.order_by(CheckIn.completed_at.desc())
        
        return query.all()
    
    def get_stats(self, child_id: str) -> CheckInStats:
        """
        获取打卡统计
        
        Args:
            child_id: 孩子 ID
            
        Returns:
            打卡统计数据
        """
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        
        # 总打卡数
        total = self.db.query(func.count(CheckIn.id)).join(DailyPlan).filter(
            DailyPlan.child_id == child_id
        ).scalar() or 0
        
        # 本周打卡数
        this_week = self.db.query(func.count(CheckIn.id)).join(DailyPlan).filter(
            and_(
                DailyPlan.child_id == child_id,
                DailyPlan.plan_date >= week_start,
            )
        ).scalar() or 0
        
        # 本月打卡数
        this_month = self.db.query(func.count(CheckIn.id)).join(DailyPlan).filter(
            and_(
                DailyPlan.child_id == child_id,
                DailyPlan.plan_date >= month_start,
            )
        ).scalar() or 0
        
        # 计算连续打卡天数
        current_streak = self._calculate_streak(child_id, today)
        longest_streak = self._calculate_longest_streak(child_id)
        
        return CheckInStats(
            total_checkins=total,
            this_week=this_week,
            this_month=this_month,
            current_streak=current_streak,
            longest_streak=longest_streak,
        )
    
    def _calculate_streak(self, child_id: str, end_date: date) -> int:
        """
        计算连续打卡天数
        
        Args:
            child_id: 孩子 ID
            end_date: 结束日期
            
        Returns:
            连续天数
        """
        streak = 0
        current_date = end_date
        
        while True:
            # 检查该日期是否有打卡
            checkin = self.db.query(CheckIn).join(DailyPlan).filter(
                and_(
                    DailyPlan.child_id == child_id,
                    DailyPlan.plan_date == current_date,
                )
            ).first()
            
            if checkin:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def _calculate_longest_streak(self, child_id: str) -> int:
        """
        计算最长连续打卡天数
        
        Args:
            child_id: 孩子 ID
            
        Returns:
            最长连续天数
        """
        # 获取所有打卡日期
        checkins = self.db.query(DailyPlan.plan_date).join(CheckIn).filter(
            DailyPlan.child_id == child_id
        ).distinct().order_by(DailyPlan.plan_date).all()
        
        if not checkins:
            return 0
        
        dates = [c[0] for c in checkins]
        
        longest = 1
        current = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        return longest
