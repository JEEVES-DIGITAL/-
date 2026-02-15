from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os

from app.services.voice_service import JeevesVoiceService

router = APIRouter(prefix="/api/v1/voice", tags=["voice"])

# 全局语音服务实例
voice_service: JeevesVoiceService = None

def init_voice_service():
    """初始化语音服务"""
    global voice_service
    try:
        voice_service = JeevesVoiceService(
            whisper_model="base",
            llm_model="phi4",
            voice="male_calm"
        )
        print("✅ 语音服务初始化成功")
    except Exception as e:
        print(f"⚠️ 语音服务初始化失败: {e}")
        voice_service = None

@router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    play: bool = False
):
    """
    语音对话接口
    
    上传音频文件，返回识别文字、AI回复、以及语音文件
    """
    if voice_service is None:
        raise HTTPException(status_code=503, detail="语音服务未初始化")
    
    # 保存上传的音频
    temp_input = tempfile.mktemp(suffix=".wav")
    with open(temp_input, "wb") as f:
        content = await audio.read()
        f.write(content)
    
    # 语音对话
    result = await voice_service.chat(temp_input, play=play)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # 返回结果和音频文件
    return {
        "success": True,
        "user_text": result["user_text"],
        "ai_text": result["ai_text"],
        "audio_url": f"/api/v1/voice/audio?path={result['audio_path']}"
    }

@router.get("/audio")
async def get_audio(path: str):
    """获取语音文件"""
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="音频文件不存在")

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """仅语音识别，无对话"""
    if voice_service is None:
        raise HTTPException(status_code=503, detail="语音服务未初始化")
    
    temp_input = tempfile.mktemp(suffix=".wav")
    with open(temp_input, "wb") as f:
        content = await audio.read()
        f.write(content)
    
    text = voice_service.listen(temp_input)
    
    return {
        "success": True,
        "text": text
    }

@router.post("/speak")
async def text_to_speech(text: str):
    """文字转语音"""
    if voice_service is None:
        raise HTTPException(status_code=503, detail="语音服务未初始化")
    
    import asyncio
    audio_path = await voice_service.speak(text)
    
    return {
        "success": True,
        "audio_url": f"/api/v1/voice/audio?path={audio_path}"
    }

@router.get("/status")
async def voice_status():
    """语音服务状态"""
    return {
        "initialized": voice_service is not None,
        "model": voice_service.llm_model if voice_service else None,
        "voice": voice_service.voice if voice_service else None
    }
