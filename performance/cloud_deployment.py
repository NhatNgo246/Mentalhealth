"""
SOULFRIEND V2.0 - Cloud Deployment Preparation & Auto-scaling
Chuẩn bị triển khai cloud và tự động mở rộng
"""
import json
import yaml
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudDeploymentManager:
    """Quản lý triển khai cloud và auto-scaling"""
    
    def __init__(self, project_path: str = "/workspaces/Mentalhealth"):
        self.project_path = project_path
        self.deployment_configs = {}
        
        # Cloud platforms supported
        self.supported_platforms = ["azure", "aws", "gcp", "docker"]
        
        # Auto-scaling configurations
        self.autoscaling_configs = {
            "cpu_threshold": 70,
            "memory_threshold": 80,
            "min_instances": 2,
            "max_instances": 10,
            "scale_up_cooldown": 300,  # 5 minutes
            "scale_down_cooldown": 600  # 10 minutes
        }
    
    def generate_docker_config(self) -> Dict[str, Any]:
        """Tạo cấu hình Docker"""
        
        # Main Dockerfile
        dockerfile_content = """
# SOULFRIEND V2.0 - Multi-stage Docker Build
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8501 8502 8503 8504 8505 8506 8507

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start application
CMD ["python", "-m", "streamlit", "run", "mental-health-support-app/mental-health-support-app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

        # Docker Compose for development
        docker_compose = {
            "version": "3.8",
            "services": {
                "soulfriend-app": {
                    "build": ".",
                    "ports": [
                        "8501:8501",
                        "8502:8502", 
                        "8503:8503",
                        "8504:8504",
                        "8505:8505",
                        "8506:8506",
                        "8507:8507"
                    ],
                    "environment": [
                        "STREAMLIT_SERVER_PORT=8501",
                        "STREAMLIT_SERVER_ADDRESS=0.0.0.0"
                    ],
                    "volumes": [
                        "./data:/app/data"
                    ],
                    "restart": "unless-stopped",
                    "networks": ["soulfriend-network"]
                },
                "redis": {
                    "image": "redis:7-alpine",
                    "ports": ["6379:6379"],
                    "volumes": ["redis-data:/data"],
                    "restart": "unless-stopped",
                    "networks": ["soulfriend-network"]
                },
                "nginx": {
                    "image": "nginx:alpine",
                    "ports": ["80:80", "443:443"],
                    "volumes": [
                        "./nginx.conf:/etc/nginx/nginx.conf",
                        "./ssl:/etc/nginx/ssl"
                    ],
                    "depends_on": ["soulfriend-app"],
                    "restart": "unless-stopped",
                    "networks": ["soulfriend-network"]
                }
            },
            "volumes": {
                "redis-data": {}
            },
            "networks": {
                "soulfriend-network": {
                    "driver": "bridge"
                }
            }
        }

        # Production Docker Compose with scaling
        docker_compose_prod = {
            "version": "3.8",
            "services": {
                "soulfriend-app": {
                    "build": ".",
                    "environment": [
                        "STREAMLIT_SERVER_PORT=8501",
                        "STREAMLIT_SERVER_ADDRESS=0.0.0.0",
                        "REDIS_URL=redis://redis:6379"
                    ],
                    "volumes": ["./data:/app/data"],
                    "networks": ["soulfriend-network"],
                    "deploy": {
                        "replicas": 3,
                        "restart_policy": {
                            "condition": "on-failure",
                            "delay": "5s",
                            "max_attempts": 3
                        },
                        "resources": {
                            "limits": {
                                "cpus": "1.0",
                                "memory": "1G"
                            },
                            "reservations": {
                                "cpus": "0.5",
                                "memory": "512M"
                            }
                        }
                    }
                },
                "redis": {
                    "image": "redis:7-alpine",
                    "volumes": ["redis-data:/data"],
                    "networks": ["soulfriend-network"],
                    "deploy": {
                        "replicas": 1,
                        "resources": {
                            "limits": {
                                "cpus": "0.5",
                                "memory": "256M"
                            }
                        }
                    }
                },
                "nginx": {
                    "image": "nginx:alpine",
                    "ports": ["80:80", "443:443"],
                    "volumes": [
                        "./nginx.conf:/etc/nginx/nginx.conf",
                        "./ssl:/etc/nginx/ssl"
                    ],
                    "networks": ["soulfriend-network"],
                    "deploy": {
                        "replicas": 2,
                        "resources": {
                            "limits": {
                                "cpus": "0.5",
                                "memory": "256M"
                            }
                        }
                    }
                }
            },
            "volumes": {
                "redis-data": {}
            },
            "networks": {
                "soulfriend-network": {
                    "driver": "overlay",
                    "attachable": True
                }
            }
        }

        return {
            "dockerfile": dockerfile_content,
            "docker_compose_dev": docker_compose,
            "docker_compose_prod": docker_compose_prod
        }
    
    def generate_azure_config(self) -> Dict[str, Any]:
        """Tạo cấu hình Azure Container Apps"""
        
        # Azure Container Apps configuration
        azure_container_app = {
            "apiVersion": "2023-05-01",
            "type": "Microsoft.App/containerApps",
            "name": "soulfriend-v2-app",
            "location": "[parameters('location')]",
            "properties": {
                "environmentId": "[resourceId('Microsoft.App/managedEnvironments', parameters('containerAppsEnvironmentName'))]",
                "configuration": {
                    "activeRevisionsMode": "Multiple",
                    "ingress": {
                        "external": True,
                        "targetPort": 8501,
                        "transport": "http",
                        "corsPolicy": {
                            "allowedOrigins": ["*"],
                            "allowedMethods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                            "allowedHeaders": ["*"]
                        }
                    },
                    "secrets": [
                        {
                            "name": "redis-connection",
                            "value": "[parameters('redisConnectionString')]"
                        }
                    ]
                },
                "template": {
                    "containers": [
                        {
                            "name": "soulfriend-app",
                            "image": "[parameters('containerImage')]",
                            "resources": {
                                "cpu": 1.0,
                                "memory": "2Gi"
                            },
                            "env": [
                                {
                                    "name": "REDIS_URL",
                                    "secretRef": "redis-connection"
                                },
                                {
                                    "name": "STREAMLIT_SERVER_PORT",
                                    "value": "8501"
                                }
                            ]
                        }
                    ],
                    "scale": {
                        "minReplicas": 2,
                        "maxReplicas": 10,
                        "rules": [
                            {
                                "name": "cpu-scaling",
                                "custom": {
                                    "type": "cpu",
                                    "metadata": {
                                        "type": "Utilization",
                                        "value": "70"
                                    }
                                }
                            },
                            {
                                "name": "memory-scaling", 
                                "custom": {
                                    "type": "memory",
                                    "metadata": {
                                        "type": "Utilization",
                                        "value": "80"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }

        # Azure Container Registry
        azure_acr = {
            "apiVersion": "2023-07-01",
            "type": "Microsoft.ContainerRegistry/registries",
            "name": "[parameters('acrName')]",
            "location": "[parameters('location')]",
            "sku": {
                "name": "Standard"
            },
            "properties": {
                "adminUserEnabled": True
            }
        }

        # Azure Application Insights
        azure_insights = {
            "apiVersion": "2020-02-02",
            "type": "Microsoft.Insights/components",
            "name": "[parameters('appInsightsName')]",
            "location": "[parameters('location')]",
            "kind": "web",
            "properties": {
                "Application_Type": "web",
                "RetentionInDays": 90
            }
        }

        return {
            "container_app": azure_container_app,
            "container_registry": azure_acr,
            "application_insights": azure_insights
        }
    
    def generate_kubernetes_config(self) -> Dict[str, Any]:
        """Tạo cấu hình Kubernetes"""
        
        # Deployment
        k8s_deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "soulfriend-app",
                "labels": {
                    "app": "soulfriend",
                    "version": "v2.0"
                }
            },
            "spec": {
                "replicas": 3,
                "selector": {
                    "matchLabels": {
                        "app": "soulfriend"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "soulfriend"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "soulfriend-app",
                                "image": "soulfriend/app:v2.0",
                                "ports": [
                                    {
                                        "containerPort": 8501
                                    }
                                ],
                                "env": [
                                    {
                                        "name": "REDIS_URL",
                                        "valueFrom": {
                                            "secretKeyRef": {
                                                "name": "app-secrets",
                                                "key": "redis-url"
                                            }
                                        }
                                    }
                                ],
                                "resources": {
                                    "requests": {
                                        "cpu": "500m",
                                        "memory": "512Mi"
                                    },
                                    "limits": {
                                        "cpu": "1000m",
                                        "memory": "1Gi"
                                    }
                                },
                                "livenessProbe": {
                                    "httpGet": {
                                        "path": "/_stcore/health",
                                        "port": 8501
                                    },
                                    "initialDelaySeconds": 60,
                                    "periodSeconds": 30
                                },
                                "readinessProbe": {
                                    "httpGet": {
                                        "path": "/_stcore/health",
                                        "port": 8501
                                    },
                                    "initialDelaySeconds": 30,
                                    "periodSeconds": 10
                                }
                            }
                        ]
                    }
                }
            }
        }

        # Service
        k8s_service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "soulfriend-service"
            },
            "spec": {
                "selector": {
                    "app": "soulfriend"
                },
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": 8501
                    }
                ],
                "type": "LoadBalancer"
            }
        }

        # Horizontal Pod Autoscaler
        k8s_hpa = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": "soulfriend-hpa"
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": "soulfriend-app"
                },
                "minReplicas": 2,
                "maxReplicas": 10,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 70
                            }
                        }
                    },
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "memory",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 80
                            }
                        }
                    }
                ]
            }
        }

        # Ingress
        k8s_ingress = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": "soulfriend-ingress",
                "annotations": {
                    "nginx.ingress.kubernetes.io/rewrite-target": "/",
                    "cert-manager.io/cluster-issuer": "letsencrypt-prod"
                }
            },
            "spec": {
                "tls": [
                    {
                        "hosts": ["soulfriend.example.com"],
                        "secretName": "soulfriend-tls"
                    }
                ],
                "rules": [
                    {
                        "host": "soulfriend.example.com",
                        "http": {
                            "paths": [
                                {
                                    "path": "/",
                                    "pathType": "Prefix",
                                    "backend": {
                                        "service": {
                                            "name": "soulfriend-service",
                                            "port": {
                                                "number": 80
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

        return {
            "deployment": k8s_deployment,
            "service": k8s_service,
            "hpa": k8s_hpa,
            "ingress": k8s_ingress
        }
    
    def generate_nginx_config(self) -> str:
        """Tạo cấu hình Nginx load balancer"""
        
        nginx_config = """
# SOULFRIEND V2.0 - Nginx Load Balancer Configuration

events {
    worker_connections 1024;
}

http {
    upstream soulfriend_app {
        least_conn;
        server soulfriend-app-1:8501 max_fails=3 fail_timeout=30s;
        server soulfriend-app-2:8501 max_fails=3 fail_timeout=30s;
        server soulfriend-app-3:8501 max_fails=3 fail_timeout=30s;
    }

    upstream soulfriend_dashboards {
        least_conn;
        server soulfriend-app-1:8502 max_fails=3 fail_timeout=30s;
        server soulfriend-app-1:8503 max_fails=3 fail_timeout=30s;
        server soulfriend-app-1:8504 max_fails=3 fail_timeout=30s;
        server soulfriend-app-1:8505 max_fails=3 fail_timeout=30s;
        server soulfriend-app-1:8506 max_fails=3 fail_timeout=30s;
    }

    upstream soulfriend_api {
        least_conn;
        server soulfriend-app-1:8507 max_fails=3 fail_timeout=30s;
        server soulfriend-app-2:8507 max_fails=3 fail_timeout=30s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=app:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=20r/s;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Main application
    server {
        listen 80;
        server_name soulfriend.example.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name soulfriend.example.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        # Main app
        location / {
            limit_req zone=app burst=20 nodelay;
            proxy_pass http://soulfriend_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support for Streamlit
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Dashboard routes
        location /dashboard/ {
            limit_req zone=app burst=10 nodelay;
            proxy_pass http://soulfriend_dashboards/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API routes
        location /api/ {
            limit_req zone=api burst=50 nodelay;
            proxy_pass http://soulfriend_api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }

        # Static files caching
        location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
"""
        return nginx_config
    
    def generate_github_actions_workflow(self) -> Dict[str, Any]:
        """Tạo GitHub Actions workflow cho CI/CD"""
        
        workflow = {
            "name": "SOULFRIEND V2.0 - CI/CD Pipeline",
            "on": {
                "push": {
                    "branches": ["main", "develop"]
                },
                "pull_request": {
                    "branches": ["main"]
                }
            },
            "env": {
                "REGISTRY": "ghcr.io",
                "IMAGE_NAME": "${{ github.repository }}"
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "name": "Checkout code",
                            "uses": "actions/checkout@v4"
                        },
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {
                                "python-version": "3.11"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "pip install -r requirements.txt"
                        },
                        {
                            "name": "Run tests",
                            "run": "python -m pytest tests/ -v"
                        },
                        {
                            "name": "Run security scan",
                            "run": "bandit -r . -f json -o security-report.json"
                        }
                    ]
                },
                "build-and-push": {
                    "runs-on": "ubuntu-latest",
                    "needs": "test",
                    "if": "github.ref == 'refs/heads/main'",
                    "permissions": {
                        "contents": "read",
                        "packages": "write"
                    },
                    "steps": [
                        {
                            "name": "Checkout code",
                            "uses": "actions/checkout@v4"
                        },
                        {
                            "name": "Log in to Container Registry",
                            "uses": "docker/login-action@v3",
                            "with": {
                                "registry": "${{ env.REGISTRY }}",
                                "username": "${{ github.actor }}",
                                "password": "${{ secrets.GITHUB_TOKEN }}"
                            }
                        },
                        {
                            "name": "Extract metadata",
                            "id": "meta",
                            "uses": "docker/metadata-action@v5",
                            "with": {
                                "images": "${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}"
                            }
                        },
                        {
                            "name": "Build and push Docker image",
                            "uses": "docker/build-push-action@v5",
                            "with": {
                                "context": ".",
                                "push": True,
                                "tags": "${{ steps.meta.outputs.tags }}",
                                "labels": "${{ steps.meta.outputs.labels }}"
                            }
                        }
                    ]
                },
                "deploy-azure": {
                    "runs-on": "ubuntu-latest",
                    "needs": "build-and-push",
                    "if": "github.ref == 'refs/heads/main'",
                    "steps": [
                        {
                            "name": "Azure Login",
                            "uses": "azure/login@v1",
                            "with": {
                                "creds": "${{ secrets.AZURE_CREDENTIALS }}"
                            }
                        },
                        {
                            "name": "Deploy to Azure Container Apps",
                            "uses": "azure/container-apps-deploy-action@v1",
                            "with": {
                                "containerAppName": "soulfriend-v2-app",
                                "resourceGroup": "${{ secrets.AZURE_RESOURCE_GROUP }}",
                                "imageToDeploy": "${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main"
                            }
                        }
                    ]
                }
            }
        }

        return workflow
    
    def create_deployment_files(self):
        """Tạo tất cả các file triển khai"""
        
        logger.info("🚀 Generating cloud deployment configurations...")
        
        # Create deployment directory
        deploy_dir = os.path.join(self.project_path, "deployment")
        os.makedirs(deploy_dir, exist_ok=True)
        
        # Docker configurations
        docker_configs = self.generate_docker_config()
        
        # Write Dockerfile
        with open(os.path.join(self.project_path, "Dockerfile"), "w", encoding="utf-8") as f:
            f.write(docker_configs["dockerfile"])
        logger.info("✅ Dockerfile created")
        
        # Write Docker Compose files
        with open(os.path.join(deploy_dir, "docker-compose.dev.yml"), "w", encoding="utf-8") as f:
            yaml.dump(docker_configs["docker_compose_dev"], f, default_flow_style=False)
        
        with open(os.path.join(deploy_dir, "docker-compose.prod.yml"), "w", encoding="utf-8") as f:
            yaml.dump(docker_configs["docker_compose_prod"], f, default_flow_style=False)
        logger.info("✅ Docker Compose files created")
        
        # Azure configurations
        azure_configs = self.generate_azure_config()
        azure_dir = os.path.join(deploy_dir, "azure")
        os.makedirs(azure_dir, exist_ok=True)
        
        for config_name, config_data in azure_configs.items():
            with open(os.path.join(azure_dir, f"{config_name}.json"), "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2)
        logger.info("✅ Azure configurations created")
        
        # Kubernetes configurations
        k8s_configs = self.generate_kubernetes_config()
        k8s_dir = os.path.join(deploy_dir, "kubernetes")
        os.makedirs(k8s_dir, exist_ok=True)
        
        for config_name, config_data in k8s_configs.items():
            with open(os.path.join(k8s_dir, f"{config_name}.yaml"), "w", encoding="utf-8") as f:
                yaml.dump(config_data, f, default_flow_style=False)
        logger.info("✅ Kubernetes configurations created")
        
        # Nginx configuration
        nginx_config = self.generate_nginx_config()
        with open(os.path.join(deploy_dir, "nginx.conf"), "w", encoding="utf-8") as f:
            f.write(nginx_config)
        logger.info("✅ Nginx configuration created")
        
        # GitHub Actions workflow
        workflow = self.generate_github_actions_workflow()
        github_dir = os.path.join(self.project_path, ".github", "workflows")
        os.makedirs(github_dir, exist_ok=True)
        
        with open(os.path.join(github_dir, "ci-cd.yml"), "w", encoding="utf-8") as f:
            yaml.dump(workflow, f, default_flow_style=False)
        logger.info("✅ GitHub Actions workflow created")
        
        # Create deployment scripts
        self.create_deployment_scripts(deploy_dir)
        
        # Create monitoring and health check configs
        self.create_monitoring_configs(deploy_dir)
        
        logger.info("🎉 All deployment configurations created successfully!")
        
        return {
            "deployment_directory": deploy_dir,
            "configurations_created": [
                "Dockerfile",
                "Docker Compose (dev & prod)",
                "Azure Container Apps",
                "Kubernetes manifests",
                "Nginx load balancer",
                "GitHub Actions CI/CD",
                "Deployment scripts",
                "Monitoring configs"
            ]
        }
    
    def create_deployment_scripts(self, deploy_dir: str):
        """Tạo deployment scripts"""
        
        scripts_dir = os.path.join(deploy_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        
        # Build and deploy script
        build_script = """#!/bin/bash
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
"""

        # Health check script
        health_script = """#!/bin/bash
# SOULFRIEND V2.0 - Health Check Script

echo "🔍 Checking SOULFRIEND V2.0 health..."

# Check main application
if curl -f -s http://localhost:8501/_stcore/health > /dev/null; then
    echo "✅ Main application: Healthy"
else
    echo "❌ Main application: Unhealthy"
    exit 1
fi

# Check dashboards
for port in 8502 8503 8504 8505 8506; do
    if curl -f -s http://localhost:$port/_stcore/health > /dev/null; then
        echo "✅ Dashboard on port $port: Healthy"
    else
        echo "⚠️ Dashboard on port $port: Not responding"
    fi
done

# Check API
if curl -f -s http://localhost:8507/health > /dev/null; then
    echo "✅ API: Healthy"
else
    echo "❌ API: Unhealthy"
    exit 1
fi

echo "🎉 All services are healthy!"
"""

        # Scaling script
        scaling_script = """#!/bin/bash
# SOULFRIEND V2.0 - Auto Scaling Script

CURRENT_LOAD=$(docker stats --no-stream --format "table {{.CPUPerc}}" | tail -n +2 | sed 's/%//' | awk '{sum+=$1} END {print sum/NR}')
MEMORY_USAGE=$(docker stats --no-stream --format "table {{.MemPerc}}" | tail -n +2 | sed 's/%//' | awk '{sum+=$1} END {print sum/NR}')

echo "Current CPU Load: ${CURRENT_LOAD}%"
echo "Current Memory Usage: ${MEMORY_USAGE}%"

# Scale up if load is high
if (( $(echo "$CURRENT_LOAD > 70" | bc -l) )); then
    echo "🔺 High CPU load detected, scaling up..."
    docker-compose -f deployment/docker-compose.prod.yml up -d --scale soulfriend-app=5
elif (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "🔺 High memory usage detected, scaling up..."
    docker-compose -f deployment/docker-compose.prod.yml up -d --scale soulfriend-app=5
# Scale down if load is low
elif (( $(echo "$CURRENT_LOAD < 30" | bc -l) )) && (( $(echo "$MEMORY_USAGE < 50" | bc -l) )); then
    echo "🔻 Low resource usage, scaling down..."
    docker-compose -f deployment/docker-compose.prod.yml up -d --scale soulfriend-app=2
fi
"""

        # Write scripts
        scripts = {
            "deploy.sh": build_script,
            "health-check.sh": health_script,
            "auto-scale.sh": scaling_script
        }

        for script_name, script_content in scripts.items():
            script_path = os.path.join(scripts_dir, script_name)
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)  # Make executable

        logger.info("✅ Deployment scripts created")
    
    def create_monitoring_configs(self, deploy_dir: str):
        """Tạo cấu hình monitoring"""
        
        monitoring_dir = os.path.join(deploy_dir, "monitoring")
        os.makedirs(monitoring_dir, exist_ok=True)
        
        # Prometheus configuration
        prometheus_config = {
            "global": {
                "scrape_interval": "15s"
            },
            "scrape_configs": [
                {
                    "job_name": "soulfriend-app",
                    "static_configs": [
                        {
                            "targets": ["localhost:8501", "localhost:8502", "localhost:8503", "localhost:8504", "localhost:8505", "localhost:8506", "localhost:8507"]
                        }
                    ]
                }
            ]
        }

        # Grafana dashboard configuration
        grafana_dashboard = {
            "dashboard": {
                "id": None,
                "title": "SOULFRIEND V2.0 - System Overview",
                "tags": ["soulfriend", "mental-health"],
                "timezone": "browser",
                "panels": [
                    {
                        "id": 1,
                        "title": "CPU Usage",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "rate(cpu_usage_total[5m])",
                                "legendFormat": "CPU Usage"
                            }
                        ]
                    },
                    {
                        "id": 2,
                        "title": "Memory Usage",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "memory_usage_bytes / memory_total_bytes * 100",
                                "legendFormat": "Memory Usage"
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "title": "Response Time",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "http_request_duration_seconds",
                                "legendFormat": "Response Time"
                            }
                        ]
                    }
                ]
            }
        }

        # Write monitoring configs
        with open(os.path.join(monitoring_dir, "prometheus.yml"), "w", encoding="utf-8") as f:
            yaml.dump(prometheus_config, f, default_flow_style=False)

        with open(os.path.join(monitoring_dir, "grafana-dashboard.json"), "w", encoding="utf-8") as f:
            json.dump(grafana_dashboard, f, indent=2)

        logger.info("✅ Monitoring configurations created")

# Global instance
cloud_deployment = CloudDeploymentManager()

if __name__ == "__main__":
    # Generate all deployment configurations
    print("☁️ SOULFRIEND V2.0 - Cloud Deployment Preparation")
    
    result = cloud_deployment.create_deployment_files()
    
    print(f"\n📁 Deployment files created in: {result['deployment_directory']}")
    print("\n📋 Configurations created:")
    for config in result['configurations_created']:
        print(f"  ✅ {config}")
    
    print("\n🚀 Next steps:")
    print("  1. Review and customize configurations")
    print("  2. Set up your cloud provider credentials")
    print("  3. Run: chmod +x deployment/scripts/*.sh")
    print("  4. Deploy: ./deployment/scripts/deploy.sh")
    
    print("\n✅ Cloud deployment preparation completed!")
