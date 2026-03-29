"""
成就系统 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.achievement_service import AchievementService
from app.schemas.achievement import (
    AchievementResponse,
    AchievementListResponse,
    AchievementType,
)

router = APIRouter(prefix="", tags=["成就系统"])


@router.get("/types", response_model=list[AchievementType])
async def get_achievement_types(
    db: Session = Depends(get_db),
):
    """
    获取所有成就类型定义
    
    返回系统中所有可获得的成就类型及其说明
    """
    service = AchievementService(db)
    
    types = service.get_achievement_types()
    
    return types


@router.get("/child/{child_id}", response_model=AchievementListResponse)
async def get_achievements(
    child_id: str,
    db: Session = Depends(get_db),
):
    """
    获取孩子的所有成就
    
    - child_id: 孩子 ID
    """
    service = AchievementService(db)
    
    # 验证孩子是否存在
    from app.models.child_profile import ChildProfile
    child = db.query(ChildProfile).filter(ChildProfile.id == child_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="孩子档案不存在",
        )
    
    achievements = service.get_by_child(child_id)
    
    return AchievementListResponse(
        status="success",
        data=[AchievementResponse.model_validate(a) for a in achievements],
    )


@router.get("/{achievement_id}", response_model=AchievementResponse)
async def get_achievement(
    achievement_id: str,
    db: Session = Depends(get_db),
):
    """
    获取成就详情
    """
    service = AchievementService(db)
    
    achievement = service.get_by_id(achievement_id)
    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成就记录不存在",
        )
    
    return AchievementResponse.model_validate(achievement)


@router.post("/child/{child_id}/check")
async def check_achievements(
    child_id: str,
    db: Session = Depends(get_db),
):
    """
    检查并授予成就
    
    根据孩子的打卡记录等数据，检查是否满足成就条件并自动授予
    """
    service = AchievementService(db)
    
    # 验证孩子是否存在
    from app.models.child_profile import ChildProfile
    child = db.query(ChildProfile).filter(ChildProfile.id == child_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="孩子档案不存在",
        )
    
    # 检查并授予成就
    new_achievements = service.check_and_award_achievements(child_id)
    
    return {
        "status": "success",
        "message": f"检查完成，新获得 {len(new_achievements)} 个成就",
        "data": {
            "new_achievements": [
                {
                    "id": a.id,
                    "name": a.achievement_name,
                    "type": a.achievement_type,
                    "achieved_at": a.achieved_at.isoformat() if a.achieved_at else None,
                }
                for a in new_achievements
            ],
            "count": len(new_achievements),
        },
    }


@router.get("/child/{child_id}/progress")
async def get_achievement_progress(
    child_id: str,
    db: Session = Depends(get_db),
):
    """
    获取成就进度
    
    返回孩子已获得和未获得的成就情况
    """
    service = AchievementService(db)
    
    # 获取所有成就类型
    all_types = service.get_achievement_types()
    
    # 获取已获得的成就
    achieved = service.get_by_child(child_id)
    achieved_types = {a.achievement_type for a in achieved}
    
    # 计算进度
    progress = []
    for achievement_type in all_types:
        progress.append({
            "type": achievement_type["type"],
            "name": achievement_type["name"],
            "description": achievement_type["description"],
            "icon": achievement_type["icon"],
            "achieved": achievement_type["type"] in achieved_types,
        })
    
    return {
        "status": "success",
        "data": {
            "child_id": child_id,
            "total": len(all_types),
            "achieved_count": len(achieved_types),
            "progress": progress,
        },
    }
