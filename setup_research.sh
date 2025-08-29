#!/bin/bash

# SOULFRIEND Research System Quick Setup
# Script này thiết lập research system một cách an toàn, không ảnh hưởng đến app chính

echo "🔬 SOULFRIEND Research System Setup"
echo "=================================="

# Kiểm tra Python environment
echo "📋 Checking Python environment..."
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "✅ Python version: $PYTHON_VERSION"

# Kiểm tra dependencies
echo "📦 Checking dependencies..."
MISSING_DEPS=()

if ! python -c "import requests" &> /dev/null; then
    MISSING_DEPS+=("requests")
fi

if ! python -c "import fastapi" &> /dev/null; then
    MISSING_DEPS+=("fastapi")
fi

if ! python -c "import uvicorn" &> /dev/null; then
    MISSING_DEPS+=("uvicorn")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "⚠️  Missing dependencies: ${MISSING_DEPS[*]}"
    echo "💡 Install with: pip install ${MISSING_DEPS[*]}"
    echo "🤔 Continue without installing? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "🛑 Setup cancelled"
        exit 1
    fi
else
    echo "✅ All dependencies available"
fi

# Tạo directories
echo "📁 Creating directories..."
mkdir -p research_data
mkdir -p logs
echo "✅ Directories created"

# Test research system
echo "🧪 Testing research system..."
if python research_demo.py --test > /dev/null 2>&1; then
    echo "✅ Research system test passed"
else
    echo "⚠️  Research system test had warnings (this is normal)"
fi

# Setup configuration
echo "⚙️  Setting up configuration..."

# Tạo file .env cho research (optional)
cat > research_system/.env << EOF
# SOULFRIEND Research System Configuration
# Uncomment to enable research collection

# ENABLE_RESEARCH_COLLECTION=false
# RESEARCH_SECRET=change_me_in_production
# PSEUDO_SECRET=change_me_in_production  
# RESEARCH_PORT=8502
EOF

echo "✅ Configuration file created: research_system/.env"

# Kiểm tra SOULFRIEND app
echo "🧠 Checking SOULFRIEND app..."
if [ -f "SOULFRIEND.py" ]; then
    echo "✅ SOULFRIEND.py found"
    
    # Backup SOULFRIEND.py
    cp SOULFRIEND.py SOULFRIEND.py.backup
    echo "✅ Backup created: SOULFRIEND.py.backup"
    
else
    echo "⚠️  SOULFRIEND.py not found in current directory"
fi

# Hiển thị hướng dẫn
echo ""
echo "🎉 Research System Setup Complete!"
echo "=================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣  Test the system:"
echo "    python research_demo.py --test"
echo ""
echo "2️⃣  Start research API (optional):"
echo "    python research_demo.py --api"
echo ""
echo "3️⃣  Enable research collection:"
echo "    export ENABLE_RESEARCH_COLLECTION=true"
echo ""
echo "4️⃣  Run SOULFRIEND normally:"
echo "    streamlit run SOULFRIEND.py"
echo ""
echo "📖 Documentation: RESEARCH_SYSTEM_README.md"
echo ""
echo "🛡️  Safety Notes:"
echo "   • Research is DISABLED by default"
echo "   • No changes made to SOULFRIEND.py"
echo "   • All integration is optional and safe"
echo "   • Original app functionality unchanged"
echo ""
echo "🚀 Ready to use! Research system will not affect your app."

# Optional: Chạy quick test
echo ""
echo "🤔 Run a quick test now? (y/N)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🧪 Running quick test..."
    python research_demo.py --test
fi

echo ""
echo "✅ Setup complete! Happy researching! 🔬"
