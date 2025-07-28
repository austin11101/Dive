#!/bin/bash

# CV Revamping Application Setup Script
echo "🚀 Setting up CV Revamping Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/uploads
mkdir -p frontend/src/assets
mkdir -p docs/src

# Set up environment files
echo "⚙️ Setting up environment files..."

# Backend environment
cat > backend/.env << EOF
# Database
DATABASE_URL=postgresql://cv_user:cv_password@postgres:5432/cv_database

# Redis
REDIS_URL=redis://redis:6379

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true

# CORS
ALLOWED_HOSTS=["http://localhost:4200", "http://localhost:3000"]

# File upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads
EOF

# Frontend environment
cat > frontend/src/environments/environment.ts << EOF
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',
  appName: 'CV Revamp'
};
EOF

cat > frontend/src/environments/environment.prod.ts << EOF
export const environment = {
  production: true,
  apiUrl: '/api/v1',
  appName: 'CV Revamp'
};
EOF

# Create nginx configuration for frontend
cat > frontend/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files \$uri \$uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

# Create nginx configuration for docs
cat > docs/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files \$uri \$uri/ /index.html;
        }
    }
}
EOF

# Build and start services
echo "🐳 Building and starting Docker services..."
docker-compose build

echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Start the application: docker-compose up -d"
echo "2. Access the frontend: http://localhost:4200"
echo "3. Access the backend API: http://localhost:8000"
echo "4. Access the documentation: http://localhost:3000"
echo "5. View API docs: http://localhost:8000/docs"
echo ""
echo "🛠️ Development commands:"
echo "- View logs: docker-compose logs -f"
echo "- Stop services: docker-compose down"
echo "- Rebuild: docker-compose up --build" 