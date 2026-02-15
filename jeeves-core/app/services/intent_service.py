import re
from typing import Optional


class IntentService:
    """意图识别服务"""
    
    def __init__(self):
        # 定义意图模式
        self.intent_patterns = {
            "turn_on_light": [
                r"开灯",
                r"打开.*灯",
                r"turn on.*light",
                r"light on",
            ],
            "turn_off_light": [
                r"关灯",
                r"关闭.*灯",
                r"turn off.*light",
                r"light off",
            ],
            "set_temperature": [
                r"温度.*调到",
                r"空调.*度",
                r"set temperature",
                r".*度",
            ],
            "coming_home": [
                r"我回家了",
                r"到家了",
                r"i['']?m home",
                r"coming home",
            ],
            "leaving_home": [
                r"我出门了",
                r"离家",
                r"leaving",
                r"i['']?m leaving",
            ],
            "weather": [
                r"天气",
                r"weather",
            ],
            "time": [
                r"几点了",
                r"时间",
                r"what time",
            ],
            "greeting": [
                r"你好",
                r"您好",
                r"hello",
                r"hi",
                r"hey",
            ],
            "goodbye": [
                r"再见",
                r"拜拜",
                r"bye",
                r"goodbye",
            ],
        }
    
    async def recognize(self, message: str) -> Optional[str]:
        """
        识别用户意图
        
        返回: 意图类型字符串 或 None
        """
        message_lower = message.lower().strip()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    return intent
        
        return "general"  # 默认意图
    
    def extract_entities(self, message: str) -> dict:
        """提取实体信息"""
        entities = {}
        
        # 提取温度
        temp_match = re.search(r'(\d+)[°度]', message)
        if temp_match:
            entities['temperature'] = int(temp_match.group(1))
        
        # 提取房间
        rooms = ['客厅', '卧室', '厨房', '卫生间', '书房', 'living room', 'bedroom', 'kitchen']
        for room in rooms:
            if room in message.lower():
                entities['room'] = room
                break
        
        # 提取设备
        devices = ['灯', '空调', '窗帘', '电视', 'light', 'ac', 'curtain', 'tv']
        for device in devices:
            if device in message.lower():
                entities['device'] = device
                break
        
        return entities
