# Dockerfile for Research Collection API
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install fastapi uvicorn requests python-multipart

# Copy research system
COPY research_system/ research_system/
COPY research_data/ research_data/
COPY logs/ logs/

# Create necessary directories
RUN mkdir -p research_data logs

# Expose port
EXPOSE 8502

# Run the API
CMD ["python", "-m", "research_system.collection_api"]
