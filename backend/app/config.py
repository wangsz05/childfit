"""
ChildFit 配置管理
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "ChildFit"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://childfit:ChildFit%402026@localhost:3306/childfit"
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PREFIX: str = "childfit"
    
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天
    
    # CORS 配置
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # 天气 API 配置 (WeatherCN)
    WEATHER_API_KEY: str = "0LaQKA2AUmvSUuLO3B1Kj5dJiJiINPPS"
    WEATHER_BASE_URL: str = "https://openapi.weathercn.com"
    WEATHER_DEFAULT_CITY: str = "南京"
    
    # 存储配置
    COS_BUCKET: str = ""
    COS_REGION: str = "ap-guangzhou"
    COS_SECRET_ID: str = ""
    COS_SECRET_KEY: str = ""
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
