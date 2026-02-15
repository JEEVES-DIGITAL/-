# Home Assistant 配置指南

## 快速开始

### 1. 获取Home Assistant访问令牌

1. 登录你的Home Assistant
2. 点击左下角用户名
3. 滚动到底部，找到 **Long-Lived Access Tokens**
4. 点击 **Create Token**
5. 输入名称：基维斯 (Jeeves)
6. 复制生成的令牌（注意：只显示一次！）

### 2. 配置基维斯

编辑 `jeeves-core/.env` 文件：

```bash
# Home Assistant 配置
HA_URL=http://192.168.1.100:8123  # 你的HA地址
HA_TOKEN=eyJhbGciOiJIUzI1NiIs...  # 你的长连接令牌
```

或在 `config.json` 中添加：

```json
{
  "ha_url": "http://192.168.1.100:8123",
  "ha_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 3. 重启基维斯服务

```bash
cd jeeves-core
uvicorn app.main:app --reload
```

### 4. 测试连接

```bash
# 检查HA连接状态
curl http://localhost:8000/api/v1/ha/status

# 获取设备列表
curl http://localhost:8000/api/v1/ha/devices

# 发送语音指令
curl -X POST http://localhost:8000/api/v1/ha/voice-command \
  -H "Content-Type: application/json" \
  -d '{"text": "打开客厅灯"}'
```

## 语音指令示例

| 你说 | 执行动作 |
|------|---------|
| "打开客厅灯" | 开灯 |
| "关掉卧室灯" | 关灯 |
| "开空调" | 打开空调 |
| "把温度调到24度" | 设置温度 |
| "打开窗帘" | 开窗帘 |
| "执行回家模式" | 执行HA场景 |
| "我要睡觉了" | 执行睡眠模式 |

## 设备映射配置

编辑 `app/services/home_assistant.py` 中的 `device_map`：

```python
self.device_map = {
    # 格式: "语音名称": "HA entity_id"
    "客厅灯": "light.living_room",
    "卧室灯": "light.bedroom",
    "主卧空调": "climate.bedroom_ac",
    "客厅窗帘": "cover.living_room_curtain",
    # 添加你的设备...
}
```

## 场景配置

在Home Assistant的 `configuration.yaml` 中定义场景：

```yaml
scene:
  - name: 回家模式
    id: scene.coming_home
    entities:
      light.living_room:
        state: on
        brightness: 180
      climate.living_room_ac:
        state: on
        temperature: 24
      
  - name: 睡眠模式
    id: scene.sleep_mode
    entities:
      light.living_room:
        state: off
      light.bedroom:
        state: on
        brightness: 10
      climate.bedroom_ac:
        temperature: 26
      cover.bedroom_curtain:
        state: closed
```

然后重启HA：
```bash
ha core restart
```

## 完整语音交互流程

```
你说: "基维斯，我回家了"
    ↓
语音识别 (faster-whisper)
    ↓
意图识别 → "trigger_scene" + {"device": "回家模式"}
    ↓
调用HA API → scene.turn_on
    ↓
HA执行场景 → 开灯+调空调+播放音乐
    ↓
语音回复 (edge-tts): "欢迎回家，先生。已为您开启回家模式。"
```

## 故障排查

### 连接失败
```bash
# 检查HA是否可访问
curl http://YOUR_HA_IP:8123/api/ -H "Authorization: Bearer YOUR_TOKEN"

# 检查令牌权限
# 确保令牌有访问设备状态的权限
```

### 设备控制失败
1. 检查设备entity_id是否正确
2. 在HA开发者工具中测试服务调用
3. 查看基维斯日志

### 语音指令不识别
1. 检查设备是否在 device_map 中
2. 尝试不同的说法："打开客厅灯" vs "开客厅灯"
3. 查看意图解析日志

## API 接口文档

启动服务后访问：http://localhost:8000/docs#/home_assistant

主要接口：
- `GET /api/v1/ha/status` - 检查连接状态
- `GET /api/v1/ha/devices` - 获取所有设备
- `POST /api/v1/ha/voice-command` - 语音控制
- `POST /api/v1/ha/command` - 直接发送命令
- `GET /api/v1/ha/scenes` - 获取场景列表
