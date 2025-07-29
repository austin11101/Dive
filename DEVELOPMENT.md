# 🚀 Development Guide

## Quick Start

### Option 1: One-Command Start (Recommended)
```bash
./dev-start.sh
```

### Option 2: Manual Start
```bash
# Install all dependencies
npm run install:all

# Start both servers
npm run dev
```

## Development Environment

### Frontend (Angular + Vite)
- **URL**: http://localhost:4200
- **Framework**: Angular 17 with Vite (ultra-fast builds)
- **Styling**: Bootstrap 5
- **Hot Reload**: ✅ Enabled
- **Source Maps**: ✅ Enabled

### Backend (FastAPI)
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Framework**: FastAPI with uvicorn
- **Database**: SQLite (local development)
- **Hot Reload**: ✅ Enabled

## Available Scripts

### Root Level Commands
```bash
npm run dev              # Start both frontend and backend
npm run dev:frontend     # Start only frontend
npm run dev:backend      # Start only backend
npm run install:all      # Install all dependencies
npm run build            # Build frontend for production
npm run test             # Run frontend tests
npm run lint             # Run frontend linting
npm run clean            # Clean cache files
npm start                # Alias for npm run dev
```

### Frontend Commands (from frontend/ directory)
```bash
ng serve                 # Start development server
ng build                 # Build for production
ng test                  # Run tests
ng lint                  # Run linting
```

### Backend Commands (from backend/ directory)
```bash
python -m uvicorn app.main:app --reload  # Start with auto-reload
python -m pytest                         # Run tests
```

## Development Features

### 🚀 Vite Integration
- **Ultra-fast builds** and hot module replacement
- **Instant server start** with no bundling delays
- **Optimized dependency pre-bundling**
- **Smart caching** for faster subsequent builds

### 🔥 Hot Module Replacement (HMR)
- **Instant updates** without full page reloads
- **State preservation** during development
- **CSS hot reload** for styling changes

### 🛠️ Development Tools
- **Source maps** for debugging
- **Error overlay** for runtime errors
- **Console logging** for development debugging
- **API documentation** at `/docs`

## Environment Configuration

### Frontend Environment
- **Development**: `frontend/src/environments/environment.development.ts`
- **Production**: `frontend/src/environments/environment.prod.ts`

### Backend Environment
- **Development**: Hardcoded in `backend/app/core/config.py`
- **Production**: Uses `.env` file

## Database

### Local Development
- **Type**: SQLite
- **File**: `backend/cv_database.db`
- **Auto-creation**: ✅ Tables created automatically

### Test Credentials
```
Email: test@example.com
Password: testpassword123
```

## Troubleshooting

### Common Issues

#### Node.js Version
```bash
# Check version
node -v

# Update if needed (using nvm)
nvm install 20.19.0
nvm use 20.19.0
```

#### Port Conflicts
```bash
# Check what's using port 4200
lsof -i :4200

# Check what's using port 8000
lsof -i :8000

# Kill processes if needed
kill -9 <PID>
```

#### Cache Issues
```bash
# Clean all cache
npm run clean

# Clear Angular cache
cd frontend && rm -rf .angular/cache

# Clear npm cache
npm cache clean --force
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Make scripts executable
chmod +x dev-start.sh
```

## Performance Tips

### Frontend
- **Use Vite's HMR** for instant updates
- **Lazy load modules** for better performance
- **Optimize images** and assets
- **Use Angular's OnPush** change detection strategy

### Backend
- **Use async/await** for database operations
- **Implement caching** for frequently accessed data
- **Use connection pooling** for database connections
- **Enable compression** for API responses

## Deployment

### Frontend Production Build
```bash
npm run build
```

### Backend Production
```bash
# Use Docker (production)
docker-compose up -d

# Or direct deployment
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with descriptive messages
6. **Push** to your branch
7. **Create** a pull request

## Support

- **Documentation**: Check the `docs/` folder
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions 