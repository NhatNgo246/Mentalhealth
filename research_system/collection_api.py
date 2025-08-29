"""
FastAPI Research Data Collection Service
Chạy trên port riêng, không ảnh hưởng đến Streamlit app chính
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import json
import os
import hmac
import hashlib
import uuid
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SOULFRIEND Research Data Collector",
    description="Anonymous research data collection service",
    version="1.0.0"
)

# Configuration
SECRET_KEY = os.environ.get("RESEARCH_SECRET", "change_me_in_production")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "research_data")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

class ResearchEvent(BaseModel):
    client_ts: str
    session_id: str
    user_hash: Optional[str] = None
    event_name: str
    payload: Dict[str, Any]
    cohort_version: str = "soulfriend_v2.0"

class ResearchEventResponse(BaseModel):
    status: str
    event_id: str
    received_at: str

def create_user_pseudo_id(user_hash: str) -> str:
    """Tạo pseudo ID không thể đảo ngược"""
    if not user_hash:
        return str(uuid.uuid4())
    
    # Hash 2 lớp để tạo pseudo ID
    pseudo_key = os.environ.get("PSEUDO_SECRET", "pseudo_key_change_me")
    pseudo_id = hmac.new(
        pseudo_key.encode(),
        user_hash.encode(), 
        hashlib.sha256
    ).hexdigest()
    
    return pseudo_id

def save_event_safely(event_data: Dict[str, Any]) -> str:
    """Lưu event một cách an toàn vào file JSON"""
    try:
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        
        # Tạo file theo ngày
        file_path = os.path.join(DATA_DIR, f"events_{timestamp}.jsonl")
        
        # Anonymize event data
        anonymized_event = {
            "event_id": event_id,
            "received_at": datetime.utcnow().isoformat(),
            "client_ts": event_data.get("client_ts"),
            "session_id": event_data.get("session_id"),
            "user_pseudo_id": create_user_pseudo_id(event_data.get("user_hash", "")),
            "event_name": event_data.get("event_name"),
            "payload": event_data.get("payload", {}),
            "cohort_version": event_data.get("cohort_version")
        }
        
        # Append to JSONL file
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(anonymized_event, ensure_ascii=False) + "\\n")
        
        return event_id
        
    except Exception as e:
        logger.error(f"Failed to save event: {e}")
        raise HTTPException(status_code=500, detail="Failed to save event")

@app.post("/collect", response_model=ResearchEventResponse)
async def collect_event(event: ResearchEvent, request: Request):
    """
    Thu thập research event
    """
    try:
        # Log the collection (without sensitive data)
        logger.info(f"Collecting event: {event.event_name} from session {event.session_id}")
        
        # Save event
        event_id = save_event_safely(event.dict())
        
        return ResearchEventResponse(
            status="collected",
            event_id=event_id,
            received_at=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Collection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "research_collector",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/stats")
async def get_collection_stats():
    """Basic collection statistics"""
    try:
        stats = {
            "total_files": 0,
            "total_events": 0,
            "latest_file": None
        }
        
        if os.path.exists(DATA_DIR):
            files = [f for f in os.listdir(DATA_DIR) if f.endswith('.jsonl')]
            stats["total_files"] = len(files)
            
            if files:
                stats["latest_file"] = max(files)
                
                # Count events in latest file
                latest_path = os.path.join(DATA_DIR, stats["latest_file"])
                with open(latest_path, "r") as f:
                    stats["total_events"] = sum(1 for line in f if line.strip())
        
        return stats
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    
    # Chạy trên port riêng để không conflict với Streamlit
    port = int(os.environ.get("RESEARCH_PORT", 8502))
    
    print(f"🔬 Starting SOULFRIEND Research Data Collector on port {port}")
    print(f"📁 Data directory: {DATA_DIR}")
    print(f"🔐 Research collection: {'ENABLED' if os.environ.get('ENABLE_RESEARCH_COLLECTION') == 'true' else 'DISABLED'}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
