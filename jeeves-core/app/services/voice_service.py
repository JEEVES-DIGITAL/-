# Jeeves Voice Service
# 基维斯语音服务 - faster-whisper + edge-tts

import asyncio
import tempfile
import os
from pathlib import Path
from typing import Optional, Callable
import subprocess

# 尝试导入 faster-whisper
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ faster-whisper 未安装，运行: pip3 install faster-whisper")

# 尝试导入 edge-tts
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ edge-tts 未安装，运行: pip3 install edge-tts")

# 尝试导入 ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️ ollama 未安装，运行: pip3 install ollama")


class JeevesVoiceService:
    """
    基维斯语音服务
    
    功能：
    1. 语音识别 (STT): faster-whisper 本地识别
    2. AI对话: Ollama 本地大模型
    3. 语音合成 (TTS): edge-tts 播报
    """
    
    # 中文语音配置
    VOICES = {
        "male_calm": "zh-CN-YunjianNeural",      # 稳重男声 - 推荐
        "male_magnetic": "zh-CN-YunxiNeural",     # 磁性男声
        "female_gentle": "zh-CN-XiaoxiaoNeural",  # 温柔女声
        "female_cute": "zh-CN-XiaoyiNeural",      # 可爱女声
    }
    
    def __init__(
        self,
        whisper_model: str = "base",
        llm_model: str = "phi4",
        voice: str = "male_calm",
        device: str = "cpu"
    ):
        """
        初始化语音服务
        
        Args:
            whisper_model: 语音识别模型 (tiny/base/small/medium/large)
            llm_model: 本地LLM模型 (phi4/glm4/llama3)
            voice: TTS声音类型
            device: 运行设备 (cpu/cuda)
        """
        self.whisper_model_name = whisper_model
        self.llm_model = llm_model
        self.voice = self.VOICES.get(voice, self.VOICES["male_calm"])
        self.device = device
        
        # 初始化组件
        self._init_whisper()
        self._init_ollama()
        
        print(f"🎙️ 基维斯语音服务已启动")
        print(f"   - 语音识别: faster-whisper ({whisper_model})")
        print(f"   - 大模型: {llm_model}")
        print(f"   - 语音合成: {self.voice}")
    
    def _init_whisper(self):
        """初始化语音识别模型"""
        if not WHISPER_AVAILABLE:
            raise RuntimeError("faster-whisper 未安装")
        
        print(f"🔄 加载语音识别模型: {self.whisper_model_name}...")
        self.whisper = WhisperModel(
            self.whisper_model_name,
            device=self.device,
            compute_type="int8"  # 量化加速
        )
        print("✅ 语音识别模型加载完成")
    
    def _init_ollama(self):
        """检查Ollama服务"""
        if not OLLAMA_AVAILABLE:
            raise RuntimeError("ollama 未安装")
        
        try:
            # 检查模型是否存在
            ollama.show(self.llm_model)
            print(f"✅ Ollama模型已就绪: {self.llm_model}")
        except Exception as e:
            print(f"⚠️ Ollama模型 {self.llm_model} 可能未下载")
            print(f"   运行: ollama pull {self.llm_model}")
    
    def listen(self, audio_path: str) -> str:
        """
        语音识别：听懂用户说的话
        
        Args:
            audio_path: 音频文件路径 (wav/mp3/m4a)
            
        Returns:
            识别的文字
        """
        if not WHISPER_AVAILABLE:
            raise RuntimeError("faster-whisper 未安装")
        
        print(f"🎤 识别音频: {audio_path}")
        
        # 语音识别
        segments, info = self.whisper.transcribe(
            audio_path,
            beam_size=5,
            language="zh"  # 指定中文
        )
        
        # 合并所有片段
        text = " ".join([segment.text for segment in segments])
        text = text.strip()
        
        print(f"👂 识别结果: {text}")
        print(f"   语言: {info.language}, 概率: {info.language_probability:.2f}")
        
        return text
    
    def think(self, text: str, system_prompt: Optional[str] = None) -> str:
        """
        AI思考：理解意图并生成回复
        
        Args:
            text: 用户输入
            system_prompt: 系统提示词（可选）
            
        Returns:
            AI回复
        """
        if not OLLAMA_AVAILABLE:
            raise RuntimeError("ollama 未安装")
        
        # 默认贾维斯人格
        if system_prompt is None:
            system_prompt = """你是基维斯(Jeeves)，智能家庭管家。
风格：专业、高效、略带英式管家气质。
能力：控制智能家居设备、回答问题、提供建议。
回答简洁，不超过100字。"""
        
        print(f"🧠 思考中...")
        
        response = ollama.chat(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            options={
                "temperature": 0.7,
                "num_predict": 200  # 限制生成长度
            }
        )
        
        reply = response.message.content
        print(f"💭 回复: {reply}")
        
        return reply
    
    async def speak(self, text: str, output_path: Optional[str] = None) -> str:
        """
        语音合成：播报回复
        
        Args:
            text: 要播报的文字
            output_path: 输出音频路径（可选）
            
        Returns:
            音频文件路径
        """
        if not EDGE_TTS_AVAILABLE:
            raise RuntimeError("edge-tts 未安装")
        
        if output_path is None:
            output_path = tempfile.mktemp(suffix=".mp3")
        
        print(f"🔊 合成语音: {text[:50]}...")
        
        # 合成语音
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        
        print(f"✅ 语音已保存: {output_path}")
        
        return output_path
    
    def play_audio(self, audio_path: str):
        """播放音频文件"""
        if os.path.exists(audio_path):
            if os.system("which afplay") == 0:  # macOS
                subprocess.run(["afplay", audio_path])
            elif os.system("which aplay") == 0:  # Linux
                subprocess.run(["aplay", audio_path])
            else:
                print(f"⚠️ 无法自动播放，文件位置: {audio_path}")
        else:
            print(f"⚠️ 音频文件不存在: {audio_path}")
    
    async def chat(self, audio_input: str, play: bool = True) -> dict:
        """
        完整语音对话流程
        
        Args:
            audio_input: 输入音频文件路径
            play: 是否自动播放回复
            
        Returns:
            对话结果字典
        """
        result = {
            "success": False,
            "user_text": "",
            "ai_text": "",
            "audio_path": "",
            "error": ""
        }
        
        try:
            # Step 1: 听懂
            user_text = self.listen(audio_input)
            result["user_text"] = user_text
            
            if not user_text:
                result["error"] = "未能识别语音"
                return result
            
            # Step 2: 思考
            ai_text = self.think(user_text)
            result["ai_text"] = ai_text
            
            # Step 3: 说话
            audio_path = await self.speak(ai_text)
            result["audio_path"] = audio_path
            
            # 播放
            if play:
                self.play_audio(audio_path)
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            print(f"❌ 错误: {e}")
        
        return result
    
    def record_and_chat(self, duration: int = 5) -> dict:
        """
        录音并对话（简化版）
        
        Args:
            duration: 录音时长（秒）
            
        Returns:
            对话结果
        """
        import sounddevice as sd
        import wavio
        
        print(f"🎙️ 录音 {duration} 秒，请说话...")
        
        # 录音
        fs = 16000  # 采样率
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        
        # 保存
        temp_file = tempfile.mktemp(suffix=".wav")
        wavio.write(temp_file, recording, fs, sampwidth=2)
        
        print(f"✅ 录音完成: {temp_file}")
        
        # 对话
        return asyncio.run(self.chat(temp_file))


# 快速测试
if __name__ == "__main__":
    print("🦞 基维斯语音服务测试\n")
    
    # 初始化
    jeeves = JeevesVoiceService(
        whisper_model="base",  # 小模型，速度快
        llm_model="phi4",      # 本地Phi-4
        voice="male_calm"      # 稳重男声
    )
    
    # 测试音频文件
    test_audio = "/tmp/test.wav"
    
    if os.path.exists(test_audio):
        print(f"\n🎤 测试语音识别: {test_audio}")
        result = asyncio.run(jeeves.chat(test_audio))
        
        print("\n📊 结果:")
        print(f"   用户说: {result['user_text']}")
        print(f"   AI回复: {result['ai_text']}")
        print(f"   音频文件: {result['audio_path']}")
    else:
        print(f"\n⚠️ 测试音频不存在: {test_audio}")
        print("   请提供音频文件路径运行测试")
        print("   或使用: jeeves.record_and_chat(5)")
