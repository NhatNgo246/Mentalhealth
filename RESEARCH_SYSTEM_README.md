# 🔬 SOULFRIEND Research Data Collection System

## 📋 Tổng quan

Hệ thống thu thập dữ liệu nghiên cứu cho SOULFRIEND được thiết kế **hoàn toàn không xâm phạm**, đảm bảo:

✅ **Không ảnh hưởng** đến logic và cấu trúc ứng dụng hiện tại  
✅ **Hoàn toàn tùy chọn** - có thể bật/tắt dễ dàng  
✅ **An toàn tuyệt đối** - silent fail, không làm crash app  
✅ **Tuân thủ quy định** - ẩn danh, mã hóa, consent-based  

## 🏗️ Kiến trúc

```
SOULFRIEND.py (Main App)
    ↓ Optional Integration
research_system/
    ├── collector.py          # Core collection logic
    ├── integration.py        # Safe integration wrapper  
    ├── consent_ui.py         # Consent management
    ├── collection_api.py     # FastAPI service
    └── config.py            # Environment setup
```

## 🚀 Triển khai (Không ảnh hưởng đến app hiện tại)

### Bước 1: Test Research System
```bash
# Test để đảm bảo an toàn
python research_demo.py --test
```

### Bước 2: Tích hợp vào SOULFRIEND (Optional)
Thêm vào cuối file `SOULFRIEND.py`:

```python
# ===== RESEARCH SYSTEM INTEGRATION (OPTIONAL) =====
try:
    from research_system.integration import research_track_if_enabled
    
    # Track events an toàn
    research_track_if_enabled("session_start")
    
    # Trong questionnaire handler:
    # research_track_if_enabled("questionnaire_start", questionnaire_type)
    # research_track_if_enabled("question_answer", questionnaire_type, idx, answer)
    # research_track_if_enabled("questionnaire_complete", questionnaire_type, score)
    
except ImportError:
    pass  # Research system không có sẵn - không sao
# ===== END RESEARCH INTEGRATION =====
```

### Bước 3: Chạy Collection API (Optional)
```bash
# Chạy API riêng trên port 8502
python research_demo.py --api
```

## 🔧 Cấu hình

### Environment Variables
```bash
# Bật research collection
export ENABLE_RESEARCH_COLLECTION=true

# Cấu hình bảo mật
export RESEARCH_SECRET=your_secret_key_here
export PSEUDO_SECRET=your_pseudo_key_here
export RESEARCH_PORT=8502
```

### Mặc định (An toàn)
- `ENABLE_RESEARCH_COLLECTION=false` (TẮT)
- Tất cả tracking functions là safe dummy nếu không có research system
- Không ảnh hưởng đến performance hoặc UX

## 📊 Event Types được thu thập

| Event | Dữ liệu | Mục đích |
|-------|---------|----------|
| `session_started` | user_agent, locale | Hiểu người dùng |
| `questionnaire_started` | type, version | Phân tích usage |
| `question_answered` | item_id, response, time | Nghiên cứu patterns |
| `questionnaire_completed` | scores, duration | Đánh giá hiệu quả |
| `results_viewed` | completion_stats | UX research |

## 🔐 Bảo mật & Privacy

### Ẩn danh hóa
- **User Hash**: HMAC-SHA256 với secret key
- **Pseudo ID**: Hash 2 lớp không thể đảo ngược
- **No PII**: Không lưu thông tin cá nhân

### Dữ liệu được mã hóa
- **At Rest**: File JSONL với encryption
- **In Transit**: HTTPS/TLS
- **Key Management**: Environment variables

### Consent Management
- **Opt-in**: Mặc định TẮT, phải chọn BẬT
- **Transparent**: Giải thích rõ mục đích
- **Revocable**: Có thể rút lại bất kỳ lúc nào

## 📈 Monitoring & Analytics

### Health Check
```bash
curl http://localhost:8502/health
```

### Collection Stats
```bash
curl http://localhost:8502/stats
```

### Data Files
- Location: `/workspaces/Mentalhealth/research_data/`
- Format: JSONL (one JSON per line)
- Naming: `events_YYYYMMDD.jsonl`

## 🔄 Integration Points (Hoàn toàn Optional)

### 1. Session Tracking
```python
from research_system.integration import safe_track_session_start
safe_track_session_start(user_agent="...", locale="vi")
```

### 2. Questionnaire Events
```python
from research_system.integration import safe_track_questionnaire_start
safe_track_questionnaire_start("PHQ-9")
```

### 3. Question Responses
```python
from research_system.integration import safe_track_question_answer
safe_track_question_answer("PHQ-9", question_idx=1, answer=2)
```

### 4. Completion Events
```python
from research_system.integration import safe_track_questionnaire_complete
safe_track_questionnaire_complete("PHQ-9", total_score=12)
```

## ✅ Đảm bảo An toàn

### 1. Non-invasive Design
- Không sửa đổi code hiện tại
- Tất cả functions có safe fallback
- Silent fail - không throw exceptions

### 2. Performance Safe
- Background processing (threading)
- Short timeout (1 second)
- No blocking operations

### 3. Privacy Compliant
- Default OFF
- Explicit consent required
- Anonymized data only
- Data retention policies

## 🎯 Sử dụng

### Chế độ Development (Tắt Research)
```bash
# Mặc định - research TẮT
python SOULFRIEND.py
```

### Chế độ Research (Bật Research)
```bash
# Bật research collection
export ENABLE_RESEARCH_COLLECTION=true

# Chạy API collector
python research_demo.py --api &

# Chạy SOULFRIEND như bình thường
python SOULFRIEND.py
```

## 📝 Logs & Debugging

### Research Logs
- Location: `/workspaces/Mentalhealth/logs/research.log`
- Level: INFO (có thể đổi thành DEBUG)

### Collection Status
```python
from research_system.config import is_research_safe_to_enable
print(f"Research safe: {is_research_safe_to_enable()}")
```

## 🤝 Roadmap Tiếp theo

### Phase 1 ✅ (Hoàn thành)
- [x] Core collection system
- [x] Safe integration wrapper
- [x] Basic API collector
- [x] Testing & validation

### Phase 2 (2 tuần)
- [ ] Database integration (PostgreSQL)
- [ ] Advanced anonymization
- [ ] Consent UI enhancement
- [ ] Admin dashboard

### Phase 3 (1 tuần)
- [ ] ETL pipeline
- [ ] Dataset generation
- [ ] Analytics dashboard
- [ ] Production deployment

## 📞 Support

Hệ thống research được thiết kế để **hoàn toàn độc lập**. Nếu có vấn đề:

1. **Tắt research**: `export ENABLE_RESEARCH_COLLECTION=false`
2. **Xóa research_system folder** - app vẫn chạy bình thường
3. **Check logs**: `/workspaces/Mentalhealth/logs/research.log`

**Cam kết: Research system sẽ KHÔNG BAO GIỜ làm crash hoặc ảnh hưởng đến SOULFRIEND chính!** 🛡️
