# Jeeves Web - 前端应用

基于 React + TypeScript + Tailwind CSS 的基维斯Web控制台。

## 技术栈

- **框架**: React 18 + Vite
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **组件库**: Headless UI / Radix UI
- **状态管理**: React Context + SWR
- **图表**: Recharts
- **图标**: Lucide React

## 功能模块

- 📊 仪表盘 - 设备状态概览
- 🏠 设备管理 - 控制与配置
- 💬 AI助手 - 对话界面
- ⚙️ 自动化 - 规则管理
- 🔧 系统设置

## 快速启动

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建
npm run build

# 预览
npm run preview
```

## API 配置

在 `.env` 中配置后端地址：
```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```
