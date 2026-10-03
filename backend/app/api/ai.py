import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.models import AIGeneration
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/ai", tags=["AI智能"])

class AIRequest(BaseModel):
    prompt: str
    model: str = "deepseek-chat"
    max_tokens: int = 2000
    temperature: float = 0.7

class ScriptRequest(BaseModel):
    topic: str
    script_type: str = "口播"  # 口播 / 分镜 / Vlog
    duration: int = 60  # 秒
    style: str = "专业"

class BreakdownRequest(BaseModel):
    video_url: str = ""
    video_title: str = ""
    analysis_type: str = "full"  # full / hook / structure / copywriting

# 通用AI调用（DeepSeek）
async def call_deepseek(prompt: str, model: str = "deepseek-chat", max_tokens: int = 2000):
    if not settings.DEEPSEEK_API_KEY:
        raise HTTPException(status_code=400, detail="请先配置DEEPSEEK_API_KEY")
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()["choices"][0]["message"]["content"]

# 通用AI对话
@router.post("/chat")
async def ai_chat(req: AIRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        result = await call_deepseek(req.prompt, req.model, req.max_tokens)
        
        record = AIGeneration(
            prompt=req.prompt,
            result=result,
            gen_type="text",
            model=req.model,
            created_by=user.username
        )
        db.add(record)
        db.commit()
        
        return {"success": True, "data": result, "record_id": record.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 生成脚本
@router.post("/generate-script")
async def generate_script(req: ScriptRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    prompt = f"""请为我生成一个{req.script_type}视频脚本。

主题：{req.topic}
时长：约{req.duration}秒
风格：{req.style}

要求：
1. 开头3秒必须有抓人钩子
2. 结构清晰，有起承转合
3. 语言口语化，适合口播
4. 包含具体的画面描述和镜头建议
5. 结尾有明确的行动号召

请按以下格式输出：
【钩子】开头3秒
【正文】主体内容（分段）
【结尾】行动号召
【镜头建议】每个段落对应的画面"""
    
    try:
        result = await call_deepseek(prompt)
        
        record = AIGeneration(
            prompt=prompt,
            result=result,
            gen_type="script",
            model="deepseek-chat",
            created_by=user.username
        )
        db.add(record)
        db.commit()
        
        return {"success": True, "data": result, "record_id": record.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 爆款视频拆解
@router.post("/breakdown")
async def breakdown_video(req: BreakdownRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    prompt = f"""请对以下爆款视频进行深度拆解分析。

视频标题：{req.video_title}
视频链接：{req.video_url}
分析类型：{req.analysis_type}

请从以下维度进行拆解：
1. 【钩子分析】开头3秒用了什么技巧抓人？
2. 【结构分析】整体内容结构是什么？起承转合如何安排？
3. 【话术分析】核心金句、关键话术有哪些？
4. 【节奏分析】视频节奏如何？哪里快哪里慢？
5. 【转化分析】如何引导用户行动？转化点在哪里？
6. 【可复用点】哪些元素可以直接借鉴复用？
7. 【优化建议】如果要做得更好，可以怎么优化？

请给出详细、具体、可操作的分析。"""
    
    try:
        result = await call_deepseek(prompt)
        
        record = AIGeneration(
            prompt=prompt,
            result=result,
            gen_type="breakdown",
            model="deepseek-chat",
            created_by=user.username
        )
        db.add(record)
        db.commit()
        
        return {"success": True, "data": result, "record_id": record.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 生成AI视频提示词
@router.post("/generate-video-prompt")
async def generate_video_prompt(req: AIRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    prompt = f"""请根据以下需求，生成一个专业的AI视频生成提示词（适用于即梦/Seedance等AI视频生成工具）。

需求：{req.prompt}

请按九维控场公式生成提示词：
1. 【主体】画面中的核心主体是什么？
2. 【动作】主体在做什么动作？
3. 【场景】在什么场景/环境中？
4. 【镜头】用什么镜头语言？（景别/角度/运动）
5. 【光线】光线效果如何？
6. 【色彩】整体色调和色彩搭配？
7. 【风格】艺术风格和视觉风格？
8. 【氛围】整体情绪和氛围？
9. 【细节】需要强调的细节元素？

最后给出一个完整的、可直接使用的英文提示词。"""
    
    try:
        result = await call_deepseek(prompt)
        
        record = AIGeneration(
            prompt=prompt,
            result=result,
            gen_type="video_prompt",
            model="deepseek-chat",
            created_by=user.username
        )
        db.add(record)
        db.commit()
        
        return {"success": True, "data": result, "record_id": record.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI生成记录列表
@router.get("/records")
def list_ai_records(
    skip: int = 0,
    limit: int = 50,
    gen_type: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(AIGeneration)
    if gen_type:
        query = query.filter(AIGeneration.gen_type == gen_type)
    records = query.order_by(AIGeneration.id.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "success": True,
        "data": [{
            "id": r.id,
            "prompt": r.prompt[:100] + "..." if len(r.prompt) > 100 else r.prompt,
            "gen_type": r.gen_type,
            "model": r.model,
            "status": r.status,
            "created_by": r.created_by,
            "created_at": r.created_at
        } for r in records],
        "total": total
    }
