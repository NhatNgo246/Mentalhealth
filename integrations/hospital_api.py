"""
SOULFRIEND V2.0 - Hospital Integration API System
Tích hợp hệ thống bệnh viện và nhà cung cấp dịch vụ chăm sóc sức khỏe
"""
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
import requests
import sqlite3
import hashlib
import hmac
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PatientData(BaseModel):
    """Dữ liệu bệnh nhân để tích hợp"""
    patient_id: str
    name: str
    email: EmailStr
    phone: str
    mental_health_score: float
    risk_level: str
    assessment_date: datetime
    emergency_contact: Optional[str] = None

class AppointmentRequest(BaseModel):
    """Yêu cầu đặt lịch hẹn"""
    patient_id: str
    provider_id: str
    appointment_type: str
    preferred_date: datetime
    notes: Optional[str] = None

class HospitalIntegrationAPI:
    """Hệ thống tích hợp API bệnh viện"""
    
    def __init__(self):
        self.app = FastAPI(title="SOULFRIEND V2.0 - Hospital Integration API")
        self.db_path = "/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/data/integration.db"
        self.init_database()
        self.setup_routes()
        
        # Hospital endpoints configuration
        self.hospital_endpoints = {
            "bach_mai": {
                "url": "https://api.bachmai.gov.vn/v1",
                "api_key": "BM_API_KEY_2024",
                "auth_type": "bearer"
            },
            "viet_duc": {
                "url": "https://api.vietduc.gov.vn/v1", 
                "api_key": "VD_API_KEY_2024",
                "auth_type": "hmac"
            },
            "cho_ray": {
                "url": "https://api.choray.vn/v1",
                "api_key": "CR_API_KEY_2024", 
                "auth_type": "oauth2"
            }
        }
    
    def init_database(self):
        """Khởi tạo cơ sở dữ liệu tích hợp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng tích hợp bệnh viện
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospital_integrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hospital_id TEXT NOT NULL,
                patient_id TEXT NOT NULL,
                integration_status TEXT DEFAULT 'pending',
                data_sent TEXT,
                response_received TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng lịch hẹn
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                provider_id TEXT NOT NULL,
                hospital_id TEXT NOT NULL,
                appointment_date TIMESTAMP,
                appointment_type TEXT,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng nhà cung cấp dịch vụ
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS healthcare_providers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialty TEXT,
                hospital_id TEXT,
                contact_info TEXT,
                availability TEXT,
                rating REAL DEFAULT 0.0
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Database initialized for hospital integrations")
    
    def setup_routes(self):
        """Thiết lập các routes API"""
        
        @self.app.post("/api/v1/integrate/patient")
        async def integrate_patient_data(patient: PatientData, hospital_id: str):
            """Tích hợp dữ liệu bệnh nhân với hệ thống bệnh viện"""
            try:
                # Validate hospital
                if hospital_id not in self.hospital_endpoints:
                    raise HTTPException(status_code=400, detail="Invalid hospital ID")
                
                # Prepare integration data
                integration_data = {
                    "patient_id": patient.patient_id,
                    "mental_health_assessment": {
                        "score": patient.mental_health_score,
                        "risk_level": patient.risk_level,
                        "assessment_date": patient.assessment_date.isoformat()
                    },
                    "contact_info": {
                        "email": patient.email,
                        "phone": patient.phone,
                        "emergency_contact": patient.emergency_contact
                    },
                    "source": "SOULFRIEND_V2",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Send to hospital API
                response = await self.send_to_hospital(hospital_id, "patients", integration_data)
                
                # Store integration record
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO hospital_integrations 
                    (hospital_id, patient_id, integration_status, data_sent, response_received)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    hospital_id,
                    patient.patient_id,
                    "success" if response.get("status") == "success" else "failed",
                    json.dumps(integration_data),
                    json.dumps(response)
                ))
                conn.commit()
                conn.close()
                
                return {
                    "status": "success",
                    "message": f"Patient data integrated with {hospital_id}",
                    "integration_id": response.get("integration_id"),
                    "hospital_response": response
                }
                
            except Exception as e:
                logger.error(f"Integration error: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/v1/schedule/appointment")
        async def schedule_appointment(request: AppointmentRequest):
            """Đặt lịch hẹn với nhà cung cấp dịch vụ"""
            try:
                # Find available providers
                providers = await self.find_available_providers(
                    request.appointment_type,
                    request.preferred_date
                )
                
                if not providers:
                    raise HTTPException(status_code=404, detail="No available providers found")
                
                # Select best provider
                selected_provider = providers[0]  # Simple selection logic
                
                # Create appointment
                appointment_data = {
                    "patient_id": request.patient_id,
                    "provider_id": selected_provider["id"],
                    "appointment_date": request.preferred_date.isoformat(),
                    "appointment_type": request.appointment_type,
                    "notes": request.notes,
                    "status": "scheduled"
                }
                
                # Send to hospital system
                hospital_id = selected_provider["hospital_id"]
                response = await self.send_to_hospital(hospital_id, "appointments", appointment_data)
                
                # Store appointment
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO appointments 
                    (patient_id, provider_id, hospital_id, appointment_date, appointment_type, status, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    request.patient_id,
                    selected_provider["id"],
                    hospital_id,
                    request.preferred_date,
                    request.appointment_type,
                    "scheduled",
                    request.notes
                ))
                appointment_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                return {
                    "status": "success",
                    "appointment_id": appointment_id,
                    "provider": selected_provider,
                    "appointment_date": request.preferred_date,
                    "hospital_confirmation": response.get("confirmation_id")
                }
                
            except Exception as e:
                logger.error(f"Appointment scheduling error: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/providers/search")
        async def search_providers(specialty: str = None, hospital_id: str = None):
            """Tìm kiếm nhà cung cấp dịch vụ"""
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM healthcare_providers WHERE 1=1"
            params = []
            
            if specialty:
                query += " AND specialty LIKE ?"
                params.append(f"%{specialty}%")
            
            if hospital_id:
                query += " AND hospital_id = ?"
                params.append(hospital_id)
            
            query += " ORDER BY rating DESC"
            
            cursor.execute(query, params)
            providers = cursor.fetchall()
            conn.close()
            
            return {
                "providers": [
                    {
                        "id": p[0],
                        "name": p[1],
                        "specialty": p[2],
                        "hospital_id": p[3],
                        "contact_info": json.loads(p[4]) if p[4] else {},
                        "availability": json.loads(p[5]) if p[5] else {},
                        "rating": p[6]
                    }
                    for p in providers
                ]
            }
        
        @self.app.get("/api/v1/integration/status/{patient_id}")
        async def get_integration_status(patient_id: str):
            """Kiểm tra trạng thái tích hợp của bệnh nhân"""
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT hospital_id, integration_status, created_at, updated_at
                FROM hospital_integrations 
                WHERE patient_id = ?
                ORDER BY created_at DESC
            ''', (patient_id,))
            
            integrations = cursor.fetchall()
            conn.close()
            
            return {
                "patient_id": patient_id,
                "integrations": [
                    {
                        "hospital_id": i[0],
                        "status": i[1],
                        "created_at": i[2],
                        "updated_at": i[3]
                    }
                    for i in integrations
                ]
            }
    
    async def send_to_hospital(self, hospital_id: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gửi dữ liệu đến API bệnh viện"""
        try:
            hospital_config = self.hospital_endpoints[hospital_id]
            url = f"{hospital_config['url']}/{endpoint}"
            
            # Prepare headers based on auth type
            headers = {"Content-Type": "application/json"}
            
            if hospital_config["auth_type"] == "bearer":
                headers["Authorization"] = f"Bearer {hospital_config['api_key']}"
            elif hospital_config["auth_type"] == "hmac":
                # HMAC signature
                timestamp = str(int(datetime.now().timestamp()))
                message = f"{timestamp}.{json.dumps(data)}"
                signature = hmac.new(
                    hospital_config['api_key'].encode(),
                    message.encode(),
                    hashlib.sha256
                ).hexdigest()
                headers["X-Timestamp"] = timestamp
                headers["X-Signature"] = signature
            
            # Simulate API call (in production, use actual HTTP requests)
            await asyncio.sleep(0.1)  # Simulate network delay
            
            return {
                "status": "success",
                "integration_id": f"INT_{hospital_id}_{int(datetime.now().timestamp())}",
                "confirmation_id": f"CONF_{hospital_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "message": f"Data successfully integrated with {hospital_id}"
            }
            
        except Exception as e:
            logger.error(f"Hospital API error: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def find_available_providers(self, appointment_type: str, preferred_date: datetime) -> List[Dict[str, Any]]:
        """Tìm nhà cung cấp dịch vụ có sẵn"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find providers by specialty
        specialty_map = {
            "consultation": "psychiatrist",
            "therapy": "psychologist", 
            "emergency": "emergency_psychiatrist",
            "counseling": "counselor"
        }
        
        specialty = specialty_map.get(appointment_type, "psychiatrist")
        
        cursor.execute('''
            SELECT * FROM healthcare_providers 
            WHERE specialty LIKE ?
            ORDER BY rating DESC
            LIMIT 10
        ''', (f"%{specialty}%",))
        
        providers = cursor.fetchall()
        conn.close()
        
        # Mock availability check
        available_providers = []
        for p in providers:
            available_providers.append({
                "id": p[0],
                "name": p[1],
                "specialty": p[2],
                "hospital_id": p[3],
                "contact_info": json.loads(p[4]) if p[4] else {},
                "rating": p[6],
                "next_available": (preferred_date + timedelta(hours=2)).isoformat()
            })
        
        return available_providers
    
    def seed_sample_providers(self):
        """Tạo dữ liệu mẫu cho nhà cung cấp dịch vụ"""
        sample_providers = [
            {
                "id": "DR_001",
                "name": "BS. Nguyễn Văn Nam",
                "specialty": "psychiatrist",
                "hospital_id": "bach_mai",
                "contact_info": json.dumps({
                    "email": "dr.nam@bachmai.gov.vn",
                    "phone": "024-3869-3731",
                    "department": "Khoa Tâm thần"
                }),
                "availability": json.dumps({
                    "monday": ["09:00-12:00", "14:00-17:00"],
                    "tuesday": ["09:00-12:00", "14:00-17:00"],
                    "wednesday": ["09:00-12:00"],
                    "thursday": ["09:00-12:00", "14:00-17:00"],
                    "friday": ["09:00-12:00", "14:00-17:00"]
                }),
                "rating": 4.8
            },
            {
                "id": "DR_002",
                "name": "ThS. Trần Thị Mai",
                "specialty": "psychologist",
                "hospital_id": "viet_duc",
                "contact_info": json.dumps({
                    "email": "ths.mai@vietduc.gov.vn",
                    "phone": "024-3825-3531",
                    "department": "Khoa Tâm lý"
                }),
                "availability": json.dumps({
                    "monday": ["08:00-12:00", "13:00-17:00"],
                    "tuesday": ["08:00-12:00", "13:00-17:00"],
                    "wednesday": ["08:00-12:00", "13:00-17:00"],
                    "thursday": ["08:00-12:00"],
                    "friday": ["08:00-12:00", "13:00-17:00"]
                }),
                "rating": 4.9
            },
            {
                "id": "DR_003",
                "name": "PGS.TS. Lê Minh Hoàng",
                "specialty": "emergency_psychiatrist",
                "hospital_id": "cho_ray",
                "contact_info": json.dumps({
                    "email": "pgs.hoang@choray.vn",
                    "phone": "028-3855-4269",
                    "department": "Cấp cứu Tâm thần"
                }),
                "availability": json.dumps({
                    "24/7": "available",
                    "emergency": "immediate_response"
                }),
                "rating": 4.7
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for provider in sample_providers:
            cursor.execute('''
                INSERT OR REPLACE INTO healthcare_providers 
                (id, name, specialty, hospital_id, contact_info, availability, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                provider["id"],
                provider["name"],
                provider["specialty"],
                provider["hospital_id"],
                provider["contact_info"],
                provider["availability"],
                provider["rating"]
            ))
        
        conn.commit()
        conn.close()
        logger.info("✅ Sample healthcare providers seeded")

# Global instance
hospital_api = HospitalIntegrationAPI()

def get_hospital_api():
    """Dependency injection cho FastAPI"""
    return hospital_api

if __name__ == "__main__":
    import uvicorn
    
    # Seed sample data
    hospital_api.seed_sample_providers()
    
    # Run API server
    uvicorn.run(
        "hospital_api:hospital_api.app",
        host="0.0.0.0",
        port=8507,
        reload=True
    )
