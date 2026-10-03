"""
认证与权限管理API
- 主创建者（creator）：只有一个，系统最高权限，可授权/撤销管理者
- 管理者（admin）：需主创建者授权，可管理用户和数据
- 普通用户（user）：基础权限
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from typing import Optional, List
from app.core.database import get_db
from app.core.config import settings
from app.models.models import User
from app.services.auth_service import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["认证与权限"])

# ==================== 请求模型 ====================

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"  # 普通注册只能是user

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: Optional[str] = None
    class Config:
        from_attributes = True

class GrantAdminRequest(BaseModel):
    user_id: int
    note: Optional[str] = ""

class RevokeAdminRequest(BaseModel):
    user_id: int
    reason: Optional[str] = ""

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

# ==================== 权限验证装饰器 ====================

def require_creator(current_user: User = Depends(get_current_user)):
    """验证是否为主创建者"""
    if current_user.role != "creator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要主创建者权限"
        )
    return current_user

def require_admin(current_user: User = Depends(get_current_user)):
    """验证是否为管理者或创建者"""
    if current_user.role not in ["creator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理者权限"
        )
    return current_user

# ==================== 认证接口 ====================

# 普通用户注册（只能注册user角色）
@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """普通用户注册，角色固定为user"""
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    role = "user"
    
    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": "注册成功",
        "user": {"id": user.id, "username": user.username, "role": user.role}
    }

# 登录
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录，返回JWT Token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "role": user.role}
    }

# 获取当前用户信息
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return {
        "success": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None
        }
    }

# 修改密码
@router.post("/change-password")
def change_password(
    req: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改当前用户密码"""
    if not verify_password(req.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="原密码错误")
    
    current_user.password_hash = hash_password(req.new_password)
    db.commit()
    
    return {"success": True, "message": "密码修改成功"}

# ==================== 主创建者接口 ====================

# 初始化创建者（首次使用，只能调用一次）
@router.post("/init-creator")
def init_creator(req: RegisterRequest, db: Session = Depends(get_db)):
    """
    初始化主创建者（系统首次使用时调用）
    - 主创建者全局唯一，只能有一个
    - 已存在创建者时调用会失败
    """
    existing_creator = db.query(User).filter(User.role == "creator").first()
    if existing_creator:
        raise HTTPException(status_code=400, detail="主创建者已存在，全局唯一，无需重复初始化")
    
    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        role="creator"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": "主创建者初始化成功（全局唯一）",
        "user": {"id": user.id, "username": user.username, "role": user.role}
    }

# 检查是否已初始化创建者
@router.get("/has-creator")
def has_creator(db: Session = Depends(get_db)):
    """检查系统是否已初始化主创建者"""
    creator = db.query(User).filter(User.role == "creator").first()
    return {
        "success": True,
        "has_creator": creator is not None,
        "creator_username": creator.username if creator else None
    }

# 主创建者授权管理者
@router.post("/grant-admin")
def grant_admin(
    req: GrantAdminRequest,
    current_user: User = Depends(require_creator),
    db: Session = Depends(get_db)
):
    """
    主创建者授权用户为管理者
    - 只有主创建者可以调用
    - 被授权用户角色变为admin
    """
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.role == "creator":
        raise HTTPException(status_code=400, detail="主创建者无需重复授权")
    
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="该用户已是管理者")
    
    old_role = user.role
    user.role = "admin"
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": f"已授权用户「{user.username}」为管理者",
        "user": {"id": user.id, "username": user.username, "role": user.role, "old_role": old_role},
        "granted_by": current_user.username,
        "note": req.note
    }

# 主创建者撤销管理者权限
@router.post("/revoke-admin")
def revoke_admin(
    req: RevokeAdminRequest,
    current_user: User = Depends(require_creator),
    db: Session = Depends(get_db)
):
    """
    主创建者撤销管理者权限
    - 只有主创建者可以调用
    - 被撤销用户角色变为user
    """
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.role == "creator":
        raise HTTPException(status_code=400, detail="不能撤销主创建者权限")
    
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="该用户不是管理者")
    
    user.role = "user"
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": f"已撤销用户「{user.username}」的管理者权限",
        "user": {"id": user.id, "username": user.username, "role": user.role},
        "revoked_by": current_user.username,
        "reason": req.reason
    }

# ==================== 管理者接口 ====================

# 获取用户列表（管理者及以上）
@router.get("/users")
def list_users(
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取用户列表（管理者及以上权限）"""
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    
    total = query.count()
    users = query.order_by(User.id).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": [
            {
                "id": u.id,
                "username": u.username,
                "role": u.role,
                "created_at": u.created_at.isoformat() if u.created_at else None
            }
            for u in users
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }

# 获取管理者列表
@router.get("/admins")
def list_admins(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取所有管理者列表"""
    admins = db.query(User).filter(User.role == "admin").all()
    creator = db.query(User).filter(User.role == "creator").first()
    
    return {
        "success": True,
        "creator": {"id": creator.id, "username": creator.username} if creator else None,
        "admins": [
            {"id": u.id, "username": u.username, "created_at": u.created_at.isoformat() if u.created_at else None}
            for u in admins
        ],
        "total_admins": len(admins)
    }

# 管理者更新用户信息（不能修改创建者）
@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    req: UpdateUserRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """管理者更新用户信息（不能修改主创建者）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.role == "creator" and current_user.role != "creator":
        raise HTTPException(status_code=403, detail="只有主创建者可以修改创建者信息")
    
    if req.role and current_user.role != "creator":
        raise HTTPException(status_code=403, detail="只有主创建者可以修改用户角色")
    
    if req.username:
        existing = db.query(User).filter(User.username == req.username, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="用户名已存在")
        user.username = req.username
    
    if req.password:
        user.password_hash = hash_password(req.password)
    
    if req.role and current_user.role == "creator":
        if req.role == "creator":
            raise HTTPException(status_code=400, detail="主创建者全局唯一，不能指定其他用户为创建者")
        user.role = req.role
    
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": "用户信息更新成功",
        "user": {"id": user.id, "username": user.username, "role": user.role}
    }

# 管理者删除用户（不能删除创建者）
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """管理者删除用户（不能删除主创建者）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.role == "creator":
        raise HTTPException(status_code=403, detail="不能删除主创建者")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    username = user.username
    db.delete(user)
    db.commit()
    
    return {
        "success": True,
        "message": f"用户「{username}」已删除",
        "deleted_by": current_user.username
    }

# ==================== 权限说明 ====================

@router.get("/permissions")
def get_permissions():
    """获取权限等级说明"""
    return {
        "success": True,
        "permissions": {
            "creator": {
                "name": "主创建者",
                "description": "系统最高权限，全局唯一，可授权/撤销管理者，管理所有用户和数据",
                "count": 1,
                "can": ["授权管理者", "撤销管理者", "管理所有用户", "管理所有数据", "系统设置", "数据清零"]
            },
            "admin": {
                "name": "管理者",
                "description": "需主创建者授权，可管理普通用户和业务数据",
                "can": ["管理普通用户", "管理业务数据", "查看统计报表", "内容审核"],
                "cannot": ["授权管理者", "撤销管理者", "修改主创建者", "系统级设置"]
            },
            "user": {
                "name": "普通用户",
                "description": "基础权限，可使用系统功能和管理自己的数据",
                "can": ["使用系统功能", "管理自己的数据", "查看公开内容"],
                "cannot": ["管理其他用户", "系统级操作", "数据清零"]
            }
        }
    }
