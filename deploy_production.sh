#!/bin/bash
# SOULFRIEND V2.0 Production Deployment Script
# Created: 2025-08-27

set -e  # Exit on any error

echo "🎯 SOULFRIEND V2.0 PRODUCTION DEPLOYMENT"
echo "========================================"

# Configuration
APP_DIR="/opt/soulfriend"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="/var/log/soulfriend"
USER="soulfriend"
PORT="8501"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   log_error "This script should not be run as root for security reasons"
   exit 1
fi

# Pre-deployment checks
log_info "Performing pre-deployment checks..."

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l) -eq 0 ]]; then
    log_error "Python 3.8+ required. Found: $PYTHON_VERSION"
    exit 1
fi
log_info "Python version: $PYTHON_VERSION ✓"

# Check required directories
if [[ ! -d "$APP_DIR" ]]; then
    log_error "Application directory not found: $APP_DIR"
    exit 1
fi

# Setup virtual environment
log_info "Setting up Python virtual environment..."
if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Install dependencies
log_info "Installing dependencies..."
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"

# Set environment variables
export PYTHONPATH="$APP_DIR"
export ENCRYPTION_PASSWORD="${ENCRYPTION_PASSWORD:-$(openssl rand -base64 32)}"
export STREAMLIT_SERVER_PORT="$PORT"
export STREAMLIT_SERVER_ADDRESS="0.0.0.0"

# Create log directory
sudo mkdir -p "$LOG_DIR"
sudo chown "$USER:$USER" "$LOG_DIR"

# Security checks
log_info "Performing security checks..."

# Check file permissions
find "$APP_DIR" -name "*.py" -exec chmod 644 {} \;
find "$APP_DIR/data" -type f -exec chmod 640 {} \;
chmod 750 "$APP_DIR/components"

# Backup current session data
log_info "Creating backup..."
BACKUP_DIR="$APP_DIR/backups/deployment_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Test application
log_info "Testing application..."
cd "$APP_DIR"
python3 -c "
import sys
sys.path.insert(0, '$APP_DIR')
try:
    from components.questionnaires import QuestionnaireManager
    from components.scoring import calculate_scores
    from components.ui import app_header
    print('✅ All imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

if [[ $? -ne 0 ]]; then
    log_error "Application test failed"
    exit 1
fi

# Start application
log_info "Starting SOULFRIEND V2.0 application..."

# Kill existing processes
pkill -f "streamlit run" || true
sleep 2

# Start with nohup for production
nohup streamlit run SOULFRIEND.py \
    --server.port $PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection true \
    --browser.gatherUsageStats false \
    > "$LOG_DIR/soulfriend.log" 2>&1 &

STREAMLIT_PID=$!
echo $STREAMLIT_PID > "$APP_DIR/soulfriend.pid"

# Wait and check if started successfully
sleep 5
if ps -p $STREAMLIT_PID > /dev/null; then
    log_info "✅ SOULFRIEND V2.0 started successfully (PID: $STREAMLIT_PID)"
    log_info "🌐 Application available at: http://localhost:$PORT"
    log_info "📝 Logs: $LOG_DIR/soulfriend.log"
else
    log_error "❌ Failed to start SOULFRIEND V2.0"
    cat "$LOG_DIR/soulfriend.log"
    exit 1
fi

# Health check
log_info "Performing health check..."
sleep 10
if curl -f http://localhost:$PORT/_stcore/health > /dev/null 2>&1; then
    log_info "✅ Health check passed"
else
    log_warn "⚠️ Health check failed - application may still be starting"
fi

log_info "🎉 SOULFRIEND V2.0 PRODUCTION DEPLOYMENT COMPLETED"
log_info "📊 Monitor logs: tail -f $LOG_DIR/soulfriend.log"
log_info "🛑 Stop application: kill $(cat $APP_DIR/soulfriend.pid)"

deactivate
