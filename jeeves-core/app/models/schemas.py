from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ==================== 通用响应 ====================

class ResponseBase(BaseModel):
    """基础响应"""
    success: bool = True
    message: Optional[str] = None


class HealthCheck(BaseModel):
    """健康检查响应"""
    status: str = "ok"
    version: str
    timestamp: datetime


# ==================== 系统信息 ====================

class SystemInfo(BaseModel):
    """系统信息"""
    version: str
    uptime: int  # 秒
    devices_count: int
    automations_count: int
    conversations_count: int
    

# ==================== AI 对话 ====================

class ChatMessage(BaseModel):
    """聊天消息"""
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    intent: Optional[str] = None
    actions: List[Dict[str, Any]] = []
    session_id: str


# ==================== 设备管理 ====================

class DeviceBase(BaseModel):
    """设备基础信息"""
    entity_id: str
    name: str
    device_type: str
    area: Optional[str] = None
    state: Optional[str] = None
    attributes: Dict[str, Any] = {}


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    area: Optional[str] = None


class DeviceResponse(DeviceBase):
    """设备响应"""
    id: UUID
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DeviceCommand(BaseModel):
    """设备命令"""
    service: str  # turn_on, turn_off, set_temperature, etc.
    data: Dict[str, Any] = {}


class DeviceListResponse(BaseModel):
    """设备列表响应"""
    devices: List[DeviceResponse]
    total: int


# ==================== 自动化 ====================

class AutomationBase(BaseModel):
    """自动化基础"""
    alias: str
    description: Optional[str] = None
    trigger: Dict[str, Any]
    condition: Optional[Dict[str, Any]] = None
    action: Dict[str, Any]


class AutomationCreate(AutomationBase):
    pass


class AutomationUpdate(BaseModel):
    alias: Optional[str] = None
    description: Optional[str] = None
    trigger: Optional[Dict[str, Any]] = None
    condition: Optional[Dict[str, Any]] = None
    action: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None


class AutomationResponse(AutomationBase):
    """自动化响应"""
    id: UUID
    is_enabled: bool
    last_triggered: Optional[datetime]
    trigger_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 记忆系统 ====================

class MemoryCreate(BaseModel):
    """创建记忆"""
    content: str
    memory_type: str = "general"
    source: Optional[str] = None


class MemoryResponse(BaseModel):
    """记忆响应"""
    id: UUID
    content: str
    memory_type: str
    source: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== WebSocket ====================

class WebSocketMessage(BaseModel):
    """WebSocket消息"""
    type: str  # chat, command, event, state_change
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
