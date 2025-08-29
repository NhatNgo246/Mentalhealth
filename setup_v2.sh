#!/bin/bash

# 🚀 SOULFRIEND V2.0 SETUP SCRIPT
# Automated setup for SOULFRIEND Mental Health Support Application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in correct directory
check_directory() {
    if [[ ! -f "README.md" ]] || [[ ! -d "mental-health-support-app" ]]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
}

# Create V2 directory structure
create_directory_structure() {
    print_status "Creating V2.0 directory structure..."
    
    # Main V2 directory
    mkdir -p mental-health-support-app/v2
    cd mental-health-support-app/v2
    
    # Core directories
    mkdir -p {components,data,pages,assets,tests,docs,config,utils}
    mkdir -p assets/{fonts,images,logos}
    mkdir -p data/{scales,exports,backups}
    mkdir -p tests/{unit,integration,e2e}
    mkdir -p config/{environments,scales}
    mkdir -p docs/{api,user,dev}
    
    print_success "Directory structure created"
}

# Copy and upgrade existing files
migrate_existing_files() {
    print_status "Migrating existing files to V2.0..."
    
    # Copy main app
    cp ../app.py ./
    
    # Copy and organize components
    if [[ -d "../components" ]]; then
        cp -r ../components/* ./components/
    fi
    
    # Copy data files
    if [[ -d "../data" ]]; then
        cp -r ../data/* ./data/
    fi
    
    # Copy pages
    if [[ -d "../pages" ]]; then
        cp -r ../pages/* ./pages/
    fi
    
    # Copy assets
    if [[ -d "../assets" ]]; then
        cp -r ../assets/* ./assets/
    fi
    
    print_success "Files migrated successfully"
}

# Setup Python virtual environment
setup_python_environment() {
    print_status "Setting up Python virtual environment..."
    
    # Check if Python 3.8+ is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.8+ is required but not installed"
        exit 1
    fi
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    print_success "Virtual environment created and activated"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Ensure we're in virtual environment
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        source venv/bin/activate
    fi
    
    # Install core dependencies
    pip install streamlit>=1.28.0
    pip install pandas>=1.5.0
    pip install numpy>=1.24.0
    pip install matplotlib>=3.6.0
    pip install plotly>=5.15.0
    pip install reportlab>=4.0.0
    pip install Pillow>=9.5.0
    pip install python-dotenv>=1.0.0
    pip install pytest>=7.0.0
    pip install black>=23.0.0
    pip install flake8>=6.0.0
    
    # Create requirements.txt
    pip freeze > requirements.txt
    
    print_success "Dependencies installed"
}

# Setup configuration files
setup_configuration() {
    print_status "Setting up configuration files..."
    
    # Create environment configuration
    cat > config/development.env << EOF
# Development Environment Configuration
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite:///data/soulfriend.db

# Security
SECRET_KEY=dev-secret-key-change-in-production
ADMIN_PASSWORD=admin123

# External APIs (Optional)
OPENAI_API_KEY=your-openai-api-key-here
GOOGLE_ANALYTICS_ID=your-ga-id-here

# Features
ENABLE_AI_ASSISTANT=false
ENABLE_ANALYTICS=false
ENABLE_EXPORT=true
ENABLE_ADMIN=true
EOF

    # Create production environment template
    cat > config/production.env.template << EOF
# Production Environment Configuration
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

# Database - Use PostgreSQL in production
DATABASE_URL=postgresql://user:password@localhost:5432/soulfriend

# Security - CHANGE THESE VALUES
SECRET_KEY=your-secure-secret-key-here
ADMIN_PASSWORD=your-secure-admin-password

# External APIs
OPENAI_API_KEY=your-openai-api-key
GOOGLE_ANALYTICS_ID=your-ga-id

# Features
ENABLE_AI_ASSISTANT=true
ENABLE_ANALYTICS=true
ENABLE_EXPORT=true
ENABLE_ADMIN=true

# Performance
MAX_UPLOAD_SIZE=10MB
SESSION_TIMEOUT=3600
CACHE_TTL=300
EOF

    # Copy development config as default
    cp config/development.env .env
    
    print_success "Configuration files created"
}

# Copy scale configurations
setup_scale_configurations() {
    print_status "Setting up assessment scale configurations..."
    
    # Copy scale configs from main directory
    cp ../../data/*.json ./data/scales/ 2>/dev/null || true
    
    # Ensure DASS-21 config exists
    if [[ ! -f "data/scales/dass21_vi.json" ]] && [[ -f "data/dass21_vi.json" ]]; then
        cp data/dass21_vi.json data/scales/
    fi
    
    print_success "Scale configurations ready"
}

# Setup testing framework
setup_testing() {
    print_status "Setting up testing framework..."
    
    # Create test configuration
    cat > tests/conftest.py << 'EOF'
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_responses():
    """Sample test responses for DASS-21"""
    return {
        f'DASS21_Q{i}': 1 for i in range(1, 22)
    }

@pytest.fixture
def scale_manager():
    """Scale manager fixture"""
    from components.scoring import ScaleManager
    return ScaleManager()
EOF

    # Create basic test
    cat > tests/unit/test_basic.py << 'EOF'
def test_import_components():
    """Test that core components can be imported"""
    try:
        from components import scoring, ui
        assert True
    except ImportError as e:
        assert False, f"Import failed: {e}"

def test_data_files_exist():
    """Test that required data files exist"""
    import os
    
    required_files = [
        'data/dass21_vi.json',
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file missing: {file_path}"
EOF

    print_success "Testing framework setup complete"
}

# Create development scripts
create_dev_scripts() {
    print_status "Creating development scripts..."
    
    # Development run script
    cat > run_dev.sh << 'EOF'
#!/bin/bash
# Development server script

# Activate virtual environment
source venv/bin/activate

# Load development environment
export $(cat .env | xargs)

# Run with hot reload
streamlit run app.py --server.port=8501 --server.address=localhost --server.runOnSave=true
EOF

    # Testing script
    cat > run_tests.sh << 'EOF'
#!/bin/bash
# Test runner script

# Activate virtual environment
source venv/bin/activate

# Run all tests
echo "🧪 Running unit tests..."
python -m pytest tests/unit/ -v

echo "🔗 Running integration tests..."
python -m pytest tests/integration/ -v

echo "📊 Generating coverage report..."
python -m pytest tests/ --cov=components --cov-report=html

echo "✅ Testing complete. Coverage report in htmlcov/"
EOF

    # Production deployment script
    cat > deploy.sh << 'EOF'
#!/bin/bash
# Production deployment script

set -e

echo "🚀 Deploying SOULFRIEND V2.0..."

# Activate virtual environment
source venv/bin/activate

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -x
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Deployment aborted."
    exit 1
fi

# Load production environment
cp config/production.env .env
export $(cat .env | xargs)

# Database migrations (if applicable)
echo "📊 Setting up database..."
python utils/setup_database.py

# Start application
echo "✅ Starting application..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
EOF

    # Make scripts executable
    chmod +x run_dev.sh run_tests.sh deploy.sh
    
    print_success "Development scripts created"
}

# Create documentation
create_documentation() {
    print_status "Creating documentation..."
    
    # API documentation
    cat > docs/api/README.md << 'EOF'
# SOULFRIEND V2.0 API Documentation

## Components

### Scoring Engine
- `ScaleManager`: Manages multiple assessment scales
- `compute_assessment()`: Computes assessment results
- `ScoreResult`: Individual domain score
- `AssessmentResult`: Complete assessment result

### Rules Engine
- `recommend_by_scale()`: Generates personalized recommendations
- `Recommendation`: Individual recommendation object

### Charts
- `bar_chart()`: Creates bar charts
- `donut_chart()`: Creates donut charts  
- `radar_chart()`: Creates radar charts

### Export
- `create_assessment_pdf()`: Generates PDF reports
- `create_csv_export()`: Creates CSV exports
EOF

    # User documentation
    cat > docs/user/README.md << 'EOF'
# SOULFRIEND V2.0 User Guide

## Getting Started

1. **Select Assessment Scales**: Choose from DASS-21, PHQ-9, GAD-7, EPDS, PSS-10
2. **Complete Questionnaires**: Answer all questions honestly
3. **Review Results**: View your scores and interpretations
4. **Follow Recommendations**: Review personalized guidance
5. **Export Results**: Download PDF or CSV reports

## Assessment Scales

- **DASS-21**: Depression, Anxiety, Stress
- **PHQ-9**: Depression screening
- **GAD-7**: Anxiety disorders
- **EPDS**: Postnatal depression
- **PSS-10**: Perceived stress
EOF

    # Developer documentation
    cat > docs/dev/README.md << 'EOF'
# SOULFRIEND V2.0 Developer Guide

## Architecture

```
app.py              # Main Streamlit application
├── components/     # Core business logic
├── pages/         # Streamlit pages
├── data/          # Configuration and data files
├── tests/         # Test suites
├── config/        # Environment configurations
└── utils/         # Utility scripts
```

## Development Workflow

1. Make changes to code
2. Run tests: `./run_tests.sh`
3. Test manually: `./run_dev.sh` 
4. Commit changes
5. Deploy: `./deploy.sh`

## Adding New Scales

1. Create JSON configuration in `data/scales/`
2. Update `ScaleManager` to load new scale
3. Add tests in `tests/unit/`
4. Update documentation
EOF

    print_success "Documentation created"
}

# Run comprehensive tests
run_initial_tests() {
    print_status "Running initial tests..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Basic import test
    python -c "
import sys
sys.path.append('.')
try:
    import streamlit
    print('✅ Streamlit import successful')
except ImportError as e:
    print(f'❌ Streamlit import failed: {e}')
    sys.exit(1)
"
    
    # Run pytest if tests exist
    if [[ -d "tests" ]]; then
        python -m pytest tests/ -v || print_warning "Some tests failed, but setup continues"
    fi
    
    print_success "Initial tests completed"
}

# Main setup function
main() {
    print_status "🚀 Starting SOULFRIEND V2.0 Setup..."
    print_status "================================================"
    
    check_directory
    create_directory_structure
    migrate_existing_files
    setup_python_environment
    install_dependencies
    setup_configuration
    setup_scale_configurations
    setup_testing
    create_dev_scripts
    create_documentation
    run_initial_tests
    
    print_success "================================================"
    print_success "🎉 SOULFRIEND V2.0 Setup Complete!"
    print_success "================================================"
    
    echo
    print_status "Next steps:"
    echo "1. cd mental-health-support-app/v2"
    echo "2. source venv/bin/activate"
    echo "3. ./run_dev.sh"
    echo
    print_status "Development server will be available at: http://localhost:8501"
    echo
    print_status "For testing: ./run_tests.sh"
    print_status "For production: ./deploy.sh"
    echo
}

# Run main function
main "$@"
