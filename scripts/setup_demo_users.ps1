# Demo User Setup Script for Windows
# This script sets up comprehensive demo users for the boiler monitoring platform
# PowerShell version for Windows environments

Write-Host "=========================================" -ForegroundColor Green
Write-Host "Setting up demo users for Boiler Monitoring Platform" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Navigate to the frontend_web directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path (Split-Path -Parent $scriptPath) "frontend_web"

if (Test-Path $frontendPath) {
    Set-Location $frontendPath
    Write-Host "Working in: $frontendPath" -ForegroundColor Yellow
} else {
    Write-Host "Error: frontend_web directory not found!" -ForegroundColor Red
    exit 1
}

try {
    # Check database connection
    Write-Host "Checking database connection..." -ForegroundColor Yellow
    python manage.py check --database default
    
    if ($LASTEXITCODE -ne 0) {
        throw "Database connection failed"
    }

    # Apply migrations
    Write-Host "Applying migrations..." -ForegroundColor Yellow
    python manage.py migrate --noinput
    
    if ($LASTEXITCODE -ne 0) {
        throw "Migration failed"
    }

    # Set up demo users
    Write-Host "Creating demo users and organizations..." -ForegroundColor Yellow
    python manage.py setup_demo_users
    
    if ($LASTEXITCODE -ne 0) {
        throw "Demo user setup failed"
    }

    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "Demo user setup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now access:" -ForegroundColor Cyan
    Write-Host "  🌐 Web Dashboard: http://localhost:8000/" -ForegroundColor White
    Write-Host "  ⚙️  Admin Panel: http://localhost:8000/admin/" -ForegroundColor White
    Write-Host ""
    Write-Host "Platform Superusers (password: admin123):" -ForegroundColor Cyan
    Write-Host "  • ceo - CEO/Executive level access" -ForegroundColor White
    Write-Host "  • head_operations - Head of Operations" -ForegroundColor White
    Write-Host "  • dev_lead - Development Team Lead" -ForegroundColor White
    Write-Host ""
    Write-Host "Platform Operators (password: operator123):" -ForegroundColor Cyan
    Write-Host "  • platform_admin - Platform administrator" -ForegroundColor White
    Write-Host "  • platform_operator - Platform operations" -ForegroundColor White
    Write-Host ""
    Write-Host "Organization Users:" -ForegroundColor Cyan
    Write-Host "  ACME Corporation (password: acme123):" -ForegroundColor White
    Write-Host "    • acme_admin, acme_manager, acme_operator1, acme_operator2, acme_tech, acme_viewer" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Tech Solutions Inc (password: tech123):" -ForegroundColor White
    Write-Host "    • tech_admin, tech_manager, tech_operator1, tech_operator2, tech_specialist" -ForegroundColor Gray
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green

} catch {
    Write-Host ""
    Write-Host "Error during setup: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please check the logs above for more details." -ForegroundColor Yellow
    exit 1
}
