# CV Revamping App - Development Stop Script
# This script stops all running development services

Write-Host "Stopping CV Revamping Application..." -ForegroundColor Red

# Function to kill processes by port
function Stop-ProcessByPort {
    param([int]$Port, [string]$ServiceName)
    
    try {
        $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        if ($connections) {
            foreach ($connection in $connections) {
                $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
                if ($process) {
                    Write-Host "Stopping $ServiceName (PID: $($process.Id))..." -ForegroundColor Yellow
                    Stop-Process -Id $process.Id -Force
                }
            }
            Write-Host "$ServiceName stopped" -ForegroundColor Green
        } else {
            Write-Host "$ServiceName is not running" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host ("Error stopping " + $ServiceName + ": " + $_.Exception.Message) -ForegroundColor Red
    }
}

# Function to kill Node.js processes (Angular dev server)
function Stop-NodeProcesses {
    try {
        $nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
        if ($nodeProcesses) {
            Write-Host "Stopping Node.js processes..." -ForegroundColor Yellow
            foreach ($process in $nodeProcesses) {
                Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            }
            Write-Host "Node.js processes stopped" -ForegroundColor Green
        } else {
            Write-Host "No Node.js processes found" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host ("Error stopping Node.js processes: " + $_.Exception.Message) -ForegroundColor Red
    }
}

# Function to kill Python processes (FastAPI server)
function Stop-PythonProcesses {
    try {
        $pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
        if ($pythonProcesses) {
            Write-Host "Stopping Python processes..." -ForegroundColor Yellow
            foreach ($process in $pythonProcesses) {
                Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            }
            Write-Host "Python processes stopped" -ForegroundColor Green
        } else {
            Write-Host "No Python processes found" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host ("Error stopping Python processes: " + $_.Exception.Message) -ForegroundColor Red
    }
}

# Main execution
try {
    # Stop services by port
    Stop-ProcessByPort 4200 "Frontend (Angular)"
    Stop-ProcessByPort 8000 "Backend (FastAPI)"
    
    # Stop Node.js and Python processes
    Stop-NodeProcesses
    Stop-PythonProcesses
    
    Write-Host ""
    Write-Host "All development services stopped successfully!" -ForegroundColor Green
}
catch {
    Write-Host ("Error stopping services: " + $_.Exception.Message) -ForegroundColor Red
} 