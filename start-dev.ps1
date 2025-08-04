# CV Revamping App - Development Startup Script
# This script starts both frontend and backend services

Write-Host "Starting CV Revamping Application..." -ForegroundColor Green

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    $connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $connection -ne $null
}

# Function to start backend
function Start-Backend {
    Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Yellow
    
    if (Test-Port 8000) {
        Write-Host "Port 8000 is already in use. Backend might already be running." -ForegroundColor Yellow
        return
    }
    
    Set-Location "backend"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    Set-Location ".."
    
    Write-Host "Backend started on http://localhost:8000" -ForegroundColor Green
}

# Function to start frontend
function Start-Frontend {
    Write-Host "Starting Frontend (Angular)..." -ForegroundColor Yellow
    
    if (Test-Port 4200) {
        Write-Host "Port 4200 is already in use. Frontend might already be running." -ForegroundColor Yellow
        return
    }
    
    Set-Location "frontend"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start"
    Set-Location ".."
    
    Write-Host "Frontend started on http://localhost:4200" -ForegroundColor Green
}

# Function to wait for services to be ready
function Wait-ForService {
    param([string]$Url, [string]$ServiceName)
    
    Write-Host "Waiting for $ServiceName to be ready..." -ForegroundColor Cyan
    
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host "$ServiceName is ready!" -ForegroundColor Green
                return $true
            }
        }
        catch {
            $attempt++
            Start-Sleep -Seconds 2
        }
    }
    
    Write-Host "$ServiceName failed to start within expected time" -ForegroundColor Red
    return $false
}

# Main execution
try {
    # Start backend first
    Start-Backend
    
    # Wait a bit for backend to initialize
    Start-Sleep -Seconds 3
    
    # Start frontend
    Start-Frontend
    
    # Wait for services to be ready
    Start-Sleep -Seconds 5
    
    $backendReady = Wait-ForService "http://localhost:8000/health" "Backend"
    $frontendReady = Wait-ForService "http://localhost:4200" "Frontend"
    
    if ($backendReady -and $frontendReady) {
        Write-Host ""
        Write-Host "CV Revamping Application is ready!" -ForegroundColor Green
        Write-Host "Frontend: http://localhost:4200" -ForegroundColor Cyan
        Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
    }
    
    # Keep the script running
    while ($true) {
        Start-Sleep -Seconds 10
    }
}
catch {
    Write-Host ("Error starting services: " + $_.Exception.Message) -ForegroundColor Red
}
finally {
    Write-Host "Stopping all services..." -ForegroundColor Yellow
} 