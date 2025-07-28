# Quick Start Guide

Get the CV Revamping Application up and running in minutes!

## 🚀 Prerequisites

- **Docker** (v20.10+) and **Docker Compose** (v2.0+)
- **Git**
- **Node.js** 18+ (for local development)
- **Python** 3.11+ (for local development)

## ⚡ Quick Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd cv-revamp-app
```

### 2. Run the Setup Script

```bash
./scripts/setup.sh
```

This script will:
- Create necessary directories
- Set up environment files
- Build Docker images
- Configure the development environment

### 3. Start the Application

```bash
docker-compose up -d
```

### 4. Access the Application

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Documentation Site**: http://localhost:3000

## 🛠️ Development Workflow

### Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if working locally)
npm install

# Start development server
npm start

# Run tests
npm test

# Build for production
npm run build:prod
```

### Backend Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Run linting
flake8 app/
black app/
```

### Database Management

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U cv_user -d cv_database

# Run migrations (when implemented)
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## 📁 Project Structure

```
cv-revamp-app/
├── frontend/                 # Angular application
│   ├── src/
│   ├── package.json
│   └── Dockerfile.dev
├── backend/                  # FastAPI application
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile.dev
├── docs/                     # Docusaurus documentation
│   ├── src/
│   ├── package.json
│   └── Dockerfile.dev
├── scripts/                  # Utility scripts
├── docker-compose.yml        # Development environment
└── .github/workflows/        # GitHub Actions CI/CD
```

## 🔧 Common Commands

### Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up --build

# Access service shell
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Development Commands

```bash
# Run setup script
./scripts/setup.sh

# Install dependencies (local development)
cd frontend && npm install
cd backend && pip install -r requirements.txt

# Run tests
cd frontend && npm test
cd backend && pytest

# Lint code
cd frontend && npm run lint
cd backend && flake8 app/
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :4200
   lsof -i :8000
   
   # Kill the process or change ports in docker-compose.yml
   ```

2. **Database Connection Issues**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # Restart database
   docker-compose restart postgres
   ```

3. **Build Failures**
   ```bash
   # Clean and rebuild
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

### Getting Help

- Check the logs: `docker-compose logs -f`
- Review the [Deployment Guide](docs/deployment.md)
- Check the [API Documentation](http://localhost:8000/docs)
- Review the [Full Documentation](http://localhost:3000)

## 🚀 Next Steps

1. **Explore the Codebase**
   - Review the Angular components in `frontend/src/app/`
   - Check the FastAPI endpoints in `backend/app/api/`
   - Examine the database models in `backend/app/models/`

2. **Set Up Your Development Environment**
   - Configure your IDE (VS Code recommended)
   - Set up pre-commit hooks
   - Configure debugging

3. **Start Contributing**
   - Create a feature branch
   - Make your changes
   - Run tests and linting
   - Submit a pull request

4. **Deploy to Production**
   - Follow the [Deployment Guide](docs/deployment.md)
   - Set up GitHub Actions secrets
   - Configure your production environment

## 📚 Additional Resources

- [Angular Documentation](https://angular.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions) 