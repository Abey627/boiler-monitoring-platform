# Quick script to get your IP address for interview demos
Write-Host "=== Boiler Monitoring Platform - Network Setup ===" -ForegroundColor Green
Write-Host ""

# Get active network IP
$ip = (Get-NetIPAddress -AddressFamily IPv4 -PrefixOrigin Dhcp | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress

if ($ip) {
    Write-Host "✅ Your IP Address: $ip" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📱 Access URLs:" -ForegroundColor Cyan
    Write-Host "   Local:    http://localhost:8000" -ForegroundColor White
    Write-Host "   Network:  http://$ip:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "🔑 Login Credentials:" -ForegroundColor Cyan
    Write-Host "   Username: admin" -ForegroundColor White
    Write-Host "   Password: steambytes123" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Share this URL with interviewer: http://$ip:8000" -ForegroundColor Green
} else {
    Write-Host "❌ Could not detect network IP. Please check your network connection." -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
Read-Host
