#!/usr/bin/env python3
"""
基维斯语音测试脚本
测试 faster-whisper + edge-tts + ollama 完整流程
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.voice_service import JeevesVoiceService


async def test_text_to_speech():
    """测试语音合成"""
    print("\n🎯 测试1: 语音合成 (edge-tts)")
    print("-" * 50)
    
    try:
        import edge_tts
        
        text = "你好，我是基维斯，你的智能管家。"
        voice = "zh-CN-YunjianNeural"
        
        print(f"📝 输入文字: {text}")
        print(f"🎙️ 使用声音: {voice}")
        
        communicate = edge_tts.Communicate(text, voice)
        output_file = "/tmp/test_tts.mp3"
        await communicate.save(output_file)
        
        print(f"✅ 语音合成成功: {output_file}")
        
        # 播放
        if os.system("which afplay") == 0:
            print("🔊 播放音频...")
            os.system(f"afplay {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False


async def test_speech_to_text():
    """测试语音识别（需要音频文件）"""
    print("\n🎯 测试2: 语音识别 (faster-whisper)")
    print("-" * 50)
    
    try:
        from faster_whisper import WhisperModel
        
        print("🔄 加载模型 (base)...")
        model = WhisperModel("base", device="cpu", compute_type="int8")
        
        # 创建一个测试音频（如果没有）
        test_audio = "/tmp/test_audio.wav"
        if not os.path.exists(test_audio):
            print(f"⚠️ 测试音频不存在: {test_audio}")
            print("   跳过此测试")
            return None
        
        print(f"🎤 识别音频: {test_audio}")
        segments, info = model.transcribe(test_audio, beam_size=5)
        
        text = " ".join([s.text for s in segments])
        print(f"👂 识别结果: {text}")
        print(f"   语言: {info.language}")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False


async def test_llm():
    """测试本地LLM"""
    print("\n🎯 测试3: 本地大模型 (Ollama)")
    print("-" * 50)
    
    try:
        import ollama
        
        model = "gemma3:27b"
        print(f"🤖 测试模型: {model}")
        
        response = ollama.chat(
            model=model,
            messages=[{
                "role": "user",
                "content": "你好，请简短介绍一下自己"
            }]
        )
        
        reply = response.message.content
        print(f"💭 AI回复: {reply[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}")
        print("   提示: 请确保Ollama已安装并运行")
        print("   运行: ollama run gemma3:27b")
        return False


async def test_full_pipeline():
    """测试完整语音对话流程"""
    print("\n🎯 测试4: 完整语音对话流程")
    print("-" * 50)
    
    try:
        jeeves = JeevesVoiceService(
            whisper_model="base",
            llm_model="gemma3:27b",
            voice="male_calm"
        )
        
        # 测试文字对话（跳过语音输入）
        print("📝 测试文字对话...")
        
        # 模拟用户输入
        user_text = "我回家了"
        print(f"👤 用户: {user_text}")
        
        # AI思考
        ai_text = jeeves.think(user_text)
        print(f"🤖 AI: {ai_text}")
        
        # AI说话
        audio_path = await jeeves.speak(ai_text)
        print(f"🔊 语音已生成: {audio_path}")
        
        # 播放
        if os.path.exists(audio_path):
            if os.system("which afplay") == 0:
                print("🔊 播放回复...")
                os.system(f"afplay {audio_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """运行所有测试"""
    print("🦞 基维斯语音服务测试")
    print("=" * 50)
    print("组件: faster-whisper + edge-tts + ollama")
    print("=" * 50)
    
    results = []
    
    # 测试1: TTS
    results.append(("语音合成", await test_text_to_speech()))
    
    # 测试2: STT (需要音频文件)
    results.append(("语音识别", await test_speech_to_text()))
    
    # 测试3: LLM
    results.append(("本地LLM", await test_llm()))
    
    # 测试4: 完整流程
    results.append(("完整流程", await test_full_pipeline()))
    
    # 汇总
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    for name, result in results:
        if result is True:
            status = "✅ 通过"
        elif result is False:
            status = "❌ 失败"
        else:
            status = "⏭️ 跳过"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)
    
    print(f"\n总计: {passed}通过, {failed}失败, {skipped}跳过")
    
    if failed == 0:
        print("\n🎉 所有测试通过！基维斯语音服务已就绪。")
    else:
        print("\n⚠️ 部分测试失败，请检查依赖安装。")


if __name__ == "__main__":
    asyncio.run(main())
