# 🚀 IMPLEMENTATION GUIDE

## 📋 PHASE 1: FOUNDATION SETUP

### Step 1: Project Structure Migration

```bash
# Move current files to new structure
mkdir -p mental-health-support-app/v2/
cd mental-health-support-app/v2/

# Create new directory structure
mkdir -p {components,data,pages,assets,tests,docs,config,utils}
mkdir -p assets/{fonts,images,logos}
mkdir -p data/{scales,exports,backups}
mkdir -p tests/{unit,integration,e2e}
mkdir -p config/{environments,scales}
```

### Step 2: Core Components Implementation

#### 2.1 Enhanced Scoring Engine

```python
# components/scoring.py
# Copy from CODE_TEMPLATES.md and implement:

class ScaleManager:
    """Manage multiple assessment scales"""
    
    def __init__(self):
        self.scales = {}
        self.load_all_scales()
    
    def load_all_scales(self):
        """Load all scale configurations"""
        scale_files = {
            'DASS-21': 'data/dass21_vi.json',
            'PHQ-9': 'data/phq9_config.json',
            'GAD-7': 'data/gad7_config.json',
            'EPDS': 'data/epds_config.json',
            'PSS-10': 'data/pss10_config.json'
        }
        
        for scale_name, file_path in scale_files.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.scales[scale_name] = json.load(f)
            except FileNotFoundError:
                st.error(f"Scale configuration not found: {file_path}")
    
    def get_scale(self, scale_name: str) -> Dict[str, Any]:
        """Get scale configuration"""
        return self.scales.get(scale_name)
    
    def list_scales(self) -> List[str]:
        """List all available scales"""
        return list(self.scales.keys())
```

#### 2.2 Multi-Scale Assessment Page

```python
# pages/1_Assessment.py
import streamlit as st
from components.scoring import ScaleManager, compute_assessment
from components.ui import progress_indicator, emergency_card

def assessment_page():
    st.title("🧠 Đánh giá sức khỏe tâm thần")
    
    # Initialize scale manager
    scale_manager = ScaleManager()
    
    # Scale selection
    st.sidebar.header("Chọn thang đo")
    selected_scales = st.sidebar.multiselect(
        "Chọn các thang đo bạn muốn thực hiện:",
        scale_manager.list_scales(),
        default=['DASS-21']
    )
    
    if not selected_scales:
        st.warning("Vui lòng chọn ít nhất một thang đo để bắt đầu.")
        return
    
    # Progress tracking
    if 'current_scale_index' not in st.session_state:
        st.session_state.current_scale_index = 0
        st.session_state.scale_responses = {}
    
    # Show progress
    progress_indicator(
        st.session_state.current_scale_index + 1,
        len(selected_scales),
        selected_scales
    )
    
    # Current scale
    current_scale = selected_scales[st.session_state.current_scale_index]
    scale_config = scale_manager.get_scale(current_scale)
    
    # Display assessment
    render_scale_assessment(current_scale, scale_config)

def render_scale_assessment(scale_name: str, scale_config: Dict[str, Any]):
    """Render individual scale assessment"""
    
    st.header(f"📋 {scale_config['name_vi']}")
    st.info(scale_config['description'])
    
    # Emergency card for sensitive scales
    if scale_name in ['PHQ-9', 'EPDS']:
        emergency_card()
    
    # Form for responses
    with st.form(f"assessment_{scale_name}"):
        responses = {}
        
        for item in scale_config['items']:
            item_id = item['id']
            question_text = item['text']
            
            # Handle different response option formats
            if 'response_options_varied' in scale_config:
                # EPDS has varied options per question
                options = get_options_for_question(scale_config, item_id)
            else:
                # Standard options for all questions
                options = scale_config['response_options']
            
            # Create radio buttons
            option_texts = [opt['text'] for opt in options]
            response = st.radio(
                question_text,
                options=range(len(option_texts)),
                format_func=lambda x: option_texts[x],
                key=f"{item_id}",
                horizontal=True
            )
            
            responses[item_id] = options[response]['value']
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "Tiếp tục" if st.session_state.current_scale_index < len(st.session_state.selected_scales) - 1 else "Hoàn thành",
                use_container_width=True
            )
        
        if submitted:
            # Store responses
            st.session_state.scale_responses[scale_name] = responses
            
            # Move to next scale or results
            if st.session_state.current_scale_index < len(st.session_state.selected_scales) - 1:
                st.session_state.current_scale_index += 1
                st.rerun()
            else:
                # All scales completed, go to results
                st.session_state.assessment_completed = True
                st.switch_page("pages/2_Results.py")

if __name__ == "__main__":
    assessment_page()
```

### Step 3: Enhanced Results Page

```python
# pages/2_Results.py
import streamlit as st
from components.scoring import ScaleManager, compute_assessment
from components.rules_engine import recommend_by_scale
from components.charts import bar_chart, donut_chart, radar_chart, chart_to_base64
from components.pdf_export import create_assessment_pdf
from datetime import datetime

def results_page():
    st.title("📊 Kết quả đánh giá")
    
    if 'scale_responses' not in st.session_state or not st.session_state.scale_responses:
        st.warning("Không có dữ liệu đánh giá. Vui lòng thực hiện đánh giá trước.")
        if st.button("Quay lại đánh giá"):
            st.switch_page("pages/1_Assessment.py")
        return
    
    scale_manager = ScaleManager()
    
    # Process all completed assessments
    all_results = {}
    all_recommendations = []
    
    for scale_name, responses in st.session_state.scale_responses.items():
        scale_config = scale_manager.get_scale(scale_name)
        
        # Compute assessment
        result = compute_assessment(responses, scale_config)
        all_results[scale_name] = result
        
        # Generate recommendations
        levels = {domain: score.level for domain, score in result.domain_scores.items()}
        recommendations = recommend_by_scale(scale_name, levels, result.flags)
        all_recommendations.extend(recommendations)
    
    # Display results
    display_results_summary(all_results)
    
    # Charts
    display_charts(all_results)
    
    # Recommendations
    display_recommendations(all_recommendations)
    
    # Export options
    display_export_options(all_results, all_recommendations)

def display_results_summary(all_results: Dict[str, Any]):
    """Display summary of all assessment results"""
    
    st.header("📈 Tổng quan kết quả")
    
    # Create columns for each scale
    cols = st.columns(len(all_results))
    
    for i, (scale_name, result) in enumerate(all_results.items()):
        with cols[i]:
            st.subheader(scale_name)
            
            for domain, score_result in result.domain_scores.items():
                color = get_level_color(score_result.level)
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {color}20, {color}10);
                    border-left: 4px solid {color};
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                ">
                    <h4 style="margin: 0; color: {color};">{domain.title()}</h4>
                    <h2 style="margin: 5px 0; color: {color};">{score_result.adjusted_score}</h2>
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        Mức độ: <strong>{score_result.level.title()}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show flags if any
            if result.flags:
                for flag, is_present in result.flags.items():
                    if is_present:
                        st.error(f"⚠️ {flag.replace('_', ' ').title()}")

def display_charts(all_results: Dict[str, Any]):
    """Display visualization charts"""
    
    st.header("📊 Biểu đồ trực quan")
    
    chart_tabs = st.tabs(["Biểu đồ cột", "Biểu đồ tròn", "Biểu đồ radar"])
    
    # Prepare data for charts
    all_domain_scores = {}
    all_levels = {}
    
    for scale_name, result in all_results.items():
        for domain, score_result in result.domain_scores.items():
            key = f"{scale_name}_{domain}"
            all_domain_scores[key] = score_result.adjusted_score
            all_levels[key] = score_result.level
    
    # Bar chart
    with chart_tabs[0]:
        try:
            chart_buffer = bar_chart(all_domain_scores, all_levels)
            chart_base64 = chart_to_base64(chart_buffer)
            st.markdown(f'<img src="{chart_base64}" style="width: 100%;">', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Không thể tạo biểu đồ cột: {e}")
    
    # Donut chart
    with chart_tabs[1]:
        try:
            chart_buffer = donut_chart(all_levels)
            if chart_buffer:
                chart_base64 = chart_to_base64(chart_buffer)
                st.markdown(f'<img src="{chart_base64}" style="width: 100%;">', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Không thể tạo biểu đồ tròn: {e}")
    
    # Radar chart
    with chart_tabs[2]:
        try:
            max_scores = {key: 42 for key in all_domain_scores.keys()}  # Adjust based on scale
            chart_buffer = radar_chart(all_domain_scores, max_scores)
            chart_base64 = chart_to_base64(chart_buffer)
            st.markdown(f'<img src="{chart_base64}" style="width: 100%;">', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Không thể tạo biểu đồ radar: {e}")

def display_recommendations(recommendations: List[Any]):
    """Display personalized recommendations"""
    
    st.header("💡 Khuyến nghị cá nhân")
    
    if not recommendations:
        st.info("Không có khuyến nghị đặc biệt.")
        return
    
    # Group by priority
    urgent = [r for r in recommendations if r.priority.value == 0]
    high = [r for r in recommendations if r.priority.value == 1]
    medium = [r for r in recommendations if r.priority.value == 2]
    low = [r for r in recommendations if r.priority.value == 3]
    
    # Display by priority
    if urgent:
        st.error("🚨 Khẩn cấp")
        for rec in urgent:
            display_recommendation_card(rec)
    
    if high:
        st.warning("⚠️ Ưu tiên cao")
        for rec in high:
            display_recommendation_card(rec)
    
    if medium:
        st.info("ℹ️ Ưu tiên trung bình")
        for rec in medium:
            display_recommendation_card(rec)
    
    if low:
        st.success("✅ Duy trì")
        for rec in low:
            display_recommendation_card(rec)

def display_export_options(all_results: Dict[str, Any], recommendations: List[Any]):
    """Display export and sharing options"""
    
    st.header("📤 Xuất kết quả")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Xuất PDF", use_container_width=True):
            try:
                # Generate charts for PDF
                chart_buffers = {}
                # ... implement chart generation
                
                # Create PDF
                pdf_buffer = create_assessment_pdf(list(all_results.values()), recommendations, chart_buffers)
                
                st.download_button(
                    label="Tải PDF",
                    data=pdf_buffer,
                    file_name=f"mental_health_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Không thể tạo PDF: {e}")
    
    with col2:
        if st.button("📊 Xuất CSV", use_container_width=True):
            try:
                # Create CSV data
                csv_data = create_csv_export(list(all_results.values())[0])  # Implement for multiple results
                
                st.download_button(
                    label="Tải CSV", 
                    data=csv_data,
                    file_name=f"assessment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Không thể tạo CSV: {e}")
    
    with col3:
        if st.button("🔄 Làm lại đánh giá", use_container_width=True):
            # Clear session state
            for key in ['scale_responses', 'current_scale_index', 'assessment_completed']:
                if key in st.session_state:
                    del st.session_state[key]
            st.switch_page("pages/1_Assessment.py")

if __name__ == "__main__":
    results_page()
```

---

## 📋 PHASE 2: TESTING & VALIDATION

### Comprehensive Test Suite

```python
# tests/test_multi_scale.py
import pytest
import json
from components.scoring import ScaleManager, compute_assessment

class TestMultiScale:
    
    def setup_method(self):
        """Setup for each test"""
        self.scale_manager = ScaleManager()
    
    def test_scale_loading(self):
        """Test all scales load correctly"""
        scales = self.scale_manager.list_scales()
        assert len(scales) >= 5
        assert 'DASS-21' in scales
        assert 'PHQ-9' in scales
        assert 'GAD-7' in scales
        assert 'EPDS' in scales
        assert 'PSS-10' in scales
    
    @pytest.mark.parametrize("scale_name", [
        'DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10'
    ])
    def test_scale_configuration(self, scale_name):
        """Test each scale has valid configuration"""
        config = self.scale_manager.get_scale(scale_name)
        
        assert config is not None
        assert 'scale' in config
        assert 'items' in config
        assert 'domains' in config
        assert 'bands' in config
        assert len(config['items']) > 0
    
    def test_phq9_scoring(self):
        """Test PHQ-9 scoring with sample responses"""
        config = self.scale_manager.get_scale('PHQ-9')
        
        # Sample responses indicating moderate depression
        responses = {
            'PHQ9_Q1': 2, 'PHQ9_Q2': 2, 'PHQ9_Q3': 1,
            'PHQ9_Q4': 2, 'PHQ9_Q5': 1, 'PHQ9_Q6': 1,
            'PHQ9_Q7': 1, 'PHQ9_Q8': 0, 'PHQ9_Q9': 0
        }
        
        result = compute_assessment(responses, config)
        
        assert result.scale == 'PHQ-9'
        assert result.total_score == 10  # Sum of responses
        assert result.domain_scores['depression'].level == 'vừa phải'
        assert not result.flags.get('suicidal_ideation', False)
    
    def test_phq9_suicidal_ideation_flag(self):
        """Test PHQ-9 suicidal ideation detection"""
        config = self.scale_manager.get_scale('PHQ-9')
        
        responses = {f'PHQ9_Q{i}': 0 for i in range(1, 10)}
        responses['PHQ9_Q9'] = 2  # Suicidal ideation
        
        result = compute_assessment(responses, config)
        
        assert result.flags.get('suicidal_ideation', False)
    
    def test_gad7_scoring(self):
        """Test GAD-7 scoring"""
        config = self.scale_manager.get_scale('GAD-7')
        
        # Sample responses for mild anxiety
        responses = {f'GAD7_Q{i}': 1 for i in range(1, 8)}
        
        result = compute_assessment(responses, config)
        
        assert result.scale == 'GAD-7'
        assert result.total_score == 7
        assert result.domain_scores['anxiety'].level == 'nhẹ'
    
    def test_epds_reverse_scoring(self):
        """Test EPDS reverse scoring for positive items"""
        config = self.scale_manager.get_scale('EPDS')
        
        # Q1 and Q2 are reverse scored
        responses = {f'EPDS_Q{i}': 0 for i in range(1, 11)}
        responses['EPDS_Q1'] = 3  # Should become 0 after reverse
        responses['EPDS_Q2'] = 3  # Should become 0 after reverse
        
        result = compute_assessment(responses, config)
        
        # Total should be 0 because reverse scoring
        assert result.total_score == 0
        assert result.domain_scores['postnatal_depression'].level == 'không có nguy cơ'
    
    def test_pss10_scoring(self):
        """Test PSS-10 scoring with reverse items"""
        config = self.scale_manager.get_scale('PSS-10')
        
        # High stress responses
        responses = {f'PSS10_Q{i}': 4 for i in range(1, 11)}
        
        result = compute_assessment(responses, config)
        
        # Should be less than 40 due to reverse scoring
        assert result.total_score < 40
        assert result.domain_scores['perceived_stress'].level in ['vừa phải', 'cao']

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## 📋 PHASE 3: DEPLOYMENT

### Production Deployment Script

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying SOULFRIEND V2.0..."

# 1. Environment setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Deployment aborted."
    exit 1
fi

# 3. Create production config
cp config/production.env .env

# 4. Database setup (if using SQLite)
python utils/setup_database.py

# 5. Warm up models (if using AI)
python utils/warmup_models.py

# 6. Start application
echo "✅ Starting SOULFRIEND V2.0..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

echo "🎉 Deployment complete!"
echo "🌐 Access at: http://localhost:8501"
```

### Requirements for V2.0

```txt
# requirements.txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
plotly>=5.15.0
reportlab>=4.0.0
Pillow>=9.5.0
python-dotenv>=1.0.0
bcrypt>=4.0.0
openai>=1.3.0  # For AI assistant
psycopg2-binary>=2.9.0  # For PostgreSQL
redis>=4.5.0  # For caching
celery>=5.3.0  # For background tasks
```

Với implementation guide này, bạn có thể:

1. **Migrate từ V1 sang V2** một cách có hệ thống
2. **Implement từng component** theo template có sẵn  
3. **Test toàn diện** trước khi deploy
4. **Scale up** với database và caching
5. **Deploy production** với monitoring

Bạn muốn bắt đầu implement component nào trước? 🎯
