from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import Automation
from app.models import schemas

router = APIRouter(prefix="/api/v1/automations", tags=["automations"])


@router.get("", response_model=List[schemas.AutomationResponse])
async def list_automations(db: AsyncSession = Depends(get_db)):
    """获取自动化列表"""
    result = await db.execute(select(Automation))
    automations = result.scalars().all()
    return [schemas.AutomationResponse.model_validate(a) for a in automations]


@router.get("/{automation_id}", response_model=schemas.AutomationResponse)
async def get_automation(automation_id: UUID, db: AsyncSession = Depends(get_db)):
    """获取自动化详情"""
    result = await db.execute(select(Automation).where(Automation.id == automation_id))
    automation = result.scalar_one_or_none()
    
    if not automation:
        raise HTTPException(status_code=404, detail="自动化规则不存在")
    
    return schemas.AutomationResponse.model_validate(automation)


@router.post("", response_model=schemas.AutomationResponse, status_code=201)
async def create_automation(
    automation: schemas.AutomationCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建自动化规则"""
    db_automation = Automation(**automation.model_dump())
    db.add(db_automation)
    await db.commit()
    await db.refresh(db_automation)
    
    return schemas.AutomationResponse.model_validate(db_automation)


@router.patch("/{automation_id}", response_model=schemas.AutomationResponse)
async def update_automation(
    automation_id: UUID,
    automation_update: schemas.AutomationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新自动化规则"""
    result = await db.execute(select(Automation).where(Automation.id == automation_id))
    automation = result.scalar_one_or_none()
    
    if not automation:
        raise HTTPException(status_code=404, detail="自动化规则不存在")
    
    update_data = automation_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(automation, key, value)
    
    await db.commit()
    await db.refresh(automation)
    
    return schemas.AutomationResponse.model_validate(automation)


@router.delete("/{automation_id}", status_code=204)
async def delete_automation(automation_id: UUID, db: AsyncSession = Depends(get_db)):
    """删除自动化规则"""
    result = await db.execute(select(Automation).where(Automation.id == automation_id))
    automation = result.scalar_one_or_none()
    
    if not automation:
        raise HTTPException(status_code=404, detail="自动化规则不存在")
    
    await db.delete(automation)
    await db.commit()
    
    return None


@router.post("/{automation_id}/trigger")
async def trigger_automation(automation_id: UUID, db: AsyncSession = Depends(get_db)):
    """手动触发自动化"""
    result = await db.execute(select(Automation).where(Automation.id == automation_id))
    automation = result.scalar_one_or_none()
    
    if not automation:
        raise HTTPException(status_code=404, detail="自动化规则不存在")
    
    # TODO: 实际执行自动化动作
    
    from datetime import datetime
    automation.last_triggered = datetime.utcnow()
    automation.trigger_count += 1
    await db.commit()
    
    return {
        "success": True,
        "message": f"自动化 '{automation.alias}' 已触发",
        "automation_id": str(automation_id)
    }
