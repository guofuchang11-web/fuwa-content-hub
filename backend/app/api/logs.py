"""
操作日志API - 与前端操作记录中心对应
支持访问记录、上传缓存、生成记录、内容存档的查询和统计
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.models import OperationLog

router = APIRouter(prefix="/api/logs", tags=["操作日志"])

# 记录操作日志
def log_operation(db: Session, log_type: str, username: str = "访客", 
                  user_role: str = "访客", page: str = "", page_name: str = "",
                  action: str = "", target_name: str = "", target_type: str = "",
                  extra_data: dict = None, user_agent: str = "", 
                  screen_size: str = "", status: str = "success"):
    """记录操作日志"""
    try:
        log = OperationLog(
            log_type=log_type,
            username=username,
            user_role=user_role,
            page=page,
            page_name=page_name,
            action=action,
            target_name=target_name,
            target_type=target_type,
            extra_data=extra_data or {},
            user_agent=user_agent,
            screen_size=screen_size,
            status=status
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        print(f"记录操作日志失败: {e}")
        return None

# 获取操作日志列表
@router.get("/")
def get_logs(
    log_type: Optional[str] = Query(None, description="access/cache/generate/archive"),
    username: Optional[str] = Query(None, description="用户名筛选"),
    page: Optional[str] = Query(None, description="页面筛选"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """获取操作日志列表，支持多条件筛选"""
    query = db.query(OperationLog)
    
    if log_type:
        query = query.filter(OperationLog.log_type == log_type)
    if username:
        query = query.filter(OperationLog.username.contains(username))
    if page:
        query = query.filter(OperationLog.page == page)
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(OperationLog.created_at >= start)
        except:
            pass
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(OperationLog.created_at < end)
        except:
            pass
    
    total = query.count()
    logs = query.order_by(desc(OperationLog.created_at)).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": [
            {
                "id": log.id,
                "log_type": log.log_type,
                "username": log.username,
                "user_role": log.user_role,
                "page": log.page,
                "page_name": log.page_name,
                "action": log.action,
                "target_name": log.target_name,
                "target_type": log.target_type,
                "extra_data": log.extra_data,
                "user_agent": log.user_agent,
                "screen_size": log.screen_size,
                "status": log.status,
                "created_at": log.created_at.isoformat() if log.created_at else None
            }
            for log in logs
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }

# 获取日志统计
@router.get("/stats")
def get_log_stats(
    time_range: str = Query("day", description="day/week/month/90days/all"),
    db: Session = Depends(get_db)
):
    """获取操作日志统计数据"""
    now = datetime.now()
    
    query = db.query(OperationLog)
    if time_range == "day":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(OperationLog.created_at >= start)
    elif time_range == "week":
        start = now - timedelta(days=7)
        query = query.filter(OperationLog.created_at >= start)
    elif time_range == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(OperationLog.created_at >= start)
    elif time_range == "90days":
        start = now - timedelta(days=90)
        query = query.filter(OperationLog.created_at >= start)
    
    # 按类型统计
    type_stats = {}
    for log_type in ["access", "cache", "generate", "archive"]:
        count = query.filter(OperationLog.log_type == log_type).count()
        type_stats[log_type] = count
    
    # 按用户统计（Top10）
    user_stats = db.query(
        OperationLog.username,
        func.count(OperationLog.id).label("count")
    ).group_by(OperationLog.username).order_by(desc("count")).limit(10).all()
    
    # 按页面统计（Top10）
    page_stats = db.query(
        OperationLog.page,
        OperationLog.page_name,
        func.count(OperationLog.id).label("count")
    ).group_by(OperationLog.page, OperationLog.page_name).order_by(desc("count")).limit(10).all()
    
    return {
        "success": True,
        "time_range": time_range,
        "total": query.count(),
        "by_type": type_stats,
        "by_user": [{"username": u, "count": c} for u, c in user_stats],
        "by_page": [{"page": p, "page_name": pn, "count": c} for p, pn, c in page_stats]
    }

# 清空日志（需要管理员权限）
@router.delete("/clear")
def clear_logs(
    log_type: Optional[str] = Query(None, description="指定类型清空，不填则清空全部"),
    db: Session = Depends(get_db)
):
    """清空操作日志"""
    try:
        query = db.query(OperationLog)
        if log_type:
            query = query.filter(OperationLog.log_type == log_type)
        count = query.count()
        query.delete(synchronize_session=False)
        db.commit()
        return {
            "success": True,
            "message": f"已清空 {count} 条日志",
            "cleared_count": count
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": "清空失败",
            "detail": str(e)
        }
