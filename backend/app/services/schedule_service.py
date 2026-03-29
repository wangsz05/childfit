"""
作息时间表管理服务
"""
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


class ScheduleService:
    """作息时间表管理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, schedule_id: str) -> Optional[Schedule]:
        """
        根据 ID 获取作息记录
        
        Args:
            schedule_id: 作息记录 ID
            
        Returns:
            作息记录对象
        """
        return self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    def get_by_child(self, child_id: str, weekday: Optional[int] = None) -> List[Schedule]:
        """
        获取孩子的作息时间表
        
        Args:
            child_id: 孩子 ID
            weekday: 星期几 (可选，0-6)
            
        Returns:
            作息记录列表
        """
        query = self.db.query(Schedule).filter(Schedule.child_id == child_id)
        
        if weekday is not None:
            query = query.filter(Schedule.weekday == weekday)
        
        query = query.order_by(Schedule.weekday, Schedule.start_time)
        
        return query.all()
    
    def create_schedule(self, schedule_data: ScheduleCreate) -> Schedule:
        """
        创建作息记录
        
        Args:
            schedule_data: 作息创建数据
            
        Returns:
            作息记录对象
        """
        schedule = Schedule(
            id=str(uuid.uuid4()),
            child_id=schedule_data.child_id,
            weekday=schedule_data.weekday,
            activity_name=schedule_data.activity_name,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
            description=schedule_data.description,
        )
        
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        
        return schedule
    
    def update_schedule(
        self,
        schedule_id: str,
        schedule_data: ScheduleUpdate,
    ) -> Optional[Schedule]:
        """
        更新作息记录
        
        Args:
            schedule_id: 作息记录 ID
            schedule_data: 作息更新数据
            
        Returns:
            更新后的作息记录对象
        """
        schedule = self.get_by_id(schedule_id)
        if not schedule:
            return None
        
        update_data = schedule_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(schedule, field, value)
        
        self.db.commit()
        self.db.refresh(schedule)
        
        return schedule
    
    def delete_schedule(self, schedule_id: str) -> bool:
        """
        删除作息记录
        
        Args:
            schedule_id: 作息记录 ID
            
        Returns:
            是否删除成功
        """
        schedule = self.get_by_id(schedule_id)
        if not schedule:
            return False
        
        self.db.delete(schedule)
        self.db.commit()
        
        return True
    
    def get_by_weekday(self, child_id: str, weekday: int) -> List[Schedule]:
        """
        获取指定星期的作息安排
        
        Args:
            child_id: 孩子 ID
            weekday: 星期几 (0-6)
            
        Returns:
            作息记录列表
        """
        return self.get_by_child(child_id, weekday)
