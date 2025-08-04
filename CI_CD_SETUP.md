# CI/CD Pipeline Setup Guide

## Overview
This project uses GitLab CI/CD for automated testing, building, and deployment.

## Pipeline Stages

### 1. Test Stage
- **test-frontend**: Runs linting, unit tests, and builds the frontend
- **test-backend**: Runs unit tests, linting, and code formatting checks

### 2. Build Stage
- **build-frontend**: Builds and pushes frontend Docker image
- **build-backend**: Builds and pushes backend Docker image

### 3. Deploy Stage
- **deploy-staging**: Deploys to staging environment (manual trigger)
- **deploy-production**: Deploys to production environment (manual trigger)

## Required Environment Variables

### GitLab CI/CD Variables
Set these in your GitLab project's Settings > CI/CD > Variables:

```
CI_REGISTRY_IMAGE=your-registry.com/your-project
SSH_PRIVATE_KEY=your-ssh-private-key
STAGING_USER=deploy-user
STAGING_HOST=staging-server.com
PRODUCTION_USER=deploy-user
PRODUCTION_HOST=production-server.com
SECRET_KEY=your-secret-key
```

### Backend Environment Variables
```
DATABASE_URL=postgresql://cv_user:cv_password@postgres:5432/cv_database
REDIS_URL=redis://redis:6379
ENVIRONMENT=production
SECRET_KEY=your-secret-key
```

## Local Development Setup

### Frontend Testing
```bash
cd frontend
npm install
npm run test
npm run lint
npm run build
```

### Backend Testing
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m pytest tests/
python -m flake8 app/
python -m black --check app/
```

## Docker Build Commands

### Frontend
```bash
cd frontend
docker build -f Dockerfile.prod -t cv-revamp-frontend .
```

### Backend
```bash
cd backend
docker build -f Dockerfile.prod -t cv-revamp-backend .
```

## Deployment

### Staging
```bash
ssh user@staging-server "cd /opt/cv-revamp && docker-compose -f docker-compose.prod.yml pull && docker-compose -f docker-compose.prod.yml up -d"
```

### Production
```bash
ssh user@production-server "cd /opt/cv-revamp && docker-compose -f docker-compose.prod.yml pull && docker-compose -f docker-compose.prod.yml up -d"
```

## Troubleshooting

### Common Issues

1. **Tests failing**: Check that all dependencies are installed and test files exist
2. **Build failing**: Verify Dockerfiles are correct and all files are present
3. **Deployment failing**: Check SSH keys and server connectivity

### Debug Commands

```bash
# Check pipeline status
gitlab-ci-lint

# Run tests locally
npm run test:ci  # Frontend
python -m pytest tests/ --cov=app  # Backend

# Check Docker images
docker images | grep cv-revamp
```

## Security Notes

- Never commit sensitive data like API keys or passwords
- Use GitLab's protected variables for sensitive information
- Regularly rotate SSH keys and secrets
- Monitor pipeline logs for security issues 