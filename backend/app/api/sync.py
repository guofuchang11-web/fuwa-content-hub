"""
数据同步API
- 上传所有业务数据到云端
- 从云端下载所有业务数据
- 同步状态查询
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import (
    Topic, Script, BenchmarkVideo, Material, FinalVideo,
    AIGeneration, Publishing, LiveReview, AdDashboard, Anchor,
    SystemConfig
)
from app.services.auth_service import get_current_user
import json
from datetime import datetime

router = APIRouter(prefix="/api/sync", tags=["数据同步"])

class SyncUploadRequest(BaseModel):
    data: dict
    sync_time: str = ""
    device_info: str = ""

class SyncStatusResponse(BaseModel):
    has_data: bool
    last_sync_time: str = ""
    total_records: int = 0
    user_id: int = 0

# 业务数据模块列表
SYNC_MODULES = {
    "topics": Topic,
    "scripts": Script,
    "benchmark_videos": BenchmarkVideo,
    "materials": Material,
    "final_videos": FinalVideo,
    "ai_generations": AIGeneration,
    "publishing": Publishing,
    "live_reviews": LiveReview,
    "ad_dashboards": AdDashboard,
    "anchors": Anchor,
}

@router.post("/upload")
async def upload_sync(
    req: SyncUploadRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    上传所有业务数据到云端
    将前端传来的所有数据保存到系统配置表中
    """
    try:
        config_key = f"sync_data_{user.id}"
        sync_config = db.query(SystemConfig).filter(
            SystemConfig.key == config_key
        ).first()
        
        sync_data = {
            "user_id": user.id,
            "username": user.username,
            "data": req.data,
            "sync_time": req.sync_time or datetime.now().isoformat(),
            "device_info": req.device_info,
            "total_records": sum(len(v) for v in req.data.values() if isinstance(v, list))
        }
        
        if sync_config:
            sync_config.value = json.dumps(sync_data, ensure_ascii=False)
            sync_config.updated_at = datetime.now()
        else:
            sync_config = SystemConfig(
                key=config_key,
                value=json.dumps(sync_data, ensure_ascii=False),
                description=f"用户{user.username}的数据同步备份"
            )
            db.add(sync_config)
        
        db.commit()
        
        return {
            "success": True,
            "message": "数据上传成功",
            "sync_time": sync_data["sync_time"],
            "total_records": sync_data["total_records"],
            "user_id": user.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

@router.get("/download")
async def download_sync(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    从云端下载所有业务数据
    """
    try:
        config_key = f"sync_data_{user.id}"
        sync_config = db.query(SystemConfig).filter(
            SystemConfig.key == config_key
        ).first()
        
        if not sync_config:
            return {
                "success": True,
                "has_data": False,
                "message": "云端暂无数据"
            }
        
        sync_data = json.loads(sync_config.value)
        
        return {
            "success": True,
            "has_data": True,
            "data": sync_data.get("data", {}),
            "sync_time": sync_data.get("sync_time", ""),
            "total_records": sync_data.get("total_records", 0),
            "username": sync_data.get("username", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")

@router.get("/status")
async def sync_status(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    查询同步状态
    """
    try:
        config_key = f"sync_data_{user.id}"
        sync_config = db.query(SystemConfig).filter(
            SystemConfig.key == config_key
        ).first()
        
        if not sync_config:
            return {
                "success": True,
                "has_data": False,
                "last_sync_time": "",
                "total_records": 0,
                "user_id": user.id,
                "username": user.username
            }
        
        sync_data = json.loads(sync_config.value)
        
        return {
            "success": True,
            "has_data": True,
            "last_sync_time": sync_data.get("sync_time", ""),
            "total_records": sync_data.get("total_records", 0),
            "user_id": user.id,
            "username": user.username,
            "device_info": sync_data.get("device_info", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询状态失败: {str(e)}")

@router.delete("/clear")
async def clear_sync(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    清空云端同步数据
    """
    try:
        config_key = f"sync_data_{user.id}"
        sync_config = db.query(SystemConfig).filter(
            SystemConfig.key == config_key
        ).first()
        
        if sync_config:
            db.delete(sync_config)
            db.commit()
        
        return {
            "success": True,
            "message": "云端数据已清空"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空失败: {str(e)}")
