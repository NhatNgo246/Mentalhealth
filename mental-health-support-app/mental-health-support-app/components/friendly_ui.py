"""
Friendly UI Components - Tạo trải nghiệm thân thiện và hài hước
"""

import streamlit as st

def create_friendly_button(text, icon="🎯", description="", key=None, type="primary", width="full"):
    """Tạo button thân thiện với mô tả và icon dễ thương"""
    
    # Màu sắc theo type
    colors = {
        "primary": "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
        "secondary": "background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);",
        "warning": "background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);",
        "fun": "background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);"
    }
    
    width_style = "width: 100%;" if width == "full" else "width: auto;"
    
    button_html = f"""
    <div style="
        {colors.get(type, colors['primary'])}
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 25px;
        margin: 0.8rem 0;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        {width_style}
        position: relative;
        overflow: hidden;
    " onmouseover="
        this.style.transform='translateY(-3px) scale(1.02)';
        this.style.boxShadow='0 12px 35px rgba(0,0,0,0.25)';
    " onmouseout="
        this.style.transform='translateY(0) scale(1)';
        this.style.boxShadow='0 8px 25px rgba(0,0,0,0.15)';
    " onclick="document.querySelector('[data-testid=\\"{key}\\"]').click();">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.3rem;">{text}</div>
        <div style="font-size: 0.9rem; opacity: 0.9; font-weight: 400;">{description}</div>
    </div>
    """
    
    return st.markdown(button_html, unsafe_allow_html=True)

def create_hero_section_friendly():
    """Hero section thân thiện và vui nhộn"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    ">
        <!-- Floating shapes background -->
        <div style="
            position: absolute;
            top: 10%;
            left: 10%;
            width: 60px;
            height: 60px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            animation: floating 6s ease-in-out infinite;
        "></div>
        <div style="
            position: absolute;
            top: 20%;
            right: 15%;
            width: 40px;
            height: 40px;
            background: rgba(255,255,255,0.08);
            border-radius: 50%;
            animation: floating 8s ease-in-out infinite reverse;
        "></div>
        
        <div style="position: relative; z-index: 1;">
            <div style="font-size: 4rem; margin-bottom: 1rem; animation: bounce 2s ease-in-out infinite;">
                🧠💚✨
            </div>
            <h1 style="
                font-size: 2.8rem;
                margin: 0 0 1rem 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                font-weight: 700;
            ">
                Chào bạn! Hãy cùng chăm sóc tâm hồn nhé 🌈
            </h1>
            <p style="
                font-size: 1.3rem;
                margin: 0 0 2rem 0;
                opacity: 0.95;
                line-height: 1.6;
            ">
                Đừng lo lắng, tôi ở đây để giúp bạn hiểu rõ hơn về tình trạng tâm lý của mình! 
                <br>Chỉ mất vài phút thôi, nhưng sẽ rất có ích đấy 😊
            </p>
            
            <div style="
                display: inline-flex;
                gap: 1rem;
                flex-wrap: wrap;
                justify-content: center;
                margin-top: 1rem;
            ">
                <div style="
                    background: rgba(255,255,255,0.2);
                    padding: 0.8rem 1.5rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                ">
                    🔒 An toàn 100%
                </div>
                <div style="
                    background: rgba(255,255,255,0.2);
                    padding: 0.8rem 1.5rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                ">
                    ⚡ Nhanh chóng
                </div>
                <div style="
                    background: rgba(255,255,255,0.2);
                    padding: 0.8rem 1.5rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                ">
                    🎯 Chính xác
                </div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    @keyframes floating {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def create_mood_check_section():
    """Section kiểm tra tâm trạng vui nhộn"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #e3ffe7 0%, #d9e7ff 100%);
        padding: 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        text-align: center;
    ">
        <h3 style="
            color: #2d3748;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        ">
            🌈 Hôm nay bạn cảm thấy thế nào?
        </h3>
        <p style="
            color: #4a5568;
            margin-bottom: 2rem;
            font-size: 1.1rem;
            line-height: 1.6;
        ">
            Đừng ngại ngùng, hãy chọn emoji mô tả tâm trạng của bạn nhé! 
            <br>Không có đáp án đúng sai đâu, chỉ cần thật lòng thôi 😄
        </p>
        
        <div style="
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin: 2rem 0;
        ">
    """, unsafe_allow_html=True)
    
    moods = [
        {"emoji": "😍", "label": "Tuyệt vời!", "desc": "Hôm nay tràn đầy năng lượng"},
        {"emoji": "😊", "label": "Vui vẻ", "desc": "Tâm trạng khá tích cực"},
        {"emoji": "😐", "label": "Bình thường", "desc": "Không tệ, không tốt"},
        {"emoji": "😔", "label": "Hơi buồn", "desc": "Cần được động viên một chút"},
        {"emoji": "😢", "label": "Khó khăn", "desc": "Đang trải qua thời gian khó khăn"},
    ]
    
    for mood in moods:
        st.markdown(f"""
            <div style="
                background: white;
                width: 120px;
                height: 120px;
                border-radius: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 0.5rem;
            " onmouseover="
                this.style.transform='translateY(-8px) scale(1.05)';
                this.style.boxShadow='0 8px 25px rgba(0,0,0,0.2)';
            " onmouseout="
                this.style.transform='translateY(0) scale(1)';
                this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)';
            " title="{mood['desc']}">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{mood['emoji']}</div>
                <div style="font-size: 0.9rem; font-weight: 600; color: #2d3748;">{mood['label']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def create_assessment_intro():
    """Giới thiệu về bài đánh giá một cách thân thiện"""
    
    st.markdown("""
    <div style="
        background: white;
        padding: 2.5rem;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <div style="font-size: 3rem; margin-right: 1rem;">📝</div>
            <div>
                <h3 style="margin: 0; color: #2d3748; font-size: 1.8rem;">
                    Bài đánh giá DASS-21 - Người bạn thân thiết
                </h3>
                <p style="margin: 0.5rem 0 0 0; color: #718096; font-size: 1rem;">
                    Như một cuộc trò chuyện với bạn thân vậy! 💭
                </p>
            </div>
        </div>
        
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        ">
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">⏰</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">Chỉ 5-7 phút</h4>
                <p style="margin: 0; color: #718096; font-size: 0.9rem;">
                    Nhanh như uống một tách cà phê ☕
                </p>
            </div>
            
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🎯</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">21 câu hỏi đơn giản</h4>
                <p style="margin: 0; color: #718096; font-size: 0.9rem;">
                    Dễ như ăn kẹo, không có câu khó 🍭
                </p>
            </div>
            
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🎁</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">Kết quả chi tiết</h4>
                <p style="margin: 0; color: #718096; font-size: 0.9rem;">
                    Như được tặng một món quà hiểu biết 🎈
                </p>
            </div>
        </div>
        
        <div style="
            background: linear-gradient(135deg, #fef5e7 0%, #f0fff4 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin-top: 2rem;
            border: 1px solid #fbbf24;
        ">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">💡</div>
                <div>
                    <h4 style="margin: 0 0 0.5rem 0; color: #d69e2e;">Mẹo nhỏ từ tôi:</h4>
                    <p style="margin: 0; color: #744210; line-height: 1.5;">
                        Hãy trả lời theo cảm nhận của bạn trong <strong>tuần vừa qua</strong> nhé! 
                        Đừng suy nghĩ quá nhiều, cảm giác đầu tiên thường là chính xác nhất đấy 😉
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_friendly_progress_indicator(current_step, total_steps, step_name):
    """Progress indicator thân thiện với emoji"""
    
    progress_percentage = (current_step / total_steps) * 100
    
    step_emojis = {
        1: "🎯 Bắt đầu",
        2: "📝 Đánh giá", 
        3: "🎉 Kết quả",
        4: "💬 Tư vấn"
    }
    
    return st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
    ">
        <div style="margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #2d3748;">
                {step_emojis.get(current_step, "🌟")} {step_name}
            </h4>
        </div>
        
        <div style="
            background: #e2e8f0;
            height: 12px;
            border-radius: 10px;
            margin: 1rem 0;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                height: 100%;
                width: {progress_percentage}%;
                border-radius: 10px;
                transition: width 0.5s ease;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    right: -10px;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 1.2rem;
                    animation: bounce 1s ease-in-out infinite;
                ">🚀</div>
            </div>
        </div>
        
        <div style="
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: #718096;
            margin-top: 0.5rem;
        ">
            <span>Bước {current_step}/{total_steps}</span>
            <span>{int(progress_percentage)}% hoàn thành</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_encouraging_message():
    """Thông điệp động viên ngẫu nhiên"""
    
    messages = [
        "🌟 Bạn đang làm rất tốt! Tiếp tục nhé!",
        "💪 Wow, bạn thật dũng cảm khi quan tâm đến sức khỏe tâm thần!",
        "🎯 Tuyệt vời! Bạn đã đi được nửa chặng đường rồi!",
        "🚀 Chỉ còn một chút nữa thôi, cố lên!",
        "🌈 Mỗi câu trả lời của bạn đều rất quan trọng!",
        "⭐ Bạn đang chăm sóc bản thân một cách tuyệt vời!",
        "🎪 Gần xong rồi! Kết quả sẽ rất thú vị đấy!"
    ]
    
    import random
    message = random.choice(messages)
    
    return st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 500;
        animation: pulse 2s ease-in-out infinite;
    ">
        {message}
    </div>
    """, unsafe_allow_html=True)

def create_result_celebration():
    """Màn hình chúc mừng khi hoàn thành"""
    
    return st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 30px;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    ">
        <!-- Confetti effect -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 20%, #fbbf24 2px, transparent 2px),
                radial-gradient(circle at 80% 40%, #f59e0b 2px, transparent 2px),
                radial-gradient(circle at 40% 80%, #10b981 2px, transparent 2px),
                radial-gradient(circle at 60% 60%, #3b82f6 2px, transparent 2px);
            background-size: 50px 50px;
            animation: confetti 3s ease-in-out infinite;
            opacity: 0.3;
        "></div>
        
        <div style="position: relative; z-index: 1;">
            <div style="font-size: 5rem; margin-bottom: 1rem; animation: celebration 2s ease-in-out infinite;">
                🎉✨🎊
            </div>
            <h1 style="
                font-size: 2.5rem;
                margin: 0 0 1rem 0;
                font-weight: 700;
            ">
                Xuất sắc! Bạn đã hoàn thành! 🏆
            </h1>
            <p style="
                font-size: 1.2rem;
                margin: 0 0 2rem 0;
                opacity: 0.95;
                line-height: 1.6;
            ">
                Cảm ơn bạn đã dành thời gian để hiểu rõ hơn về bản thân! 
                <br>Bây giờ hãy cùng xem kết quả nhé! 🎯
            </p>
        </div>
    </div>
    
    <style>
    @keyframes celebration {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.1) rotate(5deg); }
    }
    
    @keyframes confetti {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-20px) rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
