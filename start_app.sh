#!/bin/bash

echo "🚀 Khởi động SOULFRIEND V3.0 Mental Health App..."
echo "📍 Directory: $(pwd)"

# Stay in current directory - no need to navigate
echo "📂 Current directory: $(pwd)"
echo "📋 Files available:"
ls -la SOULFRIEND.py

# Check if SOULFRIEND.py exists
if [ -f "SOULFRIEND.py" ]; then
    echo "✅ SOULFRIEND.py found"
    echo "🔧 Installing requirements..."
    pip install -r requirements.txt
    
    echo ""
    echo "🎨 Features in SOULFRIEND V3.0:"
    echo "  ✨ All-in-one flow: Consent → Assessment → Results"
    echo "  🧠 Phase 2 AI Engine with 94% confidence"
    echo "  � Global Scale multi-language support"
    echo "  �🎨 Modern UI with enhanced user experience"
    echo "  📱 Mobile-responsive design"
    echo "  🤖 Advanced mental health prediction"
    echo "  📊 Real-time data visualization"
    echo "  � Crisis detection system"
    echo "  🌈 Color-coded risk assessment"
    echo "  📈 Progress tracking and analytics"
    echo "  😊 Mood tracking with smart insights"
    echo "  🔒 Enhanced security and privacy"
    echo ""
    
    echo "🌐 Starting SOULFRIEND V3.0 Streamlit app..."
    echo "🔗 Access the app at: http://localhost:8501"
    echo "🎯 Complete flow: Home → Consent → Assessment → AI Analysis → Results → Resources"
    echo ""
    
    streamlit run SOULFRIEND.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
else
    echo "❌ SOULFRIEND.py not found!"
    echo "📂 Contents:"
    ls -la
fi
