from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.core.database import Base

# 用户表
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # creator / admin / user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 选题表
class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    tags = Column(JSON, default=list)
    status = Column(String(20), default="draft")  # draft / in_progress / completed
    priority = Column(Integer, default=0)
    created_by = Column(String(100), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 脚本表
class Script(Base):
    __tablename__ = "scripts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, default="")
    topic_id = Column(Integer, default=0)
    script_type = Column(String(50), default="口播")  # 口播 / 分镜 / Vlog
    duration = Column(Integer, default=0)  # 秒
    status = Column(String(20), default="draft")
    created_by = Column(String(100), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 对标视频表
class BenchmarkVideo(Base):
    __tablename__ = "benchmark_videos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), default="")
    platform = Column(String(50), default="抖音")  # 抖音 / 小红书 / 视频号 / 快手
    author = Column(String(200), default="")
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    breakdown = Column(Text, default="")  # 拆解内容
    tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 拍摄素材表
class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(500), nullable=False)
    file_path = Column(String(1000), default="")
    file_type = Column(String(50), default="")  # video / image / audio / document
    file_size = Column(Integer, default=0)
    duration = Column(Float, default=0)  # 视频时长（秒）
    tags = Column(JSON, default=list)
    description = Column(Text, default="")
    uploaded_by = Column(String(100), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 成片表
class FinalVideo(Base):
    __tablename__ = "final_videos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    filename = Column(String(500), default="")
    file_path = Column(String(1000), default="")
    script_id = Column(Integer, default=0)
    duration = Column(Float, default=0)
    resolution = Column(String(50), default="1080x1920")
    status = Column(String(20), default="completed")  # editing / completed / published
    created_by = Column(String(100), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# AI生成记录表
class AIGeneration(Base):
    __tablename__ = "ai_generations"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, default="")
    result = Column(Text, default="")
    gen_type = Column(String(50), default="video")  # video / image / script / text
    model = Column(String(100), default="")
    status = Column(String(20), default="completed")
    created_by = Column(String(100), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 发布记录表
class Publishing(Base):
    __tablename__ = "publishing"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, default=0)
    title = Column(String(500), default="")
    platform = Column(String(50), default="抖音")  # 抖音 / 小红书 / 视频号 / 快手
    account = Column(String(200), default="")
    status = Column(String(20), default="published")  # pending / publishing / published / failed
    publish_url = Column(String(1000), default="")
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(100), default="")

# 直播复盘表
class LiveReview(Base):
    __tablename__ = "live_reviews"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), default="")
    anchor_name = Column(String(200), default="")
    account = Column(String(200), default="")
    platform = Column(String(50), default="抖音")
    gmv = Column(Float, default=0)  # 总GMV（元）
    orders = Column(Integer, default=0)  # 成交单数
    avg_price = Column(Float, default=0)  # 客单价
    viewers = Column(Integer, default=0)  # 观看人数
    uv = Column(Integer, default=0)  # UV值
    avg_duration = Column(Float, default=0)  # 人均停留（秒）
    interaction_rate = Column(Float, default=0)  # 互动率
    conversion_rate = Column(Float, default=0)  # 转化率
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    report = Column(Text, default="")  # 复盘报告
    remark = Column(Text, default="")  # 备注
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 投放数据表
class AdDashboard(Base):
    __tablename__ = "ad_dashboards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), default="")
    platform = Column(String(50), default="抖音")  # 抖音 / 小红书 / 视频号 / 快手
    account = Column(String(200), default="")
    anchor_name = Column(String(200), default="")
    total_cost = Column(Float, default=0)  # 总消耗（元）
    impressions = Column(Integer, default=0)  # 曝光量
    clicks = Column(Integer, default=0)  # 点击量
    ctr = Column(Float, default=0)  # 点击率
    cpc = Column(Float, default=0)  # 平均点击成本
    conversions = Column(Integer, default=0)  # 转化数
    conversion_cost = Column(Float, default=0)  # 转化成本
    roi = Column(Float, default=0)  # ROI
    video_name = Column(String(500), default="")  # 引流视频名称
    video_cost = Column(Float, default=0)  # 引流视频消耗
    date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 主播表
class Anchor(Base):
    __tablename__ = "anchors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    account = Column(String(200), default="")
    platform = Column(String(50), default="抖音")
    total_gmv = Column(Float, default=0)
    total_uv = Column(Integer, default=0)
    live_count = Column(Integer, default=0)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 系统配置表
class SystemConfig(Base):
    __tablename__ = "system_configs"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True)
    value = Column(Text, default="")
    description = Column(String(500), default="")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 操作日志表（与前端操作记录中心对应）
class OperationLog(Base):
    __tablename__ = "operation_logs"
    id = Column(Integer, primary_key=True, index=True)
    log_type = Column(String(50), default="access")  # access / cache / generate / archive
    username = Column(String(100), default="访客")
    user_role = Column(String(20), default="访客")  # creator / admin / user / guest
    page = Column(String(100), default="")
    page_name = Column(String(200), default="")
    action = Column(String(200), default="")  # 操作描述
    target_name = Column(String(500), default="")  # 操作对象名称
    target_type = Column(String(50), default="")  # file / script / video / report
    extra_data = Column(JSON, default=dict)  # 额外数据
    user_agent = Column(String(500), default="")
    screen_size = Column(String(50), default="")
    ip_address = Column(String(50), default="")
    status = Column(String(20), default="success")  # success / failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
