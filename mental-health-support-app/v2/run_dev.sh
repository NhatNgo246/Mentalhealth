#!/bin/bash

# 🚀 SOULFRIEND V2.0 Development Server

echo "🌟 Starting SOULFRIEND V2.0 Development Server..."

# Navigate to V2 directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/installed" ]; then
    echo "📚 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/installed
fi

# Set development environment
export ENVIRONMENT=development
export DEBUG=True

# Start Streamlit server
echo "🚀 Launching SOULFRIEND V2.0..."
echo "🌐 Access at: http://localhost:8501"
echo "🔄 Hot reload enabled - edit files and see changes instantly!"
echo ""

streamlit run app.py \
    --server.port=8501 \
    --server.address=localhost \
    --server.runOnSave=true \
    --theme.base=light \
    --theme.primaryColor="#667eea" \
    --theme.backgroundColor="#ffffff" \
    --theme.secondaryBackgroundColor="#f0f2f6"
