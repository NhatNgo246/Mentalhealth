#!/usr/bin/env python3
"""
🔍 Quick Research Data Viewer
Xem nhanh dữ liệu nghiên cứu SOULFRIEND
"""

import streamlit as st
import pandas as pd
import json
import sqlite3
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="🔍 SOULFRIEND Data Viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .data-header {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="data-header">
    <h1>🔍 SOULFRIEND Research Data Viewer</h1>
    <p>Xem nhanh dữ liệu nghiên cứu và analytics</p>
</div>
""", unsafe_allow_html=True)

# Data directory
RESEARCH_DIR = "/workspaces/Mentalhealth/research_data"

def load_database_data():
    """Load data from SQLite database"""
    db_path = os.path.join(RESEARCH_DIR, "research.db")
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            
            # Get table names
            tables = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table';", 
                conn
            )
            
            data = {}
            for table_name in tables['name']:
                try:
                    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 100", conn)
                    data[table_name] = df
                except Exception as e:
                    st.warning(f"Cannot read table {table_name}: {e}")
            
            conn.close()
            return data
        except Exception as e:
            st.error(f"Database error: {e}")
            return {}
    return {}

def load_json_files():
    """Load data from JSON files"""
    json_data = {}
    if os.path.exists(RESEARCH_DIR):
        files = [f for f in os.listdir(RESEARCH_DIR) if f.endswith('.json')]
        for file in files:
            try:
                with open(os.path.join(RESEARCH_DIR, file), 'r', encoding='utf-8') as f:
                    json_data[file] = json.load(f)
            except Exception as e:
                st.warning(f"Cannot read {file}: {e}")
    return json_data

# Main content
col1, col2, col3, col4 = st.columns(4)

# Load data
db_data = load_database_data()
json_data = load_json_files()

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>💾 Database Tables</h3>
        <h2>{}</h2>
    </div>
    """.format(len(db_data)), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>📄 JSON Files</h3>
        <h2>{}</h2>
    </div>
    """.format(len(json_data)), unsafe_allow_html=True)

with col3:
    total_records = sum(len(df) for df in db_data.values())
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Total Records</h3>
        <h2>{}</h2>
    </div>
    """.format(total_records), unsafe_allow_html=True)

with col4:
    db_size = 0
    db_path = os.path.join(RESEARCH_DIR, "research.db")
    if os.path.exists(db_path):
        db_size = os.path.getsize(db_path) / 1024  # KB
    st.markdown("""
    <div class="metric-card">
        <h3>💾 DB Size</h3>
        <h2>{:.1f} KB</h2>
    </div>
    """.format(db_size), unsafe_allow_html=True)

# Tabs for different data views
tab1, tab2, tab3 = st.tabs(["💾 Database Data", "📄 JSON Data", "📊 Analytics"])

with tab1:
    st.header("💾 Database Tables")
    if db_data:
        for table_name, df in db_data.items():
            st.subheader(f"📋 Table: {table_name}")
            st.write(f"Records: {len(df)}")
            
            if not df.empty:
                st.dataframe(df.head(10), use_container_width=True)
                
                # Show basic stats if numeric columns exist
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    st.write("📊 Numeric Summary:")
                    st.dataframe(df[numeric_cols].describe())
            else:
                st.info("Table is empty")
    else:
        st.info("No database tables found")

with tab2:
    st.header("📄 JSON Files")
    if json_data:
        for filename, data in json_data.items():
            st.subheader(f"📄 {filename}")
            
            if isinstance(data, dict):
                st.write("📋 Keys:", list(data.keys()))
                st.json(data)
            elif isinstance(data, list):
                st.write(f"📊 List with {len(data)} items")
                if len(data) > 0:
                    st.write("Sample item:")
                    st.json(data[0])
            else:
                st.write("📄 Raw data:")
                st.text(str(data))
    else:
        st.info("No JSON files found")

with tab3:
    st.header("📊 Analytics Dashboard")
    
    # Create some basic analytics if we have data
    if db_data:
        for table_name, df in db_data.items():
            if not df.empty and 'timestamp' in df.columns:
                st.subheader(f"📈 Timeline for {table_name}")
                
                # Convert timestamp to datetime if needed
                try:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    
                    # Group by date
                    daily_counts = df.groupby(df['timestamp'].dt.date).size().reset_index()
                    daily_counts.columns = ['date', 'count']
                    
                    # Create line chart
                    fig = px.line(daily_counts, x='date', y='count', 
                                title=f"Daily Activity - {table_name}")
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.warning(f"Cannot create timeline for {table_name}: {e}")
    
    # JSON analytics
    if json_data:
        for filename, data in json_data.items():
            if 'deployment_metrics' in filename and isinstance(data, dict):
                st.subheader(f"📊 Metrics from {filename}")
                
                if 'test_results' in data:
                    test_results = data['test_results']
                    if 'success_rate' in test_results:
                        # Create gauge chart
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = test_results['success_rate'],
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Success Rate %"},
                            gauge = {
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 50], 'color': "lightgray"},
                                    {'range': [50, 80], 'color': "yellow"},
                                    {'range': [80, 100], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 90
                                }
                            }
                        ))
                        st.plotly_chart(fig, use_container_width=True)

# Sidebar controls
with st.sidebar:
    st.markdown("### 🔧 Data Controls")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Data Summary")
    
    if os.path.exists(RESEARCH_DIR):
        all_files = os.listdir(RESEARCH_DIR)
        st.write(f"📁 Total files: {len(all_files)}")
        
        for file in all_files:
            file_path = os.path.join(RESEARCH_DIR, file)
            size = os.path.getsize(file_path)
            st.write(f"📄 {file}: {size} bytes")
    
    st.markdown("---")
    st.info("🔍 Quick Data Viewer V1.0")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    🔍 <strong>SOULFRIEND Quick Data Viewer</strong> | 
    Research Analytics | 
    © 2025
</div>
""", unsafe_allow_html=True)
