# Jeeves Core API 设计

## 基础接口

### 健康检查
```
GET /health
Response: {"status": "ok", "version": "0.1.0"}
```

### 系统信息
```
GET /api/v1/system/info
Response: {
    "version": "0.1.0",
    "uptime": 3600,
    "devices_count": 15,
    "automations_count": 5
}
```

## AI对话接口

### 发送消息
```
POST /api/v1/chat
Body: {
    "message": "我回家了",
    "session_id": "uuid",
    "context": {}
}
Response: {
    "response": "欢迎回家，已为您开启回家模式。",
    "actions": [
        {"type": "light", "entity": "living_room", "state": "on"},
        {"type": "climate", "entity": "living_room", "temperature": 24}
    ],
    "session_id": "uuid"
}
```

### 语音输入
```
POST /api/v1/chat/voice
Content-Type: multipart/form-data
Body: audio_file
Response: 同上
```

## 设备管理接口

### 获取设备列表
```
GET /api/v1/devices
Response: {
    "devices": [
        {
            "entity_id": "light.living_room",
            "name": "客厅灯",
            "type": "light",
            "state": "on",
            "attributes": {"brightness": 255}
        }
    ]
}
```

### 控制设备
```
POST /api/v1/devices/{entity_id}/command
Body: {
    "service": "turn_on",
    "data": {"brightness": 200}
}
```

## 自动化接口

### 获取自动化列表
```
GET /api/v1/automations
```

### 创建自动化
```
POST /api/v1/automations
Body: {
    "alias": "回家模式",
    "trigger": {...},
    "condition": {...},
    "action": {...}
}
```

### 触发自动化
```
POST /api/v1/automations/{automation_id}/trigger
```

## 技能接口

### 获取技能列表
```
GET /api/v1/skills
```

### 安装技能
```
POST /api/v1/skills/install
Body: {"skill_url": "https://github.com/..."}
```

### 执行技能
```
POST /api/v1/skills/{skill_name}/execute
Body: {"parameters": {...}}
```

## WebSocket 实时接口

### 连接
```
WS /api/v1/ws
Headers: Authorization: Bearer {token}
```

### 订阅设备状态
```json
{"type": "subscribe", "entity_ids": ["light.living_room"]}
```

### 接收状态更新
```json
{
    "type": "state_changed",
    "entity_id": "light.living_room",
    "old_state": {"state": "off"},
    "new_state": {"state": "on", "brightness": 255}
}
```
