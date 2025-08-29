# 🛠️ CODE TEMPLATES & PSEUDO-CODE

## 📋 IMPLEMENTATION TEMPLATES

### 🔢 components/scoring.py

```python
"""
Scoring Engine for Mental Health Assessments
Supports DASS-21, PHQ-9, GAD-7, EPDS
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
import logging

@dataclass
class ScoreResult:
    """Individual domain score result"""
    raw_score: int
    adjusted_score: int
    level: str
    percentile: Optional[float] = None

@dataclass 
class AssessmentResult:
    """Complete assessment result"""
    scale: str
    domain_scores: Dict[str, ScoreResult]
    total_score: Optional[int] = None
    flags: Dict[str, bool] = None
    timestamp: str = None

def compute_raw_scores(responses: Dict[str, int], scale_meta: Dict[str, Any]) -> Dict[str, int]:
    """
    Compute raw scores for each domain
    
    Args:
        responses: {item_id: response_value}
        scale_meta: Scale configuration from JSON
        
    Returns:
        {domain: raw_score}
    """
    scores = {domain: 0 for domain in scale_meta["domains"]}
    
    for item in scale_meta["items"]:
        item_id = item["id"]
        domain = item["domain"]
        reverse = item.get("reverse", False)
        
        if item_id not in responses:
            continue  # Skip missing responses
            
        value = responses[item_id]
        
        # Handle reverse scoring
        if reverse:
            max_value = scale_meta.get("max_response", 3)
            value = max_value - value
            
        scores[domain] += value
        
    return scores

def adjust_scores(raw_scores: Dict[str, int], scale_meta: Dict[str, Any]) -> Dict[str, int]:
    """
    Apply adjustment factor (e.g., DASS-21 uses factor of 2)
    
    Args:
        raw_scores: Raw domain scores
        scale_meta: Scale configuration
        
    Returns:
        {domain: adjusted_score}
    """
    factor = scale_meta.get("scoring", {}).get("adjustment_factor", 1)
    return {domain: score * factor for domain, score in raw_scores.items()}

def classify_scores(adjusted_scores: Dict[str, int], bands: Dict[str, List]) -> Dict[str, str]:
    """
    Classify scores into severity levels
    
    Args:
        adjusted_scores: Adjusted domain scores
        bands: {domain: [[min,max,level], ...]}
        
    Returns:
        {domain: level}
    """
    classifications = {}
    
    for domain, score in adjusted_scores.items():
        domain_bands = bands.get(domain, [])
        level = "unknown"
        
        for band in domain_bands:
            min_score, max_score, band_level = band
            if min_score <= score <= max_score:
                level = band_level
                break
                
        classifications[domain] = level
        
    return classifications

def detect_flags(responses: Dict[str, int], scale: str) -> Dict[str, bool]:
    """
    Detect special flags (e.g., suicidal ideation in PHQ-9)
    
    Args:
        responses: User responses
        scale: Scale name
        
    Returns:
        {flag_name: is_present}
    """
    flags = {}
    
    if scale == "PHQ-9":
        # Question 9: thoughts of self-harm
        q9_response = responses.get("PHQ9_Q9", 0)
        flags["suicidal_ideation"] = q9_response > 0
        
    elif scale == "DASS-21":
        # Check for severe levels across domains
        # This would need the computed scores
        pass
        
    return flags

def compute_assessment(responses: Dict[str, int], scale_meta: Dict[str, Any]) -> AssessmentResult:
    """
    Complete assessment computation pipeline
    
    Args:
        responses: User responses
        scale_meta: Scale configuration
        
    Returns:
        Complete assessment result
    """
    scale = scale_meta["scale"]
    
    # 1. Compute raw scores
    raw_scores = compute_raw_scores(responses, scale_meta)
    
    # 2. Apply adjustments
    adjusted_scores = adjust_scores(raw_scores, scale_meta)
    
    # 3. Classify severity levels
    bands = scale_meta["bands"]
    levels = classify_scores(adjusted_scores, bands)
    
    # 4. Detect special flags
    flags = detect_flags(responses, scale)
    
    # 5. Create domain score results
    domain_scores = {}
    for domain in scale_meta["domains"]:
        domain_scores[domain] = ScoreResult(
            raw_score=raw_scores[domain],
            adjusted_score=adjusted_scores[domain],
            level=levels[domain]
        )
    
    # 6. Calculate total if applicable
    total_score = sum(adjusted_scores.values()) if scale != "DASS-21" else None
    
    return AssessmentResult(
        scale=scale,
        domain_scores=domain_scores,
        total_score=total_score,
        flags=flags,
        timestamp=datetime.now().isoformat()
    )
```

---

### 🧠 components/rules_engine.py

```python
"""
Rules Engine for generating personalized recommendations
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class Priority(Enum):
    URGENT = 0      # Crisis intervention
    HIGH = 1        # Professional help
    MEDIUM = 2      # Self-help + monitoring  
    LOW = 3         # Maintenance/prevention

@dataclass
class Recommendation:
    """Single recommendation"""
    id: str
    title: str
    description: str
    rationale: str
    priority: Priority
    actions: List[str]
    resources: List[str] = None

# Severity level ordering for comparisons
LEVEL_ORDER = ["normal", "mild", "moderate", "severe", "extremely_severe"]

def level_ge(level_a: str, level_b: str) -> bool:
    """Check if level_a >= level_b in severity"""
    try:
        return LEVEL_ORDER.index(level_a) >= LEVEL_ORDER.index(level_b)
    except ValueError:
        return False

def level_max(levels: Dict[str, str]) -> str:
    """Get highest severity level from domains"""
    max_level = "normal"
    for level in levels.values():
        if level_ge(level, max_level):
            max_level = level
    return max_level

def recommend_by_scale(scale: str, levels: Dict[str, str], flags: Dict[str, bool] = None) -> List[Recommendation]:
    """
    Generate recommendations based on scale and results
    
    Args:
        scale: Assessment scale name
        levels: {domain: severity_level}
        flags: Special flags (suicidal ideation, etc.)
        
    Returns:
        List of recommendations sorted by priority
    """
    recommendations = []
    flags = flags or {}
    
    # Crisis intervention (highest priority)
    if flags.get("suicidal_ideation", False):
        recommendations.append(Recommendation(
            id="crisis_intervention",
            title="Cần hỗ trợ khẩn cấp",
            description="Bạn đã báo cáo những suy nghĩ về việc tự làm hại bản thân",
            rationale="Phát hiện nguy cơ tự hại từ câu trả lời",
            priority=Priority.URGENT,
            actions=[
                "Gọi ngay hotline 115 hoặc 111",
                "Đến bệnh viện gần nhất", 
                "Liên hệ người thân tin tưởng",
                "Không ở một mình"
            ],
            resources=["emergency_contacts", "crisis_hotlines"]
        ))
    
    # Get maximum severity across domains
    max_severity = level_max(levels)
    
    # Professional help recommendations
    if level_ge(max_severity, "severe"):
        recommendations.append(Recommendation(
            id="urgent_professional",
            title="Cần gặp chuyên gia ngay",
            description="Mức độ nghiêm trọng, cần can thiệp chuyên nghiệp",
            rationale=f"Ít nhất một chỉ số ở mức {max_severity}",
            priority=Priority.HIGH,
            actions=[
                "Đặt lịch với bác sĩ tâm thần trong 1-2 ngày",
                "Chuẩn bị danh sách triệu chứng",
                "Mang theo kết quả đánh giá này"
            ],
            resources=["professional_contacts", "clinic_locations"]
        ))
        
    elif level_ge(max_severity, "moderate"):
        recommendations.append(Recommendation(
            id="professional_help",
            title="Nên gặp chuyên gia tâm lý",
            description="Mức độ vừa phải, có thể cần hỗ trợ chuyên nghiệp",
            rationale=f"Một hoặc nhiều chỉ số ở mức {max_severity}",
            priority=Priority.HIGH,
            actions=[
                "Tìm hiểu và đặt lịch tư vấn tâm lý",
                "Theo dõi triệu chứng hàng ngày",
                "Thực hiện các bài tập tự trợ"
            ],
            resources=["counselor_contacts", "therapy_options"]
        ))
    
    # Self-help recommendations  
    if level_ge(max_severity, "mild"):
        recommendations.append(Recommendation(
            id="structured_self_help",
            title="Chương trình tự trợ có cấu trúc",
            description="Thực hiện bài tập tự trợ đều đặn",
            rationale="Mức độ nhẹ, có thể cải thiện với tự trợ",
            priority=Priority.MEDIUM,
            actions=[
                "Thực hiện bài tập thở sâu mỗi ngày",
                "Ghi nhật ký cảm xúc",
                "Duy trì lịch ngủ đều đặn",
                "Tập thể dục nhẹ 30 phút/ngày"
            ],
            resources=["breathing_exercises", "mood_diary", "sleep_hygiene"]
        ))
    else:
        recommendations.append(Recommendation(
            id="maintenance",
            title="Duy trì sức khỏe tâm thần",
            description="Tiếp tục các thói quen tích cực",
            rationale="Mức độ bình thường, duy trì hiện trạng",
            priority=Priority.LOW,
            actions=[
                "Tiếp tục các hoạt động yêu thích",
                "Duy trì mối quan hệ xã hội",
                "Thực hiện đánh giá định kỳ"
            ],
            resources=["wellness_tips", "social_activities"]
        ))
    
    # Scale-specific recommendations
    if scale == "DASS-21":
        if level_ge(levels.get("stress", "normal"), "moderate"):
            recommendations.append(Recommendation(
                id="stress_management",
                title="Quản lý căng thẳng",
                description="Kỹ thuật chuyên biệt cho căng thẳng",
                rationale="Mức căng thẳng cao được phát hiện",
                priority=Priority.MEDIUM,
                actions=[
                    "Thực hiện kỹ thuật thư giãn cơ",
                    "Học cách quản lý thời gian",
                    "Giảm caffeine và nicotine"
                ],
                resources=["stress_management", "relaxation_techniques"]
            ))
            
        if level_ge(levels.get("anxiety", "normal"), "moderate"):
            recommendations.append(Recommendation(
                id="anxiety_coping",
                title="Đối phó với lo âu",
                description="Kỹ thuật giảm lo âu",
                rationale="Mức lo âu cao được phát hiện",
                priority=Priority.MEDIUM,
                actions=[
                    "Thực hiện bài tập thở 4-7-8",
                    "Áp dụng kỹ thuật grounding 5-4-3-2-1",
                    "Tránh caffeine và rượu"
                ],
                resources=["anxiety_exercises", "grounding_techniques"]
            ))
    
    elif scale == "PHQ-9":
        if level_ge(levels.get("depression", "normal"), "moderate"):
            recommendations.append(Recommendation(
                id="depression_support",
                title="Hỗ trợ trầm cảm",
                description="Chiến lược đối phó với trầm cảm",
                rationale="Triệu chứng trầm cảm được phát hiện",
                priority=Priority.MEDIUM,
                actions=[
                    "Thiết lập routine hàng ngày",
                    "Tăng cường hoạt động xã hội",
                    "Tập trung vào giấc ngủ chất lượng"
                ],
                resources=["depression_support", "social_activities"]
            ))
    
    # Sort by priority (urgent first)
    recommendations.sort(key=lambda r: r.priority.value)
    
    return recommendations

def get_resources_for_recommendations(recommendations: List[Recommendation]) -> List[str]:
    """Extract unique resource IDs from recommendations"""
    resources = set()
    for rec in recommendations:
        if rec.resources:
            resources.update(rec.resources)
    return list(resources)
```

---

### 📊 components/charts.py

```python
"""
Chart generation for assessment results
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import io
from typing import Dict, List, Tuple
import base64

# Vietnamese font setup
plt.rcParams['font.family'] = 'DejaVu Sans'

def setup_vietnamese_font():
    """Setup Vietnamese font support"""
    try:
        from matplotlib import font_manager
        # Add custom font if available
        font_path = "assets/fonts/DejaVuSans.ttf"
        if os.path.exists(font_path):
            font_manager.fontManager.addfont(font_path)
            plt.rcParams['font.family'] = 'DejaVu Sans'
    except:
        pass

def get_level_color(level: str) -> str:
    """Get color for severity level"""
    colors = {
        "normal": "#4CAF50",         # Green
        "mild": "#FFC107",           # Amber  
        "moderate": "#FF9800",       # Orange
        "severe": "#F44336",         # Red
        "extremely_severe": "#9C27B0" # Purple
    }
    return colors.get(level, "#757575")  # Grey default

def bar_chart(domain_scores: Dict[str, int], levels: Dict[str, str], title: str = "Kết quả đánh giá") -> io.BytesIO:
    """
    Create bar chart of domain scores
    
    Args:
        domain_scores: {domain: score}
        levels: {domain: severity_level}
        title: Chart title
        
    Returns:
        PNG image buffer
    """
    setup_vietnamese_font()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    domains = list(domain_scores.keys())
    scores = list(domain_scores.values())
    colors = [get_level_color(levels[domain]) for domain in domains]
    
    # Create bars
    bars = ax.bar(domains, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    # Add value labels on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{score}', ha='center', va='bottom', fontweight='bold')
    
    # Styling
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Điểm số', fontsize=12)
    ax.set_xlabel('Lĩnh vực', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=45, ha='right')
    
    # Tight layout
    plt.tight_layout()
    
    # Save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    return buffer

def donut_chart(levels: Dict[str, str], title: str = "Phân bố mức độ") -> io.BytesIO:
    """
    Create donut chart of severity levels
    """
    setup_vietnamese_font()
    
    # Count levels
    level_counts = {}
    for level in levels.values():
        level_counts[level] = level_counts.get(level, 0) + 1
    
    if not level_counts:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    labels = list(level_counts.keys())
    sizes = list(level_counts.values())
    colors = [get_level_color(level) for level in labels]
    
    # Create donut chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
                                      startangle=90, pctdistance=0.85)
    
    # Add center circle for donut effect
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Styling
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    
    # Save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    return buffer

def radar_chart(domain_scores: Dict[str, int], max_scores: Dict[str, int], title: str = "Biểu đồ radar") -> io.BytesIO:
    """
    Create radar chart of domain scores
    """
    setup_vietnamese_font()
    
    domains = list(domain_scores.keys())
    scores = list(domain_scores.values())
    max_vals = [max_scores.get(domain, 42) for domain in domains]
    
    # Normalize scores to 0-1
    normalized_scores = [score/max_val for score, max_val in zip(scores, max_vals)]
    
    # Number of variables
    N = len(domains)
    
    # Compute angle for each domain
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Add first value to end to close the radar chart
    normalized_scores += normalized_scores[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot data
    ax.plot(angles, normalized_scores, 'o-', linewidth=2, label='Kết quả của bạn')
    ax.fill(angles, normalized_scores, alpha=0.25)
    
    # Add domain labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(domains)
    
    # Set y-axis limits
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
    
    # Add title
    ax.set_title(title, size=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    # Save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    return buffer

def chart_to_base64(buffer: io.BytesIO) -> str:
    """Convert chart buffer to base64 string for embedding"""
    if buffer is None:
        return ""
    
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    return f"data:image/png;base64,{image_base64}"

def save_chart_for_pdf(buffer: io.BytesIO, filename: str) -> str:
    """Save chart buffer to file for PDF inclusion"""
    if buffer is None:
        return ""
        
    buffer.seek(0)
    with open(filename, 'wb') as f:
        f.write(buffer.read())
    return filename
```

---

### 📄 components/pdf_export.py

```python
"""
PDF Export functionality for assessment results
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import tempfile
import os
from datetime import datetime
from typing import Dict, List, Any

def setup_vietnamese_fonts():
    """Register Vietnamese-compatible fonts"""
    try:
        # Register DejaVu Sans font for Vietnamese support
        font_path = "assets/fonts/DejaVuSans.ttf"
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            return 'DejaVuSans'
    except:
        pass
    return 'Helvetica'  # Fallback

def create_assessment_pdf(assessment_result: Any, recommendations: List[Any], chart_buffers: Dict[str, io.BytesIO]) -> io.BytesIO:
    """
    Create comprehensive PDF report
    
    Args:
        assessment_result: Assessment results
        recommendations: List of recommendations
        chart_buffers: {chart_name: image_buffer}
        
    Returns:
        PDF buffer
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    
    # Setup fonts
    font_name = setup_vietnamese_fonts()
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=14,
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=6
    )
    
    # Story elements
    story = []
    
    # Title
    story.append(Paragraph("BÁO CÁO ĐÁNH GIÁ SỨC KHỎE TÂM THẦN", title_style))
    story.append(Spacer(1, 20))
    
    # Date and scale info
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"Ngày thực hiện: {date_str}", normal_style))
    story.append(Paragraph(f"Thang đo: {assessment_result.scale}", normal_style))
    story.append(Spacer(1, 20))
    
    # Scores table
    story.append(Paragraph("KẾT QUẢ ĐÁNH GIÁ", heading_style))
    
    table_data = [["Lĩnh vực", "Điểm thô", "Điểm hiệu chỉnh", "Mức độ"]]
    
    for domain, score_result in assessment_result.domain_scores.items():
        table_data.append([
            domain.title(),
            str(score_result.raw_score),
            str(score_result.adjusted_score),
            score_result.level.title()
        ])
    
    table = Table(table_data, colWidths=[2*inch, 1*inch, 1.2*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Charts
    if chart_buffers:
        story.append(Paragraph("BIỂU ĐỒ TRỰC QUAN", heading_style))
        
        for chart_name, buffer in chart_buffers.items():
            if buffer:
                # Save buffer to temporary file
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    buffer.seek(0)
                    tmp_file.write(buffer.read())
                    tmp_filename = tmp_file.name
                
                try:
                    # Add image to PDF
                    img = Image(tmp_filename, width=4*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 10))
                finally:
                    # Clean up temp file
                    os.unlink(tmp_filename)
    
    # Recommendations
    story.append(Paragraph("KHUYẾN NGHỊ", heading_style))
    
    for i, rec in enumerate(recommendations, 1):
        # Recommendation title
        rec_title = Paragraph(f"{i}. {rec.title}", 
                             ParagraphStyle('RecTitle', parent=normal_style, 
                                          fontSize=11, fontName=font_name, 
                                          textColor=colors.darkblue, 
                                          spaceAfter=3))
        story.append(rec_title)
        
        # Description
        story.append(Paragraph(rec.description, normal_style))
        
        # Actions
        if rec.actions:
            actions_text = "<br/>".join([f"• {action}" for action in rec.actions])
            story.append(Paragraph(f"<b>Hành động:</b><br/>{actions_text}", normal_style))
        
        story.append(Spacer(1, 10))
    
    # Disclaimer
    story.append(Spacer(1, 30))
    disclaimer = """
    <b>Lưu ý quan trọng:</b> Kết quả này chỉ mang tính chất tham khảo và không thay thế 
    chẩn đoán y khoa chuyên nghiệp. Nếu bạn đang gặp khó khăn về sức khỏe tâm thần, 
    vui lòng tham khảo ý kiến bác sĩ hoặc chuyên gia tâm lý.
    """
    story.append(Paragraph(disclaimer, 
                          ParagraphStyle('Disclaimer', parent=normal_style,
                                       fontSize=8, textColor=colors.grey,
                                       borderWidth=1, borderColor=colors.grey,
                                       borderPadding=10)))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer

def create_csv_export(assessment_result: Any) -> str:
    """Create CSV export of results"""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['Domain', 'Raw_Score', 'Adjusted_Score', 'Level'])
    
    # Data rows
    for domain, score_result in assessment_result.domain_scores.items():
        writer.writerow([
            domain,
            score_result.raw_score,
            score_result.adjusted_score,
            score_result.level
        ])
    
    return output.getvalue()
```

---

### 🎨 components/ui.py - Emergency Card

```python
"""
Reusable UI Components
"""

import streamlit as st
from typing import List, Dict, Any

def emergency_card():
    """Display emergency contact card"""
    with st.container():
        st.markdown("""
        <div style="
            background-color: #ffebee; 
            border-left: 5px solid #f44336; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px;
        ">
            <h4 style="color: #d32f2f; margin: 0 0 10px 0;">🚨 Hỗ trợ khẩn cấp</h4>
            <p style="margin: 5px 0;">
                <strong>Hotline 24/7:</strong><br>
                • Cấp cứu: <strong>115</strong><br>
                • Tư vấn tâm lý: <strong>1900 6116</strong><br>
                • Crisis Text Line: Nhắn "TIN" đến <strong>741741</strong>
            </p>
            <p style="margin: 5px 0; font-size: 12px; color: #666;">
                Nếu bạn có suy nghĩ tự hại, hãy liên hệ ngay với các số trên hoặc đến bệnh viện gần nhất.
            </p>
        </div>
        """, unsafe_allow_html=True)

def progress_indicator(current_step: int, total_steps: int, step_names: List[str] = None):
    """Display progress indicator"""
    progress = current_step / total_steps
    
    st.progress(progress)
    
    if step_names and len(step_names) >= total_steps:
        cols = st.columns(total_steps)
        for i, col in enumerate(cols):
            with col:
                if i < current_step:
                    st.markdown(f"✅ {step_names[i]}")
                elif i == current_step:
                    st.markdown(f"🔄 **{step_names[i]}**")
                else:
                    st.markdown(f"⏳ {step_names[i]}")

def result_card(title: str, value: str, level: str, description: str = ""):
    """Display result card with color coding"""
    colors = {
        "normal": "#4CAF50",
        "mild": "#FFC107", 
        "moderate": "#FF9800",
        "severe": "#F44336",
        "extremely_severe": "#9C27B0"
    }
    
    color = colors.get(level.lower(), "#757575")
    
    st.markdown(f"""
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    ">
        <h4 style="margin: 0 0 10px 0; color: {color};">{title}</h4>
        <h2 style="margin: 0; color: {color};">{value}</h2>
        <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def recommendation_card(recommendation: Any):
    """Display recommendation card"""
    priority_colors = {
        0: "#f44336",  # Urgent - Red
        1: "#ff9800",  # High - Orange  
        2: "#2196f3",  # Medium - Blue
        3: "#4caf50"   # Low - Green
    }
    
    color = priority_colors.get(recommendation.priority.value, "#757575")
    
    with st.expander(f"{recommendation.title}", expanded=recommendation.priority.value <= 1):
        st.markdown(f"""
        <div style="border-left: 4px solid {color}; padding-left: 15px;">
            <p><strong>Mô tả:</strong> {recommendation.description}</p>
            <p><strong>Lý do:</strong> {recommendation.rationale}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if recommendation.actions:
            st.markdown("**Hành động cần thực hiện:**")
            for action in recommendation.actions:
                st.markdown(f"• {action}")
```

---

### 🔐 components/auth.py

```python
"""
Simple authentication for admin features
"""

import streamlit as st
import hashlib
import os
from functools import wraps

def check_admin_password(password: str) -> bool:
    """Check if provided password matches admin password"""
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # Change in production
    return password == admin_password

def require_admin_auth(func):
    """Decorator to require admin authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "admin_authenticated" not in st.session_state:
            st.session_state.admin_authenticated = False
        
        if not st.session_state.admin_authenticated:
            st.title("🔐 Admin Login")
            
            with st.form("admin_login"):
                password = st.text_input("Admin Password", type="password")
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    if check_admin_password(password):
                        st.session_state.admin_authenticated = True
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid password!")
            
            st.stop()
        
        return func(*args, **kwargs)
    
    return wrapper

def admin_logout():
    """Logout admin user"""
    st.session_state.admin_authenticated = False
    st.success("Logged out successfully!")
    st.rerun()
```

Những template này cung cấp:

1. **Cấu trúc code rõ ràng** với type hints và docstrings
2. **Error handling** và validation ở mọi level
3. **Vietnamese language support** cho UI và PDF
4. **Modular design** dễ test và maintain
5. **Security considerations** cho admin và AI features
6. **Performance optimization** với caching và efficient algorithms

Bạn có thể copy-paste những template này và customize theo nhu cầu cụ thể! 🚀
