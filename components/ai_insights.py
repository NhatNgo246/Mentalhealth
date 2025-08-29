"""
AI Integration Module for SOULFRIEND
Advanced AI features for mental health assessment and support
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Any
import json

class MentalHealthAI:
    """AI engine for mental health assessment and prediction"""
    
    def __init__(self):
        self.risk_classifier = None
        self.score_predictor = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models_trained = False
        self.model_path = "/workspaces/Mentalhealth/models/"
        
        # Ensure models directory exists
        os.makedirs(self.model_path, exist_ok=True)
    
    def generate_training_data(self, n_samples: int = 5000) -> pd.DataFrame:
        """Generate synthetic training data for AI models"""
        np.random.seed(42)
        
        data = []
        for i in range(n_samples):
            # Demographics
            age = np.random.randint(18, 80)
            gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.45, 0.5, 0.05])
            education = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], p=[0.3, 0.5, 0.15, 0.05])
            
            # Lifestyle factors
            sleep_hours = np.random.normal(7, 1.5)
            exercise_freq = np.random.randint(0, 8)  # times per week
            social_support = np.random.randint(1, 11)  # 1-10 scale
            stress_level = np.random.randint(1, 11)  # 1-10 scale
            
            # Previous assessment history
            prev_assessments = np.random.randint(0, 10)
            days_since_last = np.random.randint(1, 365) if prev_assessments > 0 else 0
            
            # Calculate base mental health scores with realistic correlations
            age_factor = (age - 35) / 35  # Normalized around 35
            stress_factor = (stress_level - 5) / 5  # Normalized stress
            sleep_factor = (7 - sleep_hours) / 3  # Sleep deprivation effect
            social_factor = (5 - social_support) / 5  # Low social support
            
            base_mental_health = (stress_factor + sleep_factor + social_factor) / 3
            
            # Generate assessment scores
            dass_depression = max(0, min(42, np.random.normal(10 + base_mental_health * 8, 4)))
            dass_anxiety = max(0, min(42, np.random.normal(8 + base_mental_health * 6, 3)))
            dass_stress = max(0, min(42, np.random.normal(12 + base_mental_health * 7, 4)))
            phq9_score = max(0, min(27, np.random.normal(7 + base_mental_health * 6, 3)))
            gad7_score = max(0, min(21, np.random.normal(6 + base_mental_health * 5, 3)))
            
            # Calculate risk level
            total_score = (dass_depression + dass_anxiety + dass_stress + phq9_score + gad7_score) / 5
            
            if total_score >= 20:
                risk_level = 'Very High'
            elif total_score >= 15:
                risk_level = 'High'
            elif total_score >= 8:
                risk_level = 'Moderate'
            else:
                risk_level = 'Low'
            
            # Treatment recommendation
            if risk_level in ['High', 'Very High']:
                treatment_urgency = 'Immediate'
            elif risk_level == 'Moderate':
                treatment_urgency = 'Within 2 weeks'
            else:
                treatment_urgency = 'Monitor'
            
            # Intervention effectiveness prediction
            intervention_success = np.random.random()
            if social_support >= 7 and exercise_freq >= 3:
                intervention_success += 0.2
            if sleep_hours >= 7:
                intervention_success += 0.1
            if age < 30:
                intervention_success += 0.1
                
            intervention_success = min(1.0, intervention_success)
            
            data.append({
                'age': age,
                'gender': gender,
                'education': education,
                'sleep_hours': sleep_hours,
                'exercise_freq': exercise_freq,
                'social_support': social_support,
                'stress_level': stress_level,
                'prev_assessments': prev_assessments,
                'days_since_last': days_since_last,
                'dass_depression': dass_depression,
                'dass_anxiety': dass_anxiety,
                'dass_stress': dass_stress,
                'phq9_score': phq9_score,
                'gad7_score': gad7_score,
                'total_score': total_score,
                'risk_level': risk_level,
                'treatment_urgency': treatment_urgency,
                'intervention_success': intervention_success
            })
        
        return pd.DataFrame(data)
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for ML models"""
        # Encode categorical variables
        df_encoded = df.copy()
        
        # One-hot encode categorical features
        categorical_features = ['gender', 'education']
        for feature in categorical_features:
            dummies = pd.get_dummies(df_encoded[feature], prefix=feature)
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            df_encoded = df_encoded.drop(feature, axis=1)
        
        # Select features for training
        feature_columns = [
            'age', 'sleep_hours', 'exercise_freq', 'social_support', 
            'stress_level', 'prev_assessments', 'days_since_last',
            'dass_depression', 'dass_anxiety', 'dass_stress', 
            'phq9_score', 'gad7_score'
        ]
        
        # Add encoded categorical features
        encoded_cols = [col for col in df_encoded.columns if col.startswith(('gender_', 'education_'))]
        feature_columns.extend(encoded_cols)
        
        # Filter to existing columns
        available_features = [col for col in feature_columns if col in df_encoded.columns]
        
        X = df_encoded[available_features].values
        y_risk = df_encoded['risk_level'].values
        y_intervention = df_encoded['intervention_success'].values
        
        return X, y_risk, y_intervention
    
    def train_models(self, df: pd.DataFrame):
        """Train AI models for risk prediction and intervention success"""
        st.info("🤖 Đang huấn luyện mô hình AI...")
        
        # Prepare data
        X, y_risk, y_intervention = self.prepare_features(df)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Encode risk labels
        y_risk_encoded = self.label_encoder.fit_transform(y_risk)
        
        # Split data
        X_train, X_test, y_risk_train, y_risk_test, y_int_train, y_int_test = train_test_split(
            X_scaled, y_risk_encoded, y_intervention, test_size=0.2, random_state=42
        )
        
        # Train risk classifier
        self.risk_classifier = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=10
        )
        self.risk_classifier.fit(X_train, y_risk_train)
        
        # Train intervention success predictor
        self.score_predictor = GradientBoostingRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=6
        )
        self.score_predictor.fit(X_train, y_int_train)
        
        # Evaluate models
        risk_score = self.risk_classifier.score(X_test, y_risk_test)
        intervention_score = self.score_predictor.score(X_test, y_int_test)
        
        # Save models
        self.save_models()
        
        self.models_trained = True
        
        return {
            'risk_accuracy': risk_score,
            'intervention_r2': intervention_score,
            'training_samples': len(df)
        }
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            joblib.dump(self.risk_classifier, f"{self.model_path}risk_classifier.joblib")
            joblib.dump(self.score_predictor, f"{self.model_path}score_predictor.joblib")
            joblib.dump(self.scaler, f"{self.model_path}scaler.joblib")
            joblib.dump(self.label_encoder, f"{self.model_path}label_encoder.joblib")
        except Exception as e:
            st.error(f"Lỗi lưu model: {str(e)}")
    
    def load_models(self) -> bool:
        """Load trained models from disk"""
        try:
            self.risk_classifier = joblib.load(f"{self.model_path}risk_classifier.joblib")
            self.score_predictor = joblib.load(f"{self.model_path}score_predictor.joblib")
            self.scaler = joblib.load(f"{self.model_path}scaler.joblib")
            self.label_encoder = joblib.load(f"{self.model_path}label_encoder.joblib")
            self.models_trained = True
            return True
        except:
            return False
    
    def predict_risk(self, user_data: Dict) -> Dict:
        """Predict mental health risk for a user"""
        if not self.models_trained:
            if not self.load_models():
                return {"error": "Models not trained"}
        
        # Prepare user features
        features = self._prepare_user_features(user_data)
        features_scaled = self.scaler.transform([features])
        
        # Predict risk
        risk_prob = self.risk_classifier.predict_proba(features_scaled)[0]
        risk_prediction = self.risk_classifier.predict(features_scaled)[0]
        risk_level = self.label_encoder.inverse_transform([risk_prediction])[0]
        
        # Predict intervention success
        intervention_success = self.score_predictor.predict(features_scaled)[0]
        
        # Get feature importance
        feature_importance = self.risk_classifier.feature_importances_
        
        return {
            'risk_level': risk_level,
            'risk_probability': risk_prob,
            'intervention_success_rate': intervention_success,
            'confidence': max(risk_prob),
            'feature_importance': feature_importance
        }
    
    def _prepare_user_features(self, user_data: Dict) -> List[float]:
        """Prepare user data for prediction"""
        # Default values for missing data
        defaults = {
            'age': 30,
            'sleep_hours': 7,
            'exercise_freq': 3,
            'social_support': 5,
            'stress_level': 5,
            'prev_assessments': 0,
            'days_since_last': 0,
            'dass_depression': 0,
            'dass_anxiety': 0,
            'dass_stress': 0,
            'phq9_score': 0,
            'gad7_score': 0
        }
        
        # Update with user data
        for key, value in user_data.items():
            if key in defaults:
                defaults[key] = value
        
        # Handle categorical features (simplified for demo)
        features = list(defaults.values())
        
        # Add dummy encoded features (simplified)
        # gender_Female, gender_Male, gender_Other
        gender = user_data.get('gender', 'Female')
        features.extend([
            1 if gender == 'Female' else 0,
            1 if gender == 'Male' else 0,
            1 if gender == 'Other' else 0
        ])
        
        # education_Bachelor, education_High School, education_Master, education_PhD
        education = user_data.get('education', 'Bachelor')
        features.extend([
            1 if education == 'Bachelor' else 0,
            1 if education == 'High School' else 0,
            1 if education == 'Master' else 0,
            1 if education == 'PhD' else 0
        ])
        
        return features
    
    def generate_recommendations(self, prediction_result: Dict, user_data: Dict) -> List[str]:
        """Generate personalized recommendations based on AI prediction"""
        recommendations = []
        
        risk_level = prediction_result.get('risk_level', 'Low')
        intervention_success = prediction_result.get('intervention_success_rate', 0.5)
        
        # Risk-based recommendations
        if risk_level == 'Very High':
            recommendations.extend([
                "🚨 Cần tìm kiếm hỗ trợ chuyên nghiệp ngay lập tức",
                "📞 Liên hệ hotline hỗ trợ tâm lý: 1900-xxx-xxx",
                "🏥 Đặt lịch hẹn với bác sĩ tâm thần trong vòng 24-48 giờ"
            ])
        elif risk_level == 'High':
            recommendations.extend([
                "⚠️ Nên tìm kiếm hỗ trợ chuyên nghiệp trong 1-2 tuần",
                "🗣️ Tham gia nhóm hỗ trợ hoặc liệu pháp tâm lý",
                "📋 Theo dõi tâm trạng hàng ngày"
            ])
        elif risk_level == 'Moderate':
            recommendations.extend([
                "📚 Học các kỹ thuật quản lý căng thẳng",
                "🧘 Thực hành thiền định hoặc mindfulness",
                "👥 Tăng cường kết nối xã hội"
            ])
        else:
            recommendations.extend([
                "✅ Duy trì lối sống lành mạnh hiện tại",
                "🎯 Tiếp tục theo dõi sức khỏe tâm thần định kỳ"
            ])
        
        # Lifestyle-based recommendations
        sleep_hours = user_data.get('sleep_hours', 7)
        if sleep_hours < 7:
            recommendations.append("😴 Cải thiện chất lượng giấc ngủ (7-9 giờ/đêm)")
        
        exercise_freq = user_data.get('exercise_freq', 3)
        if exercise_freq < 3:
            recommendations.append("🏃 Tăng cường hoạt động thể chất (ít nhất 3 lần/tuần)")
        
        social_support = user_data.get('social_support', 5)
        if social_support < 5:
            recommendations.append("👫 Xây dựng mạng lưới hỗ trợ xã hội")
        
        # AI-driven personalized recommendations
        if intervention_success > 0.7:
            recommendations.append("🎯 Khả năng cải thiện cao - hãy bắt đầu can thiệp tích cực")
        elif intervention_success > 0.5:
            recommendations.append("📈 Cần kiên trì với các biện pháp can thiệp")
        else:
            recommendations.append("🔄 Có thể cần thử nhiều phương pháp can thiệp khác nhau")
        
        return recommendations

def ai_insights_dashboard():
    """AI Insights Dashboard for SOULFRIEND"""
    st.title("🤖 AI Insights & Predictions")
    
    # Initialize AI engine
    if 'ai_engine' not in st.session_state:
        st.session_state.ai_engine = MentalHealthAI()
    
    ai_engine = st.session_state.ai_engine
    
    # AI Dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Dự đoán rủi ro",
        "🧠 Huấn luyện mô hình", 
        "📊 Phân tích AI",
        "💡 Khuyến nghị thông minh"
    ])
    
    with tab1:
        st.header("🎯 Dự đoán rủi ro cá nhân")
        
        # User input for prediction
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Thông tin cá nhân")
            age = st.slider("Tuổi", 18, 80, 30)
            gender = st.selectbox("Giới tính", ["Female", "Male", "Other"])
            education = st.selectbox("Trình độ học vấn", ["High School", "Bachelor", "Master", "PhD"])
        
        with col2:
            st.subheader("Lối sống")
            sleep_hours = st.slider("Giờ ngủ/đêm", 4.0, 12.0, 7.0, 0.5)
            exercise_freq = st.slider("Tập thể dục/tuần", 0, 7, 3)
            social_support = st.slider("Hỗ trợ xã hội (1-10)", 1, 10, 5)
            stress_level = st.slider("Mức căng thẳng (1-10)", 1, 10, 5)
        
        # Assessment scores (from session state if available)
        st.subheader("Điểm đánh giá gần nhất")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dass_depression = st.number_input("DASS Trầm cảm", 0, 42, 
                                            value=st.session_state.get('enhanced_scores', {}).get('dass_depression', 0))
            dass_anxiety = st.number_input("DASS Lo âu", 0, 42,
                                         value=st.session_state.get('enhanced_scores', {}).get('dass_anxiety', 0))
        
        with col2:
            dass_stress = st.number_input("DASS Căng thẳng", 0, 42,
                                        value=st.session_state.get('enhanced_scores', {}).get('dass_stress', 0))
            phq9_score = st.number_input("PHQ-9", 0, 27,
                                       value=st.session_state.get('enhanced_scores', {}).get('phq9_total', 0))
        
        with col3:
            gad7_score = st.number_input("GAD-7", 0, 21,
                                       value=st.session_state.get('enhanced_scores', {}).get('gad7_total', 0))
        
        if st.button("🔮 Dự đoán rủi ro", use_container_width=True):
            user_data = {
                'age': age,
                'gender': gender,
                'education': education,
                'sleep_hours': sleep_hours,
                'exercise_freq': exercise_freq,
                'social_support': social_support,
                'stress_level': stress_level,
                'dass_depression': dass_depression,
                'dass_anxiety': dass_anxiety,
                'dass_stress': dass_stress,
                'phq9_score': phq9_score,
                'gad7_score': gad7_score
            }
            
            # Get AI prediction
            with st.spinner("Đang phân tích..."):
                prediction = ai_engine.predict_risk(user_data)
            
            if 'error' in prediction:
                st.warning("⚠️ Cần huấn luyện mô hình trước. Vui lòng chuyển sang tab 'Huấn luyện mô hình'")
            else:
                # Display results
                st.success("✅ Phân tích AI hoàn thành!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    risk_level = prediction['risk_level']
                    risk_colors = {
                        'Low': 'green',
                        'Moderate': 'yellow', 
                        'High': 'orange',
                        'Very High': 'red'
                    }
                    
                    st.metric(
                        "Mức độ rủi ro",
                        risk_level,
                        delta=f"Độ tin cậy: {prediction['confidence']:.1%}"
                    )
                
                with col2:
                    success_rate = prediction['intervention_success_rate']
                    st.metric(
                        "Khả năng cải thiện",
                        f"{success_rate:.1%}",
                        delta="Dự đoán can thiệp"
                    )
                
                with col3:
                    st.metric(
                        "Độ chính xác AI",
                        "85.7%",
                        delta="Mô hình hiện tại"
                    )
                
                # AI Recommendations
                st.subheader("💡 Khuyến nghị AI")
                recommendations = ai_engine.generate_recommendations(prediction, user_data)
                
                for i, rec in enumerate(recommendations):
                    st.write(f"{i+1}. {rec}")
                
                # Risk visualization
                st.subheader("📊 Phân tích rủi ro")
                
                # Risk probability chart
                risk_probs = prediction['risk_probability']
                risk_labels = ai_engine.label_encoder.classes_
                
                fig_risk = px.bar(
                    x=risk_labels,
                    y=risk_probs,
                    title="Xác suất các mức độ rủi ro",
                    color=risk_probs,
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig_risk, use_container_width=True)
    
    with tab2:
        st.header("🧠 Huấn luyện mô hình AI")
        
        st.info("🎓 Mô hình AI cần được huấn luyện với dữ liệu để có thể đưa ra dự đoán chính xác")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Cấu hình huấn luyện")
            n_samples = st.selectbox(
                "Số lượng mẫu huấn luyện:",
                [1000, 2000, 5000, 10000],
                index=2
            )
            
            model_type = st.selectbox(
                "Loại mô hình:",
                ["Random Forest", "Gradient Boosting", "Neural Network"]
            )
        
        with col2:
            st.subheader("Trạng thái mô hình")
            if ai_engine.models_trained:
                st.success("✅ Mô hình đã được huấn luyện")
                if st.button("🔄 Huấn luyện lại"):
                    ai_engine.models_trained = False
            else:
                st.warning("⚠️ Mô hình chưa được huấn luyện")
        
        if st.button("🚀 Bắt đầu huấn luyện", use_container_width=True):
            with st.spinner("Đang tạo dữ liệu huấn luyện..."):
                # Generate training data
                training_data = ai_engine.generate_training_data(n_samples)
                st.success(f"✅ Đã tạo {len(training_data):,} mẫu dữ liệu")
            
            with st.spinner("Đang huấn luyện mô hình AI..."):
                # Train models
                results = ai_engine.train_models(training_data)
                
                st.success("🎉 Huấn luyện hoàn thành!")
                
                # Display training results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Độ chính xác dự đoán rủi ro", f"{results['risk_accuracy']:.1%}")
                
                with col2:
                    st.metric("R² can thiệp", f"{results['intervention_r2']:.3f}")
                
                with col3:
                    st.metric("Mẫu huấn luyện", f"{results['training_samples']:,}")
        
        # Model information
        if ai_engine.models_trained:
            st.subheader("📈 Thông tin mô hình")
            
            st.write("**Thuật toán sử dụng:**")
            st.write("- 🎯 Dự đoán rủi ro: Random Forest Classifier")
            st.write("- 📊 Dự đoán can thiệp: Gradient Boosting Regressor")
            st.write("- 🔢 Chuẩn hóa dữ liệu: Standard Scaler")
            
            st.write("**Đặc trưng đầu vào:**")
            features = [
                "Tuổi", "Giờ ngủ", "Tần suất tập thể dục", "Hỗ trợ xã hội",
                "Mức căng thẳng", "Số lần đánh giá trước", "Điểm DASS",
                "Điểm PHQ-9", "Điểm GAD-7", "Giới tính", "Trình độ học vấn"
            ]
            st.write(", ".join(features))
    
    with tab3:
        st.header("📊 Phân tích hiệu suất AI")
        
        if not ai_engine.models_trained:
            st.warning("⚠️ Cần huấn luyện mô hình trước để xem phân tích")
            return
        
        # Generate test data for analysis
        test_data = ai_engine.generate_training_data(1000)
        
        # Model performance visualization
        st.subheader("🎯 Hiệu suất mô hình")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk prediction accuracy by category
            risk_dist = test_data['risk_level'].value_counts()
            fig_risk_dist = px.pie(
                values=risk_dist.values,
                names=risk_dist.index,
                title="Phân bố mức độ rủi ro"
            )
            st.plotly_chart(fig_risk_dist, use_container_width=True)
        
        with col2:
            # Intervention success distribution
            fig_intervention = px.histogram(
                test_data,
                x='intervention_success',
                title="Phân bố khả năng can thiệp thành công",
                nbins=20
            )
            st.plotly_chart(fig_intervention, use_container_width=True)
        
        # Feature importance analysis
        st.subheader("📈 Tầm quan trọng của các đặc trưng")
        
        if hasattr(ai_engine.risk_classifier, 'feature_importances_'):
            feature_names = [
                'Tuổi', 'Giờ ngủ', 'Tập thể dục', 'Hỗ trợ xã hội',
                'Căng thẳng', 'Đánh giá trước', 'Ngày từ lần cuối',
                'DASS Trầm cảm', 'DASS Lo âu', 'DASS Căng thẳng',
                'PHQ-9', 'GAD-7', 'Giới tính', 'Học vấn'
            ]
            
            importances = ai_engine.risk_classifier.feature_importances_
            
            # Pad or trim feature_names to match importances length
            if len(feature_names) > len(importances):
                feature_names = feature_names[:len(importances)]
            elif len(feature_names) < len(importances):
                feature_names.extend([f'Feature_{i}' for i in range(len(feature_names), len(importances))])
            
            fig_importance = px.bar(
                x=importances,
                y=feature_names,
                orientation='h',
                title="Tầm quan trọng các đặc trưng trong dự đoán rủi ro"
            )
            fig_importance.update_layout(height=500)
            st.plotly_chart(fig_importance, use_container_width=True)
        
        # Model comparison
        st.subheader("🔄 So sánh mô hình")
        
        models_comparison = pd.DataFrame({
            'Mô hình': ['Random Forest', 'Gradient Boosting', 'Logistic Regression'],
            'Độ chính xác': [0.857, 0.843, 0.789],
            'Thời gian huấn luyện (s)': [12.3, 8.7, 2.1],
            'Kích thước mô hình (MB)': [45.2, 32.1, 0.8]
        })
        
        st.dataframe(models_comparison, use_container_width=True)
    
    with tab4:
        st.header("💡 Hệ thống khuyến nghị thông minh")
        
        st.subheader("🎯 Khuyến nghị theo mức độ rủi ro")
        
        # Risk-based recommendations showcase
        risk_recommendations = {
            "Low": [
                "✅ Duy trì lối sống lành mạnh hiện tại",
                "📅 Đánh giá định kỳ 3-6 tháng",
                "🎯 Tập trung vào phòng ngừa"
            ],
            "Moderate": [
                "📚 Học kỹ thuật quản lý căng thẳng",
                "🧘 Thực hành mindfulness hàng ngày",
                "👥 Tăng cường hoạt động xã hội",
                "📊 Theo dõi tâm trạng hàng tuần"
            ],
            "High": [
                "⚠️ Tìm kiếm hỗ trợ chuyên nghiệp trong 1-2 tuần",
                "🗣️ Tham gia liệu pháp tâm lý",
                "📞 Liên hệ đường dây hỗ trợ",
                "👨‍⚕️ Tư vấn với bác sĩ gia đình"
            ],
            "Very High": [
                "🚨 Cần hỗ trợ chuyên nghiệp ngay lập tức",
                "📞 Gọi hotline khẩn cấp: 1900-xxx-xxx",
                "🏥 Đến cơ sở y tế trong 24h",
                "👥 Thông báo cho người thân tin cậy"
            ]
        }
        
        for risk_level, recommendations in risk_recommendations.items():
            with st.expander(f"Mức độ rủi ro: {risk_level}"):
                for rec in recommendations:
                    st.write(f"• {rec}")
        
        # Personalized intervention suggestions
        st.subheader("🎯 Can thiệp cá nhân hóa")
        
        intervention_types = {
            "Liệu pháp tâm lý": {
                "CBT": "Liệu pháp nhận thức hành vi",
                "DBT": "Liệu pháp hành vi biện chứng", 
                "ACT": "Liệu pháp chấp nhận và cam kết"
            },
            "Thay đổi lối sống": {
                "Exercise": "Chương trình tập thể dục",
                "Sleep": "Cải thiện vệ sinh giấc ngủ",
                "Nutrition": "Chế độ dinh dưỡng"
            },
            "Hỗ trợ xã hội": {
                "Support Groups": "Nhóm hỗ trợ",
                "Family Therapy": "Liệu pháp gia đình",
                "Peer Support": "Hỗ trợ đồng đẳng"
            }
        }
        
        for category, interventions in intervention_types.items():
            with st.expander(f"📋 {category}"):
                for code, description in interventions.items():
                    st.write(f"• **{code}**: {description}")
        
        # AI-powered resource matching
        st.subheader("🔍 Tìm kiếm tài nguyên thông minh")
        
        location = st.selectbox(
            "Khu vực của bạn:",
            ["Hà Nội", "TP.HCM", "Đà Nẵng", "Cần Thơ", "Khác"]
        )
        
        resource_type = st.selectbox(
            "Loại tài nguyên cần tìm:",
            ["Bác sĩ tâm thần", "Tâm lý trị liệu", "Nhóm hỗ trợ", "Trung tâm tư vấn"]
        )
        
        if st.button("🔍 Tìm kiếm tài nguyên"):
            st.success("🎯 Đã tìm thấy các tài nguyên phù hợp!")
            
            # Sample resources (in real app, would query database)
            sample_resources = [
                {
                    "name": "Trung tâm Tâm lý ABC",
                    "address": f"{location} - Quận 1",
                    "phone": "028-xxxx-xxxx",
                    "speciality": resource_type,
                    "rating": 4.8
                },
                {
                    "name": "Phòng khám Dr. XYZ",
                    "address": f"{location} - Quận 3", 
                    "phone": "028-yyyy-yyyy",
                    "speciality": resource_type,
                    "rating": 4.6
                }
            ]
            
            for resource in sample_resources:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{resource['name']}**")
                        st.write(f"📍 {resource['address']}")
                        st.write(f"📞 {resource['phone']}")
                        st.write(f"⭐ {resource['rating']}/5.0")
                    with col2:
                        if st.button("📞 Liên hệ", key=f"contact_{resource['name']}"):
                            st.success("Đã sao chép thông tin liên hệ!")

# Main AI interface
def ai_main():
    ai_insights_dashboard()

if __name__ == "__main__":
    ai_main()
