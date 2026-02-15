# Home Assistant 集成开发
# 基维斯对接HA实现语音控制设备

from typing import Dict, Any, Optional
import aiohttp
import json


class HomeAssistantClient:
    """
    Home Assistant API 客户端
    
    功能：
    - 设备状态同步
    - 设备控制（开关、调光、调温度等）
    - 场景执行
    - 实时状态监听（WebSocket）
    """
    
    def __init__(self, url: str, token: str):
        """
        初始化HA客户端
        
        Args:
            url: Home Assistant地址，如 http://192.168.1.100:8123
            token: 长连接访问令牌（Long-Lived Access Token）
        """
        self.url = url.rstrip('/')
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建HTTP会话"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def test_connection(self) -> bool:
        """测试HA连接"""
        try:
            session = await self._get_session()
            async with session.get(
                f"{self.url}/api/",
                headers=self.headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ HA连接成功: {data.get('message', 'OK')}")
                    return True
                else:
                    print(f"❌ HA连接失败: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ HA连接错误: {e}")
            return False
    
    async def get_states(self) -> list:
        """获取所有设备状态"""
        try:
            session = await self._get_session()
            async with session.get(
                f"{self.url}/api/states",
                headers=self.headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                return []
        except Exception as e:
            print(f"❌ 获取状态失败: {e}")
            return []
    
    async def get_entity(self, entity_id: str) -> Optional[Dict]:
        """获取特定设备状态"""
        try:
            session = await self._get_session()
            async with session.get(
                f"{self.url}/api/states/{entity_id}",
                headers=self.headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception as e:
            print(f"❌ 获取设备失败: {e}")
            return None
    
    async def call_service(self, domain: str, service: str, data: Dict) -> bool:
        """
        调用HA服务
        
        Args:
            domain: 服务域（light, climate, switch等）
            service: 服务名（turn_on, turn_off, set_temperature等）
            data: 服务数据
        """
        try:
            session = await self._get_session()
            async with session.post(
                f"{self.url}/api/services/{domain}/{service}",
                headers=self.headers,
                json=data
            ) as response:
                if response.status in [200, 201]:
                    print(f"✅ 服务调用成功: {domain}.{service}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ 服务调用失败: {response.status} - {text}")
                    return False
        except Exception as e:
            print(f"❌ 服务调用错误: {e}")
            return False
    
    # ========== 设备控制快捷方法 ==========
    
    async def turn_on_light(self, entity_id: str, brightness: Optional[int] = None) -> bool:
        """开灯"""
        data = {"entity_id": entity_id}
        if brightness is not None:
            data["brightness"] = brightness  # 0-255
        return await self.call_service("light", "turn_on", data)
    
    async def turn_off_light(self, entity_id: str) -> bool:
        """关灯"""
        return await self.call_service("light", "turn_off", {"entity_id": entity_id})
    
    async def set_climate_temperature(self, entity_id: str, temperature: float) -> bool:
        """设置空调温度"""
        return await self.call_service("climate", "set_temperature", {
            "entity_id": entity_id,
            "temperature": temperature
        })
    
    async def turn_on_climate(self, entity_id: str) -> bool:
        """开空调"""
        return await self.call_service("climate", "turn_on", {"entity_id": entity_id})
    
    async def turn_off_climate(self, entity_id: str) -> bool:
        """关空调"""
        return await self.call_service("climate", "turn_off", {"entity_id": entity_id})
    
    async def open_cover(self, entity_id: str) -> bool:
        """开窗帘"""
        return await self.call_service("cover", "open_cover", {"entity_id": entity_id})
    
    async def close_cover(self, entity_id: str) -> bool:
        """关窗帘"""
        return await self.call_service("cover", "close_cover", {"entity_id": entity_id})
    
    async def turn_on_switch(self, entity_id: str) -> bool:
        """打开开关"""
        return await self.call_service("switch", "turn_on", {"entity_id": entity_id})
    
    async def turn_off_switch(self, entity_id: str) -> bool:
        """关闭开关"""
        return await self.call_service("switch", "turn_off", {"entity_id": entity_id})
    
    async def trigger_scene(self, entity_id: str) -> bool:
        """执行场景"""
        return await self.call_service("scene", "turn_on", {"entity_id": entity_id})
    
    async def close(self):
        """关闭连接"""
        if self.session and not self.session.closed:
            await self.session.close()


class DeviceController:
    """
    设备控制器
    
    将语音指令映射到HA设备控制
    """
    
    def __init__(self, ha_client: HomeAssistantClient):
        self.ha = ha_client
        # 设备映射表（entity_id映射）
        self.device_map = {
            "客厅灯": "light.living_room",
            "卧室灯": "light.bedroom",
            "主卧灯": "light.bedroom_master",
            "次卧灯": "light.bedroom_guest",
            "餐厅灯": "light.dining_room",
            "厨房灯": "light.kitchen",
            "客厅空调": "climate.living_room_ac",
            "主卧空调": "climate.bedroom_ac",
            "客厅窗帘": "cover.living_room_curtain",
            "电视": "media_player.tv",
            "投影仪": "media_player.projector",
        }
    
    def get_entity_id(self, device_name: str) -> Optional[str]:
        """根据设备名获取entity_id"""
        # 直接匹配
        if device_name in self.device_map:
            return self.device_map[device_name]
        
        # 模糊匹配（简单实现）
        for name, entity_id in self.device_map.items():
            if name in device_name or device_name in name:
                return entity_id
        
        return None
    
    async def execute_command(self, intent: str, params: Dict) -> str:
        """
        执行语音指令
        
        Args:
            intent: 意图（turn_on_light, set_temperature等）
            params: 参数
        
        Returns:
            执行结果描述
        """
        device_name = params.get("device", "")
        entity_id = self.get_entity_id(device_name)
        
        if not entity_id:
            return f"抱歉，没有找到设备：{device_name}"
        
        try:
            if intent == "turn_on_light":
                brightness = params.get("brightness")
                success = await self.ha.turn_on_light(entity_id, brightness)
                if success:
                    return f"已为您打开{device_name}"
                return f"打开{device_name}失败"
            
            elif intent == "turn_off_light":
                success = await self.ha.turn_off_light(entity_id)
                if success:
                    return f"已为您关闭{device_name}"
                return f"关闭{device_name}失败"
            
            elif intent == "set_temperature":
                temp = params.get("temperature", 24)
                success = await self.ha.set_climate_temperature(entity_id, temp)
                if success:
                    return f"已为您将{device_name}温度调至{temp}度"
                return f"调节温度失败"
            
            elif intent == "turn_on_climate":
                success = await self.ha.turn_on_climate(entity_id)
                if success:
                    return f"已为您打开{device_name}"
                return f"打开{device_name}失败"
            
            elif intent == "turn_off_climate":
                success = await self.ha.turn_off_climate(entity_id)
                if success:
                    return f"已为您关闭{device_name}"
                return f"关闭{device_name}失败"
            
            elif intent == "open_cover":
                success = await self.ha.open_cover(entity_id)
                if success:
                    return f"已为您打开{device_name}"
                return f"打开{device_name}失败"
            
            elif intent == "close_cover":
                success = await self.ha.close_cover(entity_id)
                if success:
                    return f"已为您关闭{device_name}"
                return f"关闭{device_name}失败"
            
            elif intent == "trigger_scene":
                success = await self.ha.trigger_scene(entity_id)
                if success:
                    return f"已为您执行{device_name}"
                return f"执行场景失败"
            
            else:
                return f"暂不支持的指令：{intent}"
                
        except Exception as e:
            return f"执行出错：{e}"


# 场景定义
SCENES = {
    "回家模式": {
        "description": "执行回家场景",
        "actions": [
            {"service": "light.turn_on", "entity_id": "light.living_room", "data": {"brightness": 180}},
            {"service": "climate.set_temperature", "entity_id": "climate.living_room_ac", "data": {"temperature": 24}},
            {"service": "media_player.play_media", "entity_id": "media_player.speaker", "data": {"media_content_id": "欢迎回家"}},
        ]
    },
    "离家模式": {
        "description": "执行离家场景",
        "actions": [
            {"service": "light.turn_off", "entity_id": "light.all"},
            {"service": "climate.turn_off", "entity_id": "climate.living_room_ac"},
        ]
    },
    "睡眠模式": {
        "description": "执行睡眠场景",
        "actions": [
            {"service": "light.turn_off", "entity_id": "light.living_room"},
            {"service": "light.turn_on", "entity_id": "light.bedroom", "data": {"brightness": 10}},
            {"service": "climate.set_temperature", "entity_id": "climate.bedroom_ac", "data": {"temperature": 26}},
            {"service": "cover.close_cover", "entity_id": "cover.bedroom_curtain"},
        ]
    },
}


# 意图识别映射
INTENT_PATTERNS = {
    "turn_on_light": ["开灯", "打开灯", "开.*灯"],
    "turn_off_light": ["关灯", "关闭灯", "关.*灯"],
    "set_temperature": ["调到.*度", "温度.*度", "空调.*度"],
    "turn_on_climate": ["开空调", "打开空调"],
    "turn_off_climate": ["关空调", "关闭空调"],
    "open_cover": ["开窗帘", "打开窗帘"],
    "close_cover": ["关窗帘", "关闭窗帘", "拉窗帘"],
    "trigger_scene": ["回家模式", "离家模式", "睡眠模式", "会客模式"],
}


def parse_intent(text: str) -> tuple:
    """
    解析语音指令意图
    
    Returns:
        (intent, params)
    """
    import re
    
    text = text.lower()
    
    # 检查场景
    for scene_name in SCENES.keys():
        if scene_name in text:
            return "trigger_scene", {"device": scene_name}
    
    # 检查设备控制
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                # 提取设备名
                device_name = extract_device_name(text)
                params = {"device": device_name}
                
                # 提取温度
                if intent == "set_temperature":
                    temp_match = re.search(r'(\d+)', text)
                    if temp_match:
                        params["temperature"] = int(temp_match.group(1))
                
                return intent, params
    
    return None, {}


def extract_device_name(text: str) -> str:
    """从指令中提取设备名"""
    import re
    
    # 常见的设备名模式
    patterns = [
        r'(客厅|卧室|主卧|次卧|餐厅|厨房|书房|卫生间).*?(灯|空调|窗帘|电视)',
        r'(.*?)的?(灯|空调|窗帘|电视)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return "未知设备"


# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def test():
        # 配置（需要用户填写）
        HA_URL = "http://192.168.1.xxx:8123"  # 你的HA地址
        HA_TOKEN = "your_long_lived_access_token"  # 你的HA令牌
        
        # 创建客户端
        ha = HomeAssistantClient(HA_URL, HA_TOKEN)
        
        # 测试连接
        if await ha.test_connection():
            # 获取所有设备
            states = await ha.get_states()
            print(f"\n发现 {len(states)} 个设备")
            
            # 打印前10个设备
            for state in states[:10]:
                print(f"  - {state['entity_id']}: {state['state']}")
        
        await ha.close()
    
    asyncio.run(test())
