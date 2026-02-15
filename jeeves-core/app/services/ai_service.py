import httpx
from typing import Optional, Dict, Any
from app.config import get_settings


class AIService:
    """AI对话服务"""
    
    def __init__(self):
        self.settings = get_settings()
        self.ollama_host = self.settings.OLLAMA_HOST
        self.ollama_model = self.settings.OLLAMA_MODEL
    
    async def chat(
        self,
        message: str,
        intent: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        与AI对话
        
        优先使用本地Ollama，如果不可用则降级处理
        """
        try:
            return await self._chat_with_ollama(message, intent, context)
        except Exception as e:
            # 本地模型失败，返回预设回复
            return self._fallback_response(message, intent)
    
    async def _chat_with_ollama(
        self,
        message: str,
        intent: Optional[str],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """使用本地Ollama模型"""
        
        # 构建系统提示
        system_prompt = self._build_system_prompt(intent)
        
        # 构建对话历史
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # 调用Ollama API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.ollama_model,
                    "messages": messages,
                    "stream": False
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
    
    def _build_system_prompt(self, intent: Optional[str]) -> str:
        """构建系统提示"""
        base_prompt = """你是基维斯(Jeeves)，一个智能家庭管家助手。你的职责是帮助用户管理家庭设备、自动化任务，并提供贴心的服务。

你应该：
1. 用温暖、专业的方式与用户交流
2. 理解用户的自然语言指令并执行相应操作
3. 主动提供有用的信息和建议
4. 保护用户隐私，所有数据本地处理

当前支持的功能：
- 控制灯光、空调等设备
- 设置自动化规则
- 回答家庭相关问题
"""
        
        if intent:
            base_prompt += f"\n用户意图识别为: {intent}\n"
        
        return base_prompt
    
    def _fallback_response(self, message: str, intent: Optional[str]) -> str:
        """降级回复（当AI服务不可用时）"""
        
        # 根据意图返回预设回复
        responses = {
            "turn_on_light": "好的，已为您开灯。",
            "turn_off_light": "好的，已为您关灯。",
            "set_temperature": "已调整空调温度。",
            "coming_home": "欢迎回家！已开启回家模式。",
            "weather": "抱歉，天气功能暂时不可用。",
            "greeting": "您好！我是基维斯，有什么可以帮您的吗？",
        }
        
        if intent and intent in responses:
            return responses[intent]
        
        return "收到您的指令，正在处理中。"
    
    async def generate_embedding(self, text: str) -> list:
        """生成文本嵌入向量（用于记忆系统）"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ollama_host}/api/embeddings",
                    json={
                        "model": "nomic-embed-text",
                        "prompt": text
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("embedding", [])
        except Exception:
            return []
