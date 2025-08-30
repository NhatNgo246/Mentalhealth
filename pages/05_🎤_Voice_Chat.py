"""
🎤 SOULFRIEND V4.0 - Voice Chat with CHUN
=========================================

Voice-enabled chatbot với Speech-to-Text và Text-to-Speech
Tích hợp emotion recognition và real-time mood detection
"""

import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import io
import numpy as np
from typing import Optional, Dict, Any
import logging
from datetime import datetime

# Import CHUN AI system
from components.gemini_ai import GeminiAI
from components.logger import setup_logger

class VoiceChatManager:
    """
    Quản lý voice chat với CHUN AI
    """
    
    def __init__(self):
        self.logger = setup_logger("voice_chat")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = self._initialize_tts()
        self.chun_ai = GeminiAI()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Voice settings
        self.speech_rate = 150  # Words per minute
        self.speech_volume = 0.8
        self.language = 'vi-VN'  # Vietnamese
        
        # Emotion detection settings
        self.emotion_keywords = {
            'happy': ['vui', 'hạnh phúc', 'tốt', 'tuyệt vời', 'thích'],
            'sad': ['buồn', 'khóc', 'tệ', 'tồi tệ', 'chán'],
            'angry': ['tức', 'giận', 'bực', 'phát điên', 'cáu'],
            'anxious': ['lo lắng', 'căng thẳng', 'sợ', 'hồi hộp', 'bối rối'],
            'excited': ['hứng thú', 'phấn khích', 'háo hức', 'mong đợi']
        }
        
    def _initialize_tts(self) -> Optional[pyttsx3.Engine]:
        """Initialize Text-to-Speech engine"""
        try:
            engine = pyttsx3.init()
            
            # Set Vietnamese voice if available
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'vietnam' in voice.name.lower() or 'vi' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.setProperty('rate', self.speech_rate)
            engine.setProperty('volume', self.speech_volume)
            
            return engine
        except Exception as e:
            self.logger.error(f"TTS initialization failed: {e}")
            return None
    
    def detect_emotion_from_text(self, text: str) -> str:
        """
        Detect emotion from text using keyword matching
        """
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            detected_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = emotion_scores[detected_emotion] / len(text_lower.split())
            return f"{detected_emotion} (confidence: {confidence:.2f})"
        
        return "neutral"
    
    def speech_to_text(self, audio_data) -> Optional[str]:
        """
        Convert speech to text using Google Speech Recognition
        """
        try:
            # Use Google's speech recognition
            text = self.recognizer.recognize_google(
                audio_data, 
                language=self.language
            )
            self.logger.info(f"Speech recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
            return None
    
    def text_to_speech(self, text: str):
        """
        Convert text to speech
        """
        if not self.tts_engine:
            st.error("🔇 Text-to-Speech không khả dụng")
            return
        
        try:
            # Remove markdown formatting for TTS
            clean_text = text.replace('**', '').replace('*', '').replace('_', '')
            
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
            st.error(f"Lỗi Text-to-Speech: {e}")
    
    def listen_for_speech(self, duration: int = 5) -> Optional[str]:
        """
        Listen for speech input
        """
        try:
            with self.microphone as source:
                st.info(f"🎤 Đang nghe... (trong {duration} giây)")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                
                st.info("🔄 Đang xử lý giọng nói...")
                
                # Convert to text
                text = self.speech_to_text(audio)
                return text
                
        except sr.WaitTimeoutError:
            st.warning("⏱️ Hết thời gian nghe. Vui lòng thử lại.")
            return None
        except Exception as e:
            self.logger.error(f"Speech listening error: {e}")
            st.error(f"Lỗi khi nghe giọng nói: {e}")
            return None

def create_voice_chat_interface():
    """
    Create the voice chat interface
    """
    st.title("🎤 Voice Chat với CHUN")
    st.markdown("---")
    
    # Initialize voice chat manager
    if 'voice_manager' not in st.session_state:
        st.session_state.voice_manager = VoiceChatManager()
    
    voice_manager = st.session_state.voice_manager
    
    # Voice chat settings
    with st.expander("⚙️ Cài đặt Voice Chat"):
        col1, col2 = st.columns(2)
        
        with col1:
            speech_rate = st.slider(
                "Tốc độ nói (words/min)", 
                min_value=100, 
                max_value=300, 
                value=voice_manager.speech_rate
            )
            voice_manager.speech_rate = speech_rate
            
        with col2:
            speech_volume = st.slider(
                "Âm lượng", 
                min_value=0.1, 
                max_value=1.0, 
                value=voice_manager.speech_volume
            )
            voice_manager.speech_volume = speech_volume
        
        if voice_manager.tts_engine:
            voice_manager.tts_engine.setProperty('rate', speech_rate)
            voice_manager.tts_engine.setProperty('volume', speech_volume)
    
    # Chat history
    if 'voice_chat_history' not in st.session_state:
        st.session_state.voice_chat_history = []
    
    # Display chat history
    st.subheader("💬 Cuộc trò chuyện")
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.voice_chat_history:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(f"🎤 **Bạn**: {message['content']}")
                    if 'emotion' in message:
                        st.caption(f"😊 Cảm xúc: {message['emotion']}")
            else:
                with st.chat_message("assistant"):
                    st.write(f"🤖 **CHUN**: {message['content']}")
    
    # Voice input controls
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎤 Bắt đầu nói", key="start_voice"):
            with st.spinner("Đang nghe..."):
                user_speech = voice_manager.listen_for_speech(duration=10)
                
                if user_speech:
                    st.success(f"✅ Đã nghe: {user_speech}")
                    
                    # Detect emotion
                    emotion = voice_manager.detect_emotion_from_text(user_speech)
                    
                    # Add to chat history
                    st.session_state.voice_chat_history.append({
                        'role': 'user',
                        'content': user_speech,
                        'emotion': emotion,
                        'timestamp': datetime.now()
                    })
                    
                    # Get CHUN response
                    with st.spinner("CHUN đang suy nghĩ..."):
                        # Enhanced prompt with emotion context
                        enhanced_prompt = f"""
                        Tin nhắn: {user_speech}
                        Cảm xúc phát hiện: {emotion}
                        
                        Hãy trả lời như CHUN với tính cách đồng cảm, 
                        đặc biệt chú ý đến cảm xúc được phát hiện.
                        """
                        
                        chun_response = voice_manager.chun_ai.get_response(enhanced_prompt)
                        
                        if chun_response:
                            # Add CHUN response to history
                            st.session_state.voice_chat_history.append({
                                'role': 'assistant',
                                'content': chun_response,
                                'timestamp': datetime.now()
                            })
                            
                            st.success("✅ CHUN đã trả lời!")
                            st.rerun()
                        else:
                            st.error("❌ CHUN không thể trả lời lúc này")
                else:
                    st.warning("❌ Không nghe được giọng nói")
    
    with col2:
        if st.button("🔊 Đọc tin nhắn cuối", key="read_last"):
            if st.session_state.voice_chat_history:
                last_message = st.session_state.voice_chat_history[-1]
                if last_message['role'] == 'assistant':
                    with st.spinner("Đang đọc..."):
                        voice_manager.text_to_speech(last_message['content'])
                    st.success("✅ Đã đọc xong!")
                else:
                    st.info("Tin nhắn cuối không phải từ CHUN")
            else:
                st.warning("Chưa có tin nhắn nào")
    
    with col3:
        if st.button("🗑️ Xóa lịch sử", key="clear_voice_history"):
            st.session_state.voice_chat_history = []
            st.success("✅ Đã xóa lịch sử chat")
            st.rerun()
    
    # Text input fallback
    st.markdown("---")
    st.subheader("⌨️ Hoặc gõ tin nhắn")
    
    text_input = st.text_input(
        "Nhập tin nhắn cho CHUN:",
        placeholder="Gõ tin nhắn hoặc sử dụng voice chat ở trên..."
    )
    
    if st.button("📤 Gửi tin nhắn", key="send_text"):
        if text_input:
            # Detect emotion from text
            emotion = voice_manager.detect_emotion_from_text(text_input)
            
            # Add to chat history
            st.session_state.voice_chat_history.append({
                'role': 'user',
                'content': text_input,
                'emotion': emotion,
                'timestamp': datetime.now()
            })
            
            # Get CHUN response
            with st.spinner("CHUN đang trả lời..."):
                enhanced_prompt = f"""
                Tin nhắn: {text_input}
                Cảm xúc phát hiện: {emotion}
                
                Hãy trả lời như CHUN với tính cách đồng cảm.
                """
                
                chun_response = voice_manager.chun_ai.get_response(enhanced_prompt)
                
                if chun_response:
                    # Add CHUN response to history
                    st.session_state.voice_chat_history.append({
                        'role': 'assistant',
                        'content': chun_response,
                        'timestamp': datetime.now()
                    })
                    
                    st.rerun()
    
    # Voice chat statistics
    st.markdown("---")
    st.subheader("📊 Thống kê Voice Chat")
    
    if st.session_state.voice_chat_history:
        user_messages = [m for m in st.session_state.voice_chat_history if m['role'] == 'user']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💬 Tin nhắn", len(st.session_state.voice_chat_history))
        
        with col2:
            st.metric("🎤 Voice inputs", 
                     sum(1 for m in user_messages if 'emotion' in m))
        
        with col3:
            if user_messages:
                emotions = [m.get('emotion', 'neutral') for m in user_messages if 'emotion' in m]
                most_common_emotion = max(set(emotions), key=emotions.count) if emotions else 'neutral'
                st.metric("😊 Cảm xúc chủ đạo", most_common_emotion)
    
    # Tips and instructions
    with st.expander("💡 Hướng dẫn sử dụng Voice Chat"):
        st.markdown("""
        ### 🎤 **Cách sử dụng Voice Chat:**
        
        1. **Bấm nút "🎤 Bắt đầu nói"**
        2. **Nói rõ ràng** trong vòng 10 giây
        3. **CHUN sẽ phân tích cảm xúc** và trả lời phù hợp
        4. **Bấm "🔊 Đọc tin nhắn cuối"** để nghe CHUN nói
        
        ### 🔧 **Tính năng:**
        - ✅ **Speech-to-Text**: Chuyển giọng nói thành text
        - ✅ **Text-to-Speech**: CHUN có thể đọc phản hồi
        - ✅ **Emotion Detection**: Phân tích cảm xúc từ giọng nói
        - ✅ **Context Awareness**: CHUN hiểu ngữ cảnh cảm xúc
        
        ### 📝 **Lưu ý:**
        - Cần **microphone và speakers** để sử dụng đầy đủ tính năng
        - **Nói tiếng Việt** để kết quả tốt nhất
        - Có thể **kết hợp voice và text** trong cùng cuộc trò chuyện
        """)

if __name__ == "__main__":
    # Required dependencies check
    try:
        import speech_recognition
        import pyttsx3
        create_voice_chat_interface()
    except ImportError as e:
        st.error(f"""
        🚫 **Thiếu dependencies cho Voice Chat**
        
        Cần cài đặt: `{e.name}`
        
        Chạy lệnh:
        ```bash
        pip install speech-recognition pyttsx3 pyaudio
        ```
        """)
