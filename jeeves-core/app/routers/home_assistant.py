from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.services.home_assistant import HomeAssistantClient, DeviceController, parse_intent

router = APIRouter(prefix="/api/v1/ha", tags=["home_assistant"])

# 全局HA客户端
ha_client: Optional[HomeAssistantClient] = None
device_controller: Optional[DeviceController] = None

# 配置（从环境变量或配置文件读取）
HA_URL = "http://192.168.1.100:8123"  # 需要用户配置
HA_TOKEN = ""  # 需要用户提供


def init_ha_client():
    """初始化HA客户端"""
    global ha_client, device_controller
    
    # 从配置文件读取
    import os
    from app.config import get_settings
    
    settings = get_settings()
    ha_url = getattr(settings, 'HA_URL', HA_URL)
    ha_token = getattr(settings, 'HA_TOKEN', HA_TOKEN)
    
    if ha_token:
        try:
            ha_client = HomeAssistantClient(ha_url, ha_token)
            device_controller = DeviceController(ha_client)
            print(f"✅ Home Assistant 客户端初始化成功")
            return True
        except Exception as e:
            print(f"⚠️ Home Assistant 初始化失败: {e}")
    
    return False


# 请求模型
class DeviceCommand(BaseModel):
    device: str
    action: str  # on/off/set_temperature
    value: Optional[Any] = None  # 温度、亮度等


class VoiceCommand(BaseModel):
    text: str  # 语音指令文字


@router.get("/status")
async def ha_status():
    """检查HA连接状态"""
    if ha_client is None:
        return {"connected": False, "message": "未配置Home Assistant"}
    
    connected = await ha_client.test_connection()
    return {
        "connected": connected,
        "url": HA_URL if connected else None
    }


@router.get("/devices")
async def list_devices():
    """获取所有设备列表"""
    if ha_client is None:
        raise HTTPException(status_code=503, detail="Home Assistant未初始化")
    
    states = await ha_client.get_states()
    
    # 过滤常用设备类型
    devices = []
    for state in states:
        entity_id = state['entity_id']
        domain = entity_id.split('.')[0]
        
        if domain in ['light', 'climate', 'switch', 'cover', 'media_player', 'sensor']:
            devices.append({
                "entity_id": entity_id,
                "domain": domain,
                "name": state['attributes'].get('friendly_name', entity_id),
                "state": state['state'],
                "attributes": state['attributes']
            })
    
    return {"devices": devices, "count": len(devices)}


@router.get("/devices/{entity_id}")
async def get_device(entity_id: str):
    """获取特定设备状态"""
    if ha_client is None:
        raise HTTPException(status_code=503, detail="Home Assistant未初始化")
    
    entity_id = entity_id.replace("_", ".", 1)  # 处理URL中的点
    state = await ha_client.get_entity(entity_id)
    
    if state is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    
    return state


@router.post("/command")
async def send_command(command: DeviceCommand):
    """发送设备控制命令"""
    if device_controller is None:
        raise HTTPException(status_code=503, detail="Home Assistant未初始化")
    
    # 构建参数
    params = {"device": command.device}
    if command.value is not None:
        if command.action == "set_temperature":
            params["temperature"] = command.value
        elif command.action == "set_brightness":
            params["brightness"] = command.value
    
    # 执行命令
    result = await device_controller.execute_command(command.action, params)
    
    return {"success": True, "message": result}


@router.post("/voice-command")
async def voice_command(command: VoiceCommand):
    """
    语音指令控制
    
    示例：
    - "打开客厅灯"
    - "关掉空调"
    - "把温度调到24度"
    - "执行回家模式"
    """
    if device_controller is None:
        raise HTTPException(status_code=503, detail="Home Assistant未初始化")
    
    # 解析意图
    intent, params = parse_intent(command.text)
    
    if intent is None:
        return {
            "success": False,
            "message": "未能理解指令",
            "intent": None,
            "original_text": command.text
        }
    
    # 执行命令
    result = await device_controller.execute_command(intent, params)
    
    return {
        "success": True,
        "message": result,
        "intent": intent,
        "params": params,
        "original_text": command.text
    }


@router.post("/scenes/{scene_name}")
async def trigger_scene(scene_name: str):
    """执行场景"""
    if device_controller is None:
        raise HTTPException(status_code=503, detail="Home Assistant未初始化")
    
    result = await device_controller.execute_command(
        "trigger_scene",
        {"device": scene_name}
    )
    
    return {"success": True, "message": result}


@router.get("/scenes")
async def list_scenes():
    """获取可用场景列表"""
    from app.services.home_assistant import SCENES
    
    return {
        "scenes": [
            {"name": name, "description": data["description"]}
            for name, data in SCENES.items()
        ]
    }
