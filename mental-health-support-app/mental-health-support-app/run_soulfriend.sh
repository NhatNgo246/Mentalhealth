#!/bin/bash

echo "🌟 Starting SOULFRIEND - Mental Health Support App"
echo "🚀 Launching on http://localhost:8501"

# Navigate to app directory
cd /workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app

# Set Python path
export PYTHONPATH=/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app

# Kill existing processes
pkill -f streamlit 2>/dev/null || true
sleep 2

# Start SOULFRIEND
python3 -m streamlit run SOULFRIEND.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --browser.gatherUsageStats false
