"""
Graphics and visual assets for the Mental Health Support App
Contains ASCII art, icons, colors, and visual elements for a friendly UX
"""

# ASCII Art for hero sections
def get_hero_ascii():
    return {
        'brain': """
    🧠✨ MENTAL HEALTH BUDDY ✨🧠
         ╭─────────────────╮
         │  Hãy cùng khám  │
         │  phá tâm hồn    │
         │  bạn nhé! 🌟    │
         ╰─────────────────╯
        """,
        
        'heart': """
    💝 Chăm sóc tâm lý 💝
         ♥ ♥ ♥ ♥ ♥
        Tình yêu bản thân
         là điều quan trọng nhất!
        """,
        
        'wellness': """
    🌈 WELLNESS JOURNEY 🌈
         ╭─○─○─○─○─○─╮
         │ Hành trình  │
         │ tự khám phá │
         ╰─○─○─○─○─○─╯
        """
    }

# Wellness and mood icons
def get_wellness_icons():
    return {
        'meditation': '🧘‍♀️',
        'sleep': '💤',
        'exercise': '🏃‍♀️',
        'nutrition': '🥗',
        'social': '👥',
        'hobby': '🎨',
        'nature': '🌳',
        'music': '🎵',
        'reading': '📚',
        'journal': '📝',
        'therapy': '💬',
        'support': '🤝'
    }

# Mood faces for different emotional states
def get_mood_faces():
    return {
        'very_happy': '😄',
        'happy': '😊',
        'neutral': '😐',
        'sad': '😔',
        'very_sad': '😭',
        'excited': '🤩',
        'calm': '😌',
        'worried': '😟',
        'angry': '😠',
        'confused': '😕'
    }

# Progress indicators and status icons
def get_progress_indicators():
    return {
        'start': '🚀',
        'progress': '⚡',
        'complete': '✅',
        'celebration': '🎉',
        'loading': '⏳',
        'thinking': '🤔',
        'lightbulb': '💡',
        'target': '🎯',
        'star': '⭐',
        'trophy': '🏆'
    }

# Severity level colors
SEVERITY_COLORS = {
    'normal': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'mild': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    'moderate': 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
    'severe': 'linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)',
    'extremely_severe': 'linear-gradient(135deg, #7c2d12 0%, #451a03 100%)'
}

# Background gradients for different moods
GRADIENTS = {
    'happy': 'linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%)',
    'calm': 'linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%)',
    'energy': 'linear-gradient(135deg, #fed7e2 0%, #f687b3 100%)',
    'nature': 'linear-gradient(135deg, #d1fae5 0%, #6ee7b7 100%)',
    'sunset': 'linear-gradient(135deg, #fed7aa 0%, #fb923c 100%)',
    'ocean': 'linear-gradient(135deg, #cffafe 0%, #22d3ee 100%)',
    'purple': 'linear-gradient(135deg, #ede9fe 0%, #a78bfa 100%)',
    'warm': 'linear-gradient(135deg, #fef2f2 0%, #fca5a5 100%)'
}

# Encouraging messages for different stages
ENCOURAGING_MESSAGES = [
    "🌟 Bạn đang làm rất tốt! Cứ tiếp tục nhé!",
    "💪 Việc chăm sóc tâm lý là dấu hiệu của sự mạnh mẽ!",
    "🌈 Mỗi bước tiến đều có ý nghĩa!",
    "✨ Tôi tin bạn có thể vượt qua mọi thử thách!",
    "🎯 Tập trung vào những điều tích cực nhé!",
    "🌱 Sự thay đổi bắt đầu từ những bước nhỏ!",
    "💝 Hãy yêu thương bản thân nhiều hơn!",
    "🦋 Bạn đang biến đổi theo hướng tốt đẹp!",
    "🌺 Tâm hồn bạn đẹp như những bông hoa!",
    "🎈 Niềm vui nhỏ cũng có thể tạo nên hạnh phúc lớn!"
]

# Fun facts about mental health
FUN_FACTS = [
    "🧠 Não bộ sử dụng 20% năng lượng của cả cơ thể!",
    "😄 Cười 15 phút có thể đốt cháy 10-40 calories!",
    "🌞 Ánh sáng mặt trời giúp não sản xuất serotonin!",
    "🎵 Nghe nhạc có thể giảm cortisol (hormone stress)!",
    "🤗 Ôm người khác 20 giây giúp giải phóng oxytocin!",
    "🌿 Dành thời gian với thiên nhiên giảm 50% stress!",
    "📝 Viết nhật ký giúp tăng hệ miễn dịch!",
    "🐶 Vuốt ve thú cưng giảm huyết áp!",
    "💃 Nhảy múa giải phóng endorphin - hormone hạnh phúc!",
    "🫂 Có bạn bè thân thiết tăng tuổi thọ lên 50%!"
]

# Helper functions
def get_random_encouraging_message():
    import random
    return random.choice(ENCOURAGING_MESSAGES)

def get_random_fun_fact():
    import random
    return random.choice(FUN_FACTS)

def get_mood_color(mood_level):
    """Return appropriate color based on mood level (1-5)"""
    if mood_level >= 4:
        return SEVERITY_COLORS['normal']
    elif mood_level == 3:
        return SEVERITY_COLORS['mild']
    elif mood_level == 2:
        return SEVERITY_COLORS['moderate']
    else:
        return SEVERITY_COLORS['severe']
