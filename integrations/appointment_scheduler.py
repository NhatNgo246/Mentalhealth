"""
SOULFRIEND V2.0 - Appointment Scheduling System
Hệ thống đặt lịch hẹn và quản lý cuộc hẹn tự động
"""
import json
import sqlite3
from datetime import datetime, timedelta, time
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppointmentStatus(Enum):
    """Trạng thái cuộc hẹn"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"

class AppointmentType(Enum):
    """Loại cuộc hẹn"""
    CONSULTATION = "consultation"
    THERAPY = "therapy"
    EMERGENCY = "emergency"
    FOLLOW_UP = "follow_up"
    GROUP_THERAPY = "group_therapy"
    ASSESSMENT = "assessment"

@dataclass
class TimeSlot:
    """Khung thời gian"""
    start_time: time
    end_time: time
    duration_minutes: int
    is_available: bool = True

@dataclass
class Provider:
    """Nhà cung cấp dịch vụ"""
    id: str
    name: str
    specialty: str
    hospital_id: str
    working_hours: Dict[str, List[TimeSlot]]
    max_patients_per_day: int
    consultation_duration: int  # minutes

class AppointmentScheduler:
    """Hệ thống đặt lịch hẹn thông minh"""
    
    def __init__(self):
        self.db_path = "/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/data/appointments.db"
        self.init_database()
        self.init_providers()
        
        # Cấu hình lịch làm việc mặc định
        self.default_working_hours = {
            "monday": [
                TimeSlot(time(8, 0), time(12, 0), 30),
                TimeSlot(time(13, 30), time(17, 0), 30)
            ],
            "tuesday": [
                TimeSlot(time(8, 0), time(12, 0), 30),
                TimeSlot(time(13, 30), time(17, 0), 30)
            ],
            "wednesday": [
                TimeSlot(time(8, 0), time(12, 0), 30),
                TimeSlot(time(13, 30), time(17, 0), 30)
            ],
            "thursday": [
                TimeSlot(time(8, 0), time(12, 0), 30),
                TimeSlot(time(13, 30), time(17, 0), 30)
            ],
            "friday": [
                TimeSlot(time(8, 0), time(12, 0), 30),
                TimeSlot(time(13, 30), time(17, 0), 30)
            ],
            "saturday": [
                TimeSlot(time(8, 0), time(12, 0), 30)
            ],
            "sunday": []  # Nghỉ chủ nhật
        }
    
    def init_database(self):
        """Khởi tạo cơ sở dữ liệu lịch hẹn"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng cuộc hẹn
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                provider_id TEXT NOT NULL,
                appointment_date TIMESTAMP NOT NULL,
                duration_minutes INTEGER DEFAULT 30,
                appointment_type TEXT NOT NULL,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                patient_notes TEXT,
                reminder_sent BOOLEAN DEFAULT 0,
                confirmation_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng nhà cung cấp dịch vụ
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS providers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                hospital_id TEXT,
                contact_info TEXT,
                working_hours TEXT,
                max_patients_per_day INTEGER DEFAULT 20,
                consultation_duration INTEGER DEFAULT 30,
                rating REAL DEFAULT 0.0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Bảng khung thời gian không có sẵn
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS provider_unavailable_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider_id TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (provider_id) REFERENCES providers(id)
            )
        ''')
        
        # Bảng lịch sử thay đổi cuộc hẹn
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointment_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                reason TEXT,
                changed_by TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (appointment_id) REFERENCES appointments(id)
            )
        ''')
        
        # Bảng cấu hình nhắc nhở
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminder_settings (
                patient_id TEXT PRIMARY KEY,
                email_reminder BOOLEAN DEFAULT 1,
                sms_reminder BOOLEAN DEFAULT 0,
                reminder_hours_before INTEGER DEFAULT 24,
                secondary_reminder_hours INTEGER DEFAULT 2
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Appointment database initialized")
    
    def init_providers(self):
        """Khởi tạo danh sách nhà cung cấp dịch vụ"""
        providers_data = [
            {
                "id": "DR_PSY_001",
                "name": "BS. Nguyễn Minh Tâm",
                "specialty": "Tâm thần học",
                "hospital_id": "bach_mai",
                "contact_info": json.dumps({
                    "email": "dr.tam@bachmai.gov.vn",
                    "phone": "024-3869-3731",
                    "department": "Khoa Tâm thần",
                    "room": "P201"
                }),
                "working_hours": json.dumps({
                    "monday": ["08:00-12:00", "13:30-17:00"],
                    "tuesday": ["08:00-12:00", "13:30-17:00"],
                    "wednesday": ["08:00-12:00"],
                    "thursday": ["08:00-12:00", "13:30-17:00"],
                    "friday": ["08:00-12:00", "13:30-17:00"],
                    "saturday": ["08:00-12:00"],
                    "sunday": []
                }),
                "max_patients_per_day": 25,
                "consultation_duration": 30,
                "rating": 4.8
            },
            {
                "id": "THS_PSY_002",
                "name": "ThS. Trần Thị Hương",
                "specialty": "Tâm lý lâm sàng",
                "hospital_id": "viet_duc",
                "contact_info": json.dumps({
                    "email": "ths.huong@vietduc.gov.vn",
                    "phone": "024-3825-3531",
                    "department": "Khoa Tâm lý",
                    "room": "P305"
                }),
                "working_hours": json.dumps({
                    "monday": ["08:00-12:00", "14:00-17:30"],
                    "tuesday": ["08:00-12:00", "14:00-17:30"],
                    "wednesday": ["08:00-12:00", "14:00-17:30"],
                    "thursday": ["08:00-12:00"],
                    "friday": ["08:00-12:00", "14:00-17:30"],
                    "saturday": [],
                    "sunday": []
                }),
                "max_patients_per_day": 20,
                "consultation_duration": 45,
                "rating": 4.9
            },
            {
                "id": "PGS_PSY_003",
                "name": "PGS.TS. Lê Văn Phúc",
                "specialty": "Tâm thần cấp cứu",
                "hospital_id": "cho_ray",
                "contact_info": json.dumps({
                    "email": "pgs.phuc@choray.vn",
                    "phone": "028-3855-4269",
                    "department": "Cấp cứu Tâm thần",
                    "room": "ICU-PSY"
                }),
                "working_hours": json.dumps({
                    "monday": ["06:00-18:00"],
                    "tuesday": ["06:00-18:00"],
                    "wednesday": ["06:00-18:00"],
                    "thursday": ["06:00-18:00"],
                    "friday": ["06:00-18:00"],
                    "saturday": ["08:00-15:00"],
                    "sunday": ["08:00-15:00"]
                }),
                "max_patients_per_day": 30,
                "consultation_duration": 20,
                "rating": 4.7
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for provider in providers_data:
            cursor.execute('''
                INSERT OR REPLACE INTO providers 
                (id, name, specialty, hospital_id, contact_info, working_hours, 
                 max_patients_per_day, consultation_duration, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                provider["id"],
                provider["name"],
                provider["specialty"],
                provider["hospital_id"],
                provider["contact_info"],
                provider["working_hours"],
                provider["max_patients_per_day"],
                provider["consultation_duration"],
                provider["rating"]
            ))
        
        conn.commit()
        conn.close()
        logger.info("✅ Providers initialized")
    
    def find_available_slots(self, provider_id: str, date: datetime, 
                           appointment_type: AppointmentType) -> List[Dict[str, Any]]:
        """Tìm khung thời gian có sẵn của nhà cung cấp"""
        try:
            # Get provider info
            provider = self.get_provider(provider_id)
            if not provider:
                return []
            
            # Get working hours for the day
            day_name = date.strftime('%A').lower()
            working_hours = json.loads(provider["working_hours"])
            day_hours = working_hours.get(day_name, [])
            
            if not day_hours:
                return []  # Provider doesn't work on this day
            
            # Get existing appointments for this day
            existing_appointments = self.get_appointments_for_date(provider_id, date)
            
            # Generate available slots
            available_slots = []
            duration = provider["consultation_duration"]
            
            for time_range in day_hours:
                start_str, end_str = time_range.split("-")
                start_time = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {start_str}", '%Y-%m-%d %H:%M')
                end_time = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {end_str}", '%Y-%m-%d %H:%M')
                
                current_time = start_time
                while current_time + timedelta(minutes=duration) <= end_time:
                    slot_end = current_time + timedelta(minutes=duration)
                    
                    # Check if slot is available
                    is_available = not any(
                        appointment["appointment_date"] <= current_time < 
                        appointment["appointment_date"] + timedelta(minutes=appointment["duration_minutes"])
                        for appointment in existing_appointments
                    )
                    
                    if is_available:
                        available_slots.append({
                            "start_time": current_time,
                            "end_time": slot_end,
                            "duration_minutes": duration,
                            "provider_id": provider_id,
                            "provider_name": provider["name"],
                            "appointment_type": appointment_type.value
                        })
                    
                    current_time += timedelta(minutes=duration)
            
            return available_slots
            
        except Exception as e:
            logger.error(f"Error finding available slots: {str(e)}")
            return []
    
    def book_appointment(self, patient_id: str, provider_id: str, 
                        appointment_date: datetime, appointment_type: AppointmentType,
                        notes: str = None, patient_notes: str = None) -> Dict[str, Any]:
        """Đặt lịch hẹn"""
        try:
            # Validate slot availability
            available_slots = self.find_available_slots(provider_id, appointment_date, appointment_type)
            slot_available = any(
                slot["start_time"] == appointment_date
                for slot in available_slots
            )
            
            if not slot_available:
                raise ValueError("Selected time slot is not available")
            
            # Generate confirmation code
            import random
            import string
            confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            # Get provider info for duration
            provider = self.get_provider(provider_id)
            duration = provider["consultation_duration"] if provider else 30
            
            # Create appointment
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO appointments 
                (patient_id, provider_id, appointment_date, duration_minutes, 
                 appointment_type, status, notes, patient_notes, confirmation_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id,
                provider_id,
                appointment_date,
                duration,
                appointment_type.value,
                AppointmentStatus.SCHEDULED.value,
                notes,
                patient_notes,
                confirmation_code
            ))
            
            appointment_id = cursor.lastrowid
            
            # Log appointment creation
            cursor.execute('''
                INSERT INTO appointment_history 
                (appointment_id, action, new_value, changed_by)
                VALUES (?, ?, ?, ?)
            ''', (
                appointment_id,
                "created",
                f"Appointment scheduled for {appointment_date}",
                patient_id
            ))
            
            conn.commit()
            conn.close()
            
            # Send confirmation notification
            self.send_appointment_confirmation(appointment_id)
            
            return {
                "status": "success",
                "appointment_id": appointment_id,
                "confirmation_code": confirmation_code,
                "appointment_date": appointment_date,
                "provider": provider,
                "message": "Appointment booked successfully"
            }
            
        except Exception as e:
            logger.error(f"Error booking appointment: {str(e)}")
            raise e
    
    def reschedule_appointment(self, appointment_id: int, new_date: datetime, 
                             reason: str = None) -> Dict[str, Any]:
        """Thay đổi lịch hẹn"""
        try:
            # Get current appointment
            appointment = self.get_appointment(appointment_id)
            if not appointment:
                raise ValueError("Appointment not found")
            
            # Check if new slot is available
            available_slots = self.find_available_slots(
                appointment["provider_id"], 
                new_date,
                AppointmentType(appointment["appointment_type"])
            )
            
            slot_available = any(
                slot["start_time"] == new_date
                for slot in available_slots
            )
            
            if not slot_available:
                raise ValueError("New time slot is not available")
            
            # Update appointment
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            old_date = appointment["appointment_date"]
            
            cursor.execute('''
                UPDATE appointments 
                SET appointment_date = ?, status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_date, AppointmentStatus.RESCHEDULED.value, appointment_id))
            
            # Log reschedule
            cursor.execute('''
                INSERT INTO appointment_history 
                (appointment_id, action, old_value, new_value, reason, changed_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                appointment_id,
                "rescheduled",
                f"Original date: {old_date}",
                f"New date: {new_date}",
                reason,
                appointment["patient_id"]
            ))
            
            conn.commit()
            conn.close()
            
            # Send reschedule notification
            self.send_reschedule_notification(appointment_id, old_date, new_date)
            
            return {
                "status": "success",
                "message": "Appointment rescheduled successfully",
                "old_date": old_date,
                "new_date": new_date
            }
            
        except Exception as e:
            logger.error(f"Error rescheduling appointment: {str(e)}")
            raise e
    
    def cancel_appointment(self, appointment_id: int, reason: str = None) -> Dict[str, Any]:
        """Hủy lịch hẹn"""
        try:
            # Get current appointment
            appointment = self.get_appointment(appointment_id)
            if not appointment:
                raise ValueError("Appointment not found")
            
            # Update appointment status
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE appointments 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (AppointmentStatus.CANCELLED.value, appointment_id))
            
            # Log cancellation
            cursor.execute('''
                INSERT INTO appointment_history 
                (appointment_id, action, old_value, new_value, reason, changed_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                appointment_id,
                "cancelled",
                AppointmentStatus.SCHEDULED.value,
                AppointmentStatus.CANCELLED.value,
                reason,
                appointment["patient_id"]
            ))
            
            conn.commit()
            conn.close()
            
            # Send cancellation notification
            self.send_cancellation_notification(appointment_id, reason)
            
            return {
                "status": "success",
                "message": "Appointment cancelled successfully"
            }
            
        except Exception as e:
            logger.error(f"Error cancelling appointment: {str(e)}")
            raise e
    
    def get_appointment(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        """Lấy thông tin cuộc hẹn"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, p.name as provider_name, p.specialty, p.contact_info
            FROM appointments a
            JOIN providers p ON a.provider_id = p.id
            WHERE a.id = ?
        ''', (appointment_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    
    def get_provider(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin nhà cung cấp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM providers WHERE id = ?', (provider_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    
    def get_appointments_for_date(self, provider_id: str, date: datetime) -> List[Dict[str, Any]]:
        """Lấy danh sách cuộc hẹn trong ngày"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)
        
        cursor.execute('''
            SELECT * FROM appointments 
            WHERE provider_id = ? 
            AND appointment_date >= ? 
            AND appointment_date < ?
            AND status != 'cancelled'
        ''', (provider_id, date_start, date_end))
        
        results = cursor.fetchall()
        conn.close()
        
        appointments = []
        if results:
            columns = [desc[0] for desc in cursor.description]
            for result in results:
                appointment = dict(zip(columns, result))
                appointment["appointment_date"] = datetime.fromisoformat(appointment["appointment_date"])
                appointments.append(appointment)
        
        return appointments
    
    def send_appointment_confirmation(self, appointment_id: int):
        """Gửi xác nhận lịch hẹn"""
        # Integration with notification system
        try:
            appointment = self.get_appointment(appointment_id)
            if appointment:
                logger.info(f"✅ Appointment confirmation sent for ID: {appointment_id}")
                # Here you would integrate with the notification system
                # notification_system.send_template_notification(...)
        except Exception as e:
            logger.error(f"Error sending confirmation: {str(e)}")
    
    def send_reschedule_notification(self, appointment_id: int, old_date: datetime, new_date: datetime):
        """Gửi thông báo thay đổi lịch"""
        try:
            appointment = self.get_appointment(appointment_id)
            if appointment:
                logger.info(f"✅ Reschedule notification sent for ID: {appointment_id}")
        except Exception as e:
            logger.error(f"Error sending reschedule notification: {str(e)}")
    
    def send_cancellation_notification(self, appointment_id: int, reason: str):
        """Gửi thông báo hủy lịch"""
        try:
            appointment = self.get_appointment(appointment_id)
            if appointment:
                logger.info(f"✅ Cancellation notification sent for ID: {appointment_id}")
        except Exception as e:
            logger.error(f"Error sending cancellation notification: {str(e)}")
    
    def get_upcoming_appointments(self, patient_id: str = None, provider_id: str = None) -> List[Dict[str, Any]]:
        """Lấy danh sách cuộc hẹn sắp tới"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT a.*, p.name as provider_name, p.specialty, p.contact_info
            FROM appointments a
            JOIN providers p ON a.provider_id = p.id
            WHERE a.appointment_date >= datetime('now')
            AND a.status NOT IN ('cancelled', 'completed')
        '''
        params = []
        
        if patient_id:
            query += ' AND a.patient_id = ?'
            params.append(patient_id)
        
        if provider_id:
            query += ' AND a.provider_id = ?'
            params.append(provider_id)
        
        query += ' ORDER BY a.appointment_date ASC'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        appointments = []
        if results:
            columns = [desc[0] for desc in cursor.description]
            for result in results:
                appointment = dict(zip(columns, result))
                appointments.append(appointment)
        
        return appointments

# Global instance
appointment_scheduler = AppointmentScheduler()

if __name__ == "__main__":
    # Test appointment scheduling
    print("📅 SOULFRIEND V2.0 - Appointment Scheduling System Testing")
    
    # Test finding available slots
    tomorrow = datetime.now() + timedelta(days=1)
    slots = appointment_scheduler.find_available_slots("DR_PSY_001", tomorrow, AppointmentType.CONSULTATION)
    print(f"✅ Found {len(slots)} available slots for tomorrow")
    
    if slots:
        # Test booking appointment
        try:
            result = appointment_scheduler.book_appointment(
                patient_id="test_patient_001",
                provider_id="DR_PSY_001",
                appointment_date=slots[0]["start_time"],
                appointment_type=AppointmentType.CONSULTATION,
                notes="Đánh giá tình trạng tâm lý",
                patient_notes="Cảm thấy lo lắng gần đây"
            )
            print("✅ Appointment booking test passed")
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
            
            appointment_id = result["appointment_id"]
            
            # Test rescheduling
            if len(slots) > 1:
                reschedule_result = appointment_scheduler.reschedule_appointment(
                    appointment_id, 
                    slots[1]["start_time"],
                    "Patient requested different time"
                )
                print("✅ Appointment rescheduling test passed")
                print(json.dumps(reschedule_result, indent=2, ensure_ascii=False, default=str))
            
        except Exception as e:
            print(f"❌ Appointment test failed: {e}")
    
    # Test getting upcoming appointments
    upcoming = appointment_scheduler.get_upcoming_appointments()
    print(f"✅ Found {len(upcoming)} upcoming appointments")
    
    print("✅ Appointment scheduling system ready!")
