"""
PDF Export Module for SOULFRIEND
Generates professional PDF reports of assessment results
"""

# Only import Streamlit when actually running in Streamlit context
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from datetime import datetime
import io
import base64
from typing import Dict, Any

def create_header_footer(canvas, doc):
    """Create header and footer for PDF pages"""
    canvas.saveState()
    
    # Header
    canvas.setFont('Helvetica-Bold', 16)
    canvas.setFillColor(colors.HexColor('#4a90e2'))
    canvas.drawString(50, letter[1] - 50, "🧠 SOULFRIEND - Báo cáo đánh giá sức khỏe tâm thần")
    
    # Header line
    canvas.setStrokeColor(colors.HexColor('#4a90e2'))
    canvas.setLineWidth(2)
    canvas.line(50, letter[1] - 70, letter[0] - 50, letter[1] - 70)
    
    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    footer_text = f"Tạo ngày: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Trang {doc.page}"
    canvas.drawString(50, 50, footer_text)
    
    # Footer disclaimer
    disclaimer = "⚠️ Báo cáo này chỉ mang tính tham khảo, không thay thế chẩn đoán y khoa chuyên nghiệp"
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.drawCentredString(letter[0]/2, 30, disclaimer)
    
    canvas.restoreState()

def create_assessment_summary_table(enhanced_result, questionnaire_type: str) -> Table:
    """Create summary table for assessment results"""
    
    data = [
        ['Thông tin đánh giá', 'Kết quả'],
        ['Loại thang đo', questionnaire_type],
        ['Ngày thực hiện', datetime.now().strftime('%d/%m/%Y')],
        ['Tổng điểm', str(enhanced_result.total_score)],
        ['Mức độ nghiêm trọng', enhanced_result.severity_level.replace('_', ' ').title()],
        ['Diễn giải', enhanced_result.interpretation[:100] + '...' if len(enhanced_result.interpretation) > 100 else enhanced_result.interpretation]
    ]
    
    table = Table(data, colWidths=[2.5*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    return table

def create_subscales_table(subscales: Dict[str, Dict]) -> Table:
    """Create detailed subscales breakdown table"""
    
    if not subscales:
        return None
    
    data = [['Lĩnh vực', 'Điểm số', 'Mức độ', 'Mô tả']]
    
    for subscale_name, subscale_data in subscales.items():
        data.append([
            subscale_name,
            str(subscale_data['score']),
            subscale_data['level'].title(),
            subscale_data.get('description', 'Không có mô tả')[:50] + '...'
        ])
    
    table = Table(data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 2.3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7b68ee')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightblue]),
    ]))
    
    return table

def create_recommendations_section(recommendations: Dict[str, Any]) -> list:
    """Create recommendations section for PDF"""
    
    styles = getSampleStyleSheet()
    story = []
    
    # Recommendations title
    rec_style = ParagraphStyle(
        'RecommendationTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#2c3e50'),
        leftIndent=0
    )
    
    story.append(Paragraph("💡 Khuyến nghị cá nhân hóa", rec_style))
    
    # Main recommendation
    if 'title' in recommendations:
        title_style = ParagraphStyle(
            'RecTitle',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#e74c3c'),
            spaceAfter=6
        )
        story.append(Paragraph(f"🎯 {recommendations['title']}", title_style))
    
    if 'message' in recommendations:
        message_style = ParagraphStyle(
            'RecMessage',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            leftIndent=20,
            rightIndent=20,
            alignment=TA_JUSTIFY
        )
        story.append(Paragraph(recommendations['message'], message_style))
    
    # Action suggestions
    if 'suggestions' in recommendations:
        story.append(Paragraph("🚀 Các bước cần thực hiện:", rec_style))
        
        suggestion_style = ParagraphStyle(
            'Suggestions',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=30,
            bulletIndent=20
        )
        
        for i, suggestion in enumerate(recommendations['suggestions'], 1):
            story.append(Paragraph(f"{i}. {suggestion}", suggestion_style))
    
    return story

def create_risk_assessment_section(severity_level: str) -> list:
    """Create risk assessment and emergency contact section"""
    
    styles = getSampleStyleSheet()
    story = []
    
    # Risk level assessment
    risk_style = ParagraphStyle(
        'RiskTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#d32f2f')
    )
    
    story.append(Paragraph("⚠️ Đánh giá mức độ rủi ro", risk_style))
    
    # Risk level description
    risk_levels = {
        'normal': ('Mức độ bình thường', 'Tiếp tục duy trì lối sống tích cực', colors.green),
        'mild': ('Mức độ nhẹ', 'Cần theo dõi và chăm sóc bản thân', colors.orange),
        'moderate': ('Mức độ trung bình', 'Nên tìm kiếm hỗ trợ chuyên nghiệp', colors.orange),
        'severe': ('Mức độ nghiêm trọng', 'Cần can thiệp chuyên nghiệp ngay lập tức', colors.red),
        'extremely_severe': ('Mức độ cực kỳ nghiêm trọng', 'Cần hỗ trợ y tế khẩn cấp', colors.red)
    }
    
    level_info = risk_levels.get(severity_level, ('Chưa xác định', 'Cần đánh giá thêm', colors.grey))
    
    risk_desc_style = ParagraphStyle(
        'RiskDesc',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        textColor=level_info[2],
        alignment=TA_LEFT
    )
    
    story.append(Paragraph(f"<b>Mức độ:</b> {level_info[0]}", risk_desc_style))
    story.append(Paragraph(f"<b>Khuyến nghị:</b> {level_info[1]}", risk_desc_style))
    
    # Emergency contacts if high risk
    if severity_level in ['severe', 'extremely_severe']:
        emergency_style = ParagraphStyle(
            'Emergency',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=colors.red,
            borderColor=colors.red,
            borderWidth=1,
            borderPadding=10
        )
        
        story.append(Paragraph("🆘 LIÊN HỆ KHẨN CẤP", risk_style))
        story.append(Paragraph("• Đường dây nóng: 1800-1567", emergency_style))
        story.append(Paragraph("• Cấp cứu: 115", emergency_style))
        story.append(Paragraph("• Tư vấn tâm lý: 1900-555-555", emergency_style))
    
    return story

def generate_pdf_report(enhanced_result, questionnaire_type: str, user_info: Dict = None) -> bytes:
    """Generate comprehensive PDF report"""
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=100,
        bottomMargin=100
    )
    
    # Story list to hold all content
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#34495e')
    )
    
    # Title
    story.append(Paragraph("Báo cáo Đánh giá Sức khỏe Tâm thần", title_style))
    story.append(Spacer(1, 20))
    
    # User info section (if provided)
    if user_info:
        story.append(Paragraph("👤 Thông tin cá nhân", heading_style))
        user_table_data = []
        for key, value in user_info.items():
            user_table_data.append([key, value])
        
        user_table = Table(user_table_data, colWidths=[2*inch, 3*inch])
        user_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(user_table)
        story.append(Spacer(1, 20))
    
    # Assessment summary
    story.append(Paragraph("📊 Tóm tắt kết quả", heading_style))
    summary_table = create_assessment_summary_table(enhanced_result, questionnaire_type)
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Subscales breakdown (if available)
    if hasattr(enhanced_result, 'subscales') and enhanced_result.subscales:
        story.append(Paragraph("📈 Chi tiết theo lĩnh vực", heading_style))
        subscales_table = create_subscales_table(enhanced_result.subscales)
        if subscales_table:
            story.append(subscales_table)
            story.append(Spacer(1, 20))
    
    # Recommendations
    if hasattr(enhanced_result, 'recommendations'):
        story.extend(create_recommendations_section(enhanced_result.recommendations))
        story.append(Spacer(1, 20))
    
    # Risk assessment
    story.extend(create_risk_assessment_section(enhanced_result.severity_level))
    story.append(Spacer(1, 20))
    
    # Legal disclaimer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_JUSTIFY,
        borderColor=colors.grey,
        borderWidth=1,
        borderPadding=10
    )
    
    disclaimer_text = """
    <b>Tuyên bố miễn trừ trách nhiệm:</b><br/><br/>
    Báo cáo này được tạo ra bởi ứng dụng SOULFRIEND và chỉ mang tính chất tham khảo. 
    Kết quả không thay thế cho việc chẩn đoán, điều trị hoặc tư vấn y khoa chuyên nghiệp. 
    Nếu bạn đang gặp phải các vấn đề nghiêm trọng về sức khỏe tâm thần, vui lòng liên hệ 
    với các chuyên gia y tế hoặc dịch vụ hỗ trợ khẩn cấp.<br/><br/>
    Ứng dụng SOULFRIEND được phát triển nhằm mục đích hỗ trợ sàng lọc ban đầu và 
    nâng cao nhận thức về sức khỏe tâm thần.
    """
    
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Build PDF
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def create_download_button(enhanced_result, questionnaire_type: str, user_info: Dict = None):
    """Create download button for PDF report"""
    
    if st.button("📄 Tải báo cáo PDF", use_container_width=True, type="secondary"):
        try:
            with st.spinner("🔄 Đang tạo báo cáo PDF..."):
                pdf_bytes = generate_pdf_report(enhanced_result, questionnaire_type, user_info)
                
                # Create download filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"SOULFRIEND_BaoCao_{questionnaire_type}_{timestamp}.pdf"
                
                st.download_button(
                    label="💾 Tải về báo cáo PDF",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success("✅ Báo cáo PDF đã sẵn sàng để tải về!")
                st.info("💡 Báo cáo bao gồm: Kết quả đánh giá, phân tích chi tiết, khuyến nghị và thông tin liên hệ khẩn cấp.")
                
        except Exception as e:
            st.error(f"❌ Lỗi khi tạo báo cáo PDF: {str(e)}")
            st.info("🔧 Vui lòng thử lại hoặc liên hệ admin để được hỗ trợ.")

def create_email_report_option(enhanced_result, questionnaire_type: str):
    """Create option to email the report (placeholder for future feature)"""
    
    with st.expander("📧 Gửi báo cáo qua email (Sắp có)"):
        email = st.text_input("Địa chỉ email của bạn:", placeholder="example@email.com")
        
        if st.button("📧 Gửi báo cáo", disabled=True):
            st.info("🚧 Tính năng gửi email sẽ có trong phiên bản tiếp theo!")
            # Future implementation:
            # - Generate PDF
            # - Send via email service (SendGrid, AWS SES, etc.)
            # - Include secure sharing options

def generate_assessment_report(assessment_data: Dict[str, Any]) -> bytes:
    """
    Generate PDF assessment report
    
    Args:
        assessment_data: Dictionary containing assessment information
        
    Returns:
        bytes: PDF file content as bytes
    """
    try:
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=100,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E86AB')
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#A23B72')
        )
        
        # Build content
        content = []
        
        # Title
        content.append(Paragraph("🧠 SOULFRIEND - BÁO CÁO ĐÁNH GIÁ SỨC KHỎE TÂM THẦN", title_style))
        content.append(Spacer(1, 20))
        
        # Assessment info
        content.append(Paragraph("📋 THÔNG TIN ĐÁNH GIÁ", header_style))
        
        assessment_info = [
            ["Ngày đánh giá:", assessment_data.get('assessment_date', 'N/A')],
            ["Loại đánh giá:", assessment_data.get('assessment_type', 'N/A')],
            ["Thời gian tạo báo cáo:", datetime.now().strftime("%d/%m/%Y %H:%M")]
        ]
        
        info_table = Table(assessment_info, colWidths=[3*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        content.append(info_table)
        content.append(Spacer(1, 20))
        
        # Scores section
        if 'scores' in assessment_data:
            content.append(Paragraph("📊 KẾT QUẢ ĐÁNH GIÁ", header_style))
            
            scores_data = [["Thang đo", "Điểm số", "Mức độ"]]
            scores = assessment_data['scores']
            
            for key, value in scores.items():
                if isinstance(value, (int, float)):
                    # Determine severity based on score
                    if value >= 20:
                        severity = "Rất cao"
                    elif value >= 15:
                        severity = "Cao" 
                    elif value >= 10:
                        severity = "Trung bình"
                    else:
                        severity = "Thấp"
                    
                    scores_data.append([key.replace('_', ' ').title(), str(value), severity])
            
            scores_table = Table(scores_data, colWidths=[2*inch, 1.5*inch, 2*inch])
            scores_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]))
            content.append(scores_table)
            content.append(Spacer(1, 20))
        
        # Risk assessment
        if 'risk_assessment' in assessment_data:
            content.append(Paragraph("🎯 ĐÁNH GIÁ RỦI RO", header_style))
            content.append(Paragraph(assessment_data['risk_assessment'], styles['Normal']))
            content.append(Spacer(1, 20))
        
        # Recommendations
        if 'recommendations' in assessment_data:
            content.append(Paragraph("💡 KHUYẾN NGHỊ", header_style))
            
            for i, rec in enumerate(assessment_data['recommendations'], 1):
                content.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            
            content.append(Spacer(1, 20))
        
        # Emergency contacts
        content.append(Paragraph("🚨 LIÊN HỆ KHẨN CẤP", header_style))
        emergency_info = """
        <b>Đường dây nóng hỗ trợ tâm lý 24/7:</b><br/>
        📞 <b>1800-1612</b> - Tư vấn miễn phí<br/>
        🏥 <b>115</b> - Cấp cứu y tế<br/>
        💬 <b>0912-345-678</b> - Tin nhắn hỗ trợ<br/><br/>
        
        <b>Khi nào cần tìm kiếm hỗ trợ ngay lập tức:</b><br/>
        • Có ý định tự làm hại bản thân<br/>
        • Cảm thấy tuyệt vọng hoàn toàn<br/>
        • Không thể kiểm soát hành vi<br/>
        • Có ảo giác hoặc ảo tưởng<br/>
        """
        content.append(Paragraph(emergency_info, styles['Normal']))
        
        # Footer disclaimer
        content.append(Spacer(1, 30))
        disclaimer = """
        <b>Lưu ý quan trọng:</b><br/>
        Báo cáo này được tạo tự động dựa trên kết quả đánh giá và chỉ mang tính chất tham khảo. 
        Không thay thế cho chẩn đoán và điều trị y khoa chuyên nghiệp. 
        Nếu bạn có lo ngại về sức khỏe tâm thần, hãy tham khảo ý kiến của các chuyên gia y tế.
        """
        content.append(Paragraph(disclaimer, styles['Normal']))
        
        # Build PDF
        doc.build(content, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
        
    except Exception as e:
        # Handle errors without Streamlit dependency
        print(f"Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
