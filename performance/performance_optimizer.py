"""
SOULFRIEND V2.0 - Performance Optimization System
Hệ thống tối ưu hóa hiệu suất và monitoring
"""
import time
import psutil
import sqlite3
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from functools import wraps
import threading
from collections import defaultdict, deque
import redis
from cachetools import TTLCache, LRUCache

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Metric hiệu suất"""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    metadata: Dict[str, Any]

@dataclass
class SystemResource:
    """Tài nguyên hệ thống"""
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_io: Dict[str, int]
    active_connections: int
    response_time: float

class PerformanceOptimizer:
    """Hệ thống tối ưu hóa hiệu suất"""
    
    def __init__(self):
        self.db_path = "/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/data/performance.db"
        self.init_database()
        
        # Performance monitoring
        self.metrics_buffer = deque(maxlen=1000)
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Caching systems
        self.init_cache_systems()
        
        # Performance thresholds
        self.thresholds = {
            "cpu_critical": 90.0,
            "cpu_warning": 75.0,
            "memory_critical": 90.0,
            "memory_warning": 80.0,
            "response_time_critical": 5.0,
            "response_time_warning": 2.0,
            "disk_usage_critical": 95.0,
            "disk_usage_warning": 85.0
        }
        
        # Database optimization settings
        self.db_optimizations = {
            "sqlite_pragmas": [
                "PRAGMA journal_mode=WAL",
                "PRAGMA synchronous=NORMAL", 
                "PRAGMA cache_size=10000",
                "PRAGMA temp_store=MEMORY",
                "PRAGMA mmap_size=268435456"  # 256MB
            ]
        }
        
        self.apply_database_optimizations()
    
    def init_database(self):
        """Khởi tạo cơ sở dữ liệu hiệu suất"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng metrics hiệu suất
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                metadata TEXT,
                INDEX(timestamp),
                INDEX(metric_name)
            )
        ''')
        
        # Bảng tài nguyên hệ thống
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cpu_percent REAL,
                memory_percent REAL,
                disk_usage REAL,
                network_io TEXT,
                active_connections INTEGER,
                response_time REAL
            )
        ''')
        
        # Bảng cảnh báo hiệu suất
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                alert_type TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                current_value REAL,
                threshold_value REAL,
                severity TEXT,
                resolved BOOLEAN DEFAULT 0,
                resolution_time TIMESTAMP
            )
        ''')
        
        # Bảng cache statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cache_name TEXT NOT NULL,
                hit_rate REAL,
                miss_rate REAL,
                total_requests INTEGER,
                cache_size INTEGER,
                evictions INTEGER
            )
        ''')
        
        # Bảng query performance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                query_type TEXT NOT NULL,
                execution_time REAL,
                rows_affected INTEGER,
                query_hash TEXT,
                optimization_applied TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Performance database initialized")
    
    def init_cache_systems(self):
        """Khởi tạo hệ thống cache"""
        # Memory caches
        self.memory_cache = LRUCache(maxsize=1000)
        self.ttl_cache = TTLCache(maxsize=500, ttl=300)  # 5 minutes TTL
        
        # Redis cache (if available)
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis_client.ping()
            self.redis_available = True
            logger.info("✅ Redis cache initialized")
        except:
            self.redis_available = False
            logger.warning("⚠️ Redis not available, using memory cache only")
        
        # Cache statistics
        self.cache_stats = {
            "memory_cache": {"hits": 0, "misses": 0, "requests": 0},
            "ttl_cache": {"hits": 0, "misses": 0, "requests": 0},
            "redis_cache": {"hits": 0, "misses": 0, "requests": 0}
        }
    
    def apply_database_optimizations(self):
        """Áp dụng tối ưu hóa cơ sở dữ liệu"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Apply SQLite optimizations
            for pragma in self.db_optimizations["sqlite_pragmas"]:
                cursor.execute(pragma)
                logger.info(f"Applied: {pragma}")
            
            # Create indexes for better performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_perf_timestamp ON performance_metrics(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_perf_metric ON performance_metrics(metric_name)",
                "CREATE INDEX IF NOT EXISTS idx_sys_timestamp ON system_resources(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_alert_timestamp ON performance_alerts(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_query_timestamp ON query_performance(timestamp)"
            ]
            
            for index in indexes:
                cursor.execute(index)
            
            conn.commit()
            conn.close()
            logger.info("✅ Database optimizations applied")
            
        except Exception as e:
            logger.error(f"Database optimization error: {str(e)}")
    
    def start_monitoring(self, interval: int = 30):
        """Bắt đầu monitoring hiệu suất"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info(f"✅ Performance monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Dừng monitoring hiệu suất"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("⏹️ Performance monitoring stopped")
    
    def _monitoring_loop(self, interval: int):
        """Vòng lặp monitoring"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                system_metrics = self.collect_system_metrics()
                
                # Store metrics
                self.store_system_metrics(system_metrics)
                
                # Check thresholds and create alerts
                self.check_performance_thresholds(system_metrics)
                
                # Update cache statistics
                self.update_cache_statistics()
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
                time.sleep(interval)
    
    def collect_system_metrics(self) -> SystemResource:
        """Thu thập metrics hệ thống"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            # Active connections (estimate)
            connections = len(psutil.net_connections())
            
            # Response time (mock measurement)
            start_time = time.time()
            # Simulate a lightweight operation
            time.sleep(0.001)
            response_time = (time.time() - start_time) * 1000  # ms
            
            return SystemResource(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage=disk_usage,
                network_io=network_io,
                active_connections=connections,
                response_time=response_time
            )
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return SystemResource(0, 0, 0, {}, 0, 0)
    
    def store_system_metrics(self, metrics: SystemResource):
        """Lưu metrics hệ thống"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_resources 
                (cpu_percent, memory_percent, disk_usage, network_io, 
                 active_connections, response_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                metrics.cpu_percent,
                metrics.memory_percent,
                metrics.disk_usage,
                json.dumps(metrics.network_io),
                metrics.active_connections,
                metrics.response_time
            ))
            
            conn.commit()
            conn.close()
            
            # Also store in buffer for real-time access
            self.metrics_buffer.append({
                "timestamp": datetime.now(),
                "metrics": metrics
            })
            
        except Exception as e:
            logger.error(f"Error storing metrics: {str(e)}")
    
    def check_performance_thresholds(self, metrics: SystemResource):
        """Kiểm tra ngưỡng hiệu suất và tạo cảnh báo"""
        alerts = []
        
        # CPU check
        if metrics.cpu_percent >= self.thresholds["cpu_critical"]:
            alerts.append(("cpu_usage", metrics.cpu_percent, self.thresholds["cpu_critical"], "critical"))
        elif metrics.cpu_percent >= self.thresholds["cpu_warning"]:
            alerts.append(("cpu_usage", metrics.cpu_percent, self.thresholds["cpu_warning"], "warning"))
        
        # Memory check
        if metrics.memory_percent >= self.thresholds["memory_critical"]:
            alerts.append(("memory_usage", metrics.memory_percent, self.thresholds["memory_critical"], "critical"))
        elif metrics.memory_percent >= self.thresholds["memory_warning"]:
            alerts.append(("memory_usage", metrics.memory_percent, self.thresholds["memory_warning"], "warning"))
        
        # Response time check
        if metrics.response_time >= self.thresholds["response_time_critical"]:
            alerts.append(("response_time", metrics.response_time, self.thresholds["response_time_critical"], "critical"))
        elif metrics.response_time >= self.thresholds["response_time_warning"]:
            alerts.append(("response_time", metrics.response_time, self.thresholds["response_time_warning"], "warning"))
        
        # Disk usage check
        if metrics.disk_usage >= self.thresholds["disk_usage_critical"]:
            alerts.append(("disk_usage", metrics.disk_usage, self.thresholds["disk_usage_critical"], "critical"))
        elif metrics.disk_usage >= self.thresholds["disk_usage_warning"]:
            alerts.append(("disk_usage", metrics.disk_usage, self.thresholds["disk_usage_warning"], "warning"))
        
        # Store alerts
        for alert in alerts:
            self.create_performance_alert(*alert)
    
    def create_performance_alert(self, metric_name: str, current_value: float, 
                               threshold_value: float, severity: str):
        """Tạo cảnh báo hiệu suất"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO performance_alerts 
                (alert_type, metric_name, current_value, threshold_value, severity)
                VALUES (?, ?, ?, ?, ?)
            ''', ("threshold_exceeded", metric_name, current_value, threshold_value, severity))
            
            conn.commit()
            conn.close()
            
            logger.warning(f"🚨 {severity.upper()} ALERT: {metric_name} = {current_value:.2f} (threshold: {threshold_value})")
            
        except Exception as e:
            logger.error(f"Error creating alert: {str(e)}")
    
    def update_cache_statistics(self):
        """Cập nhật thống kê cache"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for cache_name, stats in self.cache_stats.items():
                if stats["requests"] > 0:
                    hit_rate = stats["hits"] / stats["requests"]
                    miss_rate = stats["misses"] / stats["requests"]
                    
                    cursor.execute('''
                        INSERT INTO cache_statistics 
                        (cache_name, hit_rate, miss_rate, total_requests, cache_size)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        cache_name,
                        hit_rate,
                        miss_rate,
                        stats["requests"],
                        getattr(self, cache_name.replace("_cache", "_cache"), {}).get("maxsize", 0) if hasattr(self, cache_name.replace("_cache", "_cache")) else 0
                    ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating cache statistics: {str(e)}")
    
    # Cache decorators and utilities
    def cached(self, cache_type: str = "memory", ttl: int = 300):
        """Decorator để cache kết quả function"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
                
                # Try to get from cache
                result = self.get_from_cache(key, cache_type)
                if result is not None:
                    self.cache_stats[f"{cache_type}_cache"]["hits"] += 1
                    self.cache_stats[f"{cache_type}_cache"]["requests"] += 1
                    return result
                
                # Cache miss - execute function
                self.cache_stats[f"{cache_type}_cache"]["misses"] += 1
                self.cache_stats[f"{cache_type}_cache"]["requests"] += 1
                
                result = func(*args, **kwargs)
                
                # Store in cache
                self.set_in_cache(key, result, cache_type, ttl)
                
                return result
            return wrapper
        return decorator
    
    def get_from_cache(self, key: str, cache_type: str = "memory") -> Any:
        """Lấy dữ liệu từ cache"""
        try:
            if cache_type == "memory":
                return self.memory_cache.get(key)
            elif cache_type == "ttl":
                return self.ttl_cache.get(key)
            elif cache_type == "redis" and self.redis_available:
                result = self.redis_client.get(key)
                return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
        return None
    
    def set_in_cache(self, key: str, value: Any, cache_type: str = "memory", ttl: int = 300):
        """Lưu dữ liệu vào cache"""
        try:
            if cache_type == "memory":
                self.memory_cache[key] = value
            elif cache_type == "ttl":
                self.ttl_cache[key] = value
            elif cache_type == "redis" and self.redis_available:
                self.redis_client.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
    
    def clear_cache(self, cache_type: str = "all"):
        """Xóa cache"""
        try:
            if cache_type in ["memory", "all"]:
                self.memory_cache.clear()
                logger.info("Memory cache cleared")
            
            if cache_type in ["ttl", "all"]:
                self.ttl_cache.clear()
                logger.info("TTL cache cleared")
            
            if cache_type in ["redis", "all"] and self.redis_available:
                self.redis_client.flushdb()
                logger.info("Redis cache cleared")
                
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Lấy tóm tắt hiệu suất"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            since = datetime.now() - timedelta(hours=hours)
            
            # Average metrics
            cursor.execute('''
                SELECT 
                    AVG(cpu_percent) as avg_cpu,
                    AVG(memory_percent) as avg_memory,
                    AVG(disk_usage) as avg_disk,
                    AVG(response_time) as avg_response_time,
                    COUNT(*) as sample_count
                FROM system_resources 
                WHERE timestamp >= ?
            ''', (since,))
            
            avg_metrics = cursor.fetchone()
            
            # Alert counts
            cursor.execute('''
                SELECT severity, COUNT(*) 
                FROM performance_alerts 
                WHERE timestamp >= ?
                GROUP BY severity
            ''', (since,))
            
            alert_counts = dict(cursor.fetchall())
            
            # Cache statistics
            cursor.execute('''
                SELECT cache_name, AVG(hit_rate), AVG(total_requests)
                FROM cache_statistics 
                WHERE timestamp >= ?
                GROUP BY cache_name
            ''', (since,))
            
            cache_stats = {}
            for row in cursor.fetchall():
                cache_stats[row[0]] = {
                    "avg_hit_rate": row[1],
                    "avg_requests": row[2]
                }
            
            conn.close()
            
            return {
                "period_hours": hours,
                "average_metrics": {
                    "cpu_percent": avg_metrics[0] or 0,
                    "memory_percent": avg_metrics[1] or 0,
                    "disk_usage": avg_metrics[2] or 0,
                    "response_time_ms": avg_metrics[3] or 0
                },
                "sample_count": avg_metrics[4],
                "alert_counts": alert_counts,
                "cache_performance": cache_stats,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {str(e)}")
            return {"error": str(e)}
    
    def optimize_database_queries(self):
        """Tối ưu hóa queries cơ sở dữ liệu"""
        optimizations = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Analyze table statistics
            cursor.execute("ANALYZE")
            optimizations.append("ANALYZE completed")
            
            # Vacuum database
            cursor.execute("VACUUM")
            optimizations.append("VACUUM completed")
            
            # Update statistics
            cursor.execute("PRAGMA optimize")
            optimizations.append("PRAGMA optimize completed")
            
            conn.close()
            
            logger.info("✅ Database optimizations completed")
            return optimizations
            
        except Exception as e:
            logger.error(f"Database optimization error: {str(e)}")
            return [f"Error: {str(e)}"]
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Lấy metrics thời gian thực"""
        if not self.metrics_buffer:
            return {"error": "No real-time data available"}
        
        latest = self.metrics_buffer[-1]
        metrics = latest["metrics"]
        
        return {
            "timestamp": latest["timestamp"].isoformat(),
            "cpu_percent": metrics.cpu_percent,
            "memory_percent": metrics.memory_percent,
            "disk_usage": metrics.disk_usage,
            "response_time_ms": metrics.response_time,
            "active_connections": metrics.active_connections,
            "cache_stats": self.cache_stats
        }

# Global instance
performance_optimizer = PerformanceOptimizer()

# Decorator exports
cached = performance_optimizer.cached

if __name__ == "__main__":
    # Test performance system
    print("⚡ SOULFRIEND V2.0 - Performance Optimization Testing")
    
    # Start monitoring
    performance_optimizer.start_monitoring(interval=5)
    
    # Test caching
    @cached(cache_type="memory")
    def expensive_calculation(n: int) -> int:
        """Simulated expensive calculation"""
        time.sleep(0.1)  # Simulate work
        return n * n
    
    # Test cache performance
    print("\n🔄 Testing cache performance...")
    start_time = time.time()
    result1 = expensive_calculation(100)  # Cache miss
    first_call_time = time.time() - start_time
    
    start_time = time.time()
    result2 = expensive_calculation(100)  # Cache hit
    second_call_time = time.time() - start_time
    
    print(f"First call (cache miss): {first_call_time:.3f}s")
    print(f"Second call (cache hit): {second_call_time:.3f}s")
    print(f"Speedup: {first_call_time / second_call_time:.1f}x")
    
    # Wait for some monitoring data
    print("\n📊 Collecting performance data...")
    time.sleep(10)
    
    # Get performance summary
    summary = performance_optimizer.get_performance_summary(hours=1)
    print("\n📈 Performance Summary:")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    # Get real-time metrics
    real_time = performance_optimizer.get_real_time_metrics()
    print("\n⏱️ Real-time Metrics:")
    print(json.dumps(real_time, indent=2, ensure_ascii=False, default=str))
    
    # Test database optimization
    print("\n🔧 Running database optimizations...")
    optimizations = performance_optimizer.optimize_database_queries()
    for opt in optimizations:
        print(f"✅ {opt}")
    
    # Stop monitoring
    performance_optimizer.stop_monitoring()
    
    print("\n✅ Performance optimization system ready!")
