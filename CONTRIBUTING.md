# 贡献指南

感谢你对基维斯 (Jeeves OS) 的兴趣！本指南将帮助你参与到项目中。

## 如何贡献

### 报告问题

1. 确认问题尚未被报告
2. 使用 issue 模板创建新 issue
3. 提供详细的问题描述和复现步骤
4. 附上系统环境和日志信息

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 开发环境

### 前置要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/jeeves-os/jeeves-core.git
cd jeeves-core

# 安装依赖
pip install -r requirements-dev.txt
npm install

# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 运行测试
pytest
npm test
```

## 代码规范

### Python

- 遵循 PEP 8
- 使用 Black 格式化代码
- 使用 isort 排序导入
- 类型注解推荐但非强制

### TypeScript/JavaScript

- 使用 ESLint + Prettier
- 遵循项目已有的 tsconfig 配置

### 提交信息

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 添加新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建/工具相关
```

## 技能开发

如果你想开发新的技能插件，请参考 [技能开发文档](docs/skill-development.md)。

## 行为准则

- 友善和耐心
- 欢迎新成员
- 尊重不同观点
- 专注于最有益于社区的事

## 联系方式

- Discord: https://discord.gg/jeeves-os
- 邮件: dev@jeeves-os.com

感谢你的贡献！
