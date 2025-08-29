#!/usr/bin/env python3
"""
🚀 SOULFRIEND Research Collection API Server
FastAPI server for research data collection with privacy protection
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app from collection_api
from research_system.collection_api import app

def main():
    """Run the research collection API server"""
    print("🚀 Starting SOULFRIEND Research Collection API...")
    print("=" * 50)
    print("📡 API Features:")
    print("   ✅ Privacy-first data collection")
    print("   ✅ GDPR compliant storage")
    print("   ✅ Real-time health monitoring")
    print("   ✅ Rate limiting protection")
    print("   ✅ Automatic data encryption")
    print("")
    print("🔗 API Endpoints:")
    print("   POST /collect - Collect research events")
    print("   GET /health - Health check")
    print("   GET /stats - Collection statistics")
    print("   GET /docs - Interactive API documentation")
    print("")
    print("🔒 Security:")
    print("   ✅ Request validation")
    print("   ✅ Data anonymization")
    print("   ✅ Privacy protection")
    print("   ✅ Audit logging")
    print("")
    
    # Configure and start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8502,
        reload=True,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
