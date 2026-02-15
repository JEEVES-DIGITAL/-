# 基维斯 (Jeeves OS) 项目README

<p align="center">
  <img src="assets/logo.png" alt="Jeeves OS Logo" width="200"/>
</p>

<h1 align="center">基维斯 Jeeves OS</h1>

<p align="center">
  <strong>开源家庭智能操作系统 - 你家的AI管家</strong>
</p>

<p align="center">
  <a href="#-核心特性">核心特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-文档">文档</a> •
  <a href="#-贡献">贡献</a> •
  <a href="#-许可证">许可证</a>
</p>

---

## 🌟 核心特性

- 🤖 **本地AI大脑** - 基于Phi-4/Llama的本地大模型，隐私优先
- 🏠 **全屋智能中枢** - 支持Matter/Zigbee/WiFi，统一控制
- 👁️ **视觉识别** - 本地YOLOv8人形/物体检测，无需上传云端
- 🎙️ **自然语音** - 支持连续对话，真正的智能助手体验
- 🔌 **插件化架构** - 丰富的技能插件，无限扩展可能
- 📱 **多端控制** - Web/App/语音，随时随地管理家庭

## 🚀 快速开始

### 方式一：官方硬件（推荐）

购买 [Jeeves Box](https://jeeves-os.com/hardware)，插电即用。

### 方式二：DIY安装

**系统要求：**
- 树莓派 4/5 (推荐8GB) 或 x86迷你主机
- 64GB+ SD卡/SSD
- 网络连接

**一键安装：**
```bash
curl -fsSL https://install.jeeves-os.com | bash
```

**Docker安装：**
```bash
git clone https://github.com/jeeves-os/jeeves-core.git
cd jeeves-core
docker-compose up -d
```

## 📚 文档

- [快速开始指南](docs/getting-started.md)
- [硬件兼容性列表](docs/supported-hardware.md)
- [技能开发教程](docs/skill-development.md)
- [API文档](docs/api.md)
- [常见问题](docs/faq.md)

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│              基维斯大脑                   │
│         (AI核心 + 技能引擎)               │
├─────────────────────────────────────────┤
│              基维斯中枢                   │
│    (设备接入 + 自动化 + 数据存储)          │
├─────────────────────────────────────────┤
│              边缘节点                     │
│      (摄像头 + 传感器 + 语音终端)          │
└─────────────────────────────────────────┘
```

查看详细架构：[ARCHITECTURE.md](ARCHITECTURE.md)

## 🎯 核心场景

### 回家模式
> "我回家了" → 灯光渐亮、空调开启、音乐响起、今日摘要播报

### 安防监控
> 人形检测 → 异常事件标记 → 实时推送通知

### 老人/儿童看护
> 跌倒检测 → 异常报警 → 紧急联系

## 🔧 硬件生态

| 设备 | 型号 | 价格 | 购买 |
|------|------|------|------|
| Jeeves Box Lite | 树莓派5 8GB | ¥899 | [购买](https://jeeves-os.com/shop/lite) |
| Jeeves Box Pro | N100 16GB | ¥1999 | [购买](https://jeeves-os.com/shop/pro) |
| Jeeves Cam | 定制摄像头 | ¥399 | [购买](https://jeeves-os.com/shop/cam) |

## 💡 技能市场

社区贡献的技能插件：

- 🌅 [晨间 routine](https://github.com/jeeves-os/skill-morning-routine)
- 🍳 [智能厨房](https://github.com/jeeves-os/skill-smart-kitchen)
- 🐱 [宠物看护](https://github.com/jeeves-os/skill-pet-monitor)
- 📦 [快递提醒](https://github.com/jeeves-os/skill-delivery-tracker)

[查看更多 →](https://jeeves-os.com/skills)

## 🤝 贡献

我们欢迎各种形式的贡献！

- 🐛 [提交Bug](https://github.com/jeeves-os/jeeves-core/issues)
- 💡 [功能建议](https://github.com/jeeves-os/jeeves-core/discussions)
- 📝 [改进文档](https://github.com/jeeves-os/docs)
- 🔧 [贡献代码](CONTRIBUTING.md)

## 💬 社区

- [Discord](https://discord.gg/jeeves-os)
- [论坛](https://community.jeeves-os.com)
- [微信公众号：基维斯OS](https://mp.weixin.qq.com/s/jeevesos)

## 📄 许可证

- 代码: [Apache 2.0](LICENSE)
- 硬件设计: [CERN-OHL-P](LICENSE.hardware)
- 文档: [CC BY-SA 4.0](LICENSE.docs)

---

<p align="center">
  Made with ❤️ by the Jeeves OS Team
</p>
