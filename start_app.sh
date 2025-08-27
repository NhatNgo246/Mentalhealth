#!/bin/bash

echo "🚀 Khởi động Mental Health Support App v2.0..."
echo "📍 Directory: $(pwd)"

# Navigate to app directory
cd mental-health-support-app/mental-health-support-app

echo "📂 Current directory: $(pwd)"
echo "📋 Files available:"
ls -la app.py

# Check if app.py exists
if [ -f "app.py" ]; then
    echo "✅ app.py found"
    echo "🔧 Installing requirements..."
    pip install -r requirements.txt
    
    echo ""
    echo "🎨 New Features in v2.0:"
    echo "  ✨ All-in-one flow: Consent → Assessment → Results"
    echo "  🎨 Modern UI with animations and gradients"
    echo "  📱 Mobile-responsive design"
    echo "  🤖 Enhanced chatbot integration"
    echo "  📊 Better data visualization"
    echo "  🖼️ ASCII Art Hero Section"
    echo "  🌈 Color-coded Results"
    echo "  📈 Progress Indicators with Graphics"
    echo "  😊 Mood Emojis"
    echo "  🔒 Improved security and privacy"
    echo ""
    
    echo "🌐 Starting Streamlit app..."
    echo "🔗 Access the app at: http://localhost:8501"
    echo "🎯 Complete flow: Home → Consent → Assessment → Results → Resources/Chat"
    echo ""
    
    streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
else
    echo "❌ app.py not found!"
    echo "📂 Contents:"
    ls -la
fi
