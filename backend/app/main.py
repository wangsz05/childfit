"""
ChildFit - 孩子运动健康推荐系统
后端 API 入口
"""
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.api import users, children, weather, recommendations, checkins, achievements, schedules

# 配置日志
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="ChildFit API",
    description="🎗️ 孩子运动健康推荐系统 - 根据天气、作息、年龄段智能推荐活动",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 配置 (生产环境需要限制)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(children.router, prefix="/api/children", tags=["孩子档案"])
app.include_router(weather.router, prefix="/api/weather", tags=["天气查询"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["智能推荐"])
app.include_router(checkins.router, prefix="/api/checkins", tags=["打卡记录"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["成就系统"])
app.include_router(schedules.router, prefix="/api", tags=["作息时间表"])


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("🚀 ChildFit 后端服务启动中...")
    # 创建数据库表 (生产环境建议用 Alembic 迁移)
    # 注意：如果数据库未连接，会记录警告但继续启动
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 数据库表初始化完成")
    except Exception as e:
        logger.warning(f"⚠️ 数据库初始化失败 (请检查数据库连接): {e}")
        logger.warning("API 仍可启动，但数据库相关功能将不可用")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("👋 ChildFit 后端服务关闭中...")


@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "message": "🎗️ ChildFit API v2.0 - 孩子运动健康推荐系统",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "python": "3.12",
        "fastapi": "0.109.0"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("启动 ChildFit 后端服务...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
