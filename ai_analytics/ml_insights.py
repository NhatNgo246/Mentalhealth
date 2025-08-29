"""
🧠 AI & Machine Learning Insights Module
Advanced analytics và AI-powered recommendations cho SOULFRIEND V2.0
"""

import pandas as pd
import numpy as np
import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

# ML Libraries
try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️ ML libraries not available. Install: pip install scikit-learn")

class MentalHealthMLInsights:
    """
    Machine Learning insights engine cho mental health data
    """
    
    def __init__(self, research_data_path: str = "/workspaces/Mentalhealth/research_data"):
        self.data_path = research_data_path
        self.db_path = os.path.join(research_data_path, "research.db")
        self.logger = self._setup_logger()
        
        # ML Models storage
        self.models = {}
        self.scalers = {}
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for ML operations"""
        logger = logging.getLogger("MLInsights")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def load_assessment_data(self) -> pd.DataFrame:
        """
        Load và clean assessment data từ database
        """
        try:
            if not os.path.exists(self.db_path):
                self.logger.warning(f"Database not found: {self.db_path}")
                return pd.DataFrame()
                
            conn = sqlite3.connect(self.db_path)
            
            # Load assessment results
            query = """
            SELECT * FROM assessment_results 
            WHERE created_at >= datetime('now', '-30 days')
            ORDER BY created_at DESC
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                self.logger.info("No recent assessment data found")
                return df
                
            # Parse JSON scores
            if 'scores' in df.columns:
                scores_expanded = pd.json_normalize(df['scores'].apply(json.loads))
                df = pd.concat([df.drop('scores', axis=1), scores_expanded], axis=1)
            
            self.logger.info(f"Loaded {len(df)} assessment records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading assessment data: {e}")
            return pd.DataFrame()
    
    def analyze_risk_patterns(self, df: pd.DataFrame) -> Dict:
        """
        Phân tích patterns trong risk levels
        """
        if df.empty or not ML_AVAILABLE:
            return {"error": "No data or ML libraries not available"}
        
        try:
            # Extract risk-related features
            risk_features = []
            for col in df.columns:
                if any(keyword in col.lower() for keyword in 
                      ['phq9', 'gad7', 'dass21', 'score', 'severity']):
                    if df[col].dtype in ['int64', 'float64']:
                        risk_features.append(col)
            
            if len(risk_features) < 2:
                return {"error": "Insufficient risk features for analysis"}
            
            # Prepare data for clustering
            feature_data = df[risk_features].fillna(0)
            
            # Standardize features
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(feature_data)
            
            # K-means clustering để identify risk groups
            n_clusters = min(4, len(df) // 5) if len(df) >= 10 else 2
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(scaled_data)
            
            # Analyze clusters
            df['risk_cluster'] = clusters
            cluster_analysis = {}
            
            for cluster_id in range(n_clusters):
                cluster_data = df[df['risk_cluster'] == cluster_id]
                cluster_analysis[f'cluster_{cluster_id}'] = {
                    'size': len(cluster_data),
                    'percentage': len(cluster_data) / len(df) * 100,
                    'avg_scores': {feat: float(cluster_data[feat].mean()) 
                                 for feat in risk_features if feat in cluster_data.columns},
                    'risk_level': self._determine_cluster_risk_level(cluster_data, risk_features)
                }
            
            # Store models
            self.models['risk_clustering'] = kmeans
            self.scalers['risk_features'] = scaler
            
            return {
                'cluster_analysis': cluster_analysis,
                'total_assessments': len(df),
                'risk_features_used': risk_features,
                'model_stored': True
            }
            
        except Exception as e:
            self.logger.error(f"Error in risk pattern analysis: {e}")
            return {"error": str(e)}
    
    def _determine_cluster_risk_level(self, cluster_data: pd.DataFrame, features: List[str]) -> str:
        """Determine risk level for a cluster based on average scores"""
        avg_scores = {feat: cluster_data[feat].mean() for feat in features if feat in cluster_data.columns}
        
        # Simple heuristic based on common mental health assessment ranges
        high_risk_indicators = 0
        total_indicators = 0
        
        for feat, score in avg_scores.items():
            if 'phq9' in feat.lower():
                total_indicators += 1
                if score >= 15:  # Severe depression
                    high_risk_indicators += 1
                elif score >= 10:  # Moderate depression
                    high_risk_indicators += 0.5
            elif 'gad7' in feat.lower():
                total_indicators += 1
                if score >= 15:  # Severe anxiety
                    high_risk_indicators += 1
                elif score >= 10:  # Moderate anxiety
                    high_risk_indicators += 0.5
        
        if total_indicators == 0:
            return "unknown"
        
        risk_ratio = high_risk_indicators / total_indicators
        
        if risk_ratio >= 0.7:
            return "high_risk"
        elif risk_ratio >= 0.4:
            return "moderate_risk"
        else:
            return "low_risk"
    
    def generate_trends_analysis(self, df: pd.DataFrame) -> Dict:
        """
        Phân tích trends theo thời gian
        """
        if df.empty:
            return {"error": "No data available"}
        
        try:
            # Convert timestamp column
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['date'] = df['created_at'].dt.date
                df['hour'] = df['created_at'].dt.hour
                df['day_of_week'] = df['created_at'].dt.day_name()
            else:
                return {"error": "No timestamp column found"}
            
            # Daily trends
            daily_counts = df.groupby('date').size()
            
            # Hourly patterns
            hourly_patterns = df.groupby('hour').size()
            
            # Day of week patterns
            weekly_patterns = df.groupby('day_of_week').size()
            
            # Risk trends over time (if risk scores available)
            risk_trends = {}
            for col in df.columns:
                if any(keyword in col.lower() for keyword in ['phq9', 'gad7', 'total_score']):
                    if df[col].dtype in ['int64', 'float64']:
                        daily_avg = df.groupby('date')[col].mean()
                        risk_trends[col] = {
                            'daily_averages': daily_avg.to_dict(),
                            'trend_direction': 'increasing' if daily_avg.iloc[-1] > daily_avg.iloc[0] else 'decreasing'
                        }
            
            return {
                'daily_assessment_counts': daily_counts.to_dict(),
                'peak_hour': int(hourly_patterns.idxmax()),
                'peak_day': weekly_patterns.idxmax(),
                'hourly_distribution': hourly_patterns.to_dict(),
                'weekly_distribution': weekly_patterns.to_dict(),
                'risk_score_trends': risk_trends,
                'analysis_period_days': (df['created_at'].max() - df['created_at'].min()).days
            }
            
        except Exception as e:
            self.logger.error(f"Error in trends analysis: {e}")
            return {"error": str(e)}
    
    def predict_risk_category(self, assessment_scores: Dict) -> Dict:
        """
        Predict risk category cho một assessment mới
        """
        if not ML_AVAILABLE or 'risk_clustering' not in self.models:
            return {"error": "ML model not available or not trained"}
        
        try:
            # Prepare features
            feature_vector = []
            model_features = ['phq9_total_score', 'gad7_total_score']  # Simplified for example
            
            for feat in model_features:
                feature_vector.append(assessment_scores.get(feat, 0))
            
            # Scale features
            if 'risk_features' in self.scalers:
                scaled_features = self.scalers['risk_features'].transform([feature_vector])
            else:
                scaled_features = [feature_vector]
            
            # Predict cluster
            cluster = self.models['risk_clustering'].predict(scaled_features)[0]
            
            # Get risk level for cluster (this would come from training data analysis)
            risk_levels = {0: "low_risk", 1: "moderate_risk", 2: "high_risk", 3: "very_high_risk"}
            predicted_risk = risk_levels.get(cluster, "unknown")
            
            return {
                'predicted_cluster': int(cluster),
                'predicted_risk_level': predicted_risk,
                'confidence': 0.75,  # Placeholder - would calculate based on cluster distances
                'recommendations': self._get_risk_recommendations(predicted_risk)
            }
            
        except Exception as e:
            self.logger.error(f"Error in risk prediction: {e}")
            return {"error": str(e)}
    
    def _get_risk_recommendations(self, risk_level: str) -> List[str]:
        """Get recommendations based on risk level"""
        recommendations = {
            "low_risk": [
                "Tiếp tục duy trì các hoạt động tích cực",
                "Thực hành mindfulness hàng ngày",
                "Duy trì lối sống lành mạnh"
            ],
            "moderate_risk": [
                "Cân nhắc tham khảo ý kiến chuyên gia",
                "Tăng cường hoạt động thể chất",
                "Kết nối với bạn bè và gia đình",
                "Thực hành các kỹ thuật giảm stress"
            ],
            "high_risk": [
                "Nên tham khảo ý kiến bác sĩ chuyên khoa",
                "Tìm kiếm hỗ trợ từ người thân",
                "Cân nhắc liệu pháp tâm lý",
                "Tránh các yếu tố gây stress"
            ],
            "very_high_risk": [
                "Cần được tư vấn chuyên nghiệp ngay lập tức",
                "Liên hệ hotline hỗ trợ tâm lý",
                "Không nên ở một mình",
                "Tìm kiếm sự giúp đỡ y tế"
            ]
        }
        
        return recommendations.get(risk_level, ["Tham khảo ý kiến chuyên gia"])
    
    def generate_insights_report(self) -> Dict:
        """
        Tạo báo cáo insights tổng hợp
        """
        try:
            # Load data
            df = self.load_assessment_data()
            
            if df.empty:
                return {"error": "No data available for analysis"}
            
            # Run all analyses
            risk_analysis = self.analyze_risk_patterns(df)
            trends_analysis = self.generate_trends_analysis(df)
            
            # Generate summary insights
            summary_insights = []
            
            if 'cluster_analysis' in risk_analysis:
                high_risk_clusters = [k for k, v in risk_analysis['cluster_analysis'].items() 
                                    if v['risk_level'] in ['high_risk', 'very_high_risk']]
                if high_risk_clusters:
                    high_risk_percentage = sum(risk_analysis['cluster_analysis'][k]['percentage'] 
                                             for k in high_risk_clusters)
                    summary_insights.append(f"🚨 {high_risk_percentage:.1f}% người dùng thuộc nhóm nguy cơ cao")
            
            if 'peak_hour' in trends_analysis:
                summary_insights.append(f"⏰ Giờ cao điểm đánh giá: {trends_analysis['peak_hour']}:00")
            
            if 'peak_day' in trends_analysis:
                summary_insights.append(f"📅 Ngày trong tuần phổ biến nhất: {trends_analysis['peak_day']}")
            
            return {
                'generated_at': datetime.now().isoformat(),
                'data_summary': {
                    'total_assessments': len(df),
                    'analysis_period_days': (df['created_at'].max() - df['created_at'].min()).days if 'created_at' in df.columns else 0,
                    'unique_sessions': df['session_id'].nunique() if 'session_id' in df.columns else 0
                },
                'risk_analysis': risk_analysis,
                'trends_analysis': trends_analysis,
                'summary_insights': summary_insights,
                'ml_status': {
                    'ml_available': ML_AVAILABLE,
                    'models_trained': list(self.models.keys()),
                    'scalers_available': list(self.scalers.keys())
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating insights report: {e}")
            return {"error": str(e)}

# Utility functions for external use
def get_ml_insights() -> MentalHealthMLInsights:
    """Factory function to create ML insights instance"""
    return MentalHealthMLInsights()

def quick_risk_assessment(phq9_score: int, gad7_score: int) -> Dict:
    """Quick risk assessment based on standard scores"""
    ml_engine = MentalHealthMLInsights()
    return ml_engine.predict_risk_category({
        'phq9_total_score': phq9_score,
        'gad7_total_score': gad7_score
    })

if __name__ == "__main__":
    # Test the ML insights
    ml_insights = MentalHealthMLInsights()
    report = ml_insights.generate_insights_report()
    print(json.dumps(report, indent=2, default=str))
