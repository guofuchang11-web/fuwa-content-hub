"""
福娃内容中台系统 - 后端API服务
技术栈：FastAPI + SQLAlchemy + SQLite/PostgreSQL
"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import init_db, engine
from app.api import auth, data, files, ai, dashboard, logs, sync

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="福娃内容中台系统后端API，覆盖内容生产全流程管理、数据大屏、AI智能、文件管理等功能",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    print(f"🚀 {settings.APP_NAME} 启动中...")
    print(f"📦 版本: {settings.APP_VERSION}")
    print(f"🔧 调试模式: {settings.DEBUG}")
    print(f"💾 数据库: {settings.DATABASE_URL}")
    print(f"📁 上传目录: {settings.UPLOAD_DIR}")
    
    # 确保上传目录存在
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs("./data", exist_ok=True)
    
    # 初始化数据库
    init_db()
    
    print("✅ 数据库初始化完成")
    print("✅ 服务启动成功")
    print(f"🌐 API文档: http://{settings.HOST}:{settings.PORT}/docs")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    print("👋 服务正在关闭...")
    engine.dispose()
    print("✅ 资源已清理")

# 根路由
@app.get("/", tags=["系统"])
async def root():
    """根路径，返回系统信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "api_endpoints": {
            "auth": "/api/auth",
            "data": "/api/data",
            "files": "/api/files",
            "ai": "/api/ai",
            "dashboard": "/api/dashboard",
            "logs": "/api/logs",
            "sync": "/api/sync"
        }
    }

# 健康检查
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "version": settings.APP_VERSION
    }

# 注册路由
app.include_router(auth.router)
app.include_router(data.router)
app.include_router(files.router)
app.include_router(ai.router)
app.include_router(dashboard.router)
app.include_router(logs.router)
app.include_router(sync.router)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    print(f"❌ 未处理异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "服务器内部错误",
            "detail": str(exc) if settings.DEBUG else None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
