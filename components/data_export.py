import io
import json
from datetime import datetime
from typing import Dict, Any
import streamlit as st

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class DataExportSystem:
    """Hệ thống xuất dữ liệu đánh giá"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None
    
    def create_assessment_pdf(self, assessment_data: Dict[str, Any]) -> bytes:
        """Tạo PDF báo cáo đánh giá"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab not available. Install with: pip install reportlab")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Prepare content
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center
            textColor=colors.darkblue
        )
        story.append(Paragraph("BÁO CÁO ĐÁNH GIÁ SỨC KHỎE TÂM THẦN", title_style))
        story.append(Spacer(1, 12))
        
        # Header info
        header_data = [
            ['Ngày đánh giá:', assessment_data.get('date', datetime.now().strftime('%d/%m/%Y'))],
            ['Thời gian:', assessment_data.get('time', datetime.now().strftime('%H:%M'))],
            ['Hệ thống:', 'SOULFRIEND V2.0'],
            ['Phiên bản:', '2.0.0']
        ]
        
        header_table = Table(header_data, colWidths=[2*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(header_table)
        story.append(Spacer(1, 20))
        
        # Assessment results
        if 'results' in assessment_data:
            story.append(Paragraph("KẾT QUẢ ĐÁNH GIÁ", self.styles['Heading2']))
            story.append(Spacer(1, 12))
            
            for assessment_name, result in assessment_data['results'].items():
                # Assessment title
                story.append(Paragraph(f"{assessment_name}", self.styles['Heading3']))
                
                # Score and severity
                result_data = [
                    ['Điểm số:', f"{result.get('score', 'N/A')}/{result.get('max_score', 'N/A')}"],
                    ['Mức độ:', result.get('severity', 'N/A')],
                    ['Đánh giá:', result.get('interpretation', 'N/A')]
                ]
                
                result_table = Table(result_data, colWidths=[1.5*inch, 4.5*inch])
                result_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(result_table)
                story.append(Spacer(1, 15))
        
        # Recommendations
        if 'recommendations' in assessment_data:
            story.append(Paragraph("KHUYẾN NGHỊ", self.styles['Heading2']))
            story.append(Spacer(1, 12))
            
            for rec in assessment_data['recommendations']:
                story.append(Paragraph(f"• {rec}", self.styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = """
        <para align="center">
        <b>Lưu ý quan trọng:</b><br/>
        Kết quả này chỉ mang tính chất tham khảo và không thay thế cho việc khám và tư vấn của chuyên gia y tế.
        Nếu bạn có các triệu chứng nghiêm trọng, hãy liên hệ với bác sĩ hoặc chuyên gia tâm lý.
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_json_export(self, assessment_data: Dict[str, Any]) -> str:
        """Tạo JSON export"""
        export_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "system": "SOULFRIEND V2.0",
                "version": "2.0.0"
            },
            "assessment_data": assessment_data
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def create_csv_export(self, assessment_data: Dict[str, Any]) -> str:
        """Tạo CSV export"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Assessment', 'Score', 'Max_Score', 'Severity', 'Date', 'Time'])
        
        # Data
        if 'results' in assessment_data:
            for assessment_name, result in assessment_data['results'].items():
                writer.writerow([
                    assessment_name,
                    result.get('score', ''),
                    result.get('max_score', ''),
                    result.get('severity', ''),
                    assessment_data.get('date', ''),
                    assessment_data.get('time', '')
                ])
        
        return output.getvalue()

# Streamlit interface functions
def display_export_options():
    """Hiển thị các tùy chọn xuất dữ liệu"""
    if 'enhanced_scores' not in st.session_state or not st.session_state.enhanced_scores:
        st.warning("Vui lòng hoàn thành đánh giá trước khi xuất kết quả.")
        return
    
    st.subheader("📥 Xuất kết quả đánh giá")
    
    export_system = DataExportSystem()
    
    # Prepare assessment data
    assessment_data = prepare_assessment_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Xuất PDF", use_container_width=True):
            try:
                if REPORTLAB_AVAILABLE:
                    pdf_data = export_system.create_assessment_pdf(assessment_data)
                    st.download_button(
                        label="💾 Tải PDF",
                        data=pdf_data,
                        file_name=f"assessment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("PDF export not available. Please install reportlab: pip install reportlab")
            except Exception as e:
                st.error(f"Error creating PDF: {e}")
    
    with col2:
        if st.button("📊 Xuất JSON", use_container_width=True):
            try:
                json_data = export_system.create_json_export(assessment_data)
                st.download_button(
                    label="💾 Tải JSON",
                    data=json_data,
                    file_name=f"assessment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Error creating JSON: {e}")
    
    with col3:
        if st.button("📈 Xuất CSV", use_container_width=True):
            try:
                csv_data = export_system.create_csv_export(assessment_data)
                st.download_button(
                    label="💾 Tải CSV",
                    data=csv_data,
                    file_name=f"assessment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error creating CSV: {e}")

def prepare_assessment_data() -> Dict[str, Any]:
    """Chuẩn bị dữ liệu đánh giá cho xuất"""
    data = {
        "date": datetime.now().strftime('%d/%m/%Y'),
        "time": datetime.now().strftime('%H:%M:%S'),
        "results": {},
        "recommendations": []
    }
    
    # Get assessment results from session state
    if 'assessment_results' in st.session_state:
        for assessment_type, result in st.session_state.assessment_results.items():
            if hasattr(result, '__dict__'):
                data["results"][assessment_type] = {
                    "score": getattr(result, 'total_score', 0),
                    "max_score": getattr(result, 'max_score', 0),
                    "severity": getattr(result, 'severity', 'Unknown'),
                    "interpretation": getattr(result, 'interpretation', ''),
                    "recommendations": getattr(result, 'recommendations', [])
                }
                # Add to global recommendations
                if hasattr(result, 'recommendations'):
                    data["recommendations"].extend(result.recommendations)
    
    return data
