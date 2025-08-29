"""
Admin Panel for SOULFRIEND
Provides administrative tools for managing questionnaires, users, and analytics
"""

import streamlit as st
import json
import os
import pandas as pd
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
                use_container_width=True,
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
    
    st.plotly_chart(fig, use_container_width=True)
    
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
        st.plotly_chart(fig_bar, use_container_width=True)
    
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
        st.plotly_chart(fig_hourly, use_container_width=True)

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
    st.dataframe(filtered_df, use_container_width=True)
    
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
        if st.button("📊 Bảng điều khiển phân tích", use_container_width=True):
            st.switch_page("analytics_dashboard.py")
    
    with col2:
        if st.button("⚙️ Cấu hình hệ thống", use_container_width=True):
            st.switch_page("config_manager.py")
    
    with col3:
        if st.button("🏠 Về trang chính", use_container_width=True):
            st.switch_page("SOULFRIEND.py")

    st.markdown("---")
    
    # Logout button
    admin_logout()
    
    # Admin navigation
    admin_tab = st.sidebar.selectbox(
        "📋 Chọn chức năng:",
        ["📊 Thống kê", "📝 Quản lý thang đo", "👥 Người dùng", "⚙️ Cài đặt"]
    )
    
    # Display selected admin function
    if admin_tab == "📊 Thống kê":
        analytics_dashboard()
    elif admin_tab == "📝 Quản lý thang đo":
        questionnaire_manager()
    elif admin_tab == "👥 Người dùng":
        user_management()
    elif admin_tab == "⚙️ Cài đặt":
        system_settings()

if __name__ == "__main__":
    admin_panel()
