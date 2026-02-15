from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models import Device
from app.models import schemas

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


@router.get("", response_model=schemas.DeviceListResponse)
async def list_devices(
    device_type: Optional[str] = None,
    area: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取设备列表"""
    query = select(Device)
    
    if device_type:
        query = query.where(Device.device_type == device_type)
    if area:
        query = query.where(Device.area == area)
    
    result = await db.execute(query)
    devices = result.scalars().all()
    
    return schemas.DeviceListResponse(
        devices=[schemas.DeviceResponse.model_validate(d) for d in devices],
        total=len(devices)
    )


@router.get("/{device_id}", response_model=schemas.DeviceResponse)
async def get_device(device_id: UUID, db: AsyncSession = Depends(get_db)):
    """获取设备详情"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    return schemas.DeviceResponse.model_validate(device)


@router.post("", response_model=schemas.DeviceResponse, status_code=201)
async def create_device(device: schemas.DeviceCreate, db: AsyncSession = Depends(get_db)):
    """创建设备"""
    # 检查是否已存在
    result = await db.execute(select(Device).where(Device.entity_id == device.entity_id))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="设备已存在")
    
    db_device = Device(**device.model_dump())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    
    return schemas.DeviceResponse.model_validate(db_device)


@router.patch("/{device_id}", response_model=schemas.DeviceResponse)
async def update_device(
    device_id: UUID,
    device_update: schemas.DeviceUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新设备"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    update_data = device_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(device, key, value)
    
    await db.commit()
    await db.refresh(device)
    
    return schemas.DeviceResponse.model_validate(device)


@router.delete("/{device_id}", status_code=204)
async def delete_device(device_id: UUID, db: AsyncSession = Depends(get_db)):
    """删除设备"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    await db.delete(device)
    await db.commit()
    
    return None


@router.post("/{device_id}/command")
async def device_command(
    device_id: UUID,
    command: schemas.DeviceCommand,
    db: AsyncSession = Depends(get_db)
):
    """发送设备命令"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    # TODO: 实际发送命令到设备
    # 这里调用 HA 或其他设备控制接口
    
    return {
        "success": True,
        "message": f"命令已发送: {command.service}",
        "device_id": str(device_id),
        "command": command.model_dump()
    }
