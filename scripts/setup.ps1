# PowerShell Setup Script for Boiler Monitoring Platform

param(
    [switch]$SkipHealthCheck
)

Write-Host "🚀 Starting Boiler Monitoring Platform..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Blue

# Function to handle cleanup on failure
function Cleanup {
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Setup failed. Cleaning up..." -ForegroundColor Red
        docker-compose down
        exit 1
    }
}

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "⚠️  No .env file found. Creating a default one..." -ForegroundColor Yellow
    
    $envContent = @"
# Database Configuration
DB_PASSWORD=steambytes_dev_password

# InfluxDB Configuration
INFLUX_PASSWORD=steambytes_influx_password
INFLUX_TOKEN=steambytes_admin_token

# Debug Mode
DEBUG=1

# Add other environment variables as needed
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "✅ Created default .env file" -ForegroundColor Green
}

# Build and start services
Write-Host "🔨 Building and starting services..." -ForegroundColor Blue
docker-compose up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services" -ForegroundColor Red
    Cleanup
}

# Wait for services to initialize
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run health checks unless skipped
if (!$SkipHealthCheck) {
    Write-Host "🏥 Running health checks..." -ForegroundColor Blue
    
    # Function to check service health
    function Test-ServiceHealth {
        param(
            [string]$ServiceName,
            [string]$Url,
            [int]$MaxAttempts = 30
        )
        
        Write-Host "Checking $ServiceName at $Url..." -ForegroundColor Cyan
        
        for ($i = 1; $i -le $MaxAttempts; $i++) {
            try {
                $response = Invoke-WebRequest -Uri $Url -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
                if ($response.StatusCode -eq 200) {
                    Write-Host "✅ $ServiceName is healthy" -ForegroundColor Green
                    return $true
                }
            } catch {
                # Service not ready yet
            }
            
            Write-Host "⏳ Attempt $i/$MaxAttempts - waiting for $ServiceName..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
        
        Write-Host "❌ $ServiceName failed health check after $MaxAttempts attempts" -ForegroundColor Red
        return $false
    }
    
    # Check databases
    Write-Host "Checking PostgreSQL database..." -ForegroundColor Cyan
    $pgCheck = docker-compose exec -T postgres pg_isready -U steambytes -d steambytes_core 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PostgreSQL is healthy" -ForegroundColor Green
    } else {
        Write-Host "❌ PostgreSQL is not responding" -ForegroundColor Red
        Cleanup
    }
    
    Write-Host "Checking Redis..." -ForegroundColor Cyan
    $redisCheck = docker-compose exec -T redis redis-cli ping 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Redis is healthy" -ForegroundColor Green
    } else {
        Write-Host "❌ Redis is not responding" -ForegroundColor Red
        Cleanup
    }
    
    # Check web services
    $services = @(
        @{Name="InfluxDB"; Url="http://localhost:8086/health"},
        @{Name="Frontend Web"; Url="http://localhost:8000"},
        @{Name="Frontend API"; Url="http://localhost:8001"},
        @{Name="IoT Ingestion"; Url="http://localhost:8002"},
        @{Name="AI Processor"; Url="http://localhost:8003"},
        @{Name="Alert Service"; Url="http://localhost:8004"},
        @{Name="Nginx"; Url="http://localhost:80"}
    )
    
    $allHealthy = $true
    foreach ($service in $services) {
        if (!(Test-ServiceHealth -ServiceName $service.Name -Url $service.Url)) {
            $allHealthy = $false
            break
        }
    }
    
    if (!$allHealthy) {
        Cleanup
    }
    
    Write-Host "=========================================" -ForegroundColor Blue
    Write-Host "🎉 All services are healthy and running!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Blue
}

Write-Host ""
Write-Host "🎉 Boiler Monitoring Platform is ready!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Blue
Write-Host "You can now access the dashboard at: http://localhost" -ForegroundColor Cyan
Write-Host ""
Write-Host "Service URLs:" -ForegroundColor Yellow
Write-Host "  • Main Dashboard: http://localhost" -ForegroundColor White
Write-Host "  • Frontend Web:   http://localhost:8000" -ForegroundColor White
Write-Host "  • Frontend API:   http://localhost:8001" -ForegroundColor White
Write-Host "  • IoT Ingestion:  http://localhost:8002" -ForegroundColor White
Write-Host "  • AI Processor:   http://localhost:8003" -ForegroundColor White
Write-Host "  • Alert Service:  http://localhost:8004" -ForegroundColor White
Write-Host "  • InfluxDB:       http://localhost:8086" -ForegroundColor White
Write-Host "  • PostgreSQL:     localhost:5432" -ForegroundColor White
Write-Host "  • Redis:          localhost:6379" -ForegroundColor White
Write-Host ""
Write-Host "To stop the platform:" -ForegroundColor Yellow
Write-Host "  docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f" -ForegroundColor White
Write-Host ""
