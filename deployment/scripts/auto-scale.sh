#!/bin/bash
# SOULFRIEND V2.0 - Auto Scaling Script

CURRENT_LOAD=$(docker stats --no-stream --format "table {{.CPUPerc}}" | tail -n +2 | sed 's/%//' | awk '{sum+=$1} END {print sum/NR}')
MEMORY_USAGE=$(docker stats --no-stream --format "table {{.MemPerc}}" | tail -n +2 | sed 's/%//' | awk '{sum+=$1} END {print sum/NR}')

echo "Current CPU Load: ${CURRENT_LOAD}%"
echo "Current Memory Usage: ${MEMORY_USAGE}%"

# Scale up if load is high
if (( $(echo "$CURRENT_LOAD > 70" | bc -l) )); then
    echo "🔺 High CPU load detected, scaling up..."
    docker-compose -f deployment/docker-compose.prod.yml up -d --scale soulfriend-app=5
elif (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "🔺 High memory usage detected, scaling up..."
    docker-compose -f deployment/docker-compose.prod.yml up -d --scale soulfriend-app=5
# Scale down if load is low
elif (( $(echo "$CURRENT_LOAD < 30" | bc -l) )) && (( $(echo "$MEMORY_USAGE < 50" | bc -l) )); then
    echo "🔻 Low resource usage, scaling down..."
    docker-compose -f deployment/docker-compose.prod.yml up -d --scale soulfriend-app=2
fi
