"""
SOULFRIEND V2.0 - Advanced NLP Chatbot
Chatbot hỗ trợ tâm lý với xử lý ngôn ngữ tự nhiên tiên tiến
"""
import json
import sqlite3
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
import logging
from dataclasses import dataclass
import asyncio

# NLP Libraries
import nltk
import spacy
from underthesea import word_tokenize, pos_tag, ner, sentiment
from langdetect import detect
from sentence_transformers import SentenceTransformer

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Tin nhắn chat"""
    id: str
    user_id: str
    message: str
    intent: str
    sentiment: str
    confidence: float
    response: str
    timestamp: datetime

@dataclass
class UserContext:
    """Bối cảnh người dùng"""
    user_id: str
    current_session: str
    conversation_history: List[ChatMessage]
    user_profile: Dict[str, Any]
    emotional_state: str
    risk_level: str

class MentalHealthNLPChatbot:
    """Chatbot hỗ trợ tâm lý với NLP tiên tiến"""
    
    def __init__(self):
        self.db_path = "/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/data/chatbot.db"
        self.init_database()
        
        # Load NLP models
        self.init_nlp_models()
        
        # Mental health keywords and patterns
        self.mental_health_keywords = {
            "depression": ["buồn", "chán nản", "tuyệt vọng", "không muốn", "mệt mỏi", "depression", "trầm cảm"],
            "anxiety": ["lo lắng", "căng thẳng", "sợ hãi", "bồn chồn", "anxiety", "anxiety", "hoang mang"],
            "stress": ["stress", "áp lực", "căng thẳng", "mệt mỏi", "quá tải", "overwhelmed"],
            "suicide": ["tự tử", "chết", "kết thúc", "suicide", "không muốn sống", "tự sát"],
            "sleep": ["ngủ", "mất ngủ", "insomnia", "thức khuya", "ngủ không sâu", "ác mông"],
            "eating": ["ăn uống", "không ăn", "ăn nhiều", "eating disorder", "chán ăn"],
            "relationship": ["gia đình", "bạn bè", "tình yêu", "cô đơn", "relationship", "hôn nhân"],
            "work": ["công việc", "học tập", "deadline", "sếp", "đồng nghiệp", "burnout"],
            "help": ["giúp đỡ", "hỗ trợ", "tư vấn", "help", "advice", "suggestion"]
        }
        
        # Emotional states
        self.emotional_states = {
            "very_positive": ["rất tích cực", "rất vui", "hạnh phúc", "tuyệt vời"],
            "positive": ["tích cực", "vui", "ổn", "khá tốt"],
            "neutral": ["bình thường", "trung tính", "không biết"],
            "negative": ["tiêu cực", "buồn", "không tốt", "tệ"],
            "very_negative": ["rất tiêu cực", "rất buồn", "tuyệt vọng", "khủng khiếp"]
        }
        
        # Response templates
        self.response_templates = {
            "greeting": [
                "Xin chào! Tôi là SOULFRIEND, trợ lý tâm lý của bạn. Hôm nay bạn cảm thấy thế nào?",
                "Chào bạn! Tôi luôn sẵn sàng lắng nghe và hỗ trợ bạn. Có điều gì bạn muốn chia sẻ không?",
                "Xin chào! Rất vui được gặp bạn. Bạn có muốn nói về cảm xúc hiện tại của mình không?"
            ],
            "depression": [
                "Tôi hiểu bạn đang cảm thấy buồn. Điều này rất bình thường và bạn không đơn độc. Bạn có muốn chia sẻ thêm về những gì đang làm bạn cảm thấy như vậy không?",
                "Cảm giác buồn chán là một phần của cuộc sống. Tôi ở đây để lắng nghe. Có điều gì cụ thể đang làm bạn lo lắng không?",
                "Tôi thấu hiểu cảm giác này. Hãy nhớ rằng những cảm xúc tiêu cực sẽ qua đi. Bạn có muốn thử một số kỹ thuật thư giãn không?"
            ],
            "anxiety": [
                "Lo lắng là phản ứng tự nhiên của cơ thể. Hãy thử hít thở sâu và từ từ thở ra. Bạn có muốn tôi hướng dẫn một bài tập thở không?",
                "Tôi hiểu cảm giác lo lắng này. Hãy cố gắng tập trung vào hiện tại. Bạn có thể kể cho tôi nghe 3 thứ bạn có thể nhìn thấy xung quanh không?",
                "Cảm giác lo lắng sẽ qua đi. Hãy nhớ rằng bạn đã vượt qua những khó khăn trước đây. Có điều gì cụ thể đang làm bạn lo lắng không?"
            ],
            "suicide": [
                "Tôi rất lo lắng cho bạn. Những suy nghĩ này rất nghiêm trọng. Hãy gọi ngay đường dây nóng 1900-6969 hoặc đến bệnh viện gần nhất. Bạn cần được hỗ trợ chuyên nghiệp ngay lập tức.",
                "Đây là tình huống khẩn cấp. Tôi khuyên bạn nên liên hệ ngay với chuyên gia tâm lý hoặc gọi cấp cứu. Cuộc sống của bạn có giá trị và có những người sẵn sàng giúp đỡ.",
                "Tôi hiểu bạn đang trải qua thời gian rất khó khăn. Nhưng hãy nhớ rằng có những giải pháp và sự giúp đỡ. Vui lòng liên hệ ngay với đường dây cấp cứu tâm lý."
            ],
            "support": [
                "Bạn đã rất dũng cảm khi chia sẻ điều này. Tôi ở đây để hỗ trợ bạn.",
                "Cảm ơn bạn đã tin tưởng tôi. Chúng ta sẽ cùng nhau tìm cách giải quyết.",
                "Tôi rất trân trọng sự cởi mở của bạn. Hãy cùng nhau tìm những cách tích cực để đối phó."
            ]
        }
        
        # Crisis keywords for immediate escalation
        self.crisis_keywords = [
            "tự tử", "tự sát", "chết", "kết thúc cuộc đời", "không muốn sống",
            "suicide", "kill myself", "end it all", "want to die"
        ]
    
    def init_database(self):
        """Khởi tạo cơ sở dữ liệu chatbot"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng cuộc trò chuyện
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                intent TEXT,
                sentiment TEXT,
                confidence REAL,
                emotional_state TEXT,
                risk_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng hồ sơ người dùng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                mental_health_history TEXT,
                current_medications TEXT,
                emergency_contact TEXT,
                preferences TEXT,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng phiên chat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                risk_assessment TEXT,
                recommendations TEXT,
                requires_followup BOOLEAN DEFAULT 0
            )
        ''')
        
        # Bảng cảnh báo khẩn cấp
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crisis_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                message TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                action_taken TEXT,
                resolved BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Chatbot database initialized")
    
    def init_nlp_models(self):
        """Khởi tạo các mô hình NLP"""
        try:
            # Load Vietnamese sentence transformer
            self.sentence_model = SentenceTransformer('keepitreal/vietnamese-sbert')
            logger.info("✅ Sentence transformer loaded")
        except:
            # Fallback to English model
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Fallback sentence transformer loaded")
        
        # Initialize other NLP components
        self.stopwords = set(['là', 'của', 'và', 'có', 'trong', 'một', 'được', 'với', 'này', 'để', 'cho', 'không', 'tôi', 'bạn'])
        
        logger.info("✅ NLP models initialized")
    
    def preprocess_text(self, text: str) -> str:
        """Tiền xử lý văn bản tiếng Việt"""
        # Lowercase
        text = text.lower()
        
        # Remove special characters but keep Vietnamese characters
        text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def extract_intent(self, text: str) -> Tuple[str, float]:
        """Trích xuất ý định từ văn bản"""
        text_lower = text.lower()
        intent_scores = {}
        
        # Check for each mental health category
        for category, keywords in self.mental_health_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            if score > 0:
                intent_scores[category] = score / len(keywords)
        
        if not intent_scores:
            return "general", 0.5
        
        # Return intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        return best_intent, min(confidence * 2, 1.0)  # Scale confidence
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Phân tích cảm xúc văn bản"""
        try:
            # Use underthesea for Vietnamese sentiment analysis
            sentiment_result = sentiment(text)
            
            if sentiment_result == "POS":
                return "positive", 0.7
            elif sentiment_result == "NEG":
                return "negative", 0.7
            else:
                return "neutral", 0.6
                
        except:
            # Fallback: simple keyword-based sentiment
            positive_words = ["vui", "hạnh phúc", "tốt", "ổn", "khỏe", "tuyệt"]
            negative_words = ["buồn", "tệ", "khó khăn", "lo lắng", "stress", "mệt"]
            
            text_lower = text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                return "positive", 0.6
            elif neg_count > pos_count:
                return "negative", 0.6
            else:
                return "neutral", 0.5
    
    def assess_risk_level(self, text: str, sentiment: str, intent: str) -> str:
        """Đánh giá mức độ rủi ro"""
        # Crisis keywords = immediate high risk
        if any(keyword in text.lower() for keyword in self.crisis_keywords):
            return "critical"
        
        # Depression + very negative sentiment = high risk
        if intent == "depression" and sentiment == "very_negative":
            return "high"
        
        # Anxiety or stress with negative sentiment = medium risk
        if intent in ["anxiety", "stress"] and sentiment == "negative":
            return "medium"
        
        # Positive sentiment = low risk
        if sentiment in ["positive", "very_positive"]:
            return "low"
        
        return "medium"
    
    def generate_response(self, intent: str, sentiment: str, risk_level: str, user_message: str) -> str:
        """Tạo phản hồi dựa trên ý định và cảm xúc"""
        
        # Crisis response
        if risk_level == "critical":
            return self.get_crisis_response()
        
        # Intent-based responses
        if intent in self.response_templates:
            import random
            base_response = random.choice(self.response_templates[intent])
        else:
            base_response = random.choice(self.response_templates["support"])
        
        # Add personalized elements based on sentiment and risk
        if risk_level == "high":
            base_response += "\n\nTôi khuyên bạn nên tìm kiếm sự hỗ trợ từ chuyên gia tâm lý. Bạn có muốn tôi giúp đặt lịch hẹn không?"
        elif sentiment == "very_negative":
            base_response += "\n\nHãy nhớ rằng mọi thứ sẽ tốt lên. Bạn có muốn thử một số kỹ thuật thư giãn không?"
        
        return base_response
    
    def get_crisis_response(self) -> str:
        """Phản hồi khẩn cấp cho tình huống nguy cơ cao"""
        return """
🚨 TÌNH HUỐNG KHẨN CẤP 🚨

Tôi rất lo lắng cho an toàn của bạn. Vui lòng liên hệ ngay:

📞 Đường dây nóng 24/7: 1900-6969
🏥 Cấp cứu: 115
👨‍⚕️ Tâm lý khẩn cấp: 1800-1567

Bạn không đơn độc. Có những người chuyên nghiệp sẵn sàng giúp đỡ bạn ngay bây giờ.

Hãy đến bệnh viện gần nhất hoặc gọi cho người thân tin cậy.
        """
    
    async def process_message(self, user_id: str, session_id: str, message: str) -> Dict[str, Any]:
        """Xử lý tin nhắn từ người dùng"""
        try:
            # Preprocess message
            cleaned_message = self.preprocess_text(message)
            
            # Extract intent and sentiment
            intent, intent_confidence = self.extract_intent(message)
            sentiment, sentiment_confidence = self.analyze_sentiment(message)
            
            # Assess risk level
            risk_level = self.assess_risk_level(message, sentiment, intent)
            
            # Generate response
            response = self.generate_response(intent, sentiment, risk_level, message)
            
            # Store conversation
            conversation_id = self.store_conversation(
                session_id, user_id, message, response, 
                intent, sentiment, intent_confidence, risk_level
            )
            
            # Handle crisis situations
            if risk_level == "critical":
                self.create_crisis_alert(user_id, session_id, message, risk_level)
            
            # Update session
            self.update_session(session_id, risk_level)
            
            return {
                "conversation_id": conversation_id,
                "response": response,
                "intent": intent,
                "sentiment": sentiment,
                "confidence": intent_confidence,
                "risk_level": risk_level,
                "requires_followup": risk_level in ["high", "critical"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "response": "Xin lỗi, tôi gặp một chút trục trặc. Bạn có thể thử lại không?",
                "error": str(e)
            }
    
    def store_conversation(self, session_id: str, user_id: str, user_message: str,
                          bot_response: str, intent: str, sentiment: str,
                          confidence: float, risk_level: str) -> int:
        """Lưu cuộc trò chuyện"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations 
            (session_id, user_id, user_message, bot_response, intent, 
             sentiment, confidence, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id, user_id, user_message, bot_response,
            intent, sentiment, confidence, risk_level
        ))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def create_crisis_alert(self, user_id: str, session_id: str, message: str, risk_level: str):
        """Tạo cảnh báo khẩn cấp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO crisis_alerts 
            (user_id, session_id, message, risk_level, action_taken)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id, session_id, message, risk_level,
            "Crisis response sent, professional help recommended"
        ))
        
        conn.commit()
        conn.close()
        
        logger.warning(f"🚨 CRISIS ALERT: User {user_id} - {risk_level} risk detected")
    
    def update_session(self, session_id: str, risk_level: str):
        """Cập nhật phiên chat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if session exists
        cursor.execute('SELECT * FROM chat_sessions WHERE session_id = ?', (session_id,))
        if cursor.fetchone():
            # Update existing session
            cursor.execute('''
                UPDATE chat_sessions 
                SET total_messages = total_messages + 1,
                    risk_assessment = ?,
                    requires_followup = ?
                WHERE session_id = ?
            ''', (risk_level, risk_level in ["high", "critical"], session_id))
        else:
            # Create new session
            cursor.execute('''
                INSERT INTO chat_sessions 
                (session_id, user_id, risk_assessment, requires_followup)
                VALUES (?, ?, ?, ?)
            ''', (session_id, "unknown", risk_level, risk_level in ["high", "critical"]))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy lịch sử cuộc trò chuyện"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_message, bot_response, intent, sentiment, risk_level, created_at
            FROM conversations 
            WHERE session_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (session_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for result in results:
            history.append({
                "user_message": result[0],
                "bot_response": result[1],
                "intent": result[2],
                "sentiment": result[3],
                "risk_level": result[4],
                "timestamp": result[5]
            })
        
        return list(reversed(history))  # Return in chronological order
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Thống kê người dùng"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total conversations
        cursor.execute('SELECT COUNT(*) FROM conversations WHERE user_id = ?', (user_id,))
        total_messages = cursor.fetchone()[0]
        
        # Sentiment distribution
        cursor.execute('''
            SELECT sentiment, COUNT(*) 
            FROM conversations 
            WHERE user_id = ? 
            GROUP BY sentiment
        ''', (user_id,))
        sentiment_dist = dict(cursor.fetchall())
        
        # Risk level distribution
        cursor.execute('''
            SELECT risk_level, COUNT(*) 
            FROM conversations 
            WHERE user_id = ? 
            GROUP BY risk_level
        ''', (user_id,))
        risk_dist = dict(cursor.fetchall())
        
        # Crisis alerts
        cursor.execute('SELECT COUNT(*) FROM crisis_alerts WHERE user_id = ?', (user_id,))
        crisis_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_messages": total_messages,
            "sentiment_distribution": sentiment_dist,
            "risk_distribution": risk_dist,
            "crisis_alerts": crisis_count,
            "last_activity": datetime.now().isoformat()
        }

# Global instance
chatbot = MentalHealthNLPChatbot()

async def chat_with_bot(user_id: str, session_id: str, message: str) -> Dict[str, Any]:
    """Interface function cho chatbot"""
    return await chatbot.process_message(user_id, session_id, message)

if __name__ == "__main__":
    # Test chatbot
    print("🤖 SOULFRIEND V2.0 - NLP Chatbot Testing")
    
    import uuid
    
    # Test conversations
    test_conversations = [
        "Xin chào, tôi cảm thấy rất buồn hôm nay",
        "Tôi lo lắng về công việc quá",
        "Gần đây tôi hay mất ngủ",
        "Cảm ơn bạn đã lắng nghe"
    ]
    
    session_id = str(uuid.uuid4())
    user_id = "test_user_001"
    
    async def test_chat():
        for message in test_conversations:
            print(f"\n👤 User: {message}")
            
            result = await chat_with_bot(user_id, session_id, message)
            
            print(f"🤖 Bot: {result['response']}")
            print(f"📊 Intent: {result['intent']}, Sentiment: {result['sentiment']}, Risk: {result['risk_level']}")
            
            await asyncio.sleep(1)  # Simulate conversation delay
    
    # Run test
    asyncio.run(test_chat())
    
    # Test statistics
    stats = chatbot.get_user_statistics(user_id)
    print(f"\n📈 User Statistics:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    print("\n✅ Chatbot system ready!")
