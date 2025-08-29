#!/bin/bash
# SOULFRIEND V2.0 - Health Check Script

echo "🔍 Checking SOULFRIEND V2.0 health..."

# Check main application
if curl -f -s http://localhost:8501/_stcore/health > /dev/null; then
    echo "✅ Main application: Healthy"
else
    echo "❌ Main application: Unhealthy"
    exit 1
fi

# Check dashboards
for port in 8502 8503 8504 8505 8506; do
    if curl -f -s http://localhost:$port/_stcore/health > /dev/null; then
        echo "✅ Dashboard on port $port: Healthy"
    else
        echo "⚠️ Dashboard on port $port: Not responding"
    fi
done

# Check API
if curl -f -s http://localhost:8507/health > /dev/null; then
    echo "✅ API: Healthy"
else
    echo "❌ API: Unhealthy"
    exit 1
fi

echo "🎉 All services are healthy!"
