import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models import Conversation
from app.models import schemas
from app.services.ai_service import AIService
from app.services.intent_service import IntentService

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# 服务实例
ai_service = AIService()
intent_service = IntentService()


@router.post("", response_model=schemas.ChatResponse)
async def chat(
    message: schemas.ChatMessage,
    db: AsyncSession = Depends(get_db)
):
    """AI对话接口"""
    
    # 生成或获取会话ID
    session_id = message.session_id or str(uuid.uuid4())
    
    # 意图识别
    intent = await intent_service.recognize(message.message)
    
    # 根据意图执行动作
    actions = []
    if intent == "turn_on_light":
        actions.append({"type": "device", "service": "turn_on", "entity": "light.living_room"})
    elif intent == "turn_off_light":
        actions.append({"type": "device", "service": "turn_off", "entity": "light.living_room"})
    elif intent == "set_temperature":
        actions.append({"type": "climate", "service": "set_temperature", "temperature": 24})
    elif intent == "coming_home":
        actions = [
            {"type": "device", "service": "turn_on", "entity": "light.living_room"},
            {"type": "climate", "service": "set_temperature", "temperature": 24},
            {"type": "media", "service": "play", "media": "welcome_home"}
        ]
    
    # 生成AI回复
    response_text = await ai_service.chat(
        message=message.message,
        intent=intent,
        context=message.context
    )
    
    # 保存对话记录
    conversation = Conversation(
        session_id=session_id,
        message=message.message,
        response=response_text,
        intent=intent,
        actions=actions
    )
    db.add(conversation)
    await db.commit()
    
    return schemas.ChatResponse(
        response=response_text,
        intent=intent,
        actions=actions,
        session_id=session_id
    )


@router.post("/voice")
async def chat_voice(
    audio_file: bytes,
    session_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """语音输入对话（TODO）"""
    # TODO: 语音识别 (STT)
    # TODO: 调用chat接口
    # TODO: 语音合成 (TTS) 返回音频
    
    return {
        "success": True,
        "message": "语音功能开发中",
        "session_id": session_id or str(uuid.uuid4())
    }
