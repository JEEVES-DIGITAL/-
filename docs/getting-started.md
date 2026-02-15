# 快速开始指南

## 硬件准备

### 推荐配置

| 配置等级 | CPU | 内存 | 存储 | 适用场景 |
|----------|-----|------|------|----------|
| 入门 | 树莓派 4B (4GB) | 4GB | 64GB SD卡 | 1-2房间，基础功能 |
| 标准 | 树莓派 5 (8GB) | 8GB | 128GB SSD | 全屋智能，本地AI |
| 专业 | Intel N100 | 16GB | 256GB SSD | 大户型，多摄像头 |

### 必备配件

- 电源适配器（树莓派需5V/5A，N100需12V/3A）
- 网线（推荐，WiFi备用）
- Zigbee/Matter协调器（ConBee II 或 SkyConnect）
- 摄像头（可选，推荐接入ONVIF协议摄像头）

## 安装步骤

### 方法一：一键安装（推荐）

在目标设备上运行：

```bash
curl -fsSL https://install.jeeves-os.com | sudo bash
```

安装完成后，访问 `http://设备IP:8123` 完成初始化配置。

### 方法二：Docker Compose

```bash
# 克隆仓库
git clone https://github.com/jeeves-os/jeeves-core.git
cd jeeves-core

# 创建配置
cp config.example.yaml config/config.yaml

# 启动服务
docker-compose up -d
```

### 方法三：开发环境

```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 安装依赖
pip install -r requirements-dev.txt

# 运行后端
python -m jeeves_core

# 运行前端 (另一个终端)
cd web
npm install
npm run dev
```

## 首次配置

### 1. 访问 Web 界面

打开浏览器，访问 `http://设备IP:8123`

### 2. 创建管理员账户

按向导创建首个管理员账户。

### 3. 配置位置

设置家庭位置（用于天气、日出日落自动化）。

### 4. 添加设备

进入 **设置 → 设备与服务 → 添加集成**，支持：

- **Zigbee设备**：通过ZHA或Zigbee2MQTT
- **WiFi设备**：米家、涂鸦等（需对应集成）
- **Matter设备**：原生支持
- **摄像头**：ONVIF、RTSP协议

### 5. 启用 AI 功能

进入 **基维斯大脑 → 模型设置**：

```yaml
# 本地模型（推荐）
llm_provider: ollama
llm_model: phi4
embedding_model: nomic-embed-text

# 云端增强（可选）
cloud_enhancement: true
cloud_provider: openai  # 或 anthropic/google
```

## 创建你的第一个自动化

### 场景：回家模式

1. 进入 **自动化 → 创建自动化**
2. 添加触发器：
   - 类型：状态
   - 实体：person.your_name
   - 变为：home
3. 添加动作：
   - 开灯：light.living_room → on
   - 调空调：climate.living_room → 24°C
   - 播报欢迎：tts.speak → "欢迎回家，Boss"

或使用 YAML：

```yaml
automation:
  - alias: "回家模式"
    trigger:
      - platform: state
        entity_id: person.boss
        to: "home"
    action:
      - service: light.turn_on
        target:
          entity_id: light.living_room
        data:
          brightness_pct: 80
          transition: 3
      - service: climate.set_temperature
        target:
          entity_id: climate.living_room
        data:
          temperature: 24
      - service: tts.speak
        data:
          message: "欢迎回家，Boss。今天有3个快递待取。"
```

## 语音控制

### 配置语音助手

1. 连接麦克风阵列（如Respeaker 2-Mic Hat）
2. 进入 **设置 → 语音助手**
3. 启用唤醒词检测（默认："Hey Jeeves"）
4. 测试语音命令：
   - "Hey Jeeves，开灯"
   - "Hey Jeeves，我回家了"
   - "Hey Jeeves，家里温度多少"

## 下一步

- 📖 [完整的技能开发教程](skill-development.md)
- 🔧 [高级配置选项](advanced-configuration.md)
- 🛠️ [故障排除](troubleshooting.md)
- 💬 [加入社区](https://discord.gg/jeeves-os)

## 常见问题

**Q: 需要外网访问吗？**
A: 不需要。所有核心功能本地运行，外网访问是可选的远程控制功能。

**Q: 支持哪些设备？**
A: 理论上任何支持Home Assistant的设备都支持。详见[兼容性列表](supported-hardware.md)。

**Q: 本地AI够用吗？**
A: Phi-4（4B参数）处理日常对话、指令理解完全够用。复杂推理可开启云端增强。

**Q: 数据安全吗？**
A: 所有数据本地存储，不上传。可选开启加密云备份。
