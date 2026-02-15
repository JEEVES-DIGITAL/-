from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.database import get_db
from app.models import schemas
from app.models import Device, Automation, Conversation

router = APIRouter(prefix="/api/v1/system", tags=["system"])


@router.get("/health", response_model=schemas.HealthCheck)
async def health_check():
    """健康检查"""
    from datetime import datetime
    from app.config import get_settings
    
    settings = get_settings()
    return schemas.HealthCheck(
        status="ok",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow()
    )


@router.get("/info", response_model=schemas.SystemInfo)
async def system_info(db: AsyncSession = Depends(get_db)):
    """系统信息"""
    from app.config import get_settings
    import psutil
    import time
    
    settings = get_settings()
    
    # 获取统计
    devices_result = await db.execute(select(func.count(Device.id)))
    devices_count = devices_result.scalar()
    
    automations_result = await db.execute(select(func.count(Automation.id)))
    automations_count = automations_result.scalar()
    
    conversations_result = await db.execute(select(func.count(Conversation.id)))
    conversations_count = conversations_result.scalar()
    
    # 系统运行时间
    uptime = int(time.time() - psutil.boot_time())
    
    return schemas.SystemInfo(
        version=settings.APP_VERSION,
        uptime=uptime,
        devices_count=devices_count,
        automations_count=automations_count,
        conversations_count=conversations_count
    )
