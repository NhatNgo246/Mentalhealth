#!/bin/bash

echo "🌟 Starting SOULFRIEND Application..."

# Navigate to the app directory
cd /workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app

# Set Python path
export PYTHONPATH=/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app

# Kill existing streamlit processes
pkill -f streamlit 2>/dev/null || true
sleep 2

echo "🚀 Launching SOULFRIEND on http://localhost:8501"
echo "📱 Also accessible at http://0.0.0.0:8501"
echo "✨ Features: Logo góc trái + UI clean"

# Start the clean version
python3 -m streamlit run SOULFRIEND.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --browser.gatherUsageStats false
