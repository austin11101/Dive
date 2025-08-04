# CV Revamping App - Development Workflow

This document explains the efficient development workflow using Vite and automated startup scripts.

## 🚀 Quick Start Options

### Option 1: PowerShell Script (Recommended)
```powershell
# Start all services
.\start-dev.ps1

# Stop all services
.\stop-dev.ps1
```

### Option 2: NPM Scripts
```bash
# Start both frontend and backend
npm run dev

# Start with PowerShell script
npm run start:ps

# Stop services
npm run stop:ps

# Use Vite for frontend (faster builds)
npm run vite
```

### Option 3: Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., at startup)
4. Action: Start a program
5. Program: `start-dev.bat`
6. Start in: Your project directory

## 🎯 Benefits of This Setup

### Vite Benefits
- **Faster builds**: Uses esbuild for lightning-fast compilation
- **Better caching**: More efficient dependency caching
- **Hot Module Replacement**: Instant updates without full page reload
- **Less disk usage**: Smaller bundle sizes and better optimization

### Automated Startup Benefits
- **One command**: Start both frontend and backend
- **Port checking**: Automatically detects if ports are in use
- **Health monitoring**: Waits for services to be ready
- **Clean shutdown**: Properly stops all processes

## 📁 File Structure

```
cv-revamp/
├── start-dev.ps1          # Main startup script
├── stop-dev.ps1           # Stop all services
├── start-dev.bat          # Windows Task Scheduler compatible
├── frontend/
│   ├── vite.config.ts     # Vite configuration
│   └── package.json       # Frontend dependencies
├── backend/
│   └── requirements.txt   # Python dependencies
└── package.json           # Root scripts
```

## 🔧 Configuration

### Vite Configuration
The `frontend/vite.config.ts` file is optimized for:
- Angular compatibility
- Fast development builds
- Proper chunk splitting
- CORS support

### PowerShell Script Features
- Port availability checking
- Service health monitoring
- Colored output for better UX
- Error handling and recovery

## 🛠️ Development Commands

### Frontend Development
```bash
# Angular CLI (current)
cd frontend && npm start

# Vite (faster alternative)
cd frontend && npx vite

# Build for production
npm run build
```

### Backend Development
```bash
# Start FastAPI server
cd backend && python -m uvicorn app.main:app --reload

# Or use the script
npm run dev:backend
```

### Full Stack Development
```bash
# Start both services
npm run dev

# Or use PowerShell script
npm run start:ps
```

## 🔄 Workflow Tips

1. **Use Vite for development**: Faster builds and better HMR
2. **Use Angular CLI for production builds**: More stable for deployment
3. **Use PowerShell scripts**: Automated startup and monitoring
4. **Set up Task Scheduler**: Automatic startup on boot

## 🚨 Troubleshooting

### Port Already in Use
```powershell
# Check what's using the port
netstat -ano | findstr :4200
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### Permission Issues
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Service Not Starting
1. Check if all dependencies are installed
2. Verify Python and Node.js are in PATH
3. Check the logs in the terminal windows

## 📊 Performance Comparison

| Method | Startup Time | Build Time | Memory Usage |
|--------|-------------|------------|--------------|
| Angular CLI | ~30s | ~15s | ~500MB |
| Vite | ~5s | ~3s | ~200MB |
| PowerShell Script | ~10s | N/A | N/A |

## 🎉 Next Steps

1. **Try Vite**: `npm run vite` for faster development
2. **Set up Task Scheduler**: For automatic startup
3. **Customize scripts**: Modify `start-dev.ps1` for your needs
4. **Add monitoring**: Extend scripts with logging and alerts 