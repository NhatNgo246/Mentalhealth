#!/bin/bash
# SoulFriend - Mental Health Support App Launcher
# Khởi chạy ứng dụng SoulFriend với các tối ưu hóa

echo "🌟 Starting SoulFriend - Mental Health Support App..."
echo "🔧 Initializing optimized UI components..."

# Kill any existing streamlit processes
pkill -f streamlit 2>/dev/null || true

# Wait a moment for cleanup
sleep 2

# Check if all required files exist
if [ ! -f "SOULFRIEND.py" ]; then
    echo "❌ Error: SOULFRIEND.py not found!"
    exit 1
fi

if [ ! -f "components/ui_optimized.py" ]; then
    echo "❌ Error: UI optimization components not found!"
    exit 1
fi

if [ ! -f "assets/ui-optimized.css" ]; then
    echo "⚠️  Warning: Optimized CSS not found, using fallback styles"
fi

echo "✅ All components ready!"
echo "🚀 Launching SoulFriend on http://localhost:8501"
echo "📱 Access from mobile: http://0.0.0.0:8501"
echo ""
echo "🎯 Features active:"
echo "   ✅ Optimized UI Components"
echo "   ✅ CSS Variables System"
echo "   ✅ Accessibility Compliance"
echo "   ✅ Production Safety Validation"
echo "   ✅ Comprehensive Logging"
echo ""

# Start the app
python3 -m streamlit run SOULFRIEND.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --theme.base "light" \
    --theme.primaryColor "#667eea" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f0f2f6"
