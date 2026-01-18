# Simple .NET Lambda

A simple .NET Lambda function that can be deployed to LocalStack for testing.

## Prerequisites

- Docker installed and running
- LocalStack running (via `docker-compose up -d`)
- AWS CLI configured for LocalStack

## Quick Start

### 1. Start LocalStack

```bash
docker-compose up -d
```

### 2. Deploy the Lambda

**Option 1: Container Image (if registry works)**
```bash
python ../../../scripts/deploy-lambda-localstack.py
```

**Option 2: ZIP Package (recommended for LocalStack)**
```bash
python ../../../scripts/deploy-lambda-localstack-zip.py
```

### 3. Test the Lambda

```bash
# Invoke the Lambda
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name simple-lambda \
  --payload '{"test":"data"}' \
  response.json

# View the response
cat response.json  # Linux/Mac
# or
Get-Content response.json  # Windows PowerShell
```

## Manual Deployment

If you prefer to deploy manually:

### 1. Build the Docker image

```bash
docker build -t simple-lambda:latest .
```

### 2. Tag for LocalStack registry

```bash
docker tag simple-lambda:latest localhost:4510/simple-lambda:latest
```

### 3. Push to LocalStack registry

```bash
docker push localhost:4510/simple-lambda:latest
```

### 4. Create Lambda function

```bash
aws --endpoint-url=http://localhost:4566 lambda create-function \
  --function-name simple-lambda \
  --package-type Image \
  --code ImageUri=localhost:4510/simple-lambda:latest \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --timeout 30 \
  --memory-size 512
```

## Building Locally

```bash
dotnet build
dotnet publish -c Release
```

## Dockerfile Details

The Dockerfile uses a multi-stage build:
1. **Build stage**: Uses .NET SDK to build and publish the Lambda
2. **Runtime stage**: Uses .NET runtime with Lambda Runtime Interface Emulator (RIE) for LocalStack compatibility

The Lambda Runtime Interface Emulator allows LocalStack to invoke the Lambda function locally.
