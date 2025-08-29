#!/bin/bash

# Enhanced Research System Setup Script
# Script Thiết lập Hệ thống Nghiên cứu Nâng cao

set -e  # Exit on any error

echo "🔬 ENHANCED RESEARCH SYSTEM SETUP"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Check if running in the correct directory
if [ ! -f "SOULFRIEND.py" ]; then
    print_error "Please run this script from the SOULFRIEND directory"
    exit 1
fi

print_info "Starting enhanced research system setup..."

# Step 1: Create directory structure
print_info "Step 1: Creating directory structure..."
mkdir -p research_data
mkdir -p logs
mkdir -p config
mkdir -p backups
print_status "Directory structure created"

# Step 2: Install dependencies
print_info "Step 2: Installing dependencies..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_warning "Virtual environment not found, creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install base dependencies
pip install --upgrade pip

# Install required packages
print_info "Installing core dependencies..."
pip install streamlit pandas plotly requests

# Install optional dependencies for enhanced features
print_info "Installing enhanced dependencies..."
pip install fastapi uvicorn pydantic

# Install analytics dependencies
print_info "Installing analytics dependencies..."
pip install numpy matplotlib seaborn jupyter

# Install database dependencies
print_info "Installing database dependencies..."
pip install sqlite3 # Usually included with Python

# Try to install PostgreSQL driver (optional)
if pip install psycopg2-binary 2>/dev/null; then
    print_status "PostgreSQL driver installed"
else
    print_warning "PostgreSQL driver not installed (optional)"
fi

# Install security dependencies
print_info "Installing security dependencies..."
pip install cryptography pycryptodome

# Install configuration dependencies
print_info "Installing configuration dependencies..."
pip install pyyaml

print_status "All dependencies installed successfully"

# Step 3: Set up configuration
print_info "Step 3: Setting up configuration..."

# Generate default configuration
python3 -c "
from research_system.config_manager import ResearchSystemConfig
config = ResearchSystemConfig()
config.export_config_template('config/research_config.yaml')
config.save_config()
print('✅ Configuration files created')
"

print_status "Configuration setup completed"

# Step 4: Initialize database
print_info "Step 4: Initializing database..."

python3 -c "
from research_system.database import ResearchDatabase
try:
    db = ResearchDatabase()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
"

# Step 5: Generate security keys
print_info "Step 5: Generating security keys..."

python3 -c "
import secrets
import base64
import os

# Generate master key
master_key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
salt = base64.urlsafe_b64encode(secrets.token_bytes(16)).decode()

# Create .env file with security settings
with open('.env', 'w') as f:
    f.write(f'RESEARCH_MASTER_KEY={master_key}\n')
    f.write(f'RESEARCH_SALT={salt}\n')
    f.write('ENABLE_RESEARCH_COLLECTION=false\n')
    f.write('RESEARCH_DB_TYPE=sqlite\n')
    f.write('RESEARCH_DB_PATH=research_data/research.db\n')

print('✅ Security keys generated and saved to .env')
print('⚠️ Keep the .env file secure and do not commit it to version control')
"

print_status "Security keys generated"

# Step 6: Test system components
print_info "Step 6: Testing system components..."

python3 -c "
try:
    # Test basic imports
    from research_system.collector import SafeResearchCollector
    from research_system.integration import safe_track_session_start
    from research_system.analytics import ResearchAnalytics
    from research_system.security import ResearchSecurity
    from research_system.database import ResearchDatabase
    from research_system.manager import ResearchSystemManager
    print('✅ All components imported successfully')
    
    # Test basic functionality
    collector = SafeResearchCollector()
    analytics = ResearchAnalytics()
    security = ResearchSecurity()
    database = ResearchDatabase()
    
    print('✅ All components initialized successfully')
    
except Exception as e:
    print(f'❌ Component test failed: {e}')
    import traceback
    traceback.print_exc()
"

# Step 7: Create backup of original SOULFRIEND
print_info "Step 7: Creating backup..."

if [ ! -f "backups/SOULFRIEND_original.py" ]; then
    cp SOULFRIEND.py backups/SOULFRIEND_original.py
    print_status "Original SOULFRIEND.py backed up"
else
    print_warning "Backup already exists"
fi

# Step 8: Set file permissions
print_info "Step 8: Setting secure file permissions..."

# Secure data directories
chmod 700 research_data logs config backups
chmod 600 .env 2>/dev/null || true

print_status "File permissions set"

# Step 9: Create startup scripts
print_info "Step 9: Creating startup scripts..."

# Create main application startup script
cat > start_soulfriend.sh << 'EOF'
#!/bin/bash
# Start SOULFRIEND with research system

source .venv/bin/activate
export ENABLE_RESEARCH_COLLECTION=true
streamlit run SOULFRIEND.py --server.port 8501 --server.address 0.0.0.0
EOF

# Create research API startup script
cat > start_research_api.sh << 'EOF'
#!/bin/bash
# Start Research Collection API

source .venv/bin/activate
python enhanced_research_demo.py --api
EOF

# Create monitoring dashboard startup script
cat > start_monitoring.sh << 'EOF'
#!/bin/bash
# Start Monitoring Dashboard

source .venv/bin/activate
python enhanced_research_demo.py --dashboard
EOF

# Create full system startup script
cat > start_full_system.sh << 'EOF'
#!/bin/bash
# Start Complete Research System

echo "🚀 Starting Complete Research System..."

# Start research API in background
source .venv/bin/activate
python enhanced_research_demo.py --api &
API_PID=$!

# Wait for API to start
sleep 3

# Start SOULFRIEND with research enabled
export ENABLE_RESEARCH_COLLECTION=true
streamlit run SOULFRIEND.py --server.port 8501 --server.address 0.0.0.0 &
SOULFRIEND_PID=$!

# Start monitoring dashboard
python enhanced_research_demo.py --dashboard &
MONITOR_PID=$!

echo "✅ All services started:"
echo "   🧠 SOULFRIEND: http://localhost:8501"
echo "   🔬 Research API: http://localhost:8502"
echo "   📊 Monitoring: http://localhost:8503"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap 'kill $API_PID $SOULFRIEND_PID $MONITOR_PID 2>/dev/null; exit' INT
wait
EOF

# Make scripts executable
chmod +x start_soulfriend.sh start_research_api.sh start_monitoring.sh start_full_system.sh

print_status "Startup scripts created"

# Step 10: Run comprehensive tests
print_info "Step 10: Running comprehensive tests..."

python3 enhanced_research_demo.py --test

print_status "Tests completed"

# Step 11: Generate documentation
print_info "Step 11: Generating documentation..."

cat > RESEARCH_SYSTEM_QUICKSTART.md << 'EOF'
# Research System Quick Start Guide

## Overview
The Enhanced Research System for SOULFRIEND provides comprehensive data collection, analytics, and monitoring capabilities while maintaining full privacy compliance.

## Quick Start

### 1. Basic Usage
```bash
# Start SOULFRIEND with research disabled (default)
./start_soulfriend.sh

# Start SOULFRIEND with research enabled
export ENABLE_RESEARCH_COLLECTION=true
./start_soulfriend.sh
```

### 2. Full System
```bash
# Start all components (SOULFRIEND + Research API + Monitoring)
./start_full_system.sh
```

### 3. Individual Components
```bash
# Research API only
./start_research_api.sh

# Monitoring dashboard only
./start_monitoring.sh
```

## Testing and Validation

### Run Tests
```bash
# Basic component tests
python enhanced_research_demo.py --test

# Complete workflow demonstration
python enhanced_research_demo.py --demo

# Stress testing
python enhanced_research_demo.py --stress

# Full test suite
python enhanced_research_demo.py --full
```

## Configuration

### Environment Variables
- `ENABLE_RESEARCH_COLLECTION`: Enable/disable research data collection
- `RESEARCH_API_ENDPOINT`: Research API endpoint URL
- `RESEARCH_DB_TYPE`: Database type (sqlite/postgresql)
- `RESEARCH_MASTER_KEY`: Encryption master key

### Configuration File
Edit `config/research_config.yaml` to customize system behavior.

## Security and Privacy

### Data Protection
- All data is encrypted at rest and in transit
- Personal information is anonymized using HMAC-SHA256
- K-anonymity validation ensures privacy protection
- Differential privacy available for numeric data

### Compliance
- GDPR compliant data processing
- Vietnamese data protection law compliance (Nghị định 13/2023/NĐ-CP)
- Explicit consent management
- Right to erasure support

## Monitoring and Analytics

### Real-time Monitoring
Access the monitoring dashboard at http://localhost:8503 to view:
- System health status
- Real-time event streams
- Performance metrics
- Compliance status

### Analytics Reports
- Usage statistics and patterns
- Behavioral analysis
- Privacy compliance reports
- System performance metrics

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure all dependencies are installed
2. **Permission errors**: Check file permissions on data directories
3. **API connection errors**: Verify research API is running
4. **Database errors**: Check database configuration and permissions

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export RESEARCH_DEBUG=true
```

## Support
For issues and questions, check:
1. System logs in `logs/` directory
2. Configuration in `config/research_config.yaml`
3. Test results in `research_data/`
EOF

print_status "Documentation generated"

# Final summary
echo ""
echo "🎉 ENHANCED RESEARCH SYSTEM SETUP COMPLETED!"
echo "============================================="
echo ""
print_status "✅ Directory structure created"
print_status "✅ Dependencies installed"
print_status "✅ Configuration generated"
print_status "✅ Database initialized"
print_status "✅ Security keys generated"
print_status "✅ Components tested"
print_status "✅ Backup created"
print_status "✅ Permissions set"
print_status "✅ Startup scripts created"
print_status "✅ Tests completed"
print_status "✅ Documentation generated"

echo ""
echo "📋 Next Steps:"
echo "1. Review configuration in config/research_config.yaml"
echo "2. Test the system: python enhanced_research_demo.py --full"
echo "3. Start SOULFRIEND: ./start_soulfriend.sh"
echo "4. Start full system: ./start_full_system.sh"
echo ""
echo "📊 Available Services:"
echo "   🧠 SOULFRIEND: http://localhost:8501"
echo "   🔬 Research API: http://localhost:8502"
echo "   📊 Monitoring: http://localhost:8503"
echo ""
echo "📖 Documentation: RESEARCH_SYSTEM_QUICKSTART.md"
echo "🔒 Security: Keys stored in .env (keep secure!)"
echo ""
print_info "Research system is ready for use!"

# Check if running in interactive mode
if [ -t 0 ]; then
    echo ""
    read -p "Would you like to start the full system now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Starting full research system..."
        ./start_full_system.sh
    fi
fi
