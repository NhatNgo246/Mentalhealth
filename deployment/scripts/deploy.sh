#!/bin/bash
# SOULFRIEND V2.0 - Build and Deploy Script

set -e

echo "🚀 Starting SOULFRIEND V2.0 deployment..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t soulfriend/app:v2.0 .
docker tag soulfriend/app:v2.0 soulfriend/app:latest

# Push to registry (if specified)
if [ -n "$REGISTRY" ]; then
    echo "📤 Pushing to registry: $REGISTRY"
    docker tag soulfriend/app:v2.0 $REGISTRY/soulfriend/app:v2.0
    docker push $REGISTRY/soulfriend/app:v2.0
fi

# Deploy based on environment
case "$DEPLOY_ENV" in
    "docker")
        echo "🐳 Deploying with Docker Compose..."
        docker-compose -f deployment/docker-compose.prod.yml up -d
        ;;
    "kubernetes")
        echo "☸️ Deploying to Kubernetes..."
        kubectl apply -f deployment/kubernetes/
        ;;
    "azure")
        echo "☁️ Deploying to Azure..."
        az containerapp update --name soulfriend-v2-app --resource-group $AZURE_RG --image $REGISTRY/soulfriend/app:v2.0
        ;;
    *)
        echo "🤖 Environment not specified, using Docker Compose..."
        docker-compose -f deployment/docker-compose.prod.yml up -d
        ;;
esac

echo "✅ Deployment completed!"
