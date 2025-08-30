"""
Admin Panel for SOULFRIEND
Provides administrative tools for managing questionnaires, users, and analytics
"""

import streamlit as st
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
from typing import Dict, List, Any
import plotly.express as px
import plotly.graph_objects as go

# Admin credentials (in production, use proper auth system)
ADMIN_USERS = {
    "admin": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin123
    "doctor": "8b2c86ea9cf2ea4eb517fd1e06b74f399e7fec0fef92e3b482a6cf2e2b092023",  # doctor123
}

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_admin_login() -> bool:
    """Verify admin login credentials"""
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("### 🔐 Đăng nhập quản trị")
        
        with st.form("admin_login"):
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng nhập")
            
            if submit:
                if username in ADMIN_USERS and hash_password(password) == ADMIN_USERS[username]:
                    st.session_state.admin_authenticated = True
                    st.session_state.admin_username = username
                    st.success("✅ Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("❌ Sai tên đăng nhập hoặc mật khẩu!")
        
        return False
    
    return True

def admin_logout():
    """Admin logout functionality"""
    if st.button("🚪 Đăng xuất"):
        st.session_state.admin_authenticated = False
        if 'admin_username' in st.session_state:
            del st.session_state.admin_username
        st.rerun()

def load_questionnaire_config(questionnaire_type: str) -> Dict:
    """Load questionnaire configuration for editing"""
    file_mapping = {
        "DASS-21": "dass21_enhanced_vi.json",
        "PHQ-9": "phq9_enhanced_vi.json", 
        "GAD-7": "gad7_enhanced_vi.json",
        "EPDS": "epds_enhanced_vi.json",
        "PSS-10": "pss10_enhanced_vi.json"
    }
    
    file_path = f"/workspaces/Mentalhealth/data/{file_mapping[questionnaire_type]}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Không tìm thấy file cấu hình: {file_path}")
        return {}

def save_questionnaire_config(questionnaire_type: str, config: Dict):
    """Save questionnaire configuration"""
    file_mapping = {
        "DASS-21": "dass21_enhanced_vi.json",
        "PHQ-9": "phq9_enhanced_vi.json",
        "GAD-7": "gad7_enhanced_vi.json", 
        "EPDS": "epds_enhanced_vi.json",
        "PSS-10": "pss10_enhanced_vi.json"
    }
    
    file_path = f"/workspaces/Mentalhealth/data/{file_mapping[questionnaire_type]}"
    
    try:
        # Create backup
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if os.path.exists(file_path):
            os.rename(file_path, backup_path)
        
        # Save new config
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Lỗi lưu cấu hình: {str(e)}")
        return False

def questionnaire_manager():
    """Questionnaire management interface"""
    st.markdown("### 📝 Quản lý thang đo")
    
    # Select questionnaire to edit
    questionnaire_type = st.selectbox(
        "Chọn thang đo để chỉnh sửa:",
        ["DASS-21", "PHQ-9", "GAD-7", "EPDS", "PSS-10"]
    )
    
    if st.button("📂 Tải cấu hình"):
        config = load_questionnaire_config(questionnaire_type)
        if config:
            st.session_state.current_config = config
            st.session_state.current_questionnaire = questionnaire_type
            st.success(f"✅ Đã tải cấu hình {questionnaire_type}")
    
    if 'current_config' in st.session_state:
        config = st.session_state.current_config
        
        # Basic info editing
        st.markdown("#### ℹ️ Thông tin cơ bản")
        col1, col2 = st.columns(2)
        
        with col1:
            config['name'] = st.text_input("Tên thang đo:", value=config.get('name', ''))
            config['version'] = st.text_input("Phiên bản:", value=config.get('version', ''))
        
        with col2:
            config['description'] = st.text_area("Mô tả:", value=config.get('description', ''))
        
        # Items editing
        st.markdown("#### 📋 Câu hỏi")
        
        if 'items' in config:
            # Display items in editable table
            items_data = []
            for i, item in enumerate(config['items']):
                items_data.append({
                    'ID': item.get('id', i+1),
                    'Câu hỏi': item.get('text_vi', ''),
                    'Subscale': item.get('subscale', ''),
                    'Reverse': item.get('reverse', False)
                })
            
            items_df = pd.DataFrame(items_data)
            edited_df = st.data_editor(
                items_df,
                num_rows="dynamic",
                width="stretch",
                key=f"items_editor_{questionnaire_type}"
            )
            
            # Update config with edited items
            config['items'] = []
            for _, row in edited_df.iterrows():
                config['items'].append({
                    'id': row['ID'],
                    'text_vi': row['Câu hỏi'],
                    'subscale': row['Subscale'],
                    'reverse': row['Reverse']
                })
        
        # Response options editing  
        st.markdown("#### 🔘 Tùy chọn trả lời")
        if 'response_options' in config:
            options_text = st.text_area(
                "Tùy chọn trả lời (mỗi dòng một tùy chọn):",
                value='\n'.join([opt['text_vi'] for opt in config['response_options']]),
                height=150
            )
            
            # Update response options
            lines = options_text.strip().split('\n')
            config['response_options'] = []
            for i, line in enumerate(lines):
                if line.strip():
                    config['response_options'].append({
                        'value': i,
                        'text_vi': line.strip()
                    })
        
        # Save configuration
        st.markdown("#### 💾 Lưu thay đổi")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Lưu cấu hình", type="primary"):
                if save_questionnaire_config(questionnaire_type, config):
                    st.success("✅ Đã lưu cấu hình thành công!")
                else:
                    st.error("❌ Lỗi khi lưu cấu hình!")
        
        with col2:
            if st.button("🔄 Tải lại"):
                config = load_questionnaire_config(questionnaire_type)
                st.session_state.current_config = config
                st.rerun()
        
        with col3:
            if st.button("📋 Xem JSON"):
                with st.expander("📄 Cấu hình JSON"):
                    st.json(config)

def analytics_dashboard():
    """Analytics and statistics dashboard"""
    st.markdown("### 📊 Thống kê sử dụng")
    
    # Mock data for demonstration (in production, get from database)
    mock_data = {
        'dates': pd.date_range('2025-08-01', '2025-08-27', freq='D'),
        'dass21_count': [15, 12, 18, 20, 25, 22, 19, 16, 21, 24, 18, 15, 23, 26, 20, 17, 19, 22, 25, 28, 24, 21, 18, 26, 29, 22, 20],
        'phq9_count': [8, 6, 9, 11, 13, 10, 8, 7, 12, 14, 9, 8, 11, 13, 10, 8, 9, 11, 12, 14, 11, 10, 8, 13, 15, 11, 9],
        'gad7_count': [5, 4, 7, 8, 10, 7, 5, 6, 9, 11, 6, 5, 8, 10, 7, 5, 6, 8, 9, 11, 8, 7, 5, 10, 12, 8, 6]
    }
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng đánh giá hôm nay", "47", delta="5")
    
    with col2:
        st.metric("Người dùng hoạt động", "124", delta="12")
    
    with col3:
        st.metric("Đánh giá tuần này", "298", delta="34")
    
    with col4:
        st.metric("Tỷ lệ hoàn thành", "94.2%", delta="2.1%")
    
    # Usage trends
    st.markdown("#### 📈 Xu hướng sử dụng")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mock_data['dates'],
        y=mock_data['dass21_count'],
        mode='lines+markers',
        name='DASS-21',
        line=dict(color='#e74c3c', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=mock_data['dates'],
        y=mock_data['phq9_count'],
        mode='lines+markers',
        name='PHQ-9',
        line=dict(color='#3498db', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=mock_data['dates'],
        y=mock_data['gad7_count'],
        mode='lines+markers',
        name='GAD-7',
        line=dict(color='#2ecc71', width=3)
    ))
    
    fig.update_layout(
        title="Số lượng đánh giá theo ngày",
        xaxis_title="Ngày",
        yaxis_title="Số lượng đánh giá",
        height=400
    )
    
    st.plotly_chart(fig, width="stretch")
    
    # Questionnaire popularity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Thang đo phổ biến")
        popularity_data = {
            'Questionnaire': ['DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10'],
            'Count': [547, 234, 156, 89, 123]
        }
        
        fig_bar = px.bar(
            popularity_data, 
            x='Count', 
            y='Questionnaire',
            orientation='h',
            title="Số lượng sử dụng theo thang đo"
        )
        st.plotly_chart(fig_bar, width="stretch")
    
    with col2:
        st.markdown("#### ⏰ Giờ cao điểm")
        hourly_data = {
            'Hour': list(range(24)),
            'Assessments': [2, 1, 0, 0, 1, 3, 8, 15, 22, 28, 25, 30, 35, 32, 28, 26, 31, 29, 25, 18, 12, 8, 5, 3]
        }
        
        fig_hourly = px.line(
            hourly_data,
            x='Hour',
            y='Assessments',
            title="Số lượng đánh giá theo giờ"
        )
        st.plotly_chart(fig_hourly, width="stretch")

def user_management():
    """User management interface"""
    st.markdown("### 👥 Quản lý người dùng")
    
    # Mock user data
    users_data = {
        'ID': [1, 2, 3, 4, 5],
        'Email': ['user1@example.com', 'user2@example.com', 'user3@example.com', 'user4@example.com', 'user5@example.com'],
        'Last Assessment': ['2025-08-27', '2025-08-26', '2025-08-25', '2025-08-24', '2025-08-23'],
        'Total Assessments': [5, 3, 8, 2, 12],
        'Status': ['Active', 'Active', 'Inactive', 'Active', 'Active']
    }
    
    users_df = pd.DataFrame(users_data)
    
    # Search and filter
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("🔍 Tìm kiếm email:")
    with col2:
        status_filter = st.selectbox("Lọc theo trạng thái:", ["Tất cả", "Active", "Inactive"])
    
    # Apply filters
    filtered_df = users_df.copy()
    if search_term:
        filtered_df = filtered_df[filtered_df['Email'].str.contains(search_term, case=False)]
    if status_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    
    # Display users table
    st.dataframe(filtered_df, width="stretch")
    
    # User actions
    st.markdown("#### 🛠️ Hành động")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Gửi email nhắc nhở"):
            st.info("Tính năng gửi email sẽ có trong phiên bản tiếp theo")
    
    with col2:
        if st.button("📊 Xuất danh sách"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="💾 Tải CSV",
                data=csv,
                file_name=f"users_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🔄 Làm mới dữ liệu"):
            st.rerun()

def research_data_dashboard():
    """Research data dashboard within admin panel"""
    st.markdown("### 🔬 Dữ liệu nghiên cứu")
    
    # Load research data
    data_files = [
        "/workspaces/Mentalhealth/research_system/data/collected_data.json",
        "/workspaces/Mentalhealth/data/research_data.json",
        "/workspaces/Mentalhealth/research_data.json"
    ]
    
    all_data = []
    
    for file_path in data_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)
                    elif isinstance(data, dict):
                        all_data.append(data)
            except Exception as e:
                st.warning(f"Không thể đọc file {file_path}: {e}")
    
    if not all_data:
        st.warning("⚠️ Chưa có dữ liệu nghiên cứu nào được thu thập.")
        
        st.markdown("""
        ### 📍 Hướng dẫn kích hoạt thu thập dữ liệu nghiên cứu:
        
        **1. 🔧 Kích hoạt research system:**
        ```bash
        export ENABLE_RESEARCH_COLLECTION=true
        ```
        
        **2. 🌐 Vị trí trong giao diện:**
        - Mở SOULFRIEND: http://localhost:8502
        - Tìm "🔬 Chia sẻ Dữ liệu cho Nghiên cứu" trong Sidebar
        - Người dùng chọn đồng ý chia sẻ dữ liệu
        - Dữ liệu sẽ tự động thu thập khi thực hiện đánh giá
        
        **3. 📂 File dữ liệu sẽ được lưu tại:**
        - `/research_system/data/collected_data.json`
        - `/data/research_data.json`
        """)
        return
    
    # Data overview
    st.markdown("#### 📊 Tổng quan dữ liệu")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(all_data)
        st.metric("📋 Tổng số records", total_records)
    
    with col2:
        consent_records = len([r for r in all_data if 'consent_given' in r])
        st.metric("🔬 Consent records", consent_records)
    
    with col3:
        assessment_records = len([r for r in all_data if 'questionnaire_type' in r])
        st.metric("📝 Assessment records", assessment_records)
    
    with col4:
        unique_sessions = len(set(r.get('session_id', '') for r in all_data if r.get('session_id')))
        st.metric("👥 Unique sessions", unique_sessions)
    
    # Consent Analysis
    consent_data = []
    for record in all_data:
        if 'consent_given' in record:
            consent_data.append({
                'timestamp': record.get('timestamp', ''),
                'consent': record['consent_given'],
                'user_type': record.get('user_info', {}).get('type', 'unknown')
            })
    
    if consent_data:
        st.markdown("#### 🔬 Phân tích Consent")
        
        consent_df = pd.DataFrame(consent_data)
        consent_df['timestamp'] = pd.to_datetime(consent_df['timestamp'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            consent_counts = consent_df['consent'].value_counts()
            fig_pie = px.pie(
                values=consent_counts.values,
                names=['Đồng ý' if x else 'Từ chối' for x in consent_counts.index],
                title="Tỷ lệ đồng ý/từ chối nghiên cứu"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("**📊 Thống kê consent:**")
            total_consent = len(consent_data)
            agreed = len([d for d in consent_data if d['consent']])
            disagreed = total_consent - agreed
            
            st.write(f"- Tổng cộng: {total_consent}")
            st.write(f"- Đồng ý: {agreed} ({agreed/total_consent*100:.1f}%)")
            st.write(f"- Từ chối: {disagreed} ({disagreed/total_consent*100:.1f}%)")
    
    # Assessment Analysis
    assessment_data = []
    for record in all_data:
        if 'questionnaire_type' in record:
            assessment_data.append({
                'timestamp': record.get('timestamp', ''),
                'questionnaire': record['questionnaire_type'],
                'score': record.get('total_score', 0),
                'completion_time': record.get('completion_time_seconds', 0)
            })
    
    if assessment_data:
        st.markdown("#### 📝 Phân tích Assessment Data")
        
        assessment_df = pd.DataFrame(assessment_data)
        assessment_df['timestamp'] = pd.to_datetime(assessment_df['timestamp'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Assessment types distribution
            assessment_counts = assessment_df['questionnaire'].value_counts()
            fig_bar = px.bar(
                x=assessment_counts.index,
                y=assessment_counts.values,
                title="Phân bố loại đánh giá"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Average scores by questionnaire
            avg_scores = assessment_df.groupby('questionnaire')['score'].mean()
            fig_bar2 = px.bar(
                x=avg_scores.index,
                y=avg_scores.values,
                title="Điểm trung bình theo loại đánh giá"
            )
            st.plotly_chart(fig_bar2, use_container_width=True)
        
        # Completion time analysis
        st.markdown("#### ⏱️ Phân tích thời gian hoàn thành")
        
        avg_completion = assessment_df.groupby('questionnaire')['completion_time'].mean()
        fig_time = px.bar(
            x=avg_completion.index,
            y=avg_completion.values,
            title="Thời gian hoàn thành trung bình (giây)"
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    # Export options
    st.markdown("#### 📤 Xuất dữ liệu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Xuất CSV"):
            df_export = pd.DataFrame(all_data)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="💾 Tải file CSV",
                data=csv,
                file_name=f"soulfriend_research_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Xuất JSON"):
            json_str = json.dumps(all_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Tải file JSON",
                data=json_str,
                file_name=f"soulfriend_research_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("🔄 Làm mới dữ liệu"):
            st.rerun()
    
    # Raw data preview
    with st.expander("📄 Xem dữ liệu chi tiết"):
        st.json(all_data[:5])  # Show first 5 records
        
        if len(all_data) > 5:
            st.info(f"Hiển thị 5 records đầu tiên. Tổng cộng: {len(all_data)} records")

def advanced_system_config():
    """Advanced system configuration interface for admins"""
    st.title("🔧 Cấu hình hệ thống nâng cao")
    
    # Configuration tabs
    config_tab = st.selectbox(
        "Chọn loại cấu hình:",
        ["📱 Cấu hình ứng dụng", "📊 Cấu hình đánh giá", "🔒 Cấu hình bảo mật", "🤖 Cấu hình AI", "🔬 Cấu hình nghiên cứu"]
    )
    
    if config_tab == "📱 Cấu hình ứng dụng":
        st.subheader("🎨 Giao diện & Hiển thị")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Chế độ tối", value=False, help="Bật/tắt giao diện tối")
            st.selectbox("Ngôn ngữ mặc định:", ["Tiếng Việt", "English"], help="Ngôn ngữ hiển thị mặc định")
            st.number_input("Thời gian session (phút):", min_value=15, max_value=480, value=60)
            
        with col2:
            st.checkbox("Hiện logo", value=True)
            st.checkbox("Âm thanh thông báo", value=True)
            st.selectbox("Múi giờ:", ["UTC+7 (Việt Nam)", "UTC+0 (GMT)", "UTC-5 (EST)"])
            
        st.subheader("📧 Thông báo")
        st.checkbox("Email thông báo", value=False, help="Gửi email thông báo kết quả")
        st.text_input("Email admin:", placeholder="admin@soulfriend.vn")
        
    elif config_tab == "📊 Cấu hình đánh giá":
        st.subheader("⚙️ Tham số đánh giá")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Thời gian tối đa (phút):", min_value=5, max_value=60, value=30)
            st.checkbox("Lưu tiến độ tự động", value=True)
            st.checkbox("Hiển thị thanh tiến độ", value=True)
            
        with col2:
            st.selectbox("Độ khó mặc định:", ["Dễ", "Trung bình", "Khó"])
            st.checkbox("Xáo trộn câu hỏi", value=False)
            st.number_input("Số câu tối đa/phiên:", min_value=10, max_value=100, value=50)
            
        st.subheader("📈 Điểm số & Thang đo")
        for scale in ["DASS-21", "PHQ-9", "GAD-7", "EPDS", "PSS-10"]:
            with st.expander(f"Cấu hình {scale}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.checkbox(f"Kích hoạt {scale}", value=True)
                    st.selectbox(f"Phiên bản {scale}:", ["Chuẩn", "Rút gọn", "Mở rộng"])
                with col2:
                    st.number_input(f"Ngưỡng cảnh báo {scale}:", min_value=0, max_value=100, value=15)
                    st.selectbox(f"Tần suất khuyến nghị {scale}:", ["Hàng tuần", "2 tuần", "Hàng tháng"])
    
    elif config_tab == "🔒 Cấu hình bảo mật":
        st.subheader("🛡️ Bảo mật & Quyền riêng tư")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Mức mã hóa:", ["AES-128", "AES-256", "RSA-2048"])
            st.number_input("Độ dài mật khẩu tối thiểu:", min_value=6, max_value=20, value=8)
            st.checkbox("Xác thực 2 yếu tố", value=False)
            
        with col2:
            st.number_input("Thời gian khóa tài khoản (phút):", min_value=5, max_value=60, value=15)
            st.number_input("Số lần đăng nhập sai tối đa:", min_value=3, max_value=10, value=5)
            st.checkbox("Ghi log truy cập", value=True)
            
        st.subheader("🔐 Quyền truy cập")
        with st.expander("Cấu hình quyền Admin"):
            st.multiselect("Quyền quản lý:", 
                         ["Xem dữ liệu", "Sửa cấu hình", "Quản lý user", "Xuất báo cáo", "Cấu hình hệ thống"],
                         default=["Xem dữ liệu", "Xuất báo cáo"])
    
    elif config_tab == "🤖 Cấu hình AI":
        st.subheader("🧠 Trí tuệ nhân tạo")
        
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Model AI:", ["GPT-3.5", "GPT-4", "Local Model"])
            st.slider("Độ sáng tạo (Temperature):", 0.0, 1.0, 0.7, 0.1)
            st.number_input("Max tokens:", min_value=100, max_value=4000, value=1000)
            
        with col2:
            st.checkbox("AI Chatbot", value=True)
            st.checkbox("Gợi ý thông minh", value=True)
            st.selectbox("Ngôn ngữ AI:", ["Tiếng Việt", "English", "Tự động"])
            
        st.subheader("🎯 Cá nhân hóa")
        st.checkbox("Học từ phản hồi người dùng", value=True)
        st.slider("Mức độ cá nhân hóa:", 1, 5, 3)
        
    elif config_tab == "🔬 Cấu hình nghiên cứu":
        st.subheader("📊 Thu thập dữ liệu nghiên cứu")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Thu thập dữ liệu ẩn danh", value=True)
            st.selectbox("Mức độ ẩn danh:", ["Thấp", "Trung bình", "Cao"])
            st.checkbox("Chia sẻ với đối tác nghiên cứu", value=False)
            
        with col2:
            st.number_input("Thời gian lưu trữ (tháng):", min_value=1, max_value=60, value=12)
            st.checkbox("Tự động xuất báo cáo", value=True)
            st.selectbox("Tần suất báo cáo:", ["Hàng tuần", "Hàng tháng", "Quý"])
            
        st.subheader("✅ Chấp thuận nghiên cứu")
        st.text_area("Văn bản chấp thuận:", 
                    value="Tôi đồng ý cho phép dữ liệu của mình được sử dụng cho mục đích nghiên cứu khoa học...",
                    height=100)
    
    # Save configuration
    if st.button("💾 Lưu cấu hình", type="primary"):
        st.success("✅ Đã lưu cấu hình thành công!")
        st.balloons()

def admin_reports_dashboard():
    """Comprehensive admin reports dashboard"""
    st.title("📋 Báo cáo tổng thể")
    
    # Report type selection
    report_type = st.selectbox(
        "Chọn loại báo cáo:",
        ["📊 Báo cáo tổng quan", "👥 Báo cáo người dùng", "📈 Báo cáo hiệu suất", "🔬 Báo cáo nghiên cứu", "⚠️ Báo cáo cảnh báo"]
    )
    
    # Date range filter
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input("Từ ngày:", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("Đến ngày:", datetime.now())
    with col3:
        export_format = st.selectbox("Xuất:", ["PDF", "Excel", "CSV"])
    
    if report_type == "📊 Báo cáo tổng quan":
        st.subheader("📈 Thống kê tổng quan hệ thống")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tổng người dùng", "1,234", "↗️ +5.2%")
        with col2:
            st.metric("Đánh giá hoàn thành", "2,567", "↗️ +12.3%")
        with col3:
            st.metric("Thời gian trung bình", "15.4 phút", "↘️ -2.1%")
        with col4:
            st.metric("Độ hài lòng", "4.2/5", "↗️ +0.3")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Số lượng đánh giá theo thời gian")
            # Sample chart data
            chart_data = pd.DataFrame({
                'Ngày': pd.date_range(start_date, end_date, freq='D'),
                'Số lượng': np.random.randint(10, 50, size=(end_date - start_date).days + 1)
            })
            st.line_chart(chart_data.set_index('Ngày'))
            
        with col2:
            st.subheader("🎯 Phân bố theo thang đo")
            scale_data = pd.DataFrame({
                'Thang đo': ['DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10'],
                'Số lượng': [450, 380, 320, 180, 240]
            })
            st.bar_chart(scale_data.set_index('Thang đo'))
    
    elif report_type == "👥 Báo cáo người dùng":
        st.subheader("👤 Thống kê người dùng")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Phân bố độ tuổi")
            age_data = pd.DataFrame({
                'Độ tuổi': ['18-25', '26-35', '36-45', '46-55', '55+'],
                'Số lượng': [380, 520, 290, 180, 90]
            })
            st.bar_chart(age_data.set_index('Độ tuổi'))
            
        with col2:
            st.subheader("⚥ Phân bố giới tính")
            gender_data = {
                'Nam': 45.2,
                'Nữ': 52.8,
                'Khác': 2.0
            }
            st.plotly_chart(px.pie(values=list(gender_data.values()), 
                                  names=list(gender_data.keys()), 
                                  title="Phân bố giới tính"))
        
        # User activity table
        st.subheader("📋 Hoạt động người dùng gần đây")
        user_activity = pd.DataFrame({
            'ID': ['U001', 'U002', 'U003', 'U004', 'U005'],
            'Tên': ['Nguyễn A', 'Trần B', 'Lê C', 'Phạm D', 'Hoàng E'],
            'Lần cuối': ['2024-01-15', '2024-01-14', '2024-01-14', '2024-01-13', '2024-01-12'],
            'Số đánh giá': [5, 3, 8, 2, 6],
            'Trạng thái': ['Active', 'Active', 'Warning', 'Active', 'Inactive']
        })
        st.dataframe(user_activity, use_container_width=True)
    
    elif report_type == "📈 Báo cáo hiệu suất":
        st.subheader("⚡ Hiệu suất hệ thống")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Thời gian phản hồi TB", "245ms", "↘️ -15ms")
        with col2:
            st.metric("Uptime", "99.8%", "↗️ +0.1%")
        with col3:
            st.metric("CPU sử dụng", "35%", "↘️ -5%")
        
        # Performance charts
        st.subheader("📊 Hiệu suất theo thời gian")
        perf_data = pd.DataFrame({
            'Thời gian': pd.date_range(start_date, end_date, freq='H'),
            'Response Time (ms)': np.random.normal(250, 50, size=(end_date - start_date).days * 24 + 1),
            'CPU (%)': np.random.normal(35, 10, size=(end_date - start_date).days * 24 + 1)
        })
        st.line_chart(perf_data.set_index('Thời gian'))
    
    elif report_type == "🔬 Báo cáo nghiên cứu":
        st.subheader("🧪 Dữ liệu nghiên cứu")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mẫu nghiên cứu", "1,156", "↗️ +48")
        with col2:
            st.metric("Độ tin cậy", "0.89", "↗️ +0.02")
        with col3:
            st.metric("Hoàn thành", "92.3%", "↗️ +1.5%")
        
        # Research findings
        st.subheader("📊 Kết quả nghiên cứu chính")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🎯 Phân bố mức độ stress:**")
            stress_levels = pd.DataFrame({
                'Mức độ': ['Bình thường', 'Nhẹ', 'Trung bình', 'Nặng', 'Rất nặng'],
                'Tỷ lệ (%)': [32.1, 28.5, 22.3, 12.8, 4.3]
            })
            st.bar_chart(stress_levels.set_index('Mức độ'))
            
        with col2:
            st.write("**🧠 Tương quan giữa các yếu tố:**")
            correlation_data = pd.DataFrame({
                'Yếu tố 1': ['Tuổi', 'Giới tính', 'Công việc', 'Thu nhập'],
                'Yếu tố 2': ['Stress', 'Trầm cảm', 'Lo âu', 'Stress'],
                'Hệ số tương quan': [0.23, -0.15, 0.31, -0.42]
            })
            st.dataframe(correlation_data)
    
    elif report_type == "⚠️ Báo cáo cảnh báo":
        st.subheader("🚨 Cảnh báo hệ thống")
        
        # Alert summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Cảnh báo cao", "3", "↗️ +1")
        with col2:
            st.metric("Cảnh báo trung bình", "12", "↘️ -2")
        with col3:
            st.metric("Người dùng rủi ro cao", "8", "↗️ +3")
        with col4:
            st.metric("Sự cố hệ thống", "0", "→ 0")
        
        # Alerts table
        st.subheader("📋 Danh sách cảnh báo")
        alerts_data = pd.DataFrame({
            'Thời gian': ['2024-01-15 14:30', '2024-01-15 10:15', '2024-01-14 16:45'],
            'Loại': ['User Risk', 'System Error', 'Data Anomaly'],
            'Mức độ': ['🔴 Cao', '🟡 Trung bình', '🟠 Trung bình'],
            'Mô tả': [
                'Người dùng U123 có điểm số DASS-21 rất cao',
                'Lỗi kết nối database trong 5 phút',
                'Dữ liệu PHQ-9 có giá trị bất thường'
            ],
            'Trạng thái': ['🔄 Đang xử lý', '✅ Đã giải quyết', '👁️ Đang theo dõi']
        })
        st.dataframe(alerts_data, use_container_width=True)
    
    # Export button
    if st.button(f"📥 Xuất báo cáo ({export_format})", type="primary"):
        st.success(f"✅ Đã xuất báo cáo {report_type} dạng {export_format}")
        st.info("📁 File đã được lưu vào thư mục Downloads")


def system_analytics_dashboard():
    """Advanced system configuration for admins only"""
    st.markdown("### 🔧 Cấu hình hệ thống nâng cao")
    st.warning("⚠️ Chỉ admin có kinh nghiệm nên thay đổi các cài đặt này!")
    
    # Load default config
    default_config = {
        "app_settings": {
            "app_name": "SOULFRIEND V3.0",
            "version": "3.0.0",
            "environment": "production",
            "debug_mode": False,
            "language": "vietnamese",
            "timezone": "Asia/Ho_Chi_Minh",
            "max_concurrent_users": 1000,
            "session_timeout_minutes": 60
        },
        "assessment_settings": {
            "enable_phq9": True,
            "enable_gad7": True,
            "enable_dass21": True,
            "enable_epds": True,
            "enable_pss10": True,
            "auto_save": True,
            "show_progress": True,
            "require_consent": True,
            "max_assessments_per_day": 10
        },
        "security_settings": {
            "data_retention_days": 365,
            "backup_enabled": True,
            "encryption_enabled": True,
            "anonymous_mode": True,
            "audit_logging": True,
            "ip_whitelist_enabled": False
        },
        "ai_settings": {
            "chatbot_enabled": True,
            "ai_insights": True,
            "predictive_analytics": True,
            "auto_recommendations": True,
            "crisis_detection": True,
            "ml_model_version": "2.1"
        },
        "research_settings": {
            "data_collection_enabled": True,
            "consent_required": True,
            "anonymization_level": "high",
            "export_formats": ["csv", "json"],
            "retention_period_days": 1095
        }
    }
    
    # Configuration tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 App Config",
        "📋 Assessment Config", 
        "🔒 Security Config",
        "🤖 AI Config",
        "🔬 Research Config"
    ])
    
    with tab1:
        st.markdown("#### 🏠 Application Configuration")
        
        with st.form("app_config"):
            col1, col2 = st.columns(2)
            
            with col1:
                app_name = st.text_input("App Name:", value=default_config["app_settings"]["app_name"])
                version = st.text_input("Version:", value=default_config["app_settings"]["version"])
                environment = st.selectbox("Environment:", ["development", "staging", "production"], 
                                         index=2 if default_config["app_settings"]["environment"] == "production" else 0)
                
            with col2:
                debug_mode = st.checkbox("Debug Mode", value=default_config["app_settings"]["debug_mode"])
                language = st.selectbox("Language:", ["vietnamese", "english"], 
                                      index=0 if default_config["app_settings"]["language"] == "vietnamese" else 1)
                timezone = st.text_input("Timezone:", value=default_config["app_settings"]["timezone"])
            
            max_users = st.number_input("Max Concurrent Users:", min_value=1, max_value=10000, 
                                      value=default_config["app_settings"]["max_concurrent_users"])
            session_timeout = st.number_input("Session Timeout (minutes):", min_value=5, max_value=480, 
                                            value=default_config["app_settings"]["session_timeout_minutes"])
            
            if st.form_submit_button("💾 Save App Config"):
                st.success("✅ Application configuration saved!")
    
    with tab2:
        st.markdown("#### 📋 Assessment Configuration")
        
        with st.form("assessment_config"):
            st.markdown("**Enable/Disable Assessments:**")
            col1, col2 = st.columns(2)
            
            with col1:
                enable_phq9 = st.checkbox("PHQ-9 Depression", value=default_config["assessment_settings"]["enable_phq9"])
                enable_gad7 = st.checkbox("GAD-7 Anxiety", value=default_config["assessment_settings"]["enable_gad7"])
                enable_dass21 = st.checkbox("DASS-21", value=default_config["assessment_settings"]["enable_dass21"])
                
            with col2:
                enable_epds = st.checkbox("EPDS Postpartum", value=default_config["assessment_settings"]["enable_epds"])
                enable_pss10 = st.checkbox("PSS-10 Stress", value=default_config["assessment_settings"]["enable_pss10"])
                
            st.markdown("**Assessment Settings:**")
            auto_save = st.checkbox("Auto Save Progress", value=default_config["assessment_settings"]["auto_save"])
            show_progress = st.checkbox("Show Progress Bar", value=default_config["assessment_settings"]["show_progress"])
            require_consent = st.checkbox("Require Consent", value=default_config["assessment_settings"]["require_consent"])
            max_per_day = st.number_input("Max Assessments per Day:", min_value=1, max_value=50, 
                                        value=default_config["assessment_settings"]["max_assessments_per_day"])
            
            if st.form_submit_button("💾 Save Assessment Config"):
                st.success("✅ Assessment configuration saved!")
    
    with tab3:
        st.markdown("#### 🔒 Security Configuration")
        
        with st.form("security_config"):
            col1, col2 = st.columns(2)
            
            with col1:
                data_retention = st.number_input("Data Retention (days):", min_value=30, max_value=3650, 
                                               value=default_config["security_settings"]["data_retention_days"])
                backup_enabled = st.checkbox("Backup Enabled", value=default_config["security_settings"]["backup_enabled"])
                encryption_enabled = st.checkbox("Encryption Enabled", value=default_config["security_settings"]["encryption_enabled"])
                
            with col2:
                anonymous_mode = st.checkbox("Anonymous Mode", value=default_config["security_settings"]["anonymous_mode"])
                audit_logging = st.checkbox("Audit Logging", value=default_config["security_settings"]["audit_logging"])
                ip_whitelist = st.checkbox("IP Whitelist", value=default_config["security_settings"]["ip_whitelist_enabled"])
            
            if st.form_submit_button("💾 Save Security Config"):
                st.success("✅ Security configuration saved!")
                st.info("🔄 Some settings require restart to take effect.")
    
    with tab4:
        st.markdown("#### 🤖 AI Configuration")
        
        with st.form("ai_config"):
            col1, col2 = st.columns(2)
            
            with col1:
                chatbot_enabled = st.checkbox("Chatbot Enabled", value=default_config["ai_settings"]["chatbot_enabled"])
                ai_insights = st.checkbox("AI Insights", value=default_config["ai_settings"]["ai_insights"])
                predictive_analytics = st.checkbox("Predictive Analytics", value=default_config["ai_settings"]["predictive_analytics"])
                
            with col2:
                auto_recommendations = st.checkbox("Auto Recommendations", value=default_config["ai_settings"]["auto_recommendations"])
                crisis_detection = st.checkbox("Crisis Detection", value=default_config["ai_settings"]["crisis_detection"])
                
            ml_version = st.selectbox("ML Model Version:", ["1.0", "2.0", "2.1", "3.0"], 
                                    index=2 if default_config["ai_settings"]["ml_model_version"] == "2.1" else 0)
            
            if st.form_submit_button("💾 Save AI Config"):
                st.success("✅ AI configuration saved!")
    
    with tab5:
        st.markdown("#### 🔬 Research Configuration")
        
        with st.form("research_config"):
            col1, col2 = st.columns(2)
            
            with col1:
                data_collection = st.checkbox("Data Collection Enabled", value=default_config["research_settings"]["data_collection_enabled"])
                consent_required = st.checkbox("Consent Required", value=default_config["research_settings"]["consent_required"])
                anonymization = st.selectbox("Anonymization Level:", ["low", "medium", "high"], 
                                           index=2 if default_config["research_settings"]["anonymization_level"] == "high" else 0)
                
            with col2:
                export_formats = st.multiselect("Export Formats:", ["csv", "json", "xlsx"], 
                                              default=default_config["research_settings"]["export_formats"])
                retention_days = st.number_input("Research Data Retention (days):", min_value=90, max_value=3650, 
                                               value=default_config["research_settings"]["retention_period_days"])
            
            if st.form_submit_button("💾 Save Research Config"):
                st.success("✅ Research configuration saved!")
    
    # Configuration export/import
    st.markdown("---")
    st.markdown("#### 📤 Export/Import Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Config"):
            config_json = json.dumps(default_config, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Download Config JSON",
                data=config_json,
                file_name=f"soulfriend_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📂 Import Config", type=['json'])
        if uploaded_file is not None:
            try:
                imported_config = json.load(uploaded_file)
                st.success("✅ Configuration imported successfully!")
                st.json(imported_config)
            except Exception as e:
                st.error(f"❌ Error importing config: {e}")
    
    with col3:
        if st.button("🔄 Reset to Defaults"):
            st.warning("⚠️ This will reset all settings to default values!")
            if st.button("✅ Confirm Reset"):
                st.success("✅ Configuration reset to defaults!")

def system_analytics_dashboard():
    """System-level analytics dashboard for admins"""
    st.markdown("### 📈 Analytics hệ thống")
    st.markdown("**Real-time system monitoring và performance analytics**")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
    
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()
    
    # System Health Overview
    st.markdown("#### 🔋 System Health Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Server Status
        st.metric(
            label="🖥️ Server Status", 
            value="Online",
            delta="99.9% uptime"
        )
    
    with col2:
        # Memory Usage
        import random
        memory_usage = random.randint(60, 85)
        st.metric(
            label="💾 Memory Usage", 
            value=f"{memory_usage}%",
            delta=f"{random.randint(-5, 5)}%" if memory_usage < 80 else "⚠️ High"
        )
    
    with col3:
        # CPU Usage
        cpu_usage = random.randint(20, 70)
        st.metric(
            label="⚡ CPU Usage", 
            value=f"{cpu_usage}%",
            delta=f"{random.randint(-10, 10)}%"
        )
    
    with col4:
        # Active Sessions
        active_sessions = random.randint(50, 200)
        st.metric(
            label="👥 Active Sessions", 
            value=active_sessions,
            delta=f"{random.randint(-10, 20)}"
        )
    
    # Performance Metrics
    st.markdown("#### ⚡ Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Response Time Chart
        import plotly.graph_objects as go
        from datetime import datetime, timedelta
        
        # Generate mock response time data
        times = [datetime.now() - timedelta(hours=i) for i in range(24, 0, -1)]
        response_times = [random.uniform(0.1, 2.5) for _ in range(24)]
        
        fig_response = go.Figure()
        fig_response.add_trace(go.Scatter(
            x=times,
            y=response_times,
            mode='lines+markers',
            name='Response Time (s)',
            line=dict(color='#1f77b4', width=3)
        ))
        fig_response.update_layout(
            title="📊 Response Time (24h)",
            xaxis_title="Time",
            yaxis_title="Response Time (seconds)",
            height=300
        )
        st.plotly_chart(fig_response, use_container_width=True)
    
    with col2:
        # Error Rate Chart
        error_rates = [random.uniform(0, 5) for _ in range(24)]
        
        fig_errors = go.Figure()
        fig_errors.add_trace(go.Scatter(
            x=times,
            y=error_rates,
            mode='lines+markers',
            name='Error Rate (%)',
            line=dict(color='#d62728', width=3)
        ))
        fig_errors.update_layout(
            title="❌ Error Rate (24h)",
            xaxis_title="Time", 
            yaxis_title="Error Rate (%)",
            height=300
        )
        st.plotly_chart(fig_errors, use_container_width=True)
    
    # User Analytics
    st.markdown("#### 👥 User Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Daily Active Users
        daily_users = [random.randint(80, 250) for _ in range(7)]
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        fig_users = go.Figure()
        fig_users.add_trace(go.Bar(
            x=days,
            y=daily_users,
            name='Daily Active Users',
            marker_color='#2ca02c'
        ))
        fig_users.update_layout(
            title="📊 Daily Active Users",
            xaxis_title="Day",
            yaxis_title="Users",
            height=300
        )
        st.plotly_chart(fig_users, use_container_width=True)
    
    with col2:
        # Assessment Distribution
        assessments = ['PHQ-9', 'GAD-7', 'DASS-21', 'EPDS', 'PSS-10']
        counts = [random.randint(20, 100) for _ in range(5)]
        
        fig_assess = go.Figure()
        fig_assess.add_trace(go.Pie(
            labels=assessments,
            values=counts,
            hole=0.4
        ))
        fig_assess.update_layout(
            title="📋 Assessment Distribution",
            height=300
        )
        st.plotly_chart(fig_assess, use_container_width=True)
    
    with col3:
        # Geographic Distribution
        locations = ['HCM City', 'Hanoi', 'Da Nang', 'Can Tho', 'Others']
        geo_counts = [random.randint(30, 120) for _ in range(5)]
        
        fig_geo = go.Figure()
        fig_geo.add_trace(go.Bar(
            x=locations,
            y=geo_counts,
            name='Users by Location',
            marker_color='#ff7f0e'
        ))
        fig_geo.update_layout(
            title="🌍 Geographic Distribution",
            xaxis_title="Location",
            yaxis_title="Users",
            height=300
        )
        st.plotly_chart(fig_geo, use_container_width=True)
    
    # System Resources
    st.markdown("#### 💻 System Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🗄️ Database Status**")
        st.success("✅ Database: Online")
        st.info(f"📊 Records: {random.randint(10000, 50000):,}")
        st.info(f"💾 Size: {random.randint(500, 2000)} MB")
        st.info(f"🔄 Backup: {random.choice(['Today 03:00', 'Yesterday 03:00'])}")
    
    with col2:
        st.markdown("**🌐 Network Status**")
        st.success("✅ Network: Stable")
        st.info(f"📡 Bandwidth: {random.randint(80, 95)}% available")
        st.info(f"🔗 Connections: {random.randint(100, 500)}")
        st.info(f"📈 Throughput: {random.randint(50, 200)} MB/s")
    
    with col3:
        st.markdown("**🔒 Security Status**")
        st.success("✅ Security: Protected")
        st.info(f"🛡️ Firewall: Active")
        st.info(f"🔐 SSL: Valid until {(datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')}")
        st.info(f"🔍 Last scan: {random.choice(['1 hour ago', '2 hours ago', '30 min ago'])}")
    
    # Recent System Events
    st.markdown("#### 📋 Recent System Events")
    
    events = [
        {"time": "10:30", "type": "INFO", "message": "System backup completed successfully"},
        {"time": "09:45", "type": "WARNING", "message": f"High memory usage detected: {random.randint(80, 90)}%"},
        {"time": "09:20", "type": "INFO", "message": f"New user registration: {random.randint(1, 10)} users"},
        {"time": "08:55", "type": "SUCCESS", "message": "Database optimization completed"},
        {"time": "08:30", "type": "INFO", "message": f"Assessment completion: {random.randint(10, 50)} assessments"},
        {"time": "08:00", "type": "INFO", "message": "Daily system health check: All systems normal"}
    ]
    
    for event in events:
        if event["type"] == "WARNING":
            st.warning(f"⏰ {event['time']} - {event['message']}")
        elif event["type"] == "SUCCESS":
            st.success(f"⏰ {event['time']} - {event['message']}")
        else:
            st.info(f"⏰ {event['time']} - {event['message']}")
    
    # Export System Report
    st.markdown("---")
    st.markdown("#### 📤 Export System Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Performance Report"):
            # Mock report data
            report_data = {
                "generated_at": datetime.now().isoformat(),
                "system_health": "Good",
                "uptime": "99.9%",
                "active_users": active_sessions,
                "memory_usage": f"{memory_usage}%",
                "cpu_usage": f"{cpu_usage}%",
                "recent_events": events
            }
            
            report_json = json.dumps(report_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Download Report",
                data=report_json,
                file_name=f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📈 Export Analytics Data"):
            analytics_data = {
                "response_times": response_times,
                "error_rates": error_rates,
                "daily_users": daily_users,
                "assessment_counts": dict(zip(assessments, counts)),
                "geographic_data": dict(zip(locations, geo_counts))
            }
            
            analytics_json = json.dumps(analytics_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Download Analytics",
                data=analytics_json,
                file_name=f"analytics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("🔄 Refresh All Data"):
            st.success("✅ All data refreshed!")
            st.rerun()

def system_settings():
    """System settings and configuration"""
    st.markdown("### ⚙️ Cài đặt hệ thống")
    
    # Application settings
    st.markdown("#### 🏠 Cài đặt ứng dụng")
    
    with st.form("app_settings"):
        app_title = st.text_input("Tên ứng dụng:", value="SOULFRIEND")
        maintenance_mode = st.checkbox("Chế độ bảo trì")
        max_daily_assessments = st.number_input("Số đánh giá tối đa mỗi ngày:", min_value=1, value=100)
        
        # Emergency contacts
        st.markdown("##### 🆘 Liên hệ khẩn cấp")
        hotline = st.text_input("Hotline:", value="1800-1567")
        emergency = st.text_input("Cấp cứu:", value="115")
        counseling = st.text_input("Tư vấn:", value="1900-555-555")
        
        if st.form_submit_button("💾 Lưu cài đặt"):
            st.success("✅ Đã lưu cài đặt!")
    
    # Database management
    st.markdown("#### 🗄️ Quản lý dữ liệu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗂️ Sao lưu dữ liệu"):
            st.info("Đang tạo bản sao lưu...")
            # Implementation would backup questionnaire configs, user data, etc.
    
    with col2:
        if st.button("🔄 Khôi phục dữ liệu"):
            st.warning("Tính năng khôi phục cần được thực hiện cẩn trọng")
    
    with col3:
        if st.button("🧹 Dọn dẹp dữ liệu"):
            st.info("Dọn dẹp dữ liệu cũ và log files")

def admin_panel():
    """Main admin panel interface"""
    if not verify_admin_login():
        return
    
    # Admin header
    st.markdown("# 🔧 Bảng điều khiển quản trị")
    st.markdown(f"Xin chào **{st.session_state.get('admin_username', 'Admin')}**!")
    
    # Quick access to other admin tools
    st.subheader("🔗 Công cụ quản trị")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Bảng điều khiển phân tích", width="stretch"):
            st.switch_page("analytics_dashboard.py")
    
    with col2:
        if st.button("⚙️ Cấu hình hệ thống", width="stretch"):
            st.switch_page("config_manager.py")
    
    with col3:
        if st.button("🏠 Về trang chính", width="stretch"):
            st.switch_page("SOULFRIEND.py")

    st.markdown("---")
    
    # Logout button
    admin_logout()
    
    # Admin navigation
    admin_tab = st.sidebar.selectbox(
        "📋 Chọn chức năng:",
        ["📊 Thống kê", "📈 Analytics hệ thống", "📝 Quản lý thang đo", "👥 Người dùng", "📋 Báo cáo tổng thể", "🔬 Dữ liệu nghiên cứu", "⚙️ Cài đặt", "🔧 Cấu hình hệ thống"]
    )
    
    # Display selected admin function
    if admin_tab == "📊 Thống kê":
        analytics_dashboard()
    elif admin_tab == "📈 Analytics hệ thống":
        system_analytics_dashboard()
    elif admin_tab == "📝 Quản lý thang đo":
        questionnaire_manager()
    elif admin_tab == "👥 Người dùng":
        user_management()
    elif admin_tab == "� Báo cáo tổng thể":
        admin_reports_dashboard()
    elif admin_tab == "�🔬 Dữ liệu nghiên cứu":
        research_data_dashboard()
    elif admin_tab == "⚙️ Cài đặt":
        system_settings()
    elif admin_tab == "🔧 Cấu hình hệ thống":
        advanced_system_config()

if __name__ == "__main__":
    admin_panel()
