import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.models import Material
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/files", tags=["文件管理"])

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# 支持的文件类型
ALLOWED_EXTENSIONS = {
    # 视频
    '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v',
    # 图片
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico',
    # 音频
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma',
    # 文档
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.csv',
    '.html', '.htm', '.xml', '.json', '.zip', '.rar', '.7z', '.tar', '.gz'
}

def get_file_type(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']:
        return "video"
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico']:
        return "image"
    elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']:
        return "audio"
    else:
        return "document"

# 上传文件
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail=f"文件大小超过限制（最大{settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB）")
    
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    material = Material(
        filename=file.filename,
        file_path=file_path,
        file_type=get_file_type(file.filename),
        file_size=file_size,
        uploaded_by=user.username
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    
    return {
        "success": True,
        "message": "上传成功",
        "data": {
            "id": material.id,
            "filename": material.filename,
            "file_type": material.file_type,
            "file_size": material.file_size,
            "file_size_mb": round(material.file_size / 1024 / 1024, 2),
            "url": f"/api/files/download/{material.id}"
        }
    }

# 批量上传文件
@router.post("/upload-batch")
async def upload_batch_files(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    results = []
    for file in files:
        try:
            content = await file.read()
            file_size = len(content)
            
            ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            material = Material(
                filename=file.filename,
                file_path=file_path,
                file_type=get_file_type(file.filename),
                file_size=file_size,
                uploaded_by=user.username
            )
            db.add(material)
            db.commit()
            db.refresh(material)
            
            results.append({
                "id": material.id,
                "filename": material.filename,
                "success": True
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {"success": True, "data": results, "total": len(results)}

# 下载文件
@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == file_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if not os.path.exists(material.file_path):
        raise HTTPException(status_code=404, detail="文件已被删除")
    
    return FileResponse(
        material.file_path,
        filename=material.filename,
        media_type="application/octet-stream"
    )

# 删除文件
@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    material = db.query(Material).filter(Material.id == file_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if os.path.exists(material.file_path):
        os.remove(material.file_path)
    
    db.delete(material)
    db.commit()
    
    return {"success": True, "message": "文件已删除"}

# 获取文件列表
@router.get("/list")
def list_files(
    skip: int = 0,
    limit: int = 100,
    file_type: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Material)
    if file_type:
        query = query.filter(Material.file_type == file_type)
    files = query.order_by(Material.id.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "success": True,
        "data": [{
            "id": f.id,
            "filename": f.filename,
            "file_type": f.file_type,
            "file_size": f.file_size,
            "file_size_mb": round(f.file_size / 1024 / 1024, 2),
            "uploaded_by": f.uploaded_by,
            "created_at": f.created_at,
            "url": f"/api/files/download/{f.id}"
        } for f in files],
        "total": total
    }
