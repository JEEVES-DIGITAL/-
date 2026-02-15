# Home Assistant 集成配置
# 基维斯对接HA控制智能家居

## 连接配置

```yaml
# config/homeassistant.yaml

home_assistant:
  # Home Assistant地址
  url: "http://192.168.1.xxx:8123"
  
  # 长连接令牌（从HA用户配置中获取）
  token: "your_long_lived_access_token"
  
  # WebSocket连接（实时状态同步）
  websocket:
    enabled: true
    reconnect_interval: 5
  
  # 自动发现设备
  auto_discover: true
  
  # 设备映射（基维斯entity_id → HA entity_id）
  devices:
    light.living_room: "light.living_room_main"
    light.bedroom: "light.bedroom_main"
    climate.living_room: "climate.living_room_ac"
    cover.curtain: "cover.living_room_curtain"
    media_player.speaker: "media_player.xiaodu_speaker"
```

## 获取HA Token步骤

1. 登录Home Assistant
2. 左下角用户名 → 滚动到底部
3. 创建长连接令牌（Long-Lived Access Tokens）
4. 复制令牌到配置文件

## 测试连接

```bash
# 测试HA连接
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://192.168.1.xxx:8123/api/

# 获取所有设备状态
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://192.168.1.xxx:8123/api/states
```

## 基维斯语音控制映射

| 语音指令 | 意图 | HA服务调用 |
|---------|------|-----------|
| "打开客厅灯" | turn_on_light | light.turn_on + entity_id: light.living_room |
| "关闭空调" | turn_off_climate | climate.turn_off + entity_id: climate.living_room |
| "关闭窗帘" | close_cover | cover.close_cover + entity_id: cover.curtain |
| "我回家了" | coming_home | scene.turn_on + scene_id: scene.coming_home |
| "我要睡觉了" | sleep_mode | scene.turn_on + scene_id: scene.sleep_mode |

## 场景配置（HA端）

```yaml
# HA configuration.yaml

scene:
  - name: 回家模式
    id: scene.coming_home
    entities:
      light.living_room_main:
        state: on
        brightness: 180
      climate.living_room_ac:
        state: on
        temperature: 24
      media_player.xiaodu_speaker:
        state: playing
        media_content_id: "欢迎回家"
        
  - name: 睡眠模式
    id: scene.sleep_mode
    entities:
      light.living_room_main:
        state: off
      light.bedroom_main:
        state: on
        brightness: 10
      climate.living_room_ac:
        state: on
        temperature: 26
      cover.living_room_curtain:
        state: closed
```
