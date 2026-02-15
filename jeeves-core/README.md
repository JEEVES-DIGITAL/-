# Jeeves Core - AI大脑核心服务

## 技术栈

- **框架**: FastAPI + Uvicorn
- **数据库**: PostgreSQL + SQLAlchemy + Alembic
- **缓存**: Redis
- **AI**: Ollama (本地) + OpenAI/Claude (云端增强)
- **消息**: WebSocket + MQTT
- **任务队列**: Celery (可选)

## 项目结构

```
jeeves-core/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # 数据模型
│   ├── routers/             # API路由
│   ├── services/            # 业务逻辑
│   └── utils/               # 工具函数
├── tests/                   # 测试
├── scripts/                 # 工具脚本
├── alembic/                 # 数据库迁移
├── requirements.txt         # 依赖
└── Dockerfile               # 容器化
```

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问文档
http://localhost:8000/docs
```
