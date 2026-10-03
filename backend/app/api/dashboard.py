from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.models import (
    LiveReview, AdDashboard, Material, FinalVideo, AIGeneration,
    Publishing, Anchor, Topic, Script, BenchmarkVideo
)

router = APIRouter(prefix="/api/dashboard", tags=["数据大屏"])

# 时间范围过滤
def filter_by_time(query, model, time_field, time_range: str):
    now = datetime.now()
    if time_range == "day":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return query.filter(time_field >= start)
    elif time_range == "week":
        start = now - timedelta(days=7)
        return query.filter(time_field >= start)
    elif time_range == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return query.filter(time_field >= start)
    elif time_range == "90days":
        start = now - timedelta(days=90)
        return query.filter(time_field >= start)
    return query

# 数据大屏总览
@router.get("/overview")
def get_overview(
    time_range: str = Query("day", description="day/week/month/90days"),
    db: Session = Depends(get_db)
):
    # 1. 总GMV（按平台细分）
    gmv_query = db.query(
        func.coalesce(func.sum(LiveReview.gmv), 0).label("total"),
        func.coalesce(func.sum(case((LiveReview.platform == "视频号", LiveReview.gmv), else_=0)), 0).label("video号"),
        func.coalesce(func.sum(case((LiveReview.platform == "抖音", LiveReview.gmv), else_=0)), 0).label("douyin"),
        func.coalesce(func.sum(case((LiveReview.platform == "小红书", LiveReview.gmv), else_=0)), 0).label("xiaohongshu"),
        func.coalesce(func.sum(case((LiveReview.platform == "快手", LiveReview.gmv), else_=0)), 0).label("kuaishou")
    )
    gmv_query = filter_by_time(gmv_query, LiveReview, LiveReview.created_at, time_range)
    gmv_data = gmv_query.first()
    
    # 2. 总消耗（按平台细分）
    cost_query = db.query(
        func.coalesce(func.sum(AdDashboard.total_cost), 0).label("total"),
        func.coalesce(func.sum(case((AdDashboard.platform == "视频号", AdDashboard.total_cost), else_=0)), 0).label("video号"),
        func.coalesce(func.sum(case((AdDashboard.platform == "抖音", AdDashboard.total_cost), else_=0)), 0).label("douyin"),
        func.coalesce(func.sum(case((AdDashboard.platform == "小红书", AdDashboard.total_cost), else_=0)), 0).label("xiaohongshu"),
        func.coalesce(func.sum(case((AdDashboard.platform == "快手", AdDashboard.total_cost), else_=0)), 0).label("kuaishou")
    )
    cost_query = filter_by_time(cost_query, AdDashboard, AdDashboard.created_at, time_range)
    cost_data = cost_query.first()
    
    # 3. 内容生产统计
    mat_count = filter_by_time(db.query(func.count(Material.id)), Material, Material.created_at, time_range).scalar() or 0
    ai_count = filter_by_time(db.query(func.count(AIGeneration.id)), AIGeneration, AIGeneration.created_at, time_range).scalar() or 0
    edit_count = filter_by_time(db.query(func.count(FinalVideo.id)), FinalVideo, FinalVideo.created_at, time_range).scalar() or 0
    pub_count = filter_by_time(db.query(func.count(Publishing.id)), Publishing, Publishing.published_at, time_range).scalar() or 0
    
    # 发布平台分布
    pub_platforms = db.query(
        Publishing.platform,
        func.count(Publishing.id).label("count")
    ).group_by(Publishing.platform).all()
    platform_dist = {"抖音": 0, "视频号": 0, "快手": 0, "小红书": 0}
    for p, c in pub_platforms:
        if p in platform_dist:
            platform_dist[p] = c
    
    content_total = mat_count + ai_count + edit_count + pub_count
    
    # 4. 视频总曝光（按平台细分）
    exposure_query = db.query(
        func.coalesce(func.sum(AdDashboard.impressions), 0).label("total"),
        func.coalesce(func.sum(case((AdDashboard.platform == "视频号", AdDashboard.impressions), else_=0)), 0).label("video号"),
        func.coalesce(func.sum(case((AdDashboard.platform == "抖音", AdDashboard.impressions), else_=0)), 0).label("douyin"),
        func.coalesce(func.sum(case((AdDashboard.platform == "小红书", AdDashboard.impressions), else_=0)), 0).label("xiaohongshu"),
        func.coalesce(func.sum(case((AdDashboard.platform == "快手", AdDashboard.impressions), else_=0)), 0).label("kuaishou")
    )
    exposure_query = filter_by_time(exposure_query, AdDashboard, AdDashboard.created_at, time_range)
    exposure_data = exposure_query.first()
    
    return {
        "success": True,
        "time_range": time_range,
        "total_gmv": {
            "total": round(float(gmv_data.total), 2),
            "platforms": {
                "视频号": round(float(gmv_data.video号), 2),
                "抖音": round(float(gmv_data.douyin), 2),
                "小红书": round(float(gmv_data.xiaohongshu), 2),
                "快手": round(float(gmv_data.kuaishou), 2)
            }
        },
        "total_cost": {
            "total": round(float(cost_data.total), 2),
            "platforms": {
                "视频号": round(float(cost_data.video号), 2),
                "抖音": round(float(cost_data.douyin), 2),
                "小红书": round(float(cost_data.xiaohongshu), 2),
                "快手": round(float(cost_data.kuaishou), 2)
            }
        },
        "content_production": {
            "total": content_total,
            "materials": mat_count,
            "ai_generation": ai_count,
            "editing": edit_count,
            "publishing": pub_count,
            "platform_dist": platform_dist
        },
        "total_exposure": {
            "total": int(exposure_data.total),
            "platforms": {
                "视频号": int(exposure_data.video号),
                "抖音": int(exposure_data.douyin),
                "小红书": int(exposure_data.xiaohongshu),
                "快手": int(exposure_data.kuaishou)
            }
        }
    }

# 主播GMV排行榜（Top10）
@router.get("/anchor-ranking")
def get_anchor_ranking(
    time_range: str = Query("day", description="day/week/month/90days"),
    db: Session = Depends(get_db)
):
    query = db.query(
        LiveReview.anchor_name,
        func.coalesce(func.sum(LiveReview.gmv), 0).label("gmv"),
        func.coalesce(func.sum(LiveReview.uv), 0).label("uv"),
        func.count(LiveReview.id).label("live_count")
    ).group_by(LiveReview.anchor_name)
    
    query = filter_by_time(query, LiveReview, LiveReview.created_at, time_range)
    results = query.order_by(func.sum(LiveReview.gmv).desc()).limit(10).all()
    
    anchors = []
    for name, gmv, uv, count in results:
        if name:
            anchors.append({
                "name": name,
                "gmv": round(float(gmv), 2),
                "uv": int(uv),
                "live_count": int(count)
            })
    
    return {"success": True, "data": anchors}

# 引流视频排行榜（Top10，按消耗降序）
@router.get("/traffic-videos")
def get_traffic_videos(
    time_range: str = Query("day", description="day/week/month/90days"),
    db: Session = Depends(get_db)
):
    query = db.query(
        AdDashboard.video_name,
        func.coalesce(func.sum(AdDashboard.video_cost), 0).label("cost")
    ).filter(AdDashboard.video_name != "").group_by(AdDashboard.video_name)
    
    query = filter_by_time(query, AdDashboard, AdDashboard.created_at, time_range)
    results = query.order_by(func.sum(AdDashboard.video_cost).desc()).limit(10).all()
    
    videos = []
    for name, cost in results:
        if name:
            videos.append({
                "title": name,
                "cost": round(float(cost), 2)
            })
    
    return {"success": True, "data": videos}

# 视频曝光排行榜（Top10，按曝光量降序）
@router.get("/exposure-videos")
def get_exposure_videos(
    time_range: str = Query("day", description="day/week/month/90days"),
    db: Session = Depends(get_db)
):
    query = db.query(
        AdDashboard.video_name,
        func.coalesce(func.sum(AdDashboard.impressions), 0).label("impressions")
    ).filter(AdDashboard.video_name != "").group_by(AdDashboard.video_name)
    
    query = filter_by_time(query, AdDashboard, AdDashboard.created_at, time_range)
    results = query.order_by(func.sum(AdDashboard.impressions).desc()).limit(10).all()
    
    videos = []
    for name, impressions in results:
        if name:
            videos.append({
                "title": name,
                "impressions": int(impressions)
            })
    
    return {"success": True, "data": videos}

# 系统统计（所有业务板块数据量）
@router.get("/system-stats")
def get_system_stats(db: Session = Depends(get_db)):
    return {
        "success": True,
        "data": {
            "topics": db.query(func.count(Topic.id)).scalar() or 0,
            "scripts": db.query(func.count(Script.id)).scalar() or 0,
            "benchmark_videos": db.query(func.count(BenchmarkVideo.id)).scalar() or 0,
            "materials": db.query(func.count(Material.id)).scalar() or 0,
            "final_videos": db.query(func.count(FinalVideo.id)).scalar() or 0,
            "ai_generations": db.query(func.count(AIGeneration.id)).scalar() or 0,
            "publishing": db.query(func.count(Publishing.id)).scalar() or 0,
            "live_reviews": db.query(func.count(LiveReview.id)).scalar() or 0,
            "ad_dashboards": db.query(func.count(AdDashboard.id)).scalar() or 0,
            "anchors": db.query(func.count(Anchor.id)).scalar() or 0
        }
    }
