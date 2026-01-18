# Setup script for LocalStack development environment (PowerShell)

Write-Host "🚀 Setting up LocalStack development environment..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Start LocalStack
Write-Host "📦 Starting LocalStack..." -ForegroundColor Cyan
docker-compose up -d localstack

# Wait for LocalStack to be ready
Write-Host "⏳ Waiting for LocalStack to be ready..." -ForegroundColor Yellow
$timeout = 60
$counter = 0
$ready = $false

while (-not $ready -and $counter -lt $timeout) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:4566/_localstack/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
        }
    } catch {
        Write-Host "   Waiting... ($counter/$timeout)" -ForegroundColor Gray
        Start-Sleep -Seconds 2
        $counter += 2
    }
}

if (-not $ready) {
    Write-Host "❌ LocalStack failed to start within $timeout seconds" -ForegroundColor Red
    exit 1
}

Write-Host "✅ LocalStack is ready!" -ForegroundColor Green

# Configure AWS CLI environment variables
Write-Host ""
Write-Host "📝 Configure your environment:" -ForegroundColor Cyan
Write-Host '$env:AWS_ENDPOINT_URL="http://localhost:4566"'
Write-Host '$env:AWS_ACCESS_KEY_ID="test"'
Write-Host '$env:AWS_SECRET_ACCESS_KEY="test"'
Write-Host '$env:AWS_DEFAULT_REGION="us-east-1"'
Write-Host ""
Write-Host "Or add these to your .env file:" -ForegroundColor Cyan
Write-Host "LOCALSTACK_ENDPOINT=http://localhost:4566"
Write-Host "USE_LOCALSTACK=true"
Write-Host ""
Write-Host "🎉 Setup complete! You can now deploy infrastructure to LocalStack." -ForegroundColor Green
