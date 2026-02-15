from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db
from app.routers import system, devices, chat, automations, voice
from app.routers.voice import init_voice_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    settings = get_settings()
    print(f"🚀 启动 {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # 初始化数据库
    await init_db()
    print("✅ 数据库初始化完成")
    
    # 初始化语音服务（可选，失败不阻断启动）
    try:
        init_voice_service()
    except Exception as e:
        print(f"⚠️ 语音服务初始化失败: {e}")
    
    yield
    
    # 关闭时清理
    print("👋 服务关闭")


# 创建FastAPI应用
settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基维斯AI大脑核心服务 - 开源家庭智能操作系统",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(system.router)
app.include_router(devices.router)
app.include_router(chat.router)
app.include_router(automations.router)
app.include_router(voice.router)


# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket实时通信"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理消息
            await websocket.send_json({
                "type": "echo",
                "message": data,
                "status": "connected"
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/system/health"
    }
