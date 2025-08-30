"""
📊 SOULFRIEND V4.0 - Advanced Analytics & Machine Learning
=========================================================

Advanced data analytics, pattern recognition, và predictive insights
cho mental health monitoring và early intervention
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class AnalyticsInsight:
    """
    Data class for analytics insights
    """
    insight_type: str
    severity: str  # low, medium, high, critical
    title: str
    description: str
    recommendations: List[str]
    confidence: float
    data_points: int
    timestamp: datetime

class AdvancedAnalytics:
    """
    Advanced Analytics Engine cho SOULFRIEND
    """
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.risk_classifier = None
        self.pattern_analyzer = None
        
        # Risk thresholds
        self.risk_thresholds = {
            'depression': {'low': 5, 'medium': 10, 'high': 15, 'severe': 20},
            'anxiety': {'low': 5, 'medium': 10, 'high': 15, 'severe': 20},
            'stress': {'low': 14, 'medium': 26, 'high': 37, 'severe': 50}
        }
        
        # Pattern recognition keywords
        self.crisis_keywords = [
            'tự tử', 'kết thúc cuộc đời', 'không muốn sống', 'tuyệt vọng',
            'vô nghĩa', 'chết đi', 'tự hại', 'không còn hy vọng'
        ]
        
        self.improvement_keywords = [
            'tốt hơn', 'cải thiện', 'vui vẻ', 'hạnh phúc', 'tích cực',
            'hy vọng', 'phục hồi', 'tiến bộ', 'khỏe mạnh'
        ]
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for analytics"""
        logger = logging.getLogger('advanced_analytics')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_user_data(self) -> pd.DataFrame:
        """
        Load và preprocess user assessment data
        """
        try:
            # Load from JSON files (simulated data structure)
            data_files = [
                'data/user_assessments.json',
                'data/chat_history.json',
                'data/research_data.json'
            ]
            
            all_data = []
            
            # Create sample data if files don't exist
            if not any(os.path.exists(f) for f in data_files):
                all_data = self._generate_sample_data()
            else:
                for file_path in data_files:
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            all_data.extend(data)
            
            df = pd.DataFrame(all_data)
            
            if not df.empty:
                # Clean and preprocess
                df['timestamp'] = pd.to_datetime(df.get('timestamp', datetime.now()))
                df = df.sort_values('timestamp')
                
                # Calculate derived features
                df = self._calculate_derived_features(df)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading user data: {e}")
            return pd.DataFrame()
    
    def _generate_sample_data(self) -> List[Dict]:
        """
        Generate sample data for demonstration
        """
        np.random.seed(42)
        
        sample_data = []
        start_date = datetime.now() - timedelta(days=90)
        
        for i in range(100):
            date = start_date + timedelta(days=np.random.randint(0, 90))
            
            # Simulate realistic mental health scores with trends
            base_depression = max(0, min(27, np.random.normal(8, 4)))
            base_anxiety = max(0, min(21, np.random.normal(7, 3)))
            base_stress = max(0, min(42, np.random.normal(16, 6)))
            
            # Add temporal correlation (getting better over time)
            improvement_factor = (i / 100) * 0.3
            
            sample_data.append({
                'user_id': f'user_{np.random.randint(1, 21)}',
                'timestamp': date.isoformat(),
                'assessment_type': np.random.choice(['phq9', 'gad7', 'dass21', 'pss10']),
                'phq9_score': max(0, base_depression - improvement_factor * 5),
                'gad7_score': max(0, base_anxiety - improvement_factor * 4),
                'dass21_depression': max(0, base_depression - improvement_factor * 3),
                'dass21_anxiety': max(0, base_anxiety - improvement_factor * 3),
                'dass21_stress': max(0, base_stress - improvement_factor * 5),
                'pss10_score': max(0, base_stress - improvement_factor * 4),
                'session_duration': np.random.randint(300, 1800),  # 5-30 minutes
                'completion_rate': np.random.uniform(0.7, 1.0),
                'chat_messages': np.random.randint(0, 50),
                'crisis_indicators': np.random.choice([0, 1], p=[0.95, 0.05]),
                'improvement_indicators': np.random.choice([0, 1], p=[0.7, 0.3])
            })
        
        return sample_data
    
    def _calculate_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate derived features for analysis
        """
        if df.empty:
            return df
        
        # Sort by user and timestamp
        df = df.sort_values(['user_id', 'timestamp'])
        
        # Calculate trends
        for user_id in df['user_id'].unique():
            user_mask = df['user_id'] == user_id
            user_data = df[user_mask].copy()
            
            if len(user_data) > 1:
                # Calculate score changes
                for score_col in ['phq9_score', 'gad7_score', 'pss10_score']:
                    if score_col in user_data.columns:
                        user_data[f'{score_col}_change'] = user_data[score_col].diff()
                        user_data[f'{score_col}_trend'] = user_data[f'{score_col}_change'].rolling(3).mean()
                
                # Update main dataframe
                df.loc[user_mask, user_data.columns] = user_data
        
        # Calculate risk categories
        df['depression_risk'] = df.get('phq9_score', 0).apply(self._categorize_depression_risk)
        df['anxiety_risk'] = df.get('gad7_score', 0).apply(self._categorize_anxiety_risk)
        df['stress_risk'] = df.get('pss10_score', 0).apply(self._categorize_stress_risk)
        
        # Overall risk score
        df['overall_risk'] = (
            df.get('phq9_score', 0) * 0.4 + 
            df.get('gad7_score', 0) * 0.3 + 
            df.get('pss10_score', 0) * 0.3
        )
        
        return df
    
    def _categorize_depression_risk(self, score: float) -> str:
        """Categorize depression risk based on PHQ-9 score"""
        if score < 5: return 'minimal'
        elif score < 10: return 'mild'
        elif score < 15: return 'moderate'
        elif score < 20: return 'moderately_severe'
        else: return 'severe'
    
    def _categorize_anxiety_risk(self, score: float) -> str:
        """Categorize anxiety risk based on GAD-7 score"""
        if score < 5: return 'minimal'
        elif score < 10: return 'mild'
        elif score < 15: return 'moderate'
        else: return 'severe'
    
    def _categorize_stress_risk(self, score: float) -> str:
        """Categorize stress risk based on PSS-10 score"""
        if score < 14: return 'low'
        elif score < 26: return 'moderate'
        else: return 'high'
    
    def detect_anomalies(self, df: pd.DataFrame) -> List[AnalyticsInsight]:
        """
        Detect anomalies in user behavior and scores
        """
        insights = []
        
        if df.empty or len(df) < 10:
            return insights
        
        try:
            # Prepare features for anomaly detection
            feature_cols = ['phq9_score', 'gad7_score', 'pss10_score', 
                          'session_duration', 'completion_rate']
            
            available_cols = [col for col in feature_cols if col in df.columns]
            if len(available_cols) < 3:
                return insights
            
            features = df[available_cols].fillna(0)
            
            # Fit anomaly detector
            features_scaled = self.scaler.fit_transform(features)
            anomalies = self.anomaly_detector.fit_predict(features_scaled)
            
            # Identify anomalous records
            anomaly_indices = np.where(anomalies == -1)[0]
            
            for idx in anomaly_indices:
                row = df.iloc[idx]
                
                # Determine severity based on scores
                severity = 'medium'
                if any(row.get(col, 0) > 15 for col in ['phq9_score', 'gad7_score']):
                    severity = 'high'
                if row.get('crisis_indicators', 0) > 0:
                    severity = 'critical'
                
                insight = AnalyticsInsight(
                    insight_type='anomaly',
                    severity=severity,
                    title='Phát hiện bất thường trong dữ liệu',
                    description=f'Phát hiện pattern bất thường cho user {row.get("user_id", "unknown")} vào {row.get("timestamp", "unknown")}',
                    recommendations=[
                        'Theo dõi sát sao user này',
                        'Cân nhắc can thiệp proactive',
                        'Kiểm tra lại kết quả assessment'
                    ],
                    confidence=0.7,
                    data_points=len(df),
                    timestamp=datetime.now()
                )
                insights.append(insight)
        
        except Exception as e:
            self.logger.error(f"Error in anomaly detection: {e}")
        
        return insights
    
    def predict_risk_trends(self, df: pd.DataFrame) -> List[AnalyticsInsight]:
        """
        Predict future risk trends using machine learning
        """
        insights = []
        
        if df.empty or len(df) < 20:
            return insights
        
        try:
            # Group by user for trend analysis
            for user_id in df['user_id'].unique():
                user_data = df[df['user_id'] == user_id].copy()
                
                if len(user_data) < 5:
                    continue
                
                user_data = user_data.sort_values('timestamp')
                
                # Calculate trend for each score
                trend_insights = self._analyze_user_trends(user_id, user_data)
                insights.extend(trend_insights)
        
        except Exception as e:
            self.logger.error(f"Error in trend prediction: {e}")
        
        return insights
    
    def _analyze_user_trends(self, user_id: str, user_data: pd.DataFrame) -> List[AnalyticsInsight]:
        """
        Analyze trends for individual user
        """
        insights = []
        
        score_columns = ['phq9_score', 'gad7_score', 'pss10_score']
        
        for score_col in score_columns:
            if score_col not in user_data.columns:
                continue
            
            scores = user_data[score_col].fillna(0)
            if len(scores) < 3:
                continue
            
            # Calculate trend
            x = np.arange(len(scores))
            trend = np.polyfit(x, scores, 1)[0]  # Linear trend
            
            latest_score = scores.iloc[-1]
            score_type = score_col.replace('_score', '')
            
            # Determine insight based on trend and latest score
            if trend > 0.5 and latest_score > 10:  # Worsening trend
                severity = 'high' if latest_score > 15 else 'medium'
                
                insight = AnalyticsInsight(
                    insight_type='trend_warning',
                    severity=severity,
                    title=f'Xu hướng xấu đi - {score_type.upper()}',
                    description=f'User {user_id} có xu hướng tăng điểm {score_type} (trend: +{trend:.2f})',
                    recommendations=[
                        'Tăng cường theo dõi user này',
                        'Đề xuất can thiệp sớm',
                        'Liên hệ với chuyên gia nếu cần'
                    ],
                    confidence=0.8,
                    data_points=len(scores),
                    timestamp=datetime.now()
                )
                insights.append(insight)
                
            elif trend < -0.5 and latest_score > 5:  # Improving trend
                insight = AnalyticsInsight(
                    insight_type='improvement',
                    severity='low',
                    title=f'Xu hướng cải thiện - {score_type.upper()}',
                    description=f'User {user_id} có xu hướng giảm điểm {score_type} (trend: {trend:.2f})',
                    recommendations=[
                        'Tiếp tục duy trì các can thiệp hiện tại',
                        'Khuyến khích user tiếp tục',
                        'Chia sẻ thành công để motivate'
                    ],
                    confidence=0.8,
                    data_points=len(scores),
                    timestamp=datetime.now()
                )
                insights.append(insight)
        
        return insights
    
    def cluster_user_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Cluster users based on behavior patterns
        """
        if df.empty or len(df) < 10:
            return {}
        
        try:
            # Aggregate user features
            user_features = df.groupby('user_id').agg({
                'phq9_score': ['mean', 'std', 'max'],
                'gad7_score': ['mean', 'std', 'max'],
                'pss10_score': ['mean', 'std', 'max'],
                'session_duration': ['mean', 'count'],
                'completion_rate': 'mean',
                'chat_messages': 'sum',
                'crisis_indicators': 'sum',
                'improvement_indicators': 'sum'
            }).fillna(0)
            
            # Flatten column names
            user_features.columns = ['_'.join(col).strip() for col in user_features.columns]
            
            if len(user_features) < 3:
                return {}
            
            # Standardize features
            features_scaled = self.scaler.fit_transform(user_features)
            
            # Determine optimal number of clusters
            n_clusters = min(4, max(2, len(user_features) // 3))
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            
            # Analyze clusters
            cluster_analysis = {}
            for i in range(n_clusters):
                cluster_mask = clusters == i
                cluster_data = user_features[cluster_mask]
                
                # Characterize cluster
                char = self._characterize_cluster(cluster_data, i)
                cluster_analysis[f'cluster_{i}'] = {
                    'size': int(cluster_mask.sum()),
                    'characteristics': char,
                    'users': user_features.index[cluster_mask].tolist()
                }
            
            return {
                'clusters': cluster_analysis,
                'total_users': len(user_features),
                'n_clusters': n_clusters
            }
            
        except Exception as e:
            self.logger.error(f"Error in clustering: {e}")
            return {}
    
    def _characterize_cluster(self, cluster_data: pd.DataFrame, cluster_id: int) -> Dict[str, Any]:
        """
        Characterize a user cluster
        """
        if cluster_data.empty:
            return {}
        
        # Calculate means for key metrics
        depression_mean = cluster_data.get('phq9_score_mean', pd.Series([0])).mean()
        anxiety_mean = cluster_data.get('gad7_score_mean', pd.Series([0])).mean()
        stress_mean = cluster_data.get('pss10_score_mean', pd.Series([0])).mean()
        engagement = cluster_data.get('session_duration_count', pd.Series([0])).mean()
        
        # Determine cluster type
        if depression_mean > 15 or anxiety_mean > 15:
            cluster_type = 'High Risk'
            recommendations = [
                'Cần can thiệp chuyên sâu',
                'Theo dõi sát sao',
                'Kết nối với chuyên gia'
            ]
        elif depression_mean > 10 or anxiety_mean > 10:
            cluster_type = 'Moderate Risk'
            recommendations = [
                'Tăng cường hỗ trợ',
                'Cung cấp resources phù hợp',
                'Theo dõi định kỳ'
            ]
        elif engagement > 10:
            cluster_type = 'Highly Engaged'
            recommendations = [
                'Duy trì engagement',
                'Tận dụng để peer support',
                'Chia sẻ success stories'
            ]
        else:
            cluster_type = 'Low Risk'
            recommendations = [
                'Maintenance mode',
                'Occasional check-ins',
                'Prevention focus'
            ]
        
        return {
            'type': cluster_type,
            'depression_avg': round(depression_mean, 2),
            'anxiety_avg': round(anxiety_mean, 2),
            'stress_avg': round(stress_mean, 2),
            'engagement_level': round(engagement, 2),
            'recommendations': recommendations
        }
    
    def generate_population_insights(self, df: pd.DataFrame) -> List[AnalyticsInsight]:
        """
        Generate population-level insights
        """
        insights = []
        
        if df.empty:
            return insights
        
        try:
            # Overall statistics
            total_users = df['user_id'].nunique()
            total_assessments = len(df)
            avg_depression = df.get('phq9_score', pd.Series([0])).mean()
            avg_anxiety = df.get('gad7_score', pd.Series([0])).mean()
            
            # High risk users
            high_risk_depression = (df.get('phq9_score', 0) >= 15).sum()
            high_risk_anxiety = (df.get('gad7_score', 0) >= 15).sum()
            
            crisis_rate = df.get('crisis_indicators', 0).sum() / total_assessments if total_assessments > 0 else 0
            improvement_rate = df.get('improvement_indicators', 0).sum() / total_assessments if total_assessments > 0 else 0
            
            # Population insight
            severity = 'medium'
            if crisis_rate > 0.1:  # More than 10% crisis indicators
                severity = 'high'
            elif improvement_rate > 0.3:  # More than 30% showing improvement
                severity = 'low'
            
            insight = AnalyticsInsight(
                insight_type='population_summary',
                severity=severity,
                title='Tổng quan tình hình sức khỏe tâm thần',
                description=f"""
                📊 Thống kê tổng quan:
                • Tổng users: {total_users}
                • Tổng assessments: {total_assessments}
                • Điểm trầm cảm trung bình: {avg_depression:.1f}/27
                • Điểm lo âu trung bình: {avg_anxiety:.1f}/21
                • Tỷ lệ high-risk depression: {high_risk_depression/total_assessments*100:.1f}%
                • Tỷ lệ high-risk anxiety: {high_risk_anxiety/total_assessments*100:.1f}%
                • Tỷ lệ crisis indicators: {crisis_rate*100:.1f}%
                • Tỷ lệ improvement: {improvement_rate*100:.1f}%
                """,
                recommendations=[
                    'Tập trung vào early intervention',
                    'Tăng cường preventive programs',
                    'Optimize resource allocation',
                    'Monitor high-risk groups closely'
                ],
                confidence=0.9,
                data_points=total_assessments,
                timestamp=datetime.now()
            )
            insights.append(insight)
            
        except Exception as e:
            self.logger.error(f"Error generating population insights: {e}")
        
        return insights

def create_advanced_analytics_dashboard():
    """
    Create advanced analytics dashboard
    """
    st.title("📊 Advanced Analytics Dashboard")
    st.markdown("---")
    
    # Initialize analytics engine
    if 'analytics_engine' not in st.session_state:
        st.session_state.analytics_engine = AdvancedAnalytics()
    
    analytics = st.session_state.analytics_engine
    
    # Load data
    with st.spinner("🔄 Đang tải và phân tích dữ liệu..."):
        df = analytics.load_user_data()
    
    if df.empty:
        st.warning("📭 Không có dữ liệu để phân tích")
        return
    
    # Analytics tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", 
        "🚨 Anomaly Detection", 
        "📊 Trend Analysis", 
        "👥 User Clustering", 
        "🎯 Insights"
    ])
    
    with tab1:
        create_overview_dashboard(df)
    
    with tab2:
        create_anomaly_dashboard(df, analytics)
    
    with tab3:
        create_trend_dashboard(df, analytics)
    
    with tab4:
        create_clustering_dashboard(df, analytics)
    
    with tab5:
        create_insights_dashboard(df, analytics)

def create_overview_dashboard(df: pd.DataFrame):
    """
    Create overview dashboard
    """
    st.subheader("📈 Tổng quan Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = df['user_id'].nunique()
        st.metric("👥 Tổng Users", total_users)
    
    with col2:
        total_assessments = len(df)
        st.metric("📋 Tổng Assessments", total_assessments)
    
    with col3:
        avg_depression = df.get('phq9_score', pd.Series([0])).mean()
        st.metric("😔 Avg Depression", f"{avg_depression:.1f}")
    
    with col4:
        avg_anxiety = df.get('gad7_score', pd.Series([0])).mean()
        st.metric("😰 Avg Anxiety", f"{avg_anxiety:.1f}")
    
    # Time series charts
    st.markdown("### 📊 Biểu đồ theo thời gian")
    
    if 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_avg = df.groupby('date').agg({
            'phq9_score': 'mean',
            'gad7_score': 'mean',
            'pss10_score': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['phq9_score'],
            mode='lines+markers',
            name='Depression (PHQ-9)',
            line=dict(color='#FF6B6B')
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['gad7_score'],
            mode='lines+markers',
            name='Anxiety (GAD-7)',
            line=dict(color='#4ECDC4')
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['pss10_score'],
            mode='lines+markers',
            name='Stress (PSS-10)',
            line=dict(color='#45B7D1')
        ))
        
        fig.update_layout(
            title="Xu hướng điểm số trung bình theo ngày",
            xaxis_title="Ngày",
            yaxis_title="Điểm số",
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution
        if 'depression_risk' in df.columns:
            risk_counts = df['depression_risk'].value_counts()
            
            fig = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Phân bổ mức độ rủi ro trầm cảm"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Score histogram
        if 'phq9_score' in df.columns:
            fig = px.histogram(
                df,
                x='phq9_score',
                title="Phân bổ điểm PHQ-9",
                nbins=20
            )
            st.plotly_chart(fig, use_container_width=True)

def create_anomaly_dashboard(df: pd.DataFrame, analytics: AdvancedAnalytics):
    """
    Create anomaly detection dashboard
    """
    st.subheader("🚨 Anomaly Detection")
    
    with st.spinner("🔍 Đang phát hiện anomalies..."):
        anomaly_insights = analytics.detect_anomalies(df)
    
    if anomaly_insights:
        st.success(f"🔍 Phát hiện {len(anomaly_insights)} anomalies")
        
        for insight in anomaly_insights:
            severity_color = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🟠',
                'critical': '🔴'
            }
            
            with st.expander(f"{severity_color.get(insight.severity, '⚪')} {insight.title}"):
                st.write(f"**Mô tả:** {insight.description}")
                st.write(f"**Độ tin cậy:** {insight.confidence:.1%}")
                st.write(f"**Data points:** {insight.data_points}")
                
                st.write("**Khuyến nghị:**")
                for rec in insight.recommendations:
                    st.write(f"• {rec}")
    else:
        st.info("✅ Không phát hiện anomaly nào đáng ngại")

def create_trend_dashboard(df: pd.DataFrame, analytics: AdvancedAnalytics):
    """
    Create trend analysis dashboard
    """
    st.subheader("📊 Trend Analysis")
    
    with st.spinner("📈 Đang phân tích trends..."):
        trend_insights = analytics.predict_risk_trends(df)
    
    if trend_insights:
        col1, col2 = st.columns(2)
        
        warnings = [i for i in trend_insights if i.insight_type == 'trend_warning']
        improvements = [i for i in trend_insights if i.insight_type == 'improvement']
        
        with col1:
            st.markdown("### ⚠️ Cảnh báo xu hướng")
            if warnings:
                for warning in warnings[:5]:  # Show top 5
                    with st.expander(f"🔴 {warning.title}"):
                        st.write(warning.description)
                        for rec in warning.recommendations:
                            st.write(f"• {rec}")
            else:
                st.success("✅ Không có cảnh báo xu hướng")
        
        with col2:
            st.markdown("### ✅ Cải thiện")
            if improvements:
                for improvement in improvements[:5]:  # Show top 5
                    with st.expander(f"🟢 {improvement.title}"):
                        st.write(improvement.description)
                        for rec in improvement.recommendations:
                            st.write(f"• {rec}")
            else:
                st.info("ℹ️ Chưa phát hiện cải thiện đáng kể")

def create_clustering_dashboard(df: pd.DataFrame, analytics: AdvancedAnalytics):
    """
    Create user clustering dashboard
    """
    st.subheader("👥 User Clustering")
    
    with st.spinner("🔄 Đang phân nhóm users..."):
        cluster_results = analytics.cluster_user_patterns(df)
    
    if cluster_results and 'clusters' in cluster_results:
        st.success(f"📊 Phân thành {cluster_results['n_clusters']} nhóm từ {cluster_results['total_users']} users")
        
        # Cluster overview
        cluster_data = []
        for cluster_id, cluster_info in cluster_results['clusters'].items():
            cluster_data.append({
                'Nhóm': cluster_id.replace('cluster_', 'Nhóm '),
                'Số lượng': cluster_info['size'],
                'Loại': cluster_info['characteristics'].get('type', 'Unknown'),
                'Avg Depression': cluster_info['characteristics'].get('depression_avg', 0),
                'Avg Anxiety': cluster_info['characteristics'].get('anxiety_avg', 0),
                'Engagement': cluster_info['characteristics'].get('engagement_level', 0)
            })
        
        cluster_df = pd.DataFrame(cluster_data)
        st.dataframe(cluster_df, use_container_width=True)
        
        # Detailed cluster analysis
        for cluster_id, cluster_info in cluster_results['clusters'].items():
            with st.expander(f"📊 Chi tiết {cluster_id.replace('cluster_', 'Nhóm ')}"):
                char = cluster_info['characteristics']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("👥 Số users", cluster_info['size'])
                    st.metric("😔 Avg Depression", f"{char.get('depression_avg', 0):.1f}")
                    st.metric("😰 Avg Anxiety", f"{char.get('anxiety_avg', 0):.1f}")
                
                with col2:
                    st.metric("📈 Engagement", f"{char.get('engagement_level', 0):.1f}")
                    st.write(f"**Loại nhóm:** {char.get('type', 'Unknown')}")
                
                st.write("**Khuyến nghị:**")
                for rec in char.get('recommendations', []):
                    st.write(f"• {rec}")

def create_insights_dashboard(df: pd.DataFrame, analytics: AdvancedAnalytics):
    """
    Create insights dashboard
    """
    st.subheader("🎯 Insights & Recommendations")
    
    with st.spinner("🧠 Đang tạo insights..."):
        population_insights = analytics.generate_population_insights(df)
    
    if population_insights:
        for insight in population_insights:
            st.markdown(f"### {insight.title}")
            st.markdown(insight.description)
            
            st.markdown("**Khuyến nghị hành động:**")
            for rec in insight.recommendations:
                st.markdown(f"• {rec}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Độ tin cậy", f"{insight.confidence:.1%}")
            with col2:
                st.metric("Data points", insight.data_points)

if __name__ == "__main__":
    # Check dependencies
    try:
        import sklearn
        create_advanced_analytics_dashboard()
    except ImportError as e:
        st.error(f"""
        🚫 **Thiếu dependencies cho Advanced Analytics**
        
        Cần cài đặt: `{e.name}`
        
        Chạy lệnh:
        ```bash
        pip install scikit-learn==1.3.0
        ```
        """)
