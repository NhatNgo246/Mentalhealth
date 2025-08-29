"""
SOULFRIEND Advanced Reports
Comprehensive reporting and insights interface
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os
from io import BytesIO
import base64

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header
from components.pdf_export import generate_assessment_report

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Reports",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    load_css()
except:
    pass

# Header
app_header()

# Generate comprehensive sample data
@st.cache_data
def generate_comprehensive_data():
    """Generate comprehensive sample data for reporting"""
    np.random.seed(42)
    
    # Extended date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 year data
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # User profiles
    user_profiles = []
    for i in range(500):  # 500 unique users
        profile = {
            'user_id': f'user_{i+1:03d}',
            'age': np.random.randint(18, 70),
            'gender': np.random.choice(['Nam', 'Nữ', 'Khác'], p=[0.4, 0.55, 0.05]),
            'location': np.random.choice(['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Cần Thơ', 'Khác'], 
                                       p=[0.25, 0.3, 0.15, 0.1, 0.2]),
            'education': np.random.choice(['Trung học', 'Cao đẳng', 'Đại học', 'Sau đại học'], 
                                        p=[0.2, 0.25, 0.45, 0.1]),
            'occupation': np.random.choice(['Học sinh/SV', 'Văn phòng', 'Y tế', 'Giáo dục', 'Khác'], 
                                         p=[0.3, 0.35, 0.1, 0.15, 0.1])
        }
        user_profiles.append(profile)
    
    # Assessment sessions
    sessions = []
    for date in date_range:
        daily_count = max(1, np.random.poisson(12))  # Average 12 sessions per day
        for _ in range(daily_count):
            user = np.random.choice(user_profiles)
            
            # Generate realistic scores based on demographics
            age_factor = (user['age'] - 35) / 35  # Normalize around 35
            stress_factor = np.random.normal(0, 1)
            
            session = {
                'session_id': f"session_{len(sessions)+1}",
                'user_id': user['user_id'],
                'date': date,
                'time': date + timedelta(
                    hours=np.random.randint(8, 22),
                    minutes=np.random.randint(0, 60)
                ),
                'assessment_type': np.random.choice(['DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10'], 
                                                  p=[0.3, 0.25, 0.2, 0.15, 0.1]),
                
                # Demographic info
                'age': user['age'],
                'gender': user['gender'],
                'location': user['location'],
                'education': user['education'],
                'occupation': user['occupation'],
                
                # Scores with realistic correlations
                'dass_depression': max(0, np.random.normal(7 + age_factor + stress_factor, 4)),
                'dass_anxiety': max(0, np.random.normal(6 + stress_factor, 3)),
                'dass_stress': max(0, np.random.normal(9 + stress_factor, 4)),
                'phq9_score': max(0, np.random.normal(7 + age_factor + stress_factor, 3)),
                'gad7_score': max(0, np.random.normal(6 + stress_factor, 3)),
                'epds_score': max(0, np.random.normal(5 + stress_factor, 3)) if user['gender'] == 'Nữ' else 0,
                'pss_score': max(0, np.random.normal(15 + stress_factor * 2, 5)),
                
                # Session metadata
                'completion_time': np.random.normal(8, 2),  # minutes
                'completed': np.random.choice([True, False], p=[0.92, 0.08]),
                'platform': np.random.choice(['Desktop', 'Mobile', 'Tablet'], p=[0.6, 0.35, 0.05]),
                'referral_source': np.random.choice(['Direct', 'Search', 'Social', 'Healthcare'], p=[0.4, 0.3, 0.2, 0.1])
            }
            
            # Calculate risk levels
            if session['assessment_type'] == 'PHQ-9':
                if session['phq9_score'] >= 20:
                    session['risk_level'] = 'Rất cao'
                elif session['phq9_score'] >= 15:
                    session['risk_level'] = 'Cao'
                elif session['phq9_score'] >= 10:
                    session['risk_level'] = 'Trung bình'
                else:
                    session['risk_level'] = 'Thấp'
            else:
                # General risk assessment
                total_score = (session['dass_depression'] + session['dass_anxiety'] + session['dass_stress']) / 3
                if total_score >= 15:
                    session['risk_level'] = 'Rất cao'
                elif total_score >= 10:
                    session['risk_level'] = 'Cao'
                elif total_score >= 5:
                    session['risk_level'] = 'Trung bình'
                else:
                    session['risk_level'] = 'Thấp'
            
            sessions.append(session)
    
    return pd.DataFrame(sessions)

# Advanced Reports Interface
def advanced_reports():
    st.title("📋 Báo cáo chuyên sâu")
    
    # Load comprehensive data
    df = generate_comprehensive_data()
    
    # Report type selector
    report_type = st.selectbox(
        "🎯 Chọn loại báo cáo:",
        [
            "📊 Báo cáo tổng quan",
            "📈 Phân tích xu hướng",
            "👥 Báo cáo nhân khẩu học",
            "🎯 Phân tích rủi ro",
            "🏥 Báo cáo lâm sàng",
            "💻 Báo cáo kỹ thuật",
            "📋 Báo cáo tùy chỉnh"
        ]
    )
    
    # Date range filter
    st.sidebar.header("🎛️ Bộ lọc")
    
    date_range = st.sidebar.date_input(
        "Khoảng thời gian:",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
    
    # Filter data
    if len(date_range) == 2:
        mask = (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))
        df_filtered = df[mask]
    else:
        df_filtered = df
    
    # Generate reports based on selection
    if report_type == "📊 Báo cáo tổng quan":
        generate_overview_report(df_filtered)
    elif report_type == "📈 Phân tích xu hướng":
        generate_trend_analysis(df_filtered)
    elif report_type == "👥 Báo cáo nhân khẩu học":
        generate_demographic_report(df_filtered)
    elif report_type == "🎯 Phân tích rủi ro":
        generate_risk_analysis(df_filtered)
    elif report_type == "🏥 Báo cáo lâm sàng":
        generate_clinical_report(df_filtered)
    elif report_type == "💻 Báo cáo kỹ thuật":
        generate_technical_report(df_filtered)
    elif report_type == "📋 Báo cáo tùy chỉnh":
        generate_custom_report(df_filtered)

def generate_overview_report(df):
    """Generate comprehensive overview report"""
    st.header("📊 Báo cáo tổng quan")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sessions = len(df)
        st.metric("Tổng số phiên", f"{total_sessions:,}")
    
    with col2:
        unique_users = df['user_id'].nunique()
        st.metric("Người dùng duy nhất", f"{unique_users:,}")
    
    with col3:
        completion_rate = df['completed'].mean() * 100
        st.metric("Tỷ lệ hoàn thành", f"{completion_rate:.1f}%")
    
    with col4:
        avg_time = df['completion_time'].mean()
        st.metric("Thời gian TB", f"{avg_time:.1f} phút")
    
    # Assessment distribution
    st.subheader("Phân bố loại đánh giá")
    
    col1, col2 = st.columns(2)
    
    with col1:
        assessment_dist = df['assessment_type'].value_counts()
        fig_pie = px.pie(
            values=assessment_dist.values,
            names=assessment_dist.index,
            title="Tỷ lệ sử dụng các thang đo"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        risk_dist = df['risk_level'].value_counts()
        colors = ['green', 'yellow', 'orange', 'red']
        fig_risk = px.pie(
            values=risk_dist.values,
            names=risk_dist.index,
            title="Phân bố mức độ rủi ro",
            color_discrete_sequence=colors
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Score distributions
    st.subheader("Phân bố điểm số")
    
    fig_scores = make_subplots(
        rows=2, cols=3,
        subplot_titles=['PHQ-9', 'GAD-7', 'DASS Trầm cảm', 'DASS Lo âu', 'DASS Stress', 'PSS-10']
    )
    
    scores_data = [
        (df['phq9_score'], 1, 1),
        (df['gad7_score'], 1, 2),
        (df['dass_depression'], 1, 3),
        (df['dass_anxiety'], 2, 1),
        (df['dass_stress'], 2, 2),
        (df['pss_score'], 2, 3)
    ]
    
    for score_data, row, col in scores_data:
        fig_scores.add_trace(
            go.Histogram(x=score_data, nbinsx=20, name=f"Row{row}Col{col}"),
            row=row, col=col
        )
    
    fig_scores.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_scores, use_container_width=True)
    
    # Export options
    st.subheader("📥 Xuất báo cáo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Xuất PDF"):
            # Generate PDF report
            pdf_buffer = generate_overview_pdf_report(df)
            st.download_button(
                "⬇️ Tải báo cáo PDF",
                data=pdf_buffer,
                file_name=f"soulfriend_overview_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
    
    with col2:
        csv_data = df.to_csv(index=False)
        st.download_button(
            "📊 Xuất dữ liệu CSV",
            data=csv_data,
            file_name=f"soulfriend_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col3:
        summary_stats = {
            "period": f"{df['date'].min()} to {df['date'].max()}",
            "total_sessions": len(df),
            "unique_users": df['user_id'].nunique(),
            "completion_rate": df['completed'].mean(),
            "avg_completion_time": df['completion_time'].mean(),
            "high_risk_percentage": (df['risk_level'].isin(['Cao', 'Rất cao']).sum() / len(df)) * 100
        }
        
        st.download_button(
            "📈 Xuất thống kê JSON",
            data=pd.DataFrame([summary_stats]).to_json(orient='records', indent=2),
            file_name=f"soulfriend_stats_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

def generate_trend_analysis(df):
    """Generate trend analysis report"""
    st.header("📈 Phân tích xu hướng")
    
    # Daily trends
    daily_stats = df.groupby('date').agg({
        'session_id': 'count',
        'phq9_score': 'mean',
        'dass_depression': 'mean',
        'dass_anxiety': 'mean',
        'dass_stress': 'mean',
        'completion_time': 'mean'
    }).reset_index()
    
    # Usage trend
    fig_usage = px.line(
        daily_stats,
        x='date',
        y='session_id',
        title="Xu hướng sử dụng hàng ngày",
        labels={'date': 'Ngày', 'session_id': 'Số phiên'}
    )
    st.plotly_chart(fig_usage, use_container_width=True)
    
    # Score trends
    st.subheader("Xu hướng điểm số")
    
    fig_scores = go.Figure()
    
    fig_scores.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['phq9_score'],
        mode='lines',
        name='PHQ-9',
        line=dict(color='red')
    ))
    
    fig_scores.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['dass_depression'],
        mode='lines',
        name='DASS Trầm cảm',
        line=dict(color='blue')
    ))
    
    fig_scores.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['dass_anxiety'],
        mode='lines',
        name='DASS Lo âu',
        line=dict(color='orange')
    ))
    
    fig_scores.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['dass_stress'],
        mode='lines',
        name='DASS Stress',
        line=dict(color='green')
    ))
    
    fig_scores.update_layout(
        title="Xu hướng điểm số trung bình",
        xaxis_title="Ngày",
        yaxis_title="Điểm số",
        height=500
    )
    
    st.plotly_chart(fig_scores, use_container_width=True)

def generate_demographic_report(df):
    """Generate demographic analysis report"""
    st.header("👥 Báo cáo nhân khẩu học")
    
    # Age distribution
    col1, col2 = st.columns(2)
    
    with col1:
        age_bins = [18, 25, 35, 45, 55, 70]
        df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=['18-24', '25-34', '35-44', '45-54', '55+'])
        age_dist = df['age_group'].value_counts()
        
        fig_age = px.bar(
            x=age_dist.index,
            y=age_dist.values,
            title="Phân bố theo nhóm tuổi",
            labels={'x': 'Nhóm tuổi', 'y': 'Số lượng'}
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        gender_dist = df['gender'].value_counts()
        fig_gender = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title="Phân bố theo giới tính"
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    # Geographic distribution
    location_dist = df['location'].value_counts()
    fig_location = px.bar(
        x=location_dist.values,
        y=location_dist.index,
        orientation='h',
        title="Phân bố theo khu vực",
        labels={'x': 'Số lượng', 'y': 'Khu vực'}
    )
    st.plotly_chart(fig_location, use_container_width=True)
    
    # Education and occupation
    col1, col2 = st.columns(2)
    
    with col1:
        edu_dist = df['education'].value_counts()
        fig_edu = px.pie(
            values=edu_dist.values,
            names=edu_dist.index,
            title="Phân bố theo trình độ học vấn"
        )
        st.plotly_chart(fig_edu, use_container_width=True)
    
    with col2:
        occ_dist = df['occupation'].value_counts()
        fig_occ = px.pie(
            values=occ_dist.values,
            names=occ_dist.index,
            title="Phân bố theo nghề nghiệp"
        )
        st.plotly_chart(fig_occ, use_container_width=True)

def generate_risk_analysis(df):
    """Generate risk analysis report"""
    st.header("🎯 Phân tích rủi ro")
    
    # Risk distribution over time
    risk_over_time = df.groupby(['date', 'risk_level']).size().reset_index(name='count')
    
    fig_risk_trend = px.area(
        risk_over_time,
        x='date',
        y='count',
        color='risk_level',
        title="Xu hướng mức độ rủi ro theo thời gian",
        color_discrete_sequence=['green', 'yellow', 'orange', 'red']
    )
    st.plotly_chart(fig_risk_trend, use_container_width=True)
    
    # Risk by demographics
    st.subheader("Rủi ro theo nhân khẩu học")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_by_age = pd.crosstab(df['age_group'], df['risk_level'])
        fig_risk_age = px.imshow(
            risk_by_age.values,
            x=risk_by_age.columns,
            y=risk_by_age.index,
            color_continuous_scale='Reds',
            title="Rủi ro theo nhóm tuổi"
        )
        st.plotly_chart(fig_risk_age, use_container_width=True)
    
    with col2:
        risk_by_gender = pd.crosstab(df['gender'], df['risk_level'])
        fig_risk_gender = px.imshow(
            risk_by_gender.values,
            x=risk_by_gender.columns,
            y=risk_by_gender.index,
            color_continuous_scale='Reds',
            title="Rủi ro theo giới tính"
        )
        st.plotly_chart(fig_risk_gender, use_container_width=True)

def generate_clinical_report(df):
    """Generate clinical insights report"""
    st.header("🏥 Báo cáo lâm sàng")
    
    # Clinical score analysis
    st.subheader("Phân tích điểm số lâm sàng")
    
    # PHQ-9 severity categories
    phq9_severity = []
    for score in df['phq9_score']:
        if score < 5:
            phq9_severity.append('Không có/Tối thiểu')
        elif score < 10:
            phq9_severity.append('Nhẹ')
        elif score < 15:
            phq9_severity.append('Trung bình')
        elif score < 20:
            phq9_severity.append('Nặng')
        else:
            phq9_severity.append('Rất nặng')
    
    df['phq9_severity'] = phq9_severity
    
    severity_dist = df['phq9_severity'].value_counts()
    fig_severity = px.bar(
        x=severity_dist.index,
        y=severity_dist.values,
        title="Phân bố mức độ nghiêm trọng PHQ-9",
        labels={'x': 'Mức độ', 'y': 'Số lượng'}
    )
    st.plotly_chart(fig_severity, use_container_width=True)
    
    # Correlation analysis
    st.subheader("Phân tích tương quan")
    
    correlation_data = df[['phq9_score', 'gad7_score', 'dass_depression', 'dass_anxiety', 'dass_stress', 'pss_score']].corr()
    
    fig_corr = px.imshow(
        correlation_data.values,
        x=correlation_data.columns,
        y=correlation_data.index,
        color_continuous_scale='RdBu',
        title="Ma trận tương quan giữa các thang đo",
        aspect="auto"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Statistical summary
    st.subheader("Tóm tắt thống kê")
    
    stats_summary = df[['phq9_score', 'gad7_score', 'dass_depression', 'dass_anxiety', 'dass_stress', 'pss_score']].describe()
    st.dataframe(stats_summary)

def generate_technical_report(df):
    """Generate technical performance report"""
    st.header("💻 Báo cáo kỹ thuật")
    
    # Platform usage
    col1, col2 = st.columns(2)
    
    with col1:
        platform_dist = df['platform'].value_counts()
        fig_platform = px.pie(
            values=platform_dist.values,
            names=platform_dist.index,
            title="Sử dụng theo nền tảng"
        )
        st.plotly_chart(fig_platform, use_container_width=True)
    
    with col2:
        referral_dist = df['referral_source'].value_counts()
        fig_referral = px.pie(
            values=referral_dist.values,
            names=referral_dist.index,
            title="Nguồn giới thiệu"
        )
        st.plotly_chart(fig_referral, use_container_width=True)
    
    # Performance metrics
    st.subheader("Hiệu suất hệ thống")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_completion_time = df['completion_time'].mean()
        st.metric("Thời gian hoàn thành TB", f"{avg_completion_time:.1f} phút")
    
    with col2:
        completion_rate = df['completed'].mean() * 100
        st.metric("Tỷ lệ hoàn thành", f"{completion_rate:.1f}%")
    
    with col3:
        bounce_rate = (1 - df['completed'].mean()) * 100
        st.metric("Tỷ lệ thoát", f"{bounce_rate:.1f}%")
    
    # Time analysis
    completion_by_platform = df.groupby('platform')['completion_time'].mean()
    
    fig_time = px.bar(
        x=completion_by_platform.index,
        y=completion_by_platform.values,
        title="Thời gian hoàn thành theo nền tảng",
        labels={'x': 'Nền tảng', 'y': 'Thời gian (phút)'}
    )
    st.plotly_chart(fig_time, use_container_width=True)

def generate_custom_report(df):
    """Generate customizable report"""
    st.header("📋 Báo cáo tùy chỉnh")
    
    # Custom filters
    st.subheader("🎛️ Bộ lọc tùy chỉnh")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_assessments = st.multiselect(
            "Chọn loại đánh giá:",
            options=df['assessment_type'].unique(),
            default=df['assessment_type'].unique()
        )
    
    with col2:
        selected_risk_levels = st.multiselect(
            "Chọn mức độ rủi ro:",
            options=df['risk_level'].unique(),
            default=df['risk_level'].unique()
        )
    
    with col3:
        selected_platforms = st.multiselect(
            "Chọn nền tảng:",
            options=df['platform'].unique(),
            default=df['platform'].unique()
        )
    
    # Apply filters
    df_custom = df[
        (df['assessment_type'].isin(selected_assessments)) &
        (df['risk_level'].isin(selected_risk_levels)) &
        (df['platform'].isin(selected_platforms))
    ]
    
    # Custom metrics
    st.subheader("📊 Thống kê tùy chỉnh")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng số phiên", f"{len(df_custom):,}")
    
    with col2:
        if len(df_custom) > 0:
            avg_phq = df_custom['phq9_score'].mean()
            st.metric("PHQ-9 TB", f"{avg_phq:.1f}")
        else:
            st.metric("PHQ-9 TB", "N/A")
    
    with col3:
        if len(df_custom) > 0:
            high_risk_pct = (df_custom['risk_level'].isin(['Cao', 'Rất cao']).sum() / len(df_custom)) * 100
            st.metric("Rủi ro cao (%)", f"{high_risk_pct:.1f}%")
        else:
            st.metric("Rủi ro cao (%)", "N/A")
    
    with col4:
        if len(df_custom) > 0:
            completion_rate = df_custom['completed'].mean() * 100
            st.metric("Tỷ lệ hoàn thành", f"{completion_rate:.1f}%")
        else:
            st.metric("Tỷ lệ hoàn thành", "N/A")
    
    # Custom visualization
    if len(df_custom) > 0:
        st.subheader("📈 Biểu đồ tùy chỉnh")
        
        chart_type = st.selectbox(
            "Chọn loại biểu đồ:",
            ["Biểu đồ đường", "Biểu đồ cột", "Biểu đồ tròn", "Histogram", "Scatter plot"]
        )
        
        if chart_type == "Biểu đồ đường":
            daily_trend = df_custom.groupby('date').size()
            fig = px.line(x=daily_trend.index, y=daily_trend.values, title="Xu hướng theo ngày")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Biểu đồ cột":
            category_dist = df_custom['assessment_type'].value_counts()
            fig = px.bar(x=category_dist.index, y=category_dist.values, title="Phân bố loại đánh giá")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Biểu đồ tròn":
            risk_dist = df_custom['risk_level'].value_counts()
            fig = px.pie(values=risk_dist.values, names=risk_dist.index, title="Phân bố mức độ rủi ro")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Histogram":
            fig = px.histogram(df_custom, x='phq9_score', title="Phân bố điểm PHQ-9")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Scatter plot":
            fig = px.scatter(df_custom, x='phq9_score', y='gad7_score', title="Tương quan PHQ-9 vs GAD-7")
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn.")

def generate_overview_pdf_report(df):
    """Generate PDF overview report"""
    try:
        # Sample assessment data for PDF
        sample_data = {
            'assessment_date': datetime.now().strftime("%d/%m/%Y"),
            'assessment_type': 'Báo cáo tổng quan',
            'scores': {
                'total_sessions': len(df),
                'unique_users': df['user_id'].nunique(),
                'completion_rate': df['completed'].mean() * 100,
                'avg_completion_time': df['completion_time'].mean()
            },
            'risk_assessment': f"Tỷ lệ rủi ro cao: {(df['risk_level'].isin(['Cao', 'Rất cao']).sum() / len(df)) * 100:.1f}%",
            'recommendations': [
                f"Tổng số {len(df):,} phiên đánh giá trong kỳ báo cáo",
                f"Có {df['user_id'].nunique():,} người dùng duy nhất",
                f"Tỷ lệ hoàn thành đạt {df['completed'].mean() * 100:.1f}%",
                "Cần tăng cường hỗ trợ cho nhóm rủi ro cao"
            ]
        }
        
        pdf_buffer = generate_assessment_report(sample_data)
        return pdf_buffer
    except Exception as e:
        st.error(f"Lỗi tạo báo cáo PDF: {str(e)}")
        return None

# Main function
def main():
    advanced_reports()

if __name__ == "__main__":
    main()
