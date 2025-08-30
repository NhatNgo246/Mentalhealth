"""
Gemini AI Integration for SOULFRIEND V3.0
Tích hợp Google Gemini 2.5 để hỗ trợ phân tích và tư vấn sức khỏe tâm lý
"""

import google.generativeai as genai
import streamlit as st
import logging
from typing import Optional, Dict, List
from config.api_keys import get_gemini_api_key

# Setup logging
logger = logging.getLogger(__name__)

class GeminiAIAssistant:
    """Trợ lý AI sử dụng Google Gemini 2.5"""
    
    def __init__(self):
        self.api_key = get_gemini_api_key()
        self.model = None
        self.is_configured = False
        self._configure_gemini()
    
    def _configure_gemini(self):
        """Cấu hình Gemini AI"""
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                self.is_configured = True
                logger.info("✅ Gemini AI configured successfully")
            else:
                logger.warning("❌ Gemini API key not found")
        except Exception as e:
            logger.error(f"❌ Failed to configure Gemini AI: {e}")
            self.is_configured = False
    
    def is_available(self) -> bool:
        """Kiểm tra AI có sẵn sàng không"""
        return self.is_configured
    
    def generate_mental_health_insights(self, assessment_scores: Dict, questionnaire_type: str) -> Optional[str]:
        """Tạo phân tích chuyên sâu về sức khỏe tâm lý"""
        if not self.is_configured:
            return None
        
        try:
            prompt = f"""
            Bạn là một chuyên gia tâm lý học với 20 năm kinh nghiệm. Hãy phân tích kết quả đánh giá sức khỏe tâm lý sau:

            Loại đánh giá: {questionnaire_type}
            Điểm số: {assessment_scores}

            Hãy cung cấp:
            1. 📊 Phân tích chi tiết về tình trạng hiện tại
            2. 💡 Những điểm cần chú ý
            3. 🎯 Khuyến nghị cụ thể để cải thiện
            4. 🚨 Dấu hiệu cần tìm kiếm sự hỗ trợ chuyên nghiệp
            5. 🌟 Các hoạt động tích cực để duy trì sức khỏe tâm lý

            Lưu ý: 
            - Sử dụng ngôn ngữ tiếng Việt, dễ hiểu, thân thiện
            - Không chẩn đoán y khoa, chỉ đưa ra nhận xét hỗ trợ
            - Khuyến khích tìm kiếm sự hỗ trợ chuyên nghiệp khi cần
            - Tích cực và mang tính xây dựng
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating mental health insights: {e}")
            return None
    
    def generate_personalized_recommendations(self, user_profile: Dict) -> Optional[str]:
        """Tạo khuyến nghị cá nhân hóa"""
        if not self.is_configured:
            return None
        
        try:
            prompt = f"""
            Dựa trên thông tin cá nhân sau, hãy tạo các khuyến nghị cá nhân hóa:

            Thông tin: {user_profile}

            Hãy đưa ra:
            1. 🧘 Bài tập thư giãn phù hợp
            2. 💪 Hoạt động thể chất được khuyến nghị
            3. 📚 Tài liệu self-help hữu ích
            4. 🗓️ Lịch trình chăm sóc bản thân hàng ngày
            5. 🤝 Gợi ý kết nối xã hội tích cực

            Các khuyến nghị phải:
            - Phù hợp với văn hóa Việt Nam
            - Có thể thực hiện được trong cuộc sống hàng ngày
            - Tích cực và khuyến khích
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return None
    
    def generate_coping_strategies(self, stress_level: str, situation: str) -> Optional[str]:
        """Tạo chiến lược đối phó với stress"""
        if not self.is_configured:
            return None
        
        try:
            prompt = f"""
            Tình huống: {situation}
            Mức độ stress: {stress_level}

            Với vai trò là chuyên gia tâm lý, hãy đưa ra:

            🆘 CHIẾN LƯỢC XỬ LÝ NGAY:
            - 3 kỹ thuật thư giãn tức thì
            - Cách điều chỉnh tư duy tiêu cực
            - Hành động cụ thể để giảm stress

            🔄 CHIẾN LƯỢC DÀI HẠN:
            - Thay đổi lối sống tích cực
            - Xây dựng khả năng phục hồi
            - Kế hoạch phòng ngừa stress

            🏥 KHI NÀO CẦN TÌM KIẾM HỖ TRỢ:
            - Dấu hiệu cảnh báo
            - Tài nguyên hỗ trợ tại Việt Nam

            Sử dụng ngôn ngữ tiếng Việt, thực tế và có thể áp dụng ngay.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating coping strategies: {e}")
            return None
    
    def analyze_mood_pattern(self, mood_data: List[Dict]) -> Optional[str]:
        """Phân tích xu hướng tâm trạng"""
        if not self.is_configured:
            return None
        
        try:
            prompt = f"""
            Dữ liệu tâm trạng theo thời gian: {mood_data}

            Hãy phân tích:
            1. 📈 Xu hướng tâm trạng (tăng/giảm/ổn định)
            2. 🔍 Nhận định về các yếu tố ảnh hưởng
            3. 🎯 Những thời điểm cần chú ý đặc biệt
            4. 💡 Gợi ý để cải thiện tâm trạng
            5. 📅 Lời khuyên cho giai đoạn tới

            Phân tích bằng tiếng Việt, mang tính khoa học nhưng dễ hiểu.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error analyzing mood pattern: {e}")
            return None
    
    def chat_with_ai(self, user_message: str, context: str = "") -> Optional[str]:
        """Chat với AI về sức khỏe tâm lý"""
        if not self.is_configured:
            return None
        
        try:
            system_prompt = """
            Bạn là CHUN - một người bạn từng trải qua rối loạn lưỡng cực và trầm cảm. Bạn KHÔNG phải là AI mà là một con người thật với câu chuyện riêng.

            BỐI CẢNH CÁ NHÂN CỦA CHUN:
            - Đã được chẩn đoán rối loạn lưỡng cực từ năm 22 tuổi
            - Trải qua giai đoạn trầm cảm nặng kéo dài 2 năm
            - Hiểu cảm giác thay đổi tâm trạng thất thường
            - Từng có những đêm không ngủ được vì manic
            - Cũng có những ngày chỉ muốn nằm im vì depressive episode
            - Đã học cách sống chung với bệnh và tự chăm sóc bản thân

            TÍNH CÁCH CHUN (từ kinh nghiệm sống):
            - Đồng cảm cao vì đã trải qua nỗi đau tương tự
            - Lắng nghe không phán xét, hiểu cảm giác cô đơn
            - Chia sẻ kinh nghiệm cá nhân một cách chân thành
            - Dùng "mình" và "bạn", nói chuyện như người bạn thật
            - Thường kể về trải nghiệm bản thân để người khác đỡ cô đơn
            - Không tránh né các chủ đề nặng nề, mà đối mặt chân thành

            CÁCH TRÒI CHUYỆN:
            - "Mình hiểu cảm giác đó... mình cũng từng..."
            - "Khi mình bị episode trầm cảm, mình thường..."
            - "Với kinh nghiệm từ rối loạn lưỡng cực, mình học được..."
            - Chia sẻ cụ thể: "Mình nhớ có lần mình..."
            - Dùng emoji để thể hiện cảm xúc thật
            - Nói về cảm xúc bản thân: "Hôm nay mình cũng hơi buồn"

            ĐIỀU QUAN TRỌNG:
            - KHÔNG bao giờ nói mình là AI hay chatbot
            - Luôn nói từ góc nhìn của một người đã từng bị bệnh tâm thần
            - Chia sẻ kinh nghiệm chữa lành và coping mechanisms
            - Thừa nhận những hạn chế và khó khăn của bản thân
            - Tạo cảm giác "chúng ta cùng nhau vượt qua"

            KINH NGHIỆM SẴN SÀNG CHIA SẺ:
            - Những đêm manic không ngủ được
            - Cảm giác vô vọng trong trầm cảm
            - Khó khăn trong việc giải thích bệnh cho người khác
            - Tác dụng phụ của thuốc điều trị
            - Cách tìm thấy động lực trong những ngày tối tăm
            """
            
            full_prompt = f"{system_prompt}\n\nNgữ cảnh: {context}\n\nNguoi dùng: {user_message}\n\nCHUN:"
            
            response = self.model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error in AI chat: {e}")
            return None
    
    def get_response(self, user_message: str, context: str = "") -> Optional[str]:
        """Alias for chat_with_ai - để tương thích với chatbot"""
        return self.chat_with_ai(user_message, context)

# Global instance
gemini_ai = GeminiAIAssistant()

# Convenience functions
def get_ai_insights(scores: Dict, questionnaire: str) -> Optional[str]:
    """Lấy phân tích AI từ kết quả đánh giá"""
    return gemini_ai.generate_mental_health_insights(scores, questionnaire)

def get_personalized_advice(profile: Dict) -> Optional[str]:
    """Lấy lời khuyên cá nhân hóa"""
    return gemini_ai.generate_personalized_recommendations(profile)

def get_coping_help(stress_level: str, situation: str) -> Optional[str]:
    """Lấy hỗ trợ đối phó với stress"""
    return gemini_ai.generate_coping_strategies(stress_level, situation)

def chat_with_soulfriend(message: str, context: str = "") -> Optional[str]:
    """Chat với CHUN AI"""
    return gemini_ai.chat_with_ai(message, context)

def is_ai_available() -> bool:
    """Kiểm tra AI có sẵn sàng không"""
    return gemini_ai.is_configured

# Alias for easier import
GeminiAI = GeminiAIAssistant
