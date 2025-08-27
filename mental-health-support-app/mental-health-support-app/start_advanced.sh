#!/bin/bash
# SoulFriend Advanced - Premium Experience Launcher
# Khởi chạy phiên bản nâng cao với UI/UX thông minh

echo "🌟 Starting SoulFriend Advanced - Premium Mental Health Experience..."
echo "🤖 Initializing AI-powered UI/UX components..."
echo "🧠 Loading smart analytics and user journey tracking..."

# Kill any existing streamlit processes
pkill -f streamlit 2>/dev/null || true
sleep 2

# Validate advanced components
echo "🔍 Validating advanced components..."

if [ ! -f "SoulFriend_Advanced.py" ]; then
    echo "❌ Error: SoulFriend_Advanced.py not found!"
    exit 1
fi

if [ ! -f "components/ui_advanced.py" ]; then
    echo "❌ Error: Advanced UI components not found!"
    exit 1
fi

echo "✅ Advanced components validated!"
echo ""
echo "🚀 Features Active:"
echo "   🎨 Premium CSS with animations"
echo "   🧠 Smart UI with user journey tracking"
echo "   📊 Advanced progress indicators"
echo "   🤖 AI-powered recommendations"
echo "   📱 Responsive design with dark mode support"
echo "   ♿ Enhanced accessibility features"
echo "   🔍 User behavior analytics"
echo "   💡 Smart notifications system"
echo ""
echo "🌐 Access URLs:"
echo "   Desktop: http://localhost:8501"
echo "   Mobile:  http://0.0.0.0:8501"
echo "   Network: http://$(hostname -I | awk '{print $1}'):8501"
echo ""

# Start advanced version
python3 -m streamlit run SoulFriend_Advanced.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --theme.base "light" \
    --theme.primaryColor "#667eea" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f8fafc" \
    --theme.textColor "#1f2937" \
    --browser.gatherUsageStats false
