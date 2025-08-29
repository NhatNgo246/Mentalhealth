# 📋 TODOLIST & KẾ HOẠCH TRIỂN KHAI SOULFRIEND V2.0

## 🎯 TỔNG QUAN DỰ ÁN

**Mục tiêu**: Phát triển hệ thống đánh giá sức khỏe tâm thần toàn diện với AI và tự trợ  
**Timeline**: 4 Sprints (8-10 tuần)  
**Tech Stack**: Python + Streamlit + SQLite + OpenAI  
**Status**: 🟢 Ready to Start

---

## 🏗️ KIẾN TRÚC & CẤU TRÚC THỨ MỤC

### 📁 Project Structure
```
soulfriend_v2/
├── app.py                         # 🏠 Home: điều hướng, guard khẩn cấp
├── pages/
│   ├── 1_Assessment.py           # 📝 Chọn thang đo + làm bài
│   ├── 2_Results.py              # 📊 Biểu đồ + gợi ý hành động
│   ├── 3_SelfHelp.py             # 🎧 Kho tự trợ (audio/video)
│   ├── 4_Consult.py              # 👨‍⚕️ Đặt lịch/ liên hệ / chat
│   └── 5_Admin.py                # ⚙️ Quản trị: bộ câu hỏi, thống kê
├── components/
│   ├── scoring.py                # 🔢 Tính điểm DASS-21/EPDS/PHQ-9/GAD-7
│   ├── rules_engine.py           # 🧠 Mapping điểm → mức → khuyến nghị
│   ├── charts.py                 # 📈 Hàm vẽ Bar/Donut/Radar
│   ├── pdf_export.py             # 📄 Xuất PDF kết quả
│   ├── ui.py                     # 🎨 Widgets tái dùng
│   ├── auth.py                   # 🔐 Đăng nhập admin
│   └── ai_helper.py              # 🤖 Stub gọi LLM, guardrail
├── data/
│   ├── dass21_vi.json           # 📋 DASS-21 Vietnamese
│   ├── phq9_vi.json             # 📋 PHQ-9 Vietnamese
│   ├── gad7_vi.json             # 📋 GAD-7 Vietnamese
│   ├── epds_vi.json             # 📋 EPDS Vietnamese
│   └── resources.json           # 🎵 Kho tự trợ metadata
├── assets/
│   ├── audio/                   # 🎵 breathing_446.mp3
│   ├── video/                   # 🎬 relax_intro.mp4
│   ├── fonts/                   # 🔤 DejaVuSans.ttf
│   └── css/                     # 🎨 custom.css
├── tests/
│   ├── test_scoring.py          # ✅ Test tính điểm
│   ├── test_rules_engine.py     # ✅ Test rules
│   └── test_validators.py       # ✅ Test validation
├── requirements.txt
└── README.md
```

---

## 🚀 SPRINT PLANNING

### 📅 SPRINT 1 (Tuần 1-2): Nền tảng + DASS-21
**Goal**: Hoàn thành core functionality với DASS-21

#### 👤 User Stories
- **U1**: "Là người dùng, tôi muốn chọn thang đo và trả lời câu hỏi để nhận điểm"
- **U2**: "Là người dùng, tôi muốn xem mức độ và gợi ý bước tiếp theo"  
- **U3**: "Là quản trị, tôi muốn nạp/sửa bộ câu hỏi từ JSON"

#### 📋 Tasks Breakdown

##### 🏗️ **T1.1: Data Schema & Validation** (2 ngày)
- [ ] Thiết kế schema JSON cho thang đo
- [ ] Implement validator schema (pydantic)
- [ ] Tạo data/dass21_vi.json theo schema mới
- [ ] Unit test cho validator

**Schema Format**:
```json
{
  "version": "v1",
  "scale": "DASS-21", 
  "domains": ["stress","anxiety","depression"],
  "items": [
    {"id":"D1","text_vi":"...","domain":"depression","reverse":false}
  ],
  "scoring": {"adjustment_factor": 2},
  "bands": {
    "depression": [[0,9,"normal"],[10,13,"mild"],[14,20,"moderate"]]
  }
}
```

##### 🔢 **T1.2: Scoring Engine** (3 ngày)
- [ ] `compute_raw_scores(responses, scale_meta) -> dict`
- [ ] `adjust_scores(raw, scale_meta) -> dict`  
- [ ] `classify(adjusted, bands) -> dict`
- [ ] Xử lý thiếu câu trả lời (graceful degradation)
- [ ] Unit tests với 3 bộ câu trả lời mẫu

##### 🧠 **T1.3: Rules Engine** (2 ngày)
- [ ] Function `recommend(scale, levels, flags) -> list[dict]`
- [ ] Logic: moderate+ → "gặp chuyên gia"
- [ ] Logic: normal/mild → "tự trợ" 
- [ ] PHQ-9 Q9 red-flag detection
- [ ] Unit test cho rules mapping

##### 📊 **T1.4: Charts Components** (2 ngày)
- [ ] `bar_chart(scores)` - matplotlib
- [ ] `donut_chart(levels)` - matplotlib  
- [ ] `radar_chart(domains)` - matplotlib
- [ ] Export to PNG buffer for PDF

##### 📝 **T1.5: Assessment Page** (3 ngày)
- [ ] UI chọn thang đo từ dropdown
- [ ] Render câu hỏi theo JSON (Likert 0-3)
- [ ] Progress indicator
- [ ] Lưu answers vào session_state
- [ ] Validation & error handling

##### 📊 **T1.6: Results Page** (3 ngày)
- [ ] Hiển thị điểm số + biểu đồ
- [ ] Bảng mức độ với color coding
- [ ] CTA buttons theo mức độ
- [ ] Download CSV functionality
- [ ] Integration với PDF export

##### 📄 **T1.7: PDF Export** (2 ngày)
- [ ] PDF A4 template (reportlab/fpdf)
- [ ] Embed charts as PNG
- [ ] Include scores, levels, recommendations
- [ ] Vietnamese font support

##### ⚙️ **T1.8: Admin Page** (2 ngày)
- [ ] Upload JSON thang đo mới
- [ ] Validate uploaded JSON
- [ ] Session-based statistics
- [ ] Basic analytics dashboard

##### ✅ **T1.9: Testing & QA** (1 ngày)
- [ ] Integration tests
- [ ] Error handling tests
- [ ] User acceptance testing

**Sprint 1 Acceptance Criteria**:
- [x] DASS-21 chạy hoàn chỉnh end-to-end
- [x] Lỗi nhập liệu không crash app
- [x] Xuất CSV/PDF hoạt động
- [x] Admin upload thang đo mới

---

### 📅 SPRINT 2 (Tuần 3-4): Mở rộng thang đo + Tự trợ
**Goal**: Thêm 3 thang đo mới + kho tự trợ

#### 👤 User Stories
- **U4**: "Tôi muốn có EPDS/PHQ-9/GAD-7 phù hợp tình huống"
- **U5**: "Tôi muốn xem bài tập tự trợ theo điểm số"

#### 📋 Tasks Breakdown

##### 📋 **T2.1: Additional Scales** (3 ngày)
- [ ] epds_vi.json (Edinburgh Postnatal Depression)
- [ ] phq9_vi.json (Patient Health Questionnaire-9)
- [ ] gad7_vi.json (Generalized Anxiety Disorder-7)
- [ ] Bands validation cho từng thang
- [ ] Update rules_engine cho từng thang

##### 🎵 **T2.2: Self-Help Resources** (3 ngày)
- [ ] data/resources.json structure
- [ ] Metadata: type, file, duration, conditions
- [ ] Filter logic theo user profile
- [ ] Asset management (audio/video)

**Resources Schema**:
```json
[{
  "id": "breath_446",
  "for": ["stress>=mild"],
  "type": "audio", 
  "file": "assets/audio/breathing_446.mp3",
  "duration_sec": 300,
  "script_vi": "Bài tập thở 4-4-6..."
}]
```

##### 🎧 **T2.3: SelfHelp Page** (4 ngày)
- [ ] Filter resources theo điểm số
- [ ] Audio/video player embedded
- [ ] Progress tracking (7-day checklist)
- [ ] localStorage integration
- [ ] Habit tracking UI

##### 🚨 **T2.4: Emergency Card** (1 ngày)
- [ ] Component hiển thị toàn app
- [ ] Hotline 111/115 prominent
- [ ] Red warning styling
- [ ] Context-aware triggers

##### 🧪 **T2.5: Extended Testing** (1 ngày)
- [ ] Test 3 thang đo mới
- [ ] Test resources filtering
- [ ] Emergency card integration

**Sprint 2 Acceptance Criteria**:
- [x] 4 thang đo hoạt động (DASS-21, EPDS, PHQ-9, GAD-7)
- [x] Kho tự trợ hiển thị theo điểm
- [x] Emergency card xuất hiện toàn app
- [x] 7-day habit tracking

---

### 📅 SPRINT 3 (Tuần 5-7): AI Assistant + Consultation
**Goal**: Tích hợp AI an toàn + booking system

#### 👤 User Stories  
- **U6**: "Tôi muốn hỏi AI những câu cơ bản và nhận gợi ý"
- **U7**: "Tôi muốn đặt lịch với chuyên gia"

#### 📋 Tasks Breakdown

##### 🤖 **T3.1: Safe AI Helper** (4 ngày)
- [ ] SafeAI class với OpenAI integration
- [ ] Guardrails: suicide/self-harm detection
- [ ] System prompt với disclaimers
- [ ] Response filtering & safety
- [ ] Fallback messages cho sensitive topics

**AI Helper Interface**:
```python
class SafeAI:
    def __init__(self, provider="openai", api_key=None): ...
    def generate(self, prompt: str, user_state: dict) -> str
    def check_safety(self, text: str) -> bool
    def get_safe_response(self, unsafe_input: str) -> str
```

##### 👨‍⚕️ **T3.2: Consultation Page** (3 ngày)
- [ ] Tab 1: AI Chat interface
- [ ] Tab 2: Professional booking
- [ ] SMTP email integration
- [ ] Calendly/Google Calendar links
- [ ] Contact form với validation

##### 🔐 **T3.3: Admin Authentication** (2 ngày) 
- [ ] Environment-based password
- [ ] Session management
- [ ] Role-based access
- [ ] Secure admin routes

##### 🛡️ **T3.4: Safety & Guardrails** (2 ngày)
- [ ] Keyword detection system
- [ ] Emergency response triggers
- [ ] Escalation protocols
- [ ] Crisis intervention messages

**Sprint 3 Acceptance Criteria**:
- [x] AI chat với OPENAI_API_KEY
- [x] Guardrails hoạt động 100%
- [x] Booking page với valid links
- [x] Admin authentication secure

---

### 📅 SPRINT 4 (Tuần 8-10): Security + Analytics
**Goal**: Data protection + pilot reporting

#### 👤 User Stories
- **U8**: "Tôi muốn biết dữ liệu được bảo vệ và chỉ lưu khi đồng ý"
- **U9**: "Quản trị muốn xem báo cáo ẩn danh để cải tiến"

#### 📋 Tasks Breakdown

##### 🛡️ **T4.1: Consent & Privacy** (2 ngày)
- [ ] Consent flow với checkboxes
- [ ] GDPR-compliant data handling
- [ ] Opt-in for anonymous analytics
- [ ] Data deletion functionality

##### 💾 **T4.2: Analytics Database** (3 ngày)
- [ ] SQLite analytics.db design
- [ ] Anonymous event logging
- [ ] No PII storage
- [ ] Data retention policies

**Schema**:
```sql
CREATE TABLE events (
    session_id TEXT,
    timestamp DATETIME,
    scale TEXT,
    domain TEXT,
    level TEXT,
    anonymous_id TEXT
);
```

##### 📊 **T4.3: Admin Dashboard** (3 ngày)
- [ ] Usage statistics
- [ ] Level distribution charts
- [ ] Time-based heatmaps
- [ ] Export analytics

##### 📋 **T4.4: Pilot Reports** (2 ngày)
- [ ] Automated PDF reports
- [ ] Template: goals, methods, results
- [ ] Statistical summaries
- [ ] Recommendations

**Sprint 4 Acceptance Criteria**:
- [x] No data saved without consent
- [x] Complete data deletion possible
- [x] Anonymous analytics working
- [x] Pilot reports generated

---

## 🔧 TECHNICAL STANDARDS

### 📝 **Code Quality**
- [ ] PEP8 compliance (ruff/flake8)
- [ ] Type hints (mypy)
- [ ] Docstrings (Google style)
- [ ] Test coverage ≥80%

### 🧪 **Testing Strategy**
- [ ] pytest for all modules
- [ ] Unit tests for scoring/rules
- [ ] Integration tests for workflows
- [ ] Security tests for AI guardrails

### 🚀 **CI/CD Pipeline**
```yaml
# .github/workflows/ci.yml
name: CI/CD
on: [push, pull_request]
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    python-version: 3.11
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
      - name: Install dependencies  
      - name: Lint with ruff
      - name: Test with pytest
      - name: Generate coverage
      - name: Build sample PDF
```

### 🌿 **Git Workflow**
- `main` (stable)
- `develop` (integration)
- `feat/*` (features)
- `fix/*` (hotfixes)

---

## ✅ MASTER CHECKLIST

### 🏗️ **Core Infrastructure**
- [ ] Project structure setup
- [ ] Requirements.txt complete
- [ ] Git repository initialized
- [ ] CI/CD pipeline configured

### 📊 **Assessment System**
- [ ] DASS-21 implementation complete
- [ ] EPDS implementation complete  
- [ ] PHQ-9 implementation complete
- [ ] GAD-7 implementation complete
- [ ] JSON schema validator working
- [ ] Scoring engine accurate
- [ ] Rules engine personalized

### 🎨 **User Interface**
- [ ] Assessment page responsive
- [ ] Results page with charts
- [ ] SelfHelp page functional
- [ ] Consultation page complete
- [ ] Admin page secure
- [ ] Emergency card omnipresent
- [ ] Mobile-friendly design

### 📈 **Visualization & Export**
- [ ] Bar charts (matplotlib)
- [ ] Donut charts (matplotlib)
- [ ] Radar charts (matplotlib)
- [ ] CSV export working
- [ ] PDF export with charts
- [ ] Charts embedded correctly

### 🤖 **AI & Safety**
- [ ] OpenAI integration safe
- [ ] Guardrails active
- [ ] Crisis detection working
- [ ] Disclaimers prominent
- [ ] Fallback responses ready

### 🛡️ **Security & Privacy**
- [ ] Consent flow implemented
- [ ] Data anonymization working
- [ ] No PII stored
- [ ] Data deletion possible
- [ ] Admin authentication secure

### 📊 **Analytics & Reporting**
- [ ] Anonymous usage tracking
- [ ] Admin dashboard complete
- [ ] Pilot reports automated
- [ ] Statistical exports working

### 🧪 **Quality Assurance**
- [ ] Unit tests ≥80% coverage
- [ ] Integration tests passing
- [ ] Security tests validated
- [ ] User acceptance complete
- [ ] Performance optimized

---

## 🎯 DELIVERABLES

### 📦 **Sprint Deliverables**
1. **Sprint 1**: Working DASS-21 with PDF export
2. **Sprint 2**: 4 scales + self-help system  
3. **Sprint 3**: AI chat + consultation booking
4. **Sprint 4**: Privacy-compliant analytics

### 📋 **Final Package**
- [ ] Production-ready application
- [ ] Complete documentation
- [ ] User manual (Vietnamese)
- [ ] Admin guide
- [ ] Deployment instructions
- [ ] Security audit report

---

## 🚨 RISKS & MITIGATIONS

### ⚠️ **Technical Risks**
- **AI Safety**: Comprehensive guardrails + human review
- **Data Privacy**: GDPR compliance + legal review
- **Performance**: Load testing + optimization
- **Scalability**: Cloud deployment ready

### 🛡️ **Security Considerations**
- Input validation everywhere
- API key management
- Session security
- Data encryption at rest
- Audit logging

---

## 📞 DEPENDENCIES & RESOURCES

### 🔧 **External Services**
- [ ] OpenAI API key setup
- [ ] SMTP server configuration  
- [ ] Calendly/Google Calendar integration
- [ ] Domain & SSL certificate

### 📚 **Content Requirements**
- [ ] Professional contact list
- [ ] Audio/video content licensing
- [ ] Logo/branding assets
- [ ] Legal disclaimers
- [ ] Crisis intervention protocols

---

## 🎊 SUCCESS METRICS

### 📊 **Technical KPIs**
- Test coverage ≥80%
- Page load time <3s
- Zero critical security issues
- 99% uptime target

### 👥 **User Experience KPIs**
- Assessment completion rate >90%
- User satisfaction >4/5
- Crisis intervention response <24h
- Resource engagement >60%

---

*Last Updated: August 27, 2025*  
*Version: 1.0*  
*Status: Ready for Implementation* 🚀
