from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import (
    Topic, Script, BenchmarkVideo, Material, FinalVideo,
    AIGeneration, Publishing, LiveReview, AdDashboard, Anchor
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/data", tags=["数据管理"])

# 通用CRUD函数
def create_item(db: Session, model, data: dict):
    item = model(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_items(db: Session, model, skip: int = 0, limit: int = 100, filters: dict = None):
    query = db.query(model)
    if filters:
        for key, value in filters.items():
            if value is not None:
                query = query.filter(getattr(model, key) == value)
    return query.order_by(model.id.desc()).offset(skip).limit(limit).all()

def get_item(db: Session, model, item_id: int):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="记录不存在")
    return item

def update_item(db: Session, model, item_id: int, data: dict):
    item = get_item(db, model, item_id)
    for key, value in data.items():
        if value is not None:
            setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, model, item_id: int):
    item = get_item(db, model, item_id)
    db.delete(item)
    db.commit()
    return {"success": True, "message": "删除成功"}

# ============ 选题 ============
class TopicCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    tags: Optional[list] = []
    status: Optional[str] = "draft"
    priority: Optional[int] = 0

@router.get("/topics")
def list_topics(skip: int = 0, limit: int = 100, status: Optional[str] = None, db: Session = Depends(get_db)):
    filters = {"status": status} if status else None
    return {"success": True, "data": get_items(db, Topic, skip, limit, filters), "total": db.query(Topic).count()}

@router.post("/topics")
def create_topic(req: TopicCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    data = req.dict()
    data["created_by"] = user.username
    return {"success": True, "data": create_item(db, Topic, data)}

@router.get("/topics/{item_id}")
def get_topic(item_id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": get_item(db, Topic, item_id)}

@router.put("/topics/{item_id}")
def update_topic(item_id: int, req: TopicCreate, db: Session = Depends(get_db)):
    return {"success": True, "data": update_item(db, Topic, item_id, req.dict())}

@router.delete("/topics/{item_id}")
def delete_topic(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return delete_item(db, Topic, item_id)

# ============ 脚本 ============
class ScriptCreate(BaseModel):
    title: str
    content: Optional[str] = ""
    topic_id: Optional[int] = 0
    script_type: Optional[str] = "口播"
    duration: Optional[int] = 0
    status: Optional[str] = "draft"

@router.get("/scripts")
def list_scripts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return {"success": True, "data": get_items(db, Script, skip, limit), "total": db.query(Script).count()}

@router.post("/scripts")
def create_script(req: ScriptCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    data = req.dict()
    data["created_by"] = user.username
    return {"success": True, "data": create_item(db, Script, data)}

@router.get("/scripts/{item_id}")
def get_script(item_id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": get_item(db, Script, item_id)}

@router.put("/scripts/{item_id}")
def update_script(item_id: int, req: ScriptCreate, db: Session = Depends(get_db)):
    return {"success": True, "data": update_item(db, Script, item_id, req.dict())}

@router.delete("/scripts/{item_id}")
def delete_script(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return delete_item(db, Script, item_id)

# ============ 直播复盘 ============
class LiveReviewCreate(BaseModel):
    title: Optional[str] = ""
    anchor_name: Optional[str] = ""
    account: Optional[str] = ""
    platform: Optional[str] = "抖音"
    gmv: Optional[float] = 0
    orders: Optional[int] = 0
    avg_price: Optional[float] = 0
    viewers: Optional[int] = 0
    uv: Optional[int] = 0
    avg_duration: Optional[float] = 0
    interaction_rate: Optional[float] = 0
    conversion_rate: Optional[float] = 0
    report: Optional[str] = ""
    remark: Optional[str] = ""

@router.get("/live-reviews")
def list_live_reviews(skip: int = 0, limit: int = 100, platform: Optional[str] = None, db: Session = Depends(get_db)):
    filters = {"platform": platform} if platform else None
    return {"success": True, "data": get_items(db, LiveReview, skip, limit, filters), "total": db.query(LiveReview).count()}

@router.post("/live-reviews")
def create_live_review(req: LiveReviewCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return {"success": True, "data": create_item(db, LiveReview, req.dict())}

@router.get("/live-reviews/{item_id}")
def get_live_review(item_id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": get_item(db, LiveReview, item_id)}

@router.put("/live-reviews/{item_id}")
def update_live_review(item_id: int, req: LiveReviewCreate, db: Session = Depends(get_db)):
    return {"success": True, "data": update_item(db, LiveReview, item_id, req.dict())}

@router.delete("/live-reviews/{item_id}")
def delete_live_review(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return delete_item(db, LiveReview, item_id)

# ============ 投放数据 ============
class AdDashboardCreate(BaseModel):
    title: Optional[str] = ""
    platform: Optional[str] = "抖音"
    account: Optional[str] = ""
    anchor_name: Optional[str] = ""
    total_cost: Optional[float] = 0
    impressions: Optional[int] = 0
    clicks: Optional[int] = 0
    ctr: Optional[float] = 0
    cpc: Optional[float] = 0
    conversions: Optional[int] = 0
    conversion_cost: Optional[float] = 0
    roi: Optional[float] = 0
    video_name: Optional[str] = ""
    video_cost: Optional[float] = 0

@router.get("/ad-dashboards")
def list_ad_dashboards(skip: int = 0, limit: int = 100, platform: Optional[str] = None, db: Session = Depends(get_db)):
    filters = {"platform": platform} if platform else None
    return {"success": True, "data": get_items(db, AdDashboard, skip, limit, filters), "total": db.query(AdDashboard).count()}

@router.post("/ad-dashboards")
def create_ad_dashboard(req: AdDashboardCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return {"success": True, "data": create_item(db, AdDashboard, req.dict())}

@router.get("/ad-dashboards/{item_id}")
def get_ad_dashboard(item_id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": get_item(db, AdDashboard, item_id)}

@router.put("/ad-dashboards/{item_id}")
def update_ad_dashboard(item_id: int, req: AdDashboardCreate, db: Session = Depends(get_db)):
    return {"success": True, "data": update_item(db, AdDashboard, item_id, req.dict())}

@router.delete("/ad-dashboards/{item_id}")
def delete_ad_dashboard(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return delete_item(db, AdDashboard, item_id)

# ============ 主播管理 ============
class AnchorCreate(BaseModel):
    name: str
    account: Optional[str] = ""
    platform: Optional[str] = "抖音"
    status: Optional[str] = "active"

@router.get("/anchors")
def list_anchors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return {"success": True, "data": get_items(db, Anchor, skip, limit), "total": db.query(Anchor).count()}

@router.post("/anchors")
def create_anchor(req: AnchorCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return {"success": True, "data": create_item(db, Anchor, req.dict())}

@router.get("/anchors/{item_id}")
def get_anchor(item_id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": get_item(db, Anchor, item_id)}

@router.put("/anchors/{item_id}")
def update_anchor(item_id: int, req: AnchorCreate, db: Session = Depends(get_db)):
    return {"success": True, "data": update_item(db, Anchor, item_id, req.dict())}

@router.delete("/anchors/{item_id}")
def delete_anchor(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return delete_item(db, Anchor, item_id)

# ============ 一键清空所有数据（需要创建者权限） ============
@router.post("/clear-all")
def clear_all_data(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role not in ["creator", "admin"]:
        raise HTTPException(status_code=403, detail="需要创建者权限才能清空数据")
    
    models = [Topic, Script, BenchmarkVideo, Material, FinalVideo, AIGeneration, Publishing, LiveReview, AdDashboard]
    counts = {}
    for model in models:
        count = db.query(model).count()
        counts[model.__tablename__] = count
        db.query(model).delete()
    db.commit()
    
    return {
        "success": True,
        "message": "所有数据已清空",
        "cleared": counts
    }
