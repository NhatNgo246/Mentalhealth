"""
Charts and Visualization Module for SOULFRIEND
Provides interactive charts for mental health assessment results
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def create_severity_gauge(score: int, max_score: int, title: str, severity_level: str) -> go.Figure:
    """Create a gauge chart showing severity level"""
    
    # Define severity colors
    severity_colors = {
        'normal': '#28a745',
        'mild': '#ffc107', 
        'moderate': '#fd7e14',
        'severe': '#dc3545',
        'extremely_severe': '#721c24',
        'excellent': '#20c997',
        'good': '#28a745',
        'fair': '#ffc107',
        'poor': '#fd7e14',
        'very_poor': '#dc3545'
    }
    
    color = severity_colors.get(severity_level.lower().replace(' ', '_'), '#6c757d')
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20}},
        delta = {'reference': max_score//2},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_score*0.2], 'color': '#d4edda'},
                {'range': [max_score*0.2, max_score*0.4], 'color': '#fff3cd'},
                {'range': [max_score*0.4, max_score*0.6], 'color': '#fde2e4'},
                {'range': [max_score*0.6, max_score*0.8], 'color': '#f8d7da'},
                {'range': [max_score*0.8, max_score], 'color': '#f5c6cb'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_score*0.8
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def create_radar_chart(subscales: Dict[str, Dict]) -> go.Figure:
    """Create radar chart for subscale scores"""
    
    categories = list(subscales.keys())
    scores = [subscales[cat].get('score', subscales[cat].get('adjusted', subscales[cat].get('raw', 0))) for cat in categories]
    
    # Normalize scores to 0-100 scale for better visualization
    max_scores = [subscales[cat].get('max_score', 21) for cat in categories]
    normalized_scores = [(score/max_score)*100 for score, max_score in zip(scores, max_scores)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_scores,
        theta=categories,
        fill='toself',
        name='Điểm hiện tại',
        line_color='rgba(102, 126, 234, 0.8)',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    # Add average line
    avg_score = sum(normalized_scores) / len(normalized_scores)
    fig.add_trace(go.Scatterpolar(
        r=[avg_score] * len(categories),
        theta=categories,
        mode='lines',
        name='Điểm trung bình',
        line=dict(color='red', dash='dash', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100],
                ticktext=['Rất thấp', 'Thấp', 'Trung bình', 'Cao', 'Rất cao']
            )
        ),
        showlegend=True,
        title="📊 Biểu đồ radar - Phân tích đa chiều",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_bar_chart(subscales: Dict[str, Dict]) -> go.Figure:
    """Create horizontal bar chart for subscale comparison"""
    
    categories = list(subscales.keys())
    scores = [subscales[cat].get('score', subscales[cat].get('adjusted', subscales[cat].get('raw', 0))) for cat in categories]
    levels = [subscales[cat].get('level', subscales[cat].get('severity', 'unknown')) for cat in categories]
    
    # Color mapping
    color_map = {
        'normal': '#28a745',
        'mild': '#ffc107',
        'moderate': '#fd7e14', 
        'severe': '#dc3545',
        'extremely_severe': '#721c24'
    }
    
    colors = [color_map.get(level, '#6c757d') for level in levels]
    
    fig = go.Figure(go.Bar(
        y=categories,
        x=scores,
        orientation='h',
        marker_color=colors,
        text=[f'{score} ({level})' for score, level in zip(scores, levels)],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Điểm: %{x}<br>Mức độ: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title="📊 So sánh điểm số theo lĩnh vực",
        xaxis_title="Điểm số",
        yaxis_title="Lĩnh vực đánh giá",
        height=300,
        margin=dict(l=100, r=50, t=60, b=40),
        showlegend=False
    )
    
    return fig

def create_donut_chart(total_score: int, max_score: int, severity_level: str) -> go.Figure:
    """Create donut chart showing overall completion percentage"""
    
    percentage = (total_score / max_score) * 100
    remaining = 100 - percentage
    
    # Severity color mapping
    severity_colors = {
        'normal': '#28a745',
        'mild': '#ffc107',
        'moderate': '#fd7e14',
        'severe': '#dc3545', 
        'extremely_severe': '#721c24'
    }
    
    color = severity_colors.get(severity_level, '#6c757d')
    
    fig = go.Figure(data=[go.Pie(
        labels=['Điểm đạt được', 'Còn lại'],
        values=[percentage, remaining],
        hole=.6,
        marker_colors=[color, '#e9ecef'],
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
    )])
    
    # Add center text
    fig.add_annotation(
        text=f"<b>{total_score}</b><br><span style='font-size:14px'>{severity_level}</span>",
        x=0.5, y=0.5,
        font_size=20,
        showarrow=False
    )
    
    fig.update_layout(
        title="🎯 Tổng quan kết quả",
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    return fig

def create_progress_timeline(assessment_history: List[Dict] = None) -> go.Figure:
    """Create timeline showing assessment progress over time"""
    
    if not assessment_history:
        # Sample data for demonstration
        assessment_history = [
            {'date': '2025-08-20', 'score': 25, 'type': 'DASS-21'},
            {'date': '2025-08-22', 'score': 20, 'type': 'DASS-21'},
            {'date': '2025-08-25', 'score': 18, 'type': 'DASS-21'},
            {'date': '2025-08-27', 'score': 14, 'type': 'GAD-7'}
        ]
    
    df = pd.DataFrame(assessment_history)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    # Group by assessment type
    for assessment_type in df['type'].unique():
        type_data = df[df['type'] == assessment_type]
        
        fig.add_trace(go.Scatter(
            x=type_data['date'],
            y=type_data['score'],
            mode='lines+markers',
            name=assessment_type,
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="📈 Tiến trình cải thiện theo thời gian",
        xaxis_title="Ngày đánh giá",
        yaxis_title="Điểm số",
        height=400,
        margin=dict(l=50, r=50, t=60, b=40),
        hovermode='x unified'
    )
    
    return fig

def create_comparison_chart(current_score: int, population_avg: float, questionnaire_type: str) -> go.Figure:
    """Create comparison with population average"""
    
    categories = ['Bạn', 'Trung bình dân số', 'Mức lý tưởng']
    
    # Estimated population averages (these would come from research data)
    pop_averages = {
        'DASS-21': {'population': 18, 'ideal': 7},
        'PHQ-9': {'population': 8, 'ideal': 2},
        'GAD-7': {'population': 6, 'ideal': 2},
        'EPDS': {'population': 9, 'ideal': 3},
        'PSS-10': {'population': 16, 'ideal': 8}
    }
    
    pop_data = pop_averages.get(questionnaire_type, {'population': 15, 'ideal': 5})
    values = [current_score, pop_data['population'], pop_data['ideal']]
    
    colors = ['#6366f1', '#94a3b8', '#10b981']
    
    fig = go.Figure(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f'{v:.0f}' for v in values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"📊 So sánh với dân số ({questionnaire_type})",
        yaxis_title="Điểm số",
        height=350,
        margin=dict(l=50, r=50, t=60, b=40),
        showlegend=False
    )
    
    return fig

def display_enhanced_charts(enhanced_result, questionnaire_type: str):
    """Main function to display all charts for enhanced results"""
    
    st.markdown("### 📊 Biểu đồ phân tích kết quả")
    
    # Create tabs for different chart types
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Tổng quan", "📊 Chi tiết", "📈 So sánh", "⏱️ Tiến trình"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gauge chart
            gauge_fig = create_severity_gauge(
                enhanced_result.get("total_score", 0),
                126 if questionnaire_type == "DASS-21" else 27,  # Max scores vary
                f"Điểm tổng {questionnaire_type}",
                enhanced_result.get("severity_level", "Không xác định")
            )
            st.plotly_chart(gauge_fig, width="stretch")
        
        with col2:
            # Donut chart
            donut_fig = create_donut_chart(
                enhanced_result.get("total_score", 0),
                126 if questionnaire_type == "DASS-21" else 27,
                enhanced_result.get("severity_level", "Không xác định")
            )
            st.plotly_chart(donut_fig, width="stretch")
    
    with tab2:
        if enhanced_result.get('subscales') and enhanced_result.get('subscales'):
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar chart
                bar_fig = create_bar_chart(enhanced_result.get('subscales', {}))
                st.plotly_chart(bar_fig, width="stretch")
            
            with col2:
                # Radar chart
                radar_fig = create_radar_chart(enhanced_result.get('subscales', {}))
                st.plotly_chart(radar_fig, width="stretch")
        else:
            st.info("📊 Biểu đồ chi tiết chỉ khả dụng cho các questionnaire có subscales")
    
    with tab3:
        # Comparison chart
        comparison_fig = create_comparison_chart(
            enhanced_result.get("total_score", 0),
            15.0,  # This would be real population data
            questionnaire_type
        )
        st.plotly_chart(comparison_fig, width="stretch")
        
        st.info("""
        💡 **Lưu ý**: Số liệu so sánh dựa trên nghiên cứu quốc tế. 
        Kết quả thấp hơn trung bình không có nghĩa là tốt hơn trong tất cả trường hợp.
        """)
    
    with tab4:
        # Timeline chart
        timeline_fig = create_progress_timeline()
        st.plotly_chart(timeline_fig, width="stretch")
        
        st.info("""
        📈 **Theo dõi tiến trình**: Tính năng này sẽ hiển thị kết quả thực tế 
        khi bạn thực hiện nhiều lần đánh giá qua thời gian.
        """)

def create_summary_statistics(enhanced_result, questionnaire_type: str):
    """Create summary statistics cards"""
    
    st.markdown("### 📈 Thống kê tóm tắt")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Safe access to total score from dict
        total_score = enhanced_result.get('total_score', enhanced_result.get('gad7_total', enhanced_result.get('phq9_total', enhanced_result.get('epds_total', enhanced_result.get('pss_total', 0)))))
        severity = enhanced_result.get('severity_level', enhanced_result.get('severity', enhanced_result.get('risk', enhanced_result.get('stress_level', 'Unknown'))))
        
        st.metric(
            label="Điểm tổng",
            value=total_score,
            delta=f"Mức: {severity}"
        )
    
    with col2:
        # Safe access to subscales
        subscales = enhanced_result.get('subscales', {})
        if subscales and isinstance(subscales, dict):
            scores = [sub.get('score', 0) for sub in subscales.values() if isinstance(sub, dict)]
            if scores:
                avg_score = sum(scores) / len(scores)
                st.metric(
                    label="Điểm TB subscales", 
                    value=f"{avg_score:.1f}",
                    delta="Trung bình các lĩnh vực"
                )
            else:
                st.metric(label="Loại đánh giá", value=questionnaire_type)
        else:
            st.metric(label="Loại đánh giá", value=questionnaire_type)
    
    with col3:
        # Calculate percentile (mock data) - safe access
        total_score = enhanced_result.get('total_score', enhanced_result.get('gad7_total', enhanced_result.get('phq9_total', enhanced_result.get('epds_total', enhanced_result.get('pss_total', 0)))))
        percentile = max(0, 100 - (total_score / 126 * 100))
        st.metric(
            label="Phần trăm tốt hơn",
            value=f"{percentile:.0f}%",
            delta="So với dân số"
        )
    
    with col4:
        # Risk level
        risk_levels = {
            'normal': 'Thấp',
            'mild': 'Nhẹ', 
            'moderate': 'Trung bình',
            'severe': 'Cao',
            'extremely_severe': 'Rất cao'
        }
        # Safe access to severity level
        severity = enhanced_result.get('severity_level', enhanced_result.get('severity', enhanced_result.get('risk', enhanced_result.get('stress_level', 'normal'))))
        risk = risk_levels.get(severity, 'Chưa xác định')
        st.metric(
            label="Mức độ quan tâm",
            value=risk,
            delta="Cần theo dõi" if risk in ['Cao', 'Rất cao'] else "Ổn định"
        )

def create_charts_interface(result_data, questionnaire_type):
    """
    Create comprehensive charts interface for assessment results
    
    Args:
        result_data: Assessment results data
        questionnaire_type: Type of questionnaire (PHQ-9, GAD-7, etc.)
    """
    
    if not result_data:
        st.warning("⚠️ Không có dữ liệu để hiển thị biểu đồ")
        return
    
    # Extract basic information
    total_score = result_data.get('total_score', 0)
    severity = result_data.get('severity', 'Unknown')
    
    # Define max scores for different questionnaires
    max_scores = {
        'PHQ-9': 27,
        'GAD-7': 21,
        'DASS-21': 42,  # Adjusted score
        'PSS-10': 40,
        'EPDS': 30
    }
    
    max_score = max_scores.get(questionnaire_type, 30)
    
    st.subheader("📊 Kết Quả Đánh Giá")
    
    # Create columns for different chart types
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge chart
        gauge_fig = create_severity_gauge(
            score=total_score,
            max_score=max_score,
            title=f"Điểm {questionnaire_type}",
            severity_level=severity
        )
        st.plotly_chart(gauge_fig, width="stretch")
        
    with col2:
        # Donut chart
        donut_fig = create_donut_chart(
            total_score=total_score,
            max_score=max_score,
            severity_level=severity
        )
        st.plotly_chart(donut_fig, width="stretch")
    
    # Comparison chart
    population_avgs = {
        'PHQ-9': 8.4,
        'GAD-7': 6.2,
        'DASS-21': 12.5,
        'PSS-10': 16.0,
        'EPDS': 7.8
    }
    
    population_avg = population_avgs.get(questionnaire_type, 10.0)
    
    comparison_fig = create_comparison_chart(
        current_score=total_score,
        population_avg=population_avg,
        questionnaire_type=questionnaire_type
    )
    st.plotly_chart(comparison_fig, width="stretch")
    
    # Summary statistics
    st.subheader("📈 Thống Kê Tóm Tắt")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Điểm Tổng",
            value=total_score,
            delta=f"{total_score - population_avg:.1f}" if total_score > population_avg else f"{total_score - population_avg:.1f}"
        )
    
    with col2:
        st.metric(
            label="Mức Độ",
            value=severity,
            delta="Cần chú ý" if severity in ['Severe', 'High', 'Moderately severe'] else "Ổn định"
        )
    
    with col3:
        percentile = min(95, max(5, (total_score / max_score) * 100))
        st.metric(
            label="Phần Trăm",
            value=f"{percentile:.0f}%",
            delta="Cao" if percentile > 70 else "Thấp"
        )
    
    with col4:
        interpretation = result_data.get('interpretation', 'Cần đánh giá thêm')
        risk_level = "Cao" if total_score > max_score * 0.7 else "Vừa" if total_score > max_score * 0.4 else "Thấp"
        st.metric(
            label="Mức Rủi Ro",
            value=risk_level,
            delta="Theo dõi" if risk_level == "Cao" else "Bình thường"
        )
    
    # Detailed interpretation
    st.subheader("📝 Giải Thích Chi Tiết")
    
    if 'interpretation' in result_data:
        st.write(f"**Kết quả:** {result_data['interpretation']}")
    
    if 'recommendations' in result_data:
        recommendations = result_data['recommendations']
        if isinstance(recommendations, dict):
            if 'immediate' in recommendations:
                st.write(f"**Khuyến nghị ngay:** {recommendations['immediate']}")
            if 'followup' in recommendations:
                st.write(f"**Theo dõi:** {recommendations['followup']}")
        else:
            st.write(f"**Khuyến nghị:** {recommendations}")
    
    # Progress timeline (placeholder)
    timeline_fig = create_progress_timeline()
    st.plotly_chart(timeline_fig, width="stretch")

class ChartManager:
    """Chart Manager for SOULFRIEND visualizations"""
    
    def __init__(self):
        self.chart_count = 0
    
    def create_score_chart(self, scores: Dict, chart_type="bar"):
        """Create score visualization chart"""
        self.chart_count += 1
        
        if chart_type == "bar":
            return create_comparison_chart(scores)
        elif chart_type == "gauge":
            # Return first score as gauge
            first_key = list(scores.keys())[0]
            return create_severity_gauge(
                score=scores[first_key].get('total_score', 0),
                max_score=100,
                title=first_key,
                severity_level=scores[first_key].get('severity', 'Unknown')
            )
        else:
            return create_comparison_chart(scores)
    
    def create_progress_chart(self, data: List):
        """Create progress over time chart"""
        return create_progress_timeline()
    
    def create_dashboard(self, assessment_results: Dict):
        """Create complete dashboard"""
        create_charts_interface(assessment_results)

# Global instance
chart_manager = ChartManager()
