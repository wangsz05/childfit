"""
智能推荐引擎服务
核心推荐逻辑：根据天气、作息、年龄推荐活动
"""
import uuid
import logging
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.activity import Activity
from app.models.daily_plan import DailyPlan
from app.models.child_profile import ChildProfile
from app.models.schedule import Schedule
from app.schemas.daily_plan import PlanRecommendation
from app.utils.age_calculator import calculate_age, get_age_group, estimate_age_from_grade
from app.utils.weather_rules import (
    WeatherCondition,
    is_outdoor_suitable,
    get_activity_recommendation,
    filter_activities_by_weather,
    get_weather_score,
)

logger = logging.getLogger(__name__)


class RecommendationService:
    """智能推荐引擎服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_suitable_activities(
        self,
        age: int,
        weather: Optional[WeatherCondition] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        获取适合的活动列表
        
        Args:
            age: 孩子年龄
            weather: 天气条件 (可选)
            limit: 返回数量限制
            
        Returns:
            活动列表
        """
        # 查询适合年龄的活动
        query = self.db.query(Activity).filter(
            and_(
                Activity.age_min <= age,
                Activity.age_max >= age,
                Activity.status == "active",
            )
        )
        
        activities = query.all()
        
        # 转换为字典列表
        activity_list = []
        for act in activities:
            activity_list.append({
                "id": act.id,
                "name": act.name,
                "description": act.description,
                "age_min": act.age_min,
                "age_max": act.age_max,
                "type": act.type,
                "cost_level": act.cost_level,
                "duration_min": act.duration_min,
            })
        
        # 根据天气过滤
        if weather:
            activity_list = filter_activities_by_weather(activity_list, weather)
        
        # 返回限制数量
        return activity_list[:limit]
    
    def generate_recommendations(
        self,
        child: ChildProfile,
        weather: Optional[WeatherCondition] = None,
        schedule: Optional[List[Schedule]] = None,
    ) -> List[PlanRecommendation]:
        """
        生成活动推荐
        
        Args:
            child: 孩子档案
            weather: 天气条件
            schedule: 作息时间表
            
        Returns:
            推荐列表
        """
        # 计算年龄 (根据年级估算)
        age = estimate_age_from_grade(child.grade)
        age_group = get_age_group(age)
        
        recommendations = []
        
        # 获取适合的活动
        activities = self.get_suitable_activities(age, weather, limit=20)
        
        # 分析天气
        weather_rec = None
        if weather:
            weather_rec = get_activity_recommendation(weather)
            is_outdoor_ok = is_outdoor_suitable(weather)
        else:
            is_outdoor_ok = True
        
        # 为每个活动生成推荐理由
        for activity in activities[:5]:  # 最多推荐 5 个活动
            reason_parts = []
            weather_adaptation = None
            
            # 年龄适配
            reason_parts.append(f"适合{age_group}年龄段")
            
            # 天气适配
            if weather:
                if activity["type"] == "outdoor" and not is_outdoor_ok:
                    continue  # 不适合户外的天气跳过户外活动
                elif activity["type"] == "indoor":
                    reason_parts.append("室内活动，不受天气影响")
                elif activity["type"] == "outdoor" and is_outdoor_ok:
                    weather_text = weather.text if weather else "晴朗"
                    reason_parts.append(f"{weather_text}天气适合户外")
                
                if weather_rec:
                    weather_adaptation = weather_rec.get("reason", "")
            
            # 时长建议
            if activity["duration_min"]:
                reason_parts.append(f"推荐时长{activity['duration_min']}分钟")
            
            recommendation = PlanRecommendation(
                activity_id=activity["id"],
                activity_name=activity["name"],
                activity_type=activity["type"],  # type: ignore
                reason="，".join(reason_parts),
                duration_min=activity["duration_min"],
                weather_adaptation=weather_adaptation,
            )
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def generate_daily_plan(
        self,
        child_id: str,
        plan_date: date,
        weather: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        生成每日计划
        
        Args:
            child_id: 孩子 ID
            plan_date: 计划日期
            weather: 天气数据
            
        Returns:
            计划数据
        """
        # 获取孩子信息
        child = self.db.query(ChildProfile).filter(ChildProfile.id == child_id).first()
        if not child:
            raise ValueError(f"孩子档案不存在：{child_id}")
        
        # 计算年龄 (根据年级估算)
        age = estimate_age_from_grade(child.grade)
        
        # 解析天气
        weather_condition = None
        if weather:
            from app.services.weather_service import WeatherService
            ws = WeatherService()
            weather_condition = ws.parse_weather_condition(weather)
        
        # 获取作息时间表
        weekday = plan_date.weekday()
        schedules = self.db.query(Schedule).filter(
            and_(
                Schedule.child_id == child_id,
                Schedule.weekday == weekday,
            )
        ).all()
        
        # 生成推荐
        recommendations = self.generate_recommendations(child, weather_condition, schedules)
        
        # 构建计划数据
        plan_data = {
            "date": plan_date.isoformat(),
            "child_id": child_id,
            "age": age,
            "weather": {
                "text": weather.get("now", {}).get("text", "未知") if weather else "未知",
                "temp": weather.get("now", {}).get("temp", 0) if weather else 0,
            } if weather else None,
            "activities": [
                {
                    "activity_id": rec.activity_id,
                    "activity_name": rec.activity_name,
                    "activity_type": rec.activity_type,
                    "reason": rec.reason,
                    "duration_min": rec.duration_min,
                    "time_slot": rec.time_slot,
                }
                for rec in recommendations
            ],
            "schedule": [
                {
                    "activity_name": s.activity_name,
                    "start_time": s.start_time.isoformat() if s.start_time else None,
                    "end_time": s.end_time.isoformat() if s.end_time else None,
                    "description": s.description,
                }
                for s in schedules
            ],
        }
        
        return plan_data
    
    def create_or_update_plan(
        self,
        child_id: str,
        plan_date: date,
        plan_data: Dict[str, Any],
        weather_snapshot: Optional[Dict[str, Any]] = None,
    ) -> DailyPlan:
        """
        创建或更新每日计划
        
        Args:
            child_id: 孩子 ID
            plan_date: 计划日期
            plan_data: 计划内容
            weather_snapshot: 天气快照
            
        Returns:
            计划对象
        """
        # 检查是否已存在
        existing_plan = self.db.query(DailyPlan).filter(
            and_(
                DailyPlan.child_id == child_id,
                DailyPlan.plan_date == plan_date,
            )
        ).first()
        
        if existing_plan:
            # 更新现有计划
            existing_plan.plan_data = plan_data
            existing_plan.weather_snapshot = weather_snapshot
            existing_plan.status = "generated"
            existing_plan.updated_at = datetime.utcnow()
            plan = existing_plan
        else:
            # 创建新计划
            plan = DailyPlan(
                id=str(uuid.uuid4()),
                child_id=child_id,
                plan_date=plan_date,
                plan_data=plan_data,
                weather_snapshot=weather_snapshot,
                status="generated",
            )
            self.db.add(plan)
        
        self.db.commit()
        self.db.refresh(plan)
        
        return plan
    
    def get_plan_by_id(self, plan_id: str) -> Optional[DailyPlan]:
        """
        根据 ID 获取计划
        
        Args:
            plan_id: 计划 ID
            
        Returns:
            计划对象
        """
        return self.db.query(DailyPlan).filter(DailyPlan.id == plan_id).first()
    
    def get_plans_by_child(
        self,
        child_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[DailyPlan]:
        """
        获取孩子的计划列表
        
        Args:
            child_id: 孩子 ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            计划列表
        """
        query = self.db.query(DailyPlan).filter(DailyPlan.child_id == child_id)
        
        if start_date:
            query = query.filter(DailyPlan.plan_date >= start_date)
        if end_date:
            query = query.filter(DailyPlan.plan_date <= end_date)
        
        query = query.order_by(DailyPlan.plan_date.desc())
        
        return query.all()
