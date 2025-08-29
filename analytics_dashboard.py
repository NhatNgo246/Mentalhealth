"""
SOULFRIEND Analytics Dashboard
Advanced analytics and reporting interface
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

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Analytics",
    page_icon="📊",
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

# Generate sample data for demonstration
@st.cache_data
def generate_sample_data():
    """Generate sample analytics data"""
    np.random.seed(42)
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Assessment data
    assessments = []
    for date in date_range:
        daily_count = np.random.poisson(15)  # Average 15 assessments per day
        for _ in range(daily_count):
            assessment = {
                'date': date,
                'time': date + timedelta(
                    hours=np.random.randint(8, 22),
                    minutes=np.random.randint(0, 60)
                ),
                'type': np.random.choice(['DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10'], 
                                       p=[0.3, 0.25, 0.2, 0.15, 0.1]),
                'dass_depression': np.random.normal(8, 4),
                'dass_anxiety': np.random.normal(6, 3),
                'dass_stress': np.random.normal(10, 5),
                'phq9_score': np.random.normal(8, 4),
                'gad7_score': np.random.normal(7, 3),
                'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+'], 
                                            p=[0.3, 0.35, 0.2, 0.1, 0.05]),
                'gender': np.random.choice(['Nam', 'Nữ', 'Khác'], p=[0.4, 0.55, 0.05]),
                'risk_level': np.random.choice(['Thấp', 'Trung bình', 'Cao', 'Rất cao'], 
                                             p=[0.4, 0.35, 0.2, 0.05])
            }
            assessments.append(assessment)
    
    return pd.DataFrame(assessments)

# Analytics Dashboard
def analytics_dashboard():
    st.title("📊 Bảng điều khiển phân tích")
    
    # Load data
    df = generate_sample_data()
    
    # Sidebar filters
    st.sidebar.header("🎯 Bộ lọc")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Khoảng thời gian:",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
    
    # Assessment type filter
    assessment_types = st.sidebar.multiselect(
        "Loại đánh giá:",
        options=df['type'].unique(),
        default=df['type'].unique()
    )
    
    # Risk level filter
    risk_levels = st.sidebar.multiselect(
        "Mức độ rủi ro:",
        options=df['risk_level'].unique(),
        default=df['risk_level'].unique()
    )
    
    # Filter data
    if len(date_range) == 2:
        mask = (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))
        df_filtered = df[mask]
    else:
        df_filtered = df
    
    df_filtered = df_filtered[df_filtered['type'].isin(assessment_types)]
    df_filtered = df_filtered[df_filtered['risk_level'].isin(risk_levels)]
    
    # Overview metrics
    st.header("📈 Tổng quan")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_assessments = len(df_filtered)
        st.metric(
            "Tổng số đánh giá",
            f"{total_assessments:,}",
            delta=f"+{np.random.randint(50, 200)}"
        )
    
    with col2:
        unique_users = np.random.randint(int(total_assessments * 0.6), int(total_assessments * 0.8))
        st.metric(
            "Người dùng duy nhất",
            f"{unique_users:,}",
            delta=f"+{np.random.randint(20, 80)}"
        )
    
    with col3:
        avg_score = df_filtered['phq9_score'].mean()
        st.metric(
            "Điểm PHQ-9 TB",
            f"{avg_score:.1f}",
            delta=f"{np.random.uniform(-0.5, 0.5):.1f}"
        )
    
    with col4:
        high_risk_pct = (df_filtered['risk_level'].isin(['Cao', 'Rất cao']).sum() / len(df_filtered) * 100)
        st.metric(
            "Rủi ro cao (%)",
            f"{high_risk_pct:.1f}%",
            delta=f"{np.random.uniform(-2, 2):.1f}%"
        )
    
    with col5:
        completion_rate = np.random.uniform(85, 95)
        st.metric(
            "Tỷ lệ hoàn thành",
            f"{completion_rate:.1f}%",
            delta=f"+{np.random.uniform(0.5, 2):.1f}%"
        )
    
    # Charts section
    st.header("📊 Biểu đồ phân tích")
    
    # Time series analysis
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Xu hướng thời gian",
        "👥 Nhân khẩu học",
        "🎯 Phân tích rủi ro",
        "📋 Chi tiết đánh giá"
    ])
    
    with tab1:
        st.subheader("Xu hướng đánh giá theo thời gian")
        
        # Daily assessment trend
        daily_counts = df_filtered.groupby('date').size().reset_index(name='count')
        
        fig_trend = px.line(
            daily_counts,
            x='date',
            y='count',
            title="Số lượng đánh giá hàng ngày",
            labels={'date': 'Ngày', 'count': 'Số lượng đánh giá'}
        )
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Assessment type over time
        col1, col2 = st.columns(2)
        
        with col1:
            type_trend = df_filtered.groupby(['date', 'type']).size().reset_index(name='count')
            fig_type = px.area(
                type_trend,
                x='date',
                y='count',
                color='type',
                title="Xu hướng theo loại đánh giá",
                labels={'date': 'Ngày', 'count': 'Số lượng', 'type': 'Loại đánh giá'}
            )
            fig_type.update_layout(height=400)
            st.plotly_chart(fig_type, use_container_width=True)
        
        with col2:
            # Hourly distribution
            df_filtered['hour'] = pd.to_datetime(df_filtered['time']).dt.hour
            hourly_dist = df_filtered.groupby('hour').size().reset_index(name='count')
            
            fig_hourly = px.bar(
                hourly_dist,
                x='hour',
                y='count',
                title="Phân bố theo giờ trong ngày",
                labels={'hour': 'Giờ', 'count': 'Số lượng đánh giá'}
            )
            fig_hourly.update_layout(height=400)
            st.plotly_chart(fig_hourly, use_container_width=True)
    
    with tab2:
        st.subheader("Phân tích nhân khẩu học")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution
            gender_dist = df_filtered['gender'].value_counts()
            fig_gender = px.pie(
                values=gender_dist.values,
                names=gender_dist.index,
                title="Phân bố theo giới tính"
            )
            fig_gender.update_layout(height=400)
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            # Age group distribution
            age_dist = df_filtered['age_group'].value_counts()
            fig_age = px.bar(
                x=age_dist.index,
                y=age_dist.values,
                title="Phân bố theo nhóm tuổi",
                labels={'x': 'Nhóm tuổi', 'y': 'Số lượng'}
            )
            fig_age.update_layout(height=400)
            st.plotly_chart(fig_age, use_container_width=True)
        
        # Cross-analysis
        st.subheader("Phân tích chéo")
        
        # Risk by demographics
        risk_demo = pd.crosstab(df_filtered['age_group'], df_filtered['risk_level'])
        fig_risk_demo = px.imshow(
            risk_demo.values,
            x=risk_demo.columns,
            y=risk_demo.index,
            color_continuous_scale='Reds',
            title="Mức độ rủi ro theo nhóm tuổi",
            labels={'x': 'Mức độ rủi ro', 'y': 'Nhóm tuổi'}
        )
        st.plotly_chart(fig_risk_demo, use_container_width=True)
    
    with tab3:
        st.subheader("Phân tích mức độ rủi ro")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk level distribution
            risk_dist = df_filtered['risk_level'].value_counts()
            colors = ['green', 'yellow', 'orange', 'red']
            
            fig_risk = px.pie(
                values=risk_dist.values,
                names=risk_dist.index,
                title="Phân bố mức độ rủi ro",
                color_discrete_sequence=colors
            )
            fig_risk.update_layout(height=400)
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # Risk trend over time
            risk_trend = df_filtered.groupby(['date', 'risk_level']).size().reset_index(name='count')
            fig_risk_trend = px.area(
                risk_trend,
                x='date',
                y='count',
                color='risk_level',
                title="Xu hướng rủi ro theo thời gian",
                color_discrete_sequence=colors
            )
            fig_risk_trend.update_layout(height=400)
            st.plotly_chart(fig_risk_trend, use_container_width=True)
        
        # Score distributions
        st.subheader("Phân bố điểm số")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig_phq = px.histogram(
                df_filtered,
                x='phq9_score',
                nbins=20,
                title="Phân bố điểm PHQ-9",
                labels={'phq9_score': 'Điểm PHQ-9', 'count': 'Tần suất'}
            )
            st.plotly_chart(fig_phq, use_container_width=True)
        
        with col2:
            fig_gad = px.histogram(
                df_filtered,
                x='gad7_score',
                nbins=20,
                title="Phân bố điểm GAD-7",
                labels={'gad7_score': 'Điểm GAD-7', 'count': 'Tần suất'}
            )
            st.plotly_chart(fig_gad, use_container_width=True)
        
        with col3:
            fig_dass = px.histogram(
                df_filtered,
                x='dass_depression',
                nbins=20,
                title="Phân bố DASS Trầm cảm",
                labels={'dass_depression': 'Điểm DASS Trầm cảm', 'count': 'Tần suất'}
            )
            st.plotly_chart(fig_dass, use_container_width=True)
    
    with tab4:
        st.subheader("Dữ liệu chi tiết")
        
        # Data table with filters
        st.dataframe(
            df_filtered[['date', 'type', 'risk_level', 'age_group', 'gender', 'phq9_score', 'gad7_score']].round(1),
            use_container_width=True,
            height=400
        )
        
        # Export options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = df_filtered.to_csv(index=False)
            st.download_button(
                "📥 Tải CSV",
                data=csv_data,
                file_name=f"soulfriend_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Summary report
            summary = {
                "total_assessments": len(df_filtered),
                "date_range": f"{df_filtered['date'].min()} to {df_filtered['date'].max()}",
                "avg_phq9": df_filtered['phq9_score'].mean(),
                "avg_gad7": df_filtered['gad7_score'].mean(),
                "high_risk_count": df_filtered['risk_level'].isin(['Cao', 'Rất cao']).sum()
            }
            
            st.download_button(
                "📊 Tải báo cáo",
                data=pd.DataFrame([summary]).to_json(orient='records', indent=2),
                file_name=f"soulfriend_summary_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        with col3:
            if st.button("🔄 Làm mới dữ liệu"):
                st.cache_data.clear()
                st.rerun()

# Main function
def main():
    analytics_dashboard()

if __name__ == "__main__":
    main()
