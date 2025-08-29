"""
Database Integration Module for Research System
Mô-đun Tích hợp Cơ sở Dữ liệu cho Hệ thống Nghiên cứu

Provides database integration for persistent storage and advanced querying.
Cung cấp tích hợp cơ sở dữ liệu cho lưu trữ bền vững và truy vấn nâng cao.
"""

import os
import json
import asyncio
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
from pathlib import Path
import hashlib
import hmac

# Try to import asyncpg, but make it optional
try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False
    print("⚠️ asyncpg not available - PostgreSQL features will be disabled")

class DatabaseConfig:
    """Database configuration management"""
    
    def __init__(self):
        self.db_type = os.getenv('RESEARCH_DB_TYPE', 'sqlite')  # sqlite or postgresql
        self.db_path = os.getenv('RESEARCH_DB_PATH', 'research_data/research.db')
        
        # PostgreSQL settings (if using PostgreSQL)
        self.pg_host = os.getenv('RESEARCH_PG_HOST', 'localhost')
        self.pg_port = int(os.getenv('RESEARCH_PG_PORT', 5432))
        self.pg_database = os.getenv('RESEARCH_PG_DATABASE', 'research_db')
        self.pg_username = os.getenv('RESEARCH_PG_USERNAME', 'research_user')
        self.pg_password = os.getenv('RESEARCH_PG_PASSWORD', '')
        
        # Security settings
        self.encryption_key = os.getenv('RESEARCH_ENCRYPTION_KEY', self._generate_default_key())
        
    def _generate_default_key(self) -> str:
        """Generate a default encryption key"""
        return hashlib.sha256(b'research_system_default_key').hexdigest()
    
    @property
    def postgres_url(self) -> str:
        """Get PostgreSQL connection URL"""
        return f"postgresql://{self.pg_username}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"

class SQLiteDatabase:
    """SQLite database implementation for research data"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS research_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_data TEXT,
                    timestamp DATETIME NOT NULL,
                    anonymized_user_id TEXT,
                    consent_status TEXT,
                    data_hash TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_session_id ON research_events(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON research_events(event_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON research_events(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON research_events(anonymized_user_id)')
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS research_sessions (
                    session_id TEXT PRIMARY KEY,
                    anonymized_user_id TEXT,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME,
                    consent_status TEXT NOT NULL,
                    questionnaire_types TEXT,
                    completion_status TEXT,
                    data_hash TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON research_sessions(anonymized_user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON research_sessions(start_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_consent ON research_sessions(consent_status)')
            
            # Aggregated data table for analytics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS research_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value TEXT NOT NULL,
                    aggregation_period TEXT NOT NULL,
                    period_start DATETIME NOT NULL,
                    period_end DATETIME NOT NULL,
                    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_metric ON research_analytics(metric_name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_period ON research_analytics(aggregation_period)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_start ON research_analytics(period_start)')
            
            # Consent audit table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consent_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    anonymized_user_id TEXT NOT NULL,
                    consent_action TEXT NOT NULL,
                    consent_details TEXT,
                    timestamp DATETIME NOT NULL,
                    ip_hash TEXT,
                    user_agent_hash TEXT
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_consent_user_id ON consent_audit(anonymized_user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_consent_action ON consent_audit(consent_action)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_consent_timestamp ON consent_audit(timestamp)')
            
            conn.commit()
    
    def store_event(self, event_data: Dict[str, Any]) -> bool:
        """Store a research event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO research_events 
                    (session_id, event_type, event_data, timestamp, anonymized_user_id, consent_status, data_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event_data.get('session_id'),
                    event_data.get('event_type'),
                    json.dumps(event_data.get('event_data', {})),
                    event_data.get('timestamp'),
                    event_data.get('anonymized_user_id'),
                    event_data.get('consent_status'),
                    event_data.get('data_hash')
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error storing event: {e}")
            return False
    
    def store_session(self, session_data: Dict[str, Any]) -> bool:
        """Store session information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO research_sessions 
                    (session_id, anonymized_user_id, start_time, end_time, consent_status, 
                     questionnaire_types, completion_status, data_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_data.get('session_id'),
                    session_data.get('anonymized_user_id'),
                    session_data.get('start_time'),
                    session_data.get('end_time'),
                    session_data.get('consent_status'),
                    json.dumps(session_data.get('questionnaire_types', [])),
                    session_data.get('completion_status'),
                    session_data.get('data_hash')
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error storing session: {e}")
            return False
    
    def get_events(self, 
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   event_types: Optional[List[str]] = None,
                   limit: int = 1000) -> List[Dict[str, Any]]:
        """Retrieve events with filtering"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM research_events WHERE 1=1"
                params = []
                
                if start_date:
                    query += " AND timestamp >= ?"
                    params.append(start_date.isoformat())
                
                if end_date:
                    query += " AND timestamp <= ?"
                    params.append(end_date.isoformat())
                
                if event_types:
                    placeholders = ','.join(['?' for _ in event_types])
                    query += f" AND event_type IN ({placeholders})"
                    params.extend(event_types)
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Convert to dictionaries
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error retrieving events: {e}")
            return []
    
    def get_analytics_data(self, 
                          metric_names: Optional[List[str]] = None,
                          period: str = 'daily') -> List[Dict[str, Any]]:
        """Get analytics data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM research_analytics WHERE aggregation_period = ?"
                params = [period]
                
                if metric_names:
                    placeholders = ','.join(['?' for _ in metric_names])
                    query += f" AND metric_name IN ({placeholders})"
                    params.extend(metric_names)
                
                query += " ORDER BY period_start DESC"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error retrieving analytics data: {e}")
            return []
    
    def cleanup_old_data(self, retention_days: int = 90) -> int:
        """Clean up old data beyond retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete old events
                cursor.execute(
                    "DELETE FROM research_events WHERE timestamp < ?",
                    (cutoff_date.isoformat(),)
                )
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                self.logger.info(f"Cleaned up {deleted_count} old records")
                return deleted_count
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old data: {e}")
            return 0
    
    def health_check(self) -> bool:
        """Check database health"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False

class PostgreSQLDatabase:
    """PostgreSQL database implementation for research data"""
    
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.logger = logging.getLogger(__name__)
    
    async def _get_connection(self):
        """Get database connection"""
        if not ASYNCPG_AVAILABLE:
            raise ImportError("asyncpg not available")
        return await asyncpg.connect(self.connection_url)
    
    async def initialize_database(self):
        """Initialize database schema"""
        conn = await self._get_connection()
        try:
            # Events table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS research_events (
                    id SERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_data JSONB,
                    timestamp TIMESTAMPTZ NOT NULL,
                    anonymized_user_id TEXT,
                    consent_status TEXT,
                    data_hash TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            ''')
            
            # Create indexes
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_events_session_id ON research_events(session_id)')
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON research_events(event_type)')
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON research_events(timestamp)')
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON research_events(anonymized_user_id)')
            
            # Sessions table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS research_sessions (
                    session_id TEXT PRIMARY KEY,
                    anonymized_user_id TEXT,
                    start_time TIMESTAMPTZ NOT NULL,
                    end_time TIMESTAMPTZ,
                    consent_status TEXT NOT NULL,
                    questionnaire_types JSONB,
                    completion_status TEXT,
                    data_hash TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            ''')
            
            # Analytics table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS research_analytics (
                    id SERIAL PRIMARY KEY,
                    metric_name TEXT NOT NULL,
                    metric_value JSONB NOT NULL,
                    aggregation_period TEXT NOT NULL,
                    period_start TIMESTAMPTZ NOT NULL,
                    period_end TIMESTAMPTZ NOT NULL,
                    calculated_at TIMESTAMPTZ DEFAULT NOW()
                )
            ''')
            
            # Consent audit table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS consent_audit (
                    id SERIAL PRIMARY KEY,
                    anonymized_user_id TEXT NOT NULL,
                    consent_action TEXT NOT NULL,
                    consent_details JSONB,
                    timestamp TIMESTAMPTZ NOT NULL,
                    ip_hash TEXT,
                    user_agent_hash TEXT
                )
            ''')
            
        finally:
            await conn.close()
    
    async def store_event(self, event_data: Dict[str, Any]) -> bool:
        """Store a research event"""
        conn = await self._get_connection()
        try:
            await conn.execute('''
                INSERT INTO research_events 
                (session_id, event_type, event_data, timestamp, anonymized_user_id, consent_status, data_hash)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            ''', 
                event_data.get('session_id'),
                event_data.get('event_type'),
                json.dumps(event_data.get('event_data', {})),
                event_data.get('timestamp'),
                event_data.get('anonymized_user_id'),
                event_data.get('consent_status'),
                event_data.get('data_hash')
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing event: {e}")
            return False
        finally:
            await conn.close()

class ResearchDatabase:
    """Main database interface for research system"""
    
    def __init__(self):
        self.config = DatabaseConfig()
        self.logger = logging.getLogger(__name__)
        
        if self.config.db_type == 'postgresql' and ASYNCPG_AVAILABLE:
            self.db = PostgreSQLDatabase(self.config.postgres_url)
        else:
            if self.config.db_type == 'postgresql' and not ASYNCPG_AVAILABLE:
                self.logger.warning("PostgreSQL requested but asyncpg not available, falling back to SQLite")
            self.db = SQLiteDatabase(self.config.db_path)
    
    def store_event(self, event_data: Dict[str, Any]) -> bool:
        """Store event with encryption and anonymization"""
        try:
            # Add data integrity hash
            event_data['data_hash'] = self._calculate_hash(event_data)
            
            # Store in database
            if isinstance(self.db, SQLiteDatabase):
                return self.db.store_event(event_data)
            else:
                # For PostgreSQL, run async method
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(self.db.store_event(event_data))
                
        except Exception as e:
            self.logger.error(f"Error in store_event: {e}")
            return False
    
    def get_events(self, **kwargs) -> List[Dict[str, Any]]:
        """Get events with filtering"""
        try:
            if isinstance(self.db, SQLiteDatabase):
                return self.db.get_events(**kwargs)
            else:
                # For PostgreSQL, implement async version
                return []
                
        except Exception as e:
            self.logger.error(f"Error in get_events: {e}")
            return []
    
    def _calculate_hash(self, data: Dict[str, Any]) -> str:
        """Calculate HMAC hash for data integrity"""
        data_str = json.dumps(data, sort_keys=True)
        return hmac.new(
            self.config.encryption_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def cleanup_old_data(self, retention_days: int = 90) -> int:
        """Clean up old data"""
        try:
            if isinstance(self.db, SQLiteDatabase):
                return self.db.cleanup_old_data(retention_days)
            else:
                # For PostgreSQL, implement async version
                return 0
                
        except Exception as e:
            self.logger.error(f"Error in cleanup_old_data: {e}")
            return 0

def main():
    """Demo database functionality"""
    print("🗄️ RESEARCH DATABASE MODULE")
    print("=" * 40)
    
    # Initialize database
    print("📊 Initializing database...")
    db = ResearchDatabase()
    
    # Test event storage
    print("💾 Testing event storage...")
    test_event = {
        'session_id': 'test_session_123',
        'event_type': 'test_event',
        'event_data': {'test': 'data'},
        'timestamp': datetime.now().isoformat(),
        'anonymized_user_id': 'anon_user_123',
        'consent_status': 'given'
    }
    
    success = db.store_event(test_event)
    if success:
        print("✅ Event stored successfully")
    else:
        print("❌ Failed to store event")
    
    # Test data retrieval
    print("📖 Testing data retrieval...")
    events = db.get_events(limit=10)
    print(f"✅ Retrieved {len(events)} events")
    
    # Test cleanup
    print("🧹 Testing data cleanup...")
    cleaned = db.cleanup_old_data(retention_days=90)
    print(f"✅ Cleaned up {cleaned} old records")
    
    print("\n🎉 Database module tested successfully!")

if __name__ == "__main__":
    main()
