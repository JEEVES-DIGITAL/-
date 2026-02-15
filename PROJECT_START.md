# 基维斯 (Jeeves OS) 项目启动指南

## 项目概述

**基维斯** 是一个开源的家庭智能操作系统，定位为家庭的AI大脑。通过本地AI + 云端增强的混合架构，实现真正的智能家庭管理。

- **定位**: 开源家庭智能操作系统
- **核心**: 本地AI大脑 + 分布式节点
- **模式**: 开源免费 + 云服务增值 + 硬件销售
- **周期**: 90天MVP到众筹

## 文件结构

```
projects/jeeves-os/
├── ARCHITECTURE.md         # 系统架构设计文档
├── README.md               # 项目主页
├── LICENSE                 # Apache 2.0 开源协议
├── CONTRIBUTING.md         # 贡献指南
├── ROADMAP.md              # 90天执行路线图
├── docker-compose.yml      # 生产环境配置
├── docker-compose.dev.yml  # 开发环境配置
├── install.sh              # 一键安装脚本
├── .gitignore              # Git忽略规则
├── docs/                   # 文档中心
│   └── getting-started.md  # 快速开始指南
├── scripts/                # 工具脚本
│   └── init-github.sh      # GitHub仓库初始化
├── jeeves-core/            # AI大脑核心 (待开发)
├── jeeves-hub/             # 设备中枢 (待开发)
├── jeeves-nodes/           # 边缘节点 (待开发)
└── assets/                 # 品牌资产 (待补充)
    └── logo.png            # 品牌Logo
```

## 立即执行

### 1. 品牌资产

需要设计：
- [ ] Logo (主Logo + 图标版)
- [ ] 品牌配色方案
- [ ] 官网设计稿

### 2. GitHub 上线

```bash
# 运行初始化脚本
cd projects/jeeves-os
./scripts/init-github.sh

# 或手动创建组织后，推送代码
cd jeeves-core
git init
git add .
git commit -m "Initial commit: Jeeves OS Core"
git branch -M main
git remote add origin https://github.com/jeeves-os/jeeves-core.git
git push -u origin main
```

### 3. 开发环境启动

```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 检查服务状态
docker-compose -f docker-compose.dev.yml ps
```

## 本周任务

| 优先级 | 任务 | 负责人 | 截止时间 |
|--------|------|--------|----------|
| P0 | Logo设计 | 外包/设计师 | Day 2 |
| P0 | GitHub仓库上线 | Boss | Day 3 |
| P0 | 后端API脚手架 | 开发 | Day 5 |
| P1 | 域名购买+备案 | Boss | Day 7 |
| P1 | 首批开发招聘 | Boss | Day 7 |

## 里程碑

- **Day 7**: GitHub 仓库开源，后端基础API可调用
- **Day 30**: 回家模式闭环，能用的MVP
- **Day 60**: 三大场景完整，GitHub开源发布
- **Day 90**: Jeeves Box 众筹上线

## 资源链接

- 架构文档: [ARCHITECTURE.md](ARCHITECTURE.md)
- 路线图: [ROADMAP.md](ROADMAP.md)
- 快速开始: [docs/getting-started.md](docs/getting-started.md)

---

**基维斯 - 让每个家庭都有自己的AI管家** 🤵
