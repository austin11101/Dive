# Deployment Guide

This guide covers deploying the CV Revamping Application to different environments.

## Prerequisites

- Docker and Docker Compose installed
- Git repository set up
- GitHub Actions configured (for CI/CD)
- Server with SSH access

## Environment Setup

### 1. Development Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd cv-revamp-app

# Run setup script
./scripts/setup.sh

# Start development environment
docker-compose up -d
```

### 2. Staging Environment

1. **Server Setup**
   ```bash
   # On your staging server
   mkdir -p /opt/cv-revamp
   cd /opt/cv-revamp
   ```

2. **Environment Variables**
   Create `.env` file with production settings:
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@host:5432/database
   
   # Redis
   REDIS_URL=redis://host:6379
   
   # Security
   SECRET_KEY=your-production-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Environment
   ENVIRONMENT=staging
   DEBUG=false
   
   # CORS
   ALLOWED_HOSTS=["https://staging.cv-revamp.com"]
   ```

3. **Docker Compose for Production**
   ```yaml
   version: '3.8'
   services:
     frontend:
       image: ghcr.io/your-username/cv-revamp/frontend:latest
       ports:
         - "80:80"
       environment:
         - NODE_ENV=production
     
     backend:
       image: ghcr.io/your-username/cv-revamp/backend:latest
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=${DATABASE_URL}
         - REDIS_URL=${REDIS_URL}
         - SECRET_KEY=${SECRET_KEY}
         - ENVIRONMENT=staging
     
     postgres:
       image: postgres:15-alpine
       environment:
         - POSTGRES_DB=cv_database
         - POSTGRES_USER=cv_user
         - POSTGRES_PASSWORD=cv_password
       volumes:
         - postgres_data:/var/lib/postgresql/data
     
     redis:
       image: redis:7-alpine
       volumes:
         - redis_data:/data
   
   volumes:
     postgres_data:
     redis_data:
   ```

### 3. Production Environment

1. **Domain and SSL**
   - Set up domain (e.g., cv-revamp.com)
   - Configure SSL certificates (Let's Encrypt)
   - Set up reverse proxy (Nginx)

2. **Database**
   - Use managed PostgreSQL service
   - Set up automated backups
   - Configure connection pooling

3. **Monitoring**
   - Set up application monitoring (e.g., Sentry)
   - Configure log aggregation
   - Set up health checks

## GitHub Actions Deployment

### Required Secrets

Add these secrets to your GitHub repository:

- `STAGING_HOST`: Staging server IP/hostname
- `STAGING_USER`: SSH username for staging
- `STAGING_SSH_KEY`: SSH private key for staging
- `PRODUCTION_HOST`: Production server IP/hostname
- `PRODUCTION_USER`: SSH username for production
- `PRODUCTION_SSH_KEY`: SSH private key for production

### Deployment Process

1. **Automatic Deployment to Staging**
   - Push to `develop` branch
   - GitHub Actions builds and deploys to staging

2. **Manual Deployment to Production**
   - Push to `main` branch
   - Manually trigger production deployment in GitHub Actions

## Monitoring and Maintenance

### Health Checks

- Frontend: `http://your-domain/health`
- Backend: `http://your-domain/api/v1/health`
- Database: Connection monitoring
- Redis: Connection monitoring

### Backup Strategy

1. **Database Backups**
   ```bash
   # Daily automated backup
   pg_dump -h host -U user database > backup_$(date +%Y%m%d).sql
   ```

2. **File Backups**
   - Backup uploads directory
   - Backup configuration files

### Scaling

1. **Horizontal Scaling**
   - Multiple backend instances
   - Load balancer configuration
   - Database read replicas

2. **Vertical Scaling**
   - Increase server resources
   - Optimize database queries
   - Implement caching strategies

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check connection string
   - Verify network connectivity
   - Check database permissions

2. **Memory Issues**
   - Monitor container memory usage
   - Optimize application code
   - Increase server resources

3. **Performance Issues**
   - Enable caching
   - Optimize database queries
   - Use CDN for static assets

### Logs

```bash
# View application logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Security Considerations

1. **Environment Variables**
   - Never commit secrets to version control
   - Use secure secret management
   - Rotate secrets regularly

2. **Network Security**
   - Use HTTPS in production
   - Configure firewall rules
   - Implement rate limiting

3. **Application Security**
   - Regular security updates
   - Input validation
   - SQL injection prevention
   - XSS protection 