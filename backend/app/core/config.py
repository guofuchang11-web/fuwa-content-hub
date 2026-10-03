import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 应用配置
    APP_NAME: str = "福娃内容中台系统 - 后端API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 数据库配置（默认SQLite，可切换MySQL/PostgreSQL）
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/content_hub.db")
    
    # JWT认证配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "youguo-content-hub-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("TOKEN_EXPIRE", "1440"))  # 24小时
    
    # 文件上传配置
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", str(8880 * 1024 * 1024 * 1024)))  # 8880TB
    
    # AI大模型配置
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "deepseek")  # deepseek / minimax / kimi
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    MINIMAX_API_KEY: str = os.getenv("MINIMAX_API_KEY", "")
    KIMI_API_KEY: str = os.getenv("KIMI_API_KEY", "")
    
    # CORS配置
    CORS_ORIGINS: list = ["*"]

settings = Settings()
